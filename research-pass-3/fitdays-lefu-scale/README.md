# fitdays-lefu-scale

Reverse-engineered Bluetooth LE protocol for the **Fitdays / Lefu 8-electrode
dual-frequency body-composition scale** (advertised as `JEETIF…`, vendor GATT
service `0xFFB0`), plus a Python codec that talks to it without the vendor app.

It gets you what the Fitdays app gets: live weight, and the scale's **ten
segmental impedance readings** (trunk, both arms, both legs, each at two
frequencies). From those you can reproduce Fitdays' full body-composition
report: body fat, water, muscle, bone, protein, visceral fat, BMR and body age,
plus a per-limb breakdown.

> Independent interoperability research. Not affiliated with Fitdays, Lefu or
> iComon. The vendor's proprietary algorithm binary is **not** included.

## What's here

| Path | What |
|---|---|
| `fitdays_scale/protocol.py` | Frame codec, checksum, decoder, and the handshake planner |
| `fitdays_scale/wla37.py` | Runs Fitdays' own body-composition model (bring your own `.so`) |
| `examples/scan_bleak.py` | Complete weigh-in from a computer using [bleak](https://github.com/hbldh/bleak) |
| `tests/` | Pinned against real captured frames |

```bash
pip install -e ".[ble,engine]"
python examples/scan_bleak.py --height 175 --age 40 --sex female --name Ann
```

Stand on the scale **barefoot** *before* the script connects and keep still
until it prints the result.

---

## Protocol

### GATT

| Char | Props | Role |
|---|---|---|
| `FFB1` | write | commands (app → scale) |
| `FFB2` | notify | live weight |
| `FFB3` | indicate | ACKs and the body-composition result |

Subscribe to **FFB3 first**, then FFB2. The scale accepts one connection at a
time, so close the Fitdays app.

### Frame envelope

Every frame, both directions:

```
[0] SEQ  [1:3] LEN (u16 BE)  [3] PART  [4] TYPE  [5:-1] payload  [-1] CHECKSUM
```

`len(frame) == LEN + 5`. Multi-byte fields are big-endian. `SEQ` increments per
frame and is not covered by the checksum.

### Checksum

A **5-bit** additive sum, with bit 5 set on every frame type except `A2`:

```python
def checksum(ftype: int, payload: bytes) -> int:
    low = (ftype + sum(payload)) & 0x1F
    return low if ftype == 0xA2 else low | 0x20
```

Verified against 602 captured frames from this unit. The low five bits also
match the handshakes published for two sibling Lefu scales (Robi S9,
Speediance) in [ble-scale-sync](https://github.com/KristianP26/ble-scale-sync),
where this checksum was previously documented as uncracked. Bit 5's true
meaning is not established: it may be channel- rather than type-derived. The
rule above is correct for every frame this unit sends and receives.

A common trap: sweeps masked `& 0xFF` can never find a mod-32 sum.

### Frame types

| Type | Dir | Meaning |
|---|---|---|
| `AA` | scale → | hello on connect; its last 5 payload bytes are a token echoed in `B6` |
| `A2` | scale → | live weight sample |
| `A0` | scale → | ACK, echoes the command's SEQ |
| `A5` | scale → | stored / previous result |
| `A7` | scale → | measurement result |
| `B0` | → scale | control (`30`, `31`, `39` before; `3A` after the result) |
| `B6` | → scale | arms the impedance sweep (payload = the `AA` token) |
| `C0` | → scale | user profile, timestamped |
| `C1` | → scale | user profile, compact |

### `A2` — live weight (12 bytes)

```
SEQ 00 07 00 A2 | STATUS 00 [W_HI W_MID W_LO] ?? | CK
```

* `STATUS`: `01` measuring, `03` settled, `00` stepped off
* **weight = BE u24 at `frame[7:10]`, in grams**

Earlier community decoders read `frame[8:10] / 100`. That drops the high byte:
it happens to look right around 70–77 kg and yields nonsense (e.g. 501 kg)
elsewhere.

### `A7` — result (40 bytes)

```
SEQ 00 23 00 A7 | ts u32 | 25 | weight u24 g | 00 0A | 10 x u16 | device id u32 | CK
```

* `[5:9]` unix timestamp; `0x25` = 37 = the algorithm model (`WLA37`)
* `[15:35]` ten impedance words, **ohms × 10**:
  slots 0–4 at frequency 1, slots 5–9 the same segments at frequency 2,
  ordered **trunk, left arm, right arm, left leg, right leg**
* an all-zero block means no electrode contact (feet not bare / not dry)

Trunk is ~20–30 Ω against ~240–320 Ω for limbs. The low/high-frequency ratio is
a consistent ~1.15, the expected BIA signature.

### Handshake — triggering the impedance sweep

Weight streams without any handshake. **Impedance does not**: the scale only
sweeps for a recognised profile, and only if that profile arrives **while
someone is standing on it**. Replaying captured bytes gets you the *previous*
stored result, because the timestamp is stale. That is why the checksum
matters.

Once live weight shows a person on the platform, write, in order, ~150 ms apart:

```
B0 30 → C0 → C1 → C0 → B6(token) → C0 → C1 → C0 → B0 31 → B0 39
```

When a settled `A7` arrives, acknowledge it: `B0 3A → C0 → C1` (with the new
weight). `plan_writes()` in `protocol.py` implements exactly this.

**Only trust an `A7` that arrives after an `A2` with status `03`.** The scale
replays its last stored result on connect, and that frame is otherwise
indistinguishable from a fresh one.

### `C0` profile

```
SEQ 00 1B 00 C0 | ts u32 | tz offset min u16 | sex | height cm | 1C
                | weight low-16 g | 1C 25 1D 6A 0F | user id u32 | 01 01 03 | name[3] | CK
```

* sex `1` male / `2` female; height as one byte (e.g. `B9` = 185)
* weight is the low 16 bits of grams (the high `0x01` byte is implied)
* `name` is 3 ASCII bytes. The scale displays it as a greeting.
* `1C`, `1C 25 1D 6A 0F` and `01 01 03` are unexplained constants

`C1` is the same profile without the timestamp/timezone header, prefixed `01`.

---

## Body composition (`WLA37`)

The Fitdays app computes composition on the phone with a native library,
`libICBodyFatAlgorithms.so`, function `ICBodyFatAlgorithmWLA37::calc`. The
input is weight, height, sex, age and the ten impedances. The output is 73
values, including per-limb fat and muscle.

`wla37.py` runs that library under [Unicorn](https://www.unicorn-engine.org/)
emulation. Emulation is needed even on ARM64 Linux, because the library links
against Android's bionic libc and cannot be `dlopen`ed under glibc.

**The binary is not in this repository.** Extract it from your own copy of the
Fitdays APK (`lib/arm64-v8a/libICBodyFatAlgorithms.so`), then point
`WLA37_SO_PATH` at it or place it in the working directory.

Validation: against one weigh-in where both the impedance block and the app's
report were captured, every headline figure and all ten segmental percentages
match the app. Two residuals look like display rounding (fat mass 0.1 lb,
right-arm muscle 0.1 lb). Treat it as validated on a single paired sample.
Varying age and "athlete mode" changed only body age for that input.

## Known limitations

* The `C0` user id is fixed to the value the vendor app used for the unit this
  was reversed on. Whether other units or multiple users need a different id is
  unknown.
* `part` is always `0` on this unit; sibling scales split results across parts.
* Left/right *leg* labelling follows the vendor engine's output layout; arms were
  confirmed independently against the app.

## Credits and prior art

* [KristianP26/ble-scale-sync](https://github.com/KristianP26/ble-scale-sync):
  Robi S9, Speediance and Hutbit Lefu adapters, the closest published siblings.
* Checksum and the `WLA37` engine were reversed with AI assistance, then
  independently verified against live hardware.

## License

MIT for everything in this repository. The vendor library is not covered and not
distributed.
