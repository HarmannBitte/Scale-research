# Research pass 6 — 2026-10-18

Scope authorised by the user: research items 1 (technical gaps) and 2 (validation evidence). Not done: maintainer contact, hardware checks, presentation. No purchases, no flashing, no human experiments. DIY BIA is research, not a DXA replacement.

## 1. MAX30009 BioZ OSR table (finding F05) — resolved

Source: `analogdevicesinc/no-OS`, `drivers/afe/max30009/max30009.h` (chunks 1–2) and `max30009.c` (chunks 3–4).

- `BIOZ_CONFIGURATION1` (0x20): `DAC_OSR` bits [7:6], `ADC_OSR` bits [5:3].
- `enum max30009_dac_osr`: `_32, _64, _128, _256` → register values 0–3.
- `enum max30009_adc_osr`: `_8, _16, _32, _64, _128, _256, _512, _1024` → register values 0–7.
- `max30009_set_adc_osr()` writes the enum value directly into the masked field, so the enum value **is** the register value. Register value 4 = OSR 128, value 5 = OSR 256, value 7 = OSR 1024.
- `max30009_set_dac_osr()` note: F_BIOZ = PLL_CLK / (KDIV × DAC_OSR).

Consequence for the UPRM code: the register byte 0xA0 gives ADC field = (0xA0 >> 3) & 7 = 4, which is OSR 128. The code's behaviour matches the driver. The stale part is the comment that says "ADC_OSR = 5 (256)". The finding is closed as a comment/documentation error, not a register-decoding error. Confirm against the datasheet OSR table before relying on the absolute sample rate.

Also confirmed from the same driver: FIFO sample format is TAG[23:20] (0x1 = BioZ I, 0x2 = BioZ Q, 0xE = marker, 0xF = invalid), DATA[19:0] signed two's complement. 0xFFFFFF = invalid, 0xFFFFFE = marker. FIFO depth 256 × 3 bytes. PLL range check 14–28 MHz. Reference clock 32.768 kHz or 32.0 kHz.

Not read: chunks 5–8 of `max30009.c` (the rest of the BioZ/lead-off/calibration code). Not needed for the OSR question.

## 2. BIA vs DXA validation evidence (search excerpts, not full-text reviewed)

Identifiers are as returned by the search. Full text has not been checked, so treat the numbers as provisional until verified.

| Population / device | Outcome | Bias (BIA − DXA) | Agreement | Source id |
|---|---|---|---|---|
| Adults, whole body, multi-frequency | %BF | −4.0 ± 2.8% | SEE 2.6%, r 0.932, CCC 0.819 | PMC11649400 |
| Women, IB770 | FM | −0.22 kg | CCC 0.99 | MDPI 25/16/5037 |
| Women, IB770 | FFM | +3.15 kg | CCC 0.91 | MDPI 25/16/5037 |
| Children, single-frequency | — | — | CCC 0.747–0.881 | Nature 41598-023-44217-0 |
| Children, multi-frequency | — | — | CCC 0.912–0.926 | Nature 41598-023-44217-0 |
| Adults, MF-BIA | R² | proportional bias noted | R² 0.72–0.97 | Frontiers 10.3389/frans.2026.1767078 |
| InBody (adults) | FM | −1.2 kg | LOA −5.7 to +3.8 kg | ScienceDirect S2667268526000409 |
| InBody, arms/legs | segmental | — | ICC 0.69–0.76 | ScienceDirect S2667268526000409 |
| Brazilian cohort | FFM / FM | +3.1 kg / −2.9 kg | CCC ≥ 0.93 | PubMed 41567330 |
| COPD patients | FM | 2.7 kg (sign not recorded) | ρc 0.95 | Nature s41598-022-05887-4 |
| Severe obesity | FM | 1.1 kg (sign not recorded) | LOA −6.9 to +9.0 kg | PubMed 42437547 |
| Frail women | whole-body LM / appendicular FM | 2.1 kg / −0.3 kg (sign of LM not recorded) | — | PubMed 23388666 |
| Older adults | ASMM | ~+2.8 kg overestimate | — | Springer s40520-021-02000-z |
| Consistent with 2008 study | %BF | −4.0 ± 2.8% | — | Frontiers 10.3389/fnut.2024.1491931 |
| Leg lean mass | — | no difference | trunk LOA −4.8 to +2.2 kg | Nature s41387-022-00223-1 |
| Commercial scales, children (InBody 520) | %BF | — | rc 0.926 / 0.912; LOA ~±11% | PMC4475745 |
| Six BIA devices | %BF | most favourable −2.21% | LOA −9.88 to +5.46% | JEN article 206 |

Summary for the evidence review:

- Whole-body multi-frequency BIA correlates strongly with DXA at group level (r ≈ 0.93–0.97, CCC ≈ 0.8–0.95).
- It has a systematic bias: body fat percentage about −4%, fat-free mass over by about 2–3 kg, fat mass under by about 2–3 kg. Bias varies with adiposity (proportional bias).
- Individual limits of agreement are wide, roughly ±6–11 kg for fat mass and about ±11% for %BF. A single reading is not a DXA-equivalent measurement.
- Consumer and commercial scales show similar or wider bias than research devices.
- Within-person trends can be more useful than absolute values, but this has not been tested for the UPRM setup.

## 3. Scale / app repositories (collection status)

Not collected this turn. Licence and file counts only, from earlier work:

- `research-pass-3/fitdays-lefu-scale` — MIT, 10 files. **Tests rerun this turn:** 11 passed, 1 skipped (pytest, editable install in a separate venv). The install artefacts (egg-info, `__pycache__`) were removed. Repo is clean.
- `research-pass-5/hume_pod_ha` — BLUE2SCALE licence (source-available), 43 files. Not tested.
- `research-pass-4/ble-scale-sync` — GPL-3.0, 631 files. Not tested (requires Node dependencies, not installed).

Not done: searching for further scale or app repos. Not done: remaining builds beyond the pytest rerun.

## 4. Open items

- Verify the literature numbers against full text before any figure goes into a deliverable.
- Datasheet OSR table: confirm the absolute sample rate per OSR setting.
- Pushing these notes to GitHub needs the user's go-ahead (not pushed).
- The GitHub token pasted in chat should be revoked.

## 5. Expanded search (candidates found, NOT cloned or tested)

Search only: no licence, activity, or protocol review yet. Listed so they can be triaged. Licence exclusion does not apply to research scope.

Scale protocols / apps:
- oliexdev/openScale (wiki documents Xiaomi Mi Scale reverse engineering); YoannDev90/openScale is a fork.
- KristianP26/ble-scale-sync and JohnTheNerd/ble-scale-sync (the second is apparently a fork of the first; the first is already in the collection as ble-scale-sync).
- faraga1/xiaomi-scale-s200-ble — Xiaomi S200, protocol reference, claims no body-composition values exist in its protocol (weight-only).
- Shah-Dom/SmartScale — IF_B2 Web Bluetooth client, includes its own estimates of body composition.
- PavelDemyanov/qn-scale — QN-Scale protocol (Libra, Renpho, FitIndex, Kamtron).
- eayrenk/bioscale-okok-alternative — Chipsea/OKOK BIA formulas (Janssen 2000, Kyle 2004 cited).
- etlami/opentara — Xiaomi/Huami body-metric formulas (claims to match Zepp Life).
- uniextra/Yunmai-dashboard — Yunmai BLE protocol.
- ronnnnnnnnnnnnn/renpho-escs20m (and iios-co fork) — Renpho ES-CS20M, body-fat algorithm 0x03/0x04 described.
- robzarry/healthtrack — RENPHO Elis 1 logger on ESP32, protocol notes in docs/protocol.md.
- ipanalytics/Xiaomi-Scale-Unlocked-Reverse-Engineering — BLE advertisement layouts, offline decoder.
- lswiderski/MiScaleBodyComposition (C#), lolouk44/xiaomi_mi_scale (Python, MQTT), zibous/ha-miscale2, zibous/hc_scale, dkuku/bodymiscale, dkuku/bodymeasurements (tape-measure model, no impedance).
- jpfranca-br/miscale-dashboard; LookHin/xiaomi-mi-body-composition-scale-2.
- Pasynkov "BodyScan" write-up (GARLYN IF_B8B protocol, DEV Community article).

Open BIA hardware / firmware:
- dyarleniber/AD5933-arduino-bioimpedance — AD5933 BIA, FM/FFM/TBW equations on Arduino, 50 kHz & 100 kHz; has a paper PDF.
- openebi/hardware and openebi/software — four-electrode AD5933 EBI spectrometer, few kHz to 100 kHz.
- syoo15/AD5933_ARDUINO_Biomass — MATLAB + Arduino AD5933 calibration and sweep.
- mjmeli/arduino-ad5933, justiceamoh/autoimpedance, ashtonchase/ad5933_analyzer — AD5933 libraries / instruments.
- analogdevicesinc/MAX32655_MAX30009 — official MAX30009 example on MAX32655. Its register writes match the no-OS driver (see section 1). Its comment gives ADC 222 Sps and DAC 14.208 kHz at ADC field 4, DAC field 3, consistent with the decoding in section 1.
- oscaroflores/UPRM-Multi_Frq-BioZ-Research — UPRM project. Already in the collection; the upstream MAX32655_MAX30009 repo is the reference.

Datasheet note: an application-note table lists BIOZ_DAC_OSR as [2:0] (values 32–256), but the no-OS driver uses a 2-bit field. Check the datasheet before using the table.

## 6. Still open
- Clone and triage the top candidates (openScale, xiaomi-scale-s200-ble, renpho-escs20m, AD5933-arduino-bioimpedance, openebi).
- Build or test any candidate that is actually relevant.
- Verify the literature numbers in section 2 against full text.
