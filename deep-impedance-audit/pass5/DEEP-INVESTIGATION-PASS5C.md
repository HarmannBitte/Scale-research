# Pass 5c: the MAX30001 BioZ path (OpenView producer and the Arduino library)

No hardware, no maintainer contact, no purchases. Research use only.

## Sources (fetched this pass, stored in `pass5/f21/`)

- `Example01_BasicECGBioZ.ino` (upstream `Protocentral/protocentral_max30001_arduino_library`, HEAD, MIT). This is the packet-type-2 producer that the OpenView audit (F20, F21) used.
- `src/protocentral_max30001.cpp` (1,249 lines) and `src/protocentral_max30001.h` (772 lines), same repo.
- Examples 02, 04 and 05 (for which API they call).
- MAX30001 datasheet (Analog Devices) text, via search snippets: BioZ 20-bit left-justified; BTAG = D[2:0]; CNFG_BIOZ RATE = D[23], 0 = 64 sps when FMSTR = 32,768 Hz.

## 1. F21 corrected: the BioZ rate label is wrong, the producer is not

- `BeginECGBioZ()` writes `cnfg_bioz.bit.rate = 0`. In the header bit-field layout, `rate` is bit 23 (after `ahpf`, bits 22:20). The library's own comment on `CNFG_BIOZ = 0x201433` also says "BioZ Rate: 64 SPS", and bit 23 of that value is 0.
- The datasheet gives RATE = 0 as 64 sps at FMSTR = 32,768 Hz. The configuration sets `fmstr = 0`.
- So the chip produces BioZ at **64 sps**. The OpenView decoder's **128 sps** label is wrong.
- The producer's alternating "skip" flag and held value match a 64 sps BioZ stream at an ECG rate of 128 sps. The sketch says so in its comments ("BioZ samples at half the ECG rate").
- Status: the F21 observation (BioZ changes every other frame) is correct. The fault is the decoder's label, not the producer.

## 2. F33 (new): the example's read path has no ready or tag check

- `getECGSample()` (lib.cpp ~364) and `getBioZSample()` (~405) read the FIFO register on every call and set `sample_valid = true` unconditionally. They do not check whether a new word exists and do not read the ETAG/BTAG.
- `Example01` calls them every loop (~8 ms). If the loop period differs from the chip's rate, the sketch emits duplicated or stale words, and empty-FIFO words as samples.
- The library's own streaming reader does check tags (valid 0x00, overflow 0x07 → FIFO reset; lines 1138–1160).
- Status: source-level. Effect on hardware is not measured.
- Severity: Medium. This affects data validity for any user of the shipped example.

## 3. F31 (new): the streaming BioZ decoder uses ECG tag bits

- `_max30001ReadBIOZFIFO` (lines ~1196–1220) copies the ECG logic. It takes `etag = (b2 & 0x38) >> 3` and keeps only words where etag == 0. Words with etag == 7 trigger a FIFO reset.
- For BioZ, D[5:3] are data bits, not an ETAG. The datasheet puts the BioZ tag in D[2:0] (BTAG).
- Model (`max30001_bioz_decode_model.py`, `.json`, synthetic uniform 20-bit data): only **25.1%** of BioZ words are kept. The rest are dropped, because the data bits D[5:4] are non-zero. With D[3] = 0 (the datasheet's tag layout), the FIFO reset path cannot occur.
- Reachability: `_max30001ReadBIOZFIFO` is called from `max30001ServiceAllInterrupts()`, which the five shipped examples do not call. So the defect is reached through the library's interrupt or burst API, not through Example01.
- Severity: High for that API (75% of BioZ dropped). Source-level; untested on hardware.

## 4. F32 (new): the two BioZ decoders differ by 16×

- The streaming decoder keeps 18 bits at 24-bit scale (value = word & 0xFFFFC0, sign-extended).
- The new API keeps 20 bits and shifts right by 4 (value = word & 0xFFFFF0, shifted).
- The model gives a median ratio of **16.0** between them (`scale_ratio_stream_over_new_median`).
- Consequence: a calibration or conversion constant for one API gives values 16× wrong with the other. The datasheet conversion (`BioZ (Ω) = ADC × VREF / (2^19 × CGMAG × GAIN)`) assumes the 20-bit code, so the new API's scale matches the datasheet and the streaming scale does not.
- Status: source plus arithmetic. Severity: Medium-High for anyone mixing the two APIs.

## 5. Revised status

| ID | Before pass 5c | After pass 5c |
|---|---|---|
| F21 | "BioZ at 128 sps, producer at half rate" | Decoder label should be 64 sps (RATE = 0). Producer hold is intentional and matches the chip. |
| F31 | none | Streaming BioZ path uses ECG tag bits; keeps 25% of words (synthetic). |
| F32 | none | Two BioZ decoders differ by 16×. |
| F33 | none | Example read path does not check FIFO readiness or tags; sample_valid always true. |
| F20 | HR/RR mismatch | unchanged (the producer sends no HR/RR, so the decoder's 0/255 pattern is a decode artifact). |

## 6. Caveats

- All findings are source-level. The shipped code's behaviour on silicon is not measured, and the bench is not authorised.
- The 25% figure comes from a synthetic uniform model. Real BioZ codes are not uniform, so the exact fraction will differ, but the structural failure does not depend on the distribution.
- The datasheet points used here come from search snippets and the datasheet text chunks, not a full read of the register map. Confirm D[3] and the BioZ word layout against the full register section before a fix is written.
