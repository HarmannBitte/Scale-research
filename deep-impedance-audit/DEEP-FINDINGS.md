# Deep impedance-software audit: findings, evidence and open items

Date: 17 October 2026 (pass 2 completed the same day; pass 3 added the same day). Machine-readable version: `findings.json` (29 findings, 5 open items). Each finding names its evidence level, so readers can tell source observations from host probes, vendor claims and unverified items.

## Safety boundary

Nothing was connected to a person, a body or any live electrode. No board was powered, flashed or configured. Host probes used simulated peripherals and synthetic data. No purchase, maintainer contact or human experiment was carried out. None of the results below is a hardware measurement, a safety qualification or a body-composition validation.

## Evidence levels

| Code | Meaning |
|---|---|
| S | Source observation at a pinned file and line |
| H | Host probe: upstream C function copied verbatim, compiled with GCC, peripherals stubbed (not target silicon) |
| D | Dart probe: upstream Dart file run with synthetic data (Dart 3.13.5) |
| DS | Vendor datasheet (MAX30009, analog.com), chunks cited |
| T | Upstream test run in this sandbox |
| U | Unverified: needs hardware, producer firmware or a register map not retrieved |

## Headline results

1. **OpenEIT bipolar drive amplitude (F12, highest review priority).** The bipolar sine-amplitude macro is `VPEAK*40/DAC_LSB` = 61,323 codes. The AD5940-family amplitude field is 11 bits (0–2047; ADI header comment says 0–800 mV). The hardware therefore keeps 1,931 codes, about 754 mV equivalent, rather than the roughly 23.96 V the macro implies. The defined `VPEAK_BIPOLAR = 12.73 mV` (33 codes) is not used by that path. Which value is intended is unknown. The ADuCM350 manual lists bits above bit 10 of the amplitude register as read-only reserved (pass 4), so the value is most likely masked. Not measured on hardware. No hazard claim is made, and no electrode-level output was measured.
2. **UPRM FIFO parser (F01, F02, F22).** `spiBurst` writes out of bounds for FIFO counts of 0 or 1 and reads past its buffer for a truncated trailing word (confirmed with AddressSanitizer in host probes). Pass 3 resolved the count formula against ADI MAX32655_MAX30009 headers and the no-OS driver: count = bit 7 of 0x0A times 256 plus 0x0B. UPRM uses the wrong formula and also reads `count` bytes rather than `count*3` (inference, not hardware-tested).
3. **Recording integrity in OpenView (F17).** The `.hpd` reader never verifies the writer's CRC-32 and silently stops on errors. A Dart probe with the upstream files showed one corrupted byte changing a sample's value with no error, and a 200-byte truncation silently losing 4 of 30 samples.
4. **Open-circuit ambiguity in Spectra (F10, F11).** An open circuit can produce a magnitude of 0 instead of an error. Results in the range 2³¹–2³² wrap negative in the 32-bit field.
5. **OpenEBI (F08, F09).** Averaging zero measurements returns NaN, and the valid-data wait has no timeout.
6. **UPRM clock and excitation (F03–F07).** Sample-rate and frequency formulas match the MAX30009 datasheet (F04). The 45.25 µA figure is a peak value; the datasheet's equivalent setting is 32 µA RMS (F03). Some comments are stale (F05, F06), and a timing variable is truncated to 0 (F07).
7. **Test status (F19).** `impedance.py test_circuit_fit` passes: 1 passed in 158.86 s with thread caps. The earlier 90 s attempt was a time limit, not a failure.
8. **OpenView HR/RR with the Arduino producer (F20, F21).** The packet-type-2 decoder reads the producer's skip flag as heart rate: a real decoder fed Arduino-example frames reports HR 0, 255, 0, 255 ... and RR 0. The producer sends no HR or RR. BioZ is also labelled 128 samples/s though it changes at about half that rate.

## Findings (summary; full detail and citations in findings.json)

| ID | Repo | Finding | Levels | Status |
|---|---|---|---|---|
| F01 | UPRM | FIFO parser out-of-bounds access | S, H | Confirmed in probe; hardware reachability U |
| F02 | UPRM vs ADI drivers | FIFO-count formula wrong: MSB is bit 7 of 0x0A (times 256), LSB 0x0B | S, DS, H | Resolved against vendor headers; hardware test pending |
| F03 | UPRM | 45.25 µA is a peak value; datasheet quotes RMS | S, H, DS | Unit convention to document |
| F04 | UPRM | Frequency and sample-rate formulas match datasheet | H, DS | Consistent |
| F05 | UPRM | ADC_OSR comment stale (code uses 128) | S, H | Documentation |
| F06 | UPRM | 150 kHz comment vs 131 328 Hz | S, H | Documentation |
| F07 | UPRM | Seconds value truncated to 0 in µs variable | S, H | Low |
| F08 | OpenEBI | average=0 gives NaN | S, H | Confirmed in probe |
| F09 | OpenEBI | Valid-data wait without timeout | S, H | Silicon hang U |
| F10 | Spectra | Zero denominator reports 0 | S, H | Confirmed in probe |
| F11 | Spectra | Wrap-around in [2³¹, 2³²) | S, H | Confirmed; outside EIT range |
| F12 | Spectra | Bipolar amplitude wraps 61,323 → 1,931 codes | S, H, DS | Confirmed; ADuCM350 manual says upper bits are read-only reserved (pass 4); HIGH review |
| F13 | ProtoCentral Arduino | BioZ is 20 bits; ECG 18 bits | S | Source |
| F14 | OpenView | Documents BioZ as 19 bits | S | Documentation conflict |
| F15 | OpenView / Arduino | Packet type 2 producer IS in the Arduino library: 12-byte payload, skip flag in byte 8, no HR or RR sent | S, D | Producer layout confirmed |
| F16 | OpenView | Framer accepts frames with and without 0x00 pad | D | Confirmed for synthetic frames |
| F17 | OpenView | `.hpd` CRC not checked; silent loss | S, D | Confirmed by Dart probe |
| F18 | MAX30009 datasheet | 20-bit ADC, 256-word FIFO, 60601-1 lockout, 680 Ω calibration resistor, vendor-measured Cole error | DS | Vendor claim |
| F19 | impedance.py | test_circuit_fit passes in 158.86 s | T | Confirmed |
| F20 | OpenView | Decoder reads the skip flag as HR (0 or 255 alternating) and RR as 0 for the Arduino producer | D, S | Reproduced with the real decoder |
| F21 | OpenView | BioZ labelled 128 samples/s; producer changes BioZ every other frame | S, D | Source observation, not measured |
| F22 | UPRM | FIFO burst reads `fifoCount` bytes, but the count is in samples (3 bytes each) | S, DS, H | Inference, hardware test pending |
| F23 | all | Native probes reproduce from archived sources (20 provenance entries identical) | T | Verified |

## What the datasheet reading did and did not settle

Read: chunks 0, 4, 5, 8, 9 of 10 (the register map was not retrieved). Settled: the frequency and sample-rate arithmetic (F04); the 20-bit ADC and FIFO depth; the drive-current table. The FIFO-count bit layout (F02) was taken from the ADI MAX32655_MAX30009 header and driver, not the datasheet. Not settled: the amplitude-register write behaviour (F12) and the ADC OSR bit table (F05).

## Open items

1. Obtain the MAX30009 register map (FIFO_DATA_COUNT bit layout, BIOZ_ADC_OSR table) to resolve F02 and F05.
2. Determine the intended bipolar amplitude in OpenEIT (F12). Check whether the AD5940-family register ignores bits above 10 on write. Do not run the bipolar mode on hardware until this is resolved.
3. Decide the intended HR/RR contract for OpenView packet type 2 (F20). The Arduino producer sends none; the decoder reads the skip flag. Requires the maintainer or a producer that does send HR/RR. No contact authorised.
4. Hardware reachability tests for F01, F08 and F09. These require a bench with no person connected and are not authorised by this work.

## Scope of what was not done

- No device was powered, connected, flashed or used.
- No reference-resistor or phantom calibration.
- Host GCC only, not ARM target builds of the probed functions.
- No DearEIS or OpenView GUI run.

## Files

- `findings.json`: all findings, evidence and open items.
- `run_native_probes.py`: regenerates the host probes from exact upstream function bodies. Provenance hashes are in `native-source-provenance.json`.
- `native-probe-results.json` and per-case logs.
- `dart-probe/`: framer probe, BIOSIG CRC probe and their upstream files (unchanged copies).
- `biosig-crc-probe.log`: output of the CRC probe.
- `MANIFEST.json`: SHA-256 for every file in this directory.
- Collection receipt: `open-projects-collection/verification/impedance-py-test_circuit_fit-long-timeout.{json,log}`.

## Pass 3 (17 October 2026)

Changes from pass 2:

- **F02 resolved against vendor sources.** ADI MAX32655_MAX30009 `MAX30009.h` (OVF_COUNTER mask 0x7F in 0x0A; LSB 0x0B) and `MAX30009.c` (`((b0&0x80)<<1)|b1`) agree with the no-OS driver. UPRM's `(c1&0x7F)*2+c2` does not match.
- **F22 (new, inference).** UPRM sizes its SPI burst at `fifoCount` bytes (`txLen = rxLen = fifoCount`, lines 245–261) and parses 3-byte samples from that buffer. If the count is in samples, every burst is one third of the data it should be. Needs a hardware test.
- **F15 refined, F20 and F21 added.** The Arduino library's `Example01_BasicECGBioZ.ino` is the packet-type-2 producer: header `0x0A 0xFA`, length `0x0C 0x00`, type `0x02`, a 12-byte payload (ECG int32 LE, BioZ int32 LE, skip flag, three zero bytes), footer `0x00 0x0B`. Running the real `packet_framer_v3.dart` and `max30001_decoders.dart` (Dart 3.13.5) on six such frames gave heartRate `0,255,0,255,0,255` and rr `0` for every frame (`producer-probe.log`, source in `producer-probe/`). OpenView therefore shows meaningless heart rate for this producer. The BioZ channel is also labelled 128 samples/s while the producer changes BioZ about every other frame.
- **F23 (reproducibility).** `run_native_probes.py` was rerun against the archived sources. All 20 provenance hashes are identical; the only output differences are ASan process IDs and stack addresses.

Still open: F12 (bits 15:11 written to the 11-bit amplitude field; the ADuCM350 register table was not retrieved), F05 (MAX30009 ADC OSR table), F22 (hardware FIFO semantics), F20 (intended HR/RR contract, maintainer question). Nothing was run on hardware.

## Pass 4 (17 October 2026): outstanding items worked

Done in this pass (no hardware, no maintainer contact, no purchases):

- **F12 resolved from the ADuCM350 manual (UG-587 Rev. E).** `AFE_WG_AMPLITUDE` (0x4008003C): bits [31:11] are RESERVED and read-only; `SINE_AMPLITUDE` is bits [10:0]. The manual's rule for unused bits is that writes have no effect. The 61,323-code bipolar value is therefore most likely masked to 1,931 codes. Still not measured on hardware.
- **F05 narrowed, not resolved.** MAX30009 chunks 0-3 and 6-11 read. The ENOB, accuracy, drive-range, PLL and lead-off tables were read. The `BIOZ_ADC_OSR` bit table was not decoded: the only timing table in the last chunk has no column headers in the fetched text.
- **F26 melazab licence.** No root licence; GitHub's licence API returns 404. The four vendored `ad5940lib/LICENSE` copies are ADI's licence: use only with ADI products, and no combining with terms that differ. This is recorded as a licence difference. The project is not excluded.
- **F25 AVR compile-only.** The MAX30001 Arduino library (`protocentral_max30001.cpp`) compiles for ATmega328P with 0 errors and 13 warnings. The AD5933 sketch compiles with 0 errors and 0 warnings. Both use minimal stub headers, not the Arduino core, and nothing ran on a microcontroller.
- **F28 OpenView tests and build.** 42 tests in 5 files pass (settings 4, update banner 6, update controller 26, widget 2, board decoders 4). `flutter build linux --debug` succeeds. Caveats: the collected snapshot has no `pubspec.lock` and omits the font and branding assets, so the working copy had its asset declarations removed and its dependencies freshly resolved (F24). Two test files first failed because the kernel killed the Dart compiler for lack of memory; after the SDK was moved off the RAM-backed `/tmp`, both passed.

Still open (not doable without hardware or a maintainer): F05 (OSR table), F20 (intended HR/RR contract), F22 (hardware FIFO semantics), F01/F08/F09 (hardware reachability), and the upstream fixes in F24 and F26.

Not run, with reasons: Zephyr (multi-GB SDK on a 2 GB machine), Android (no SDK), MATLAB (no licence), AVR runtime (needs hardware).

Receipts: `deep-impedance-audit/pass4/PASS4-RECEIPT.json` and the logs beside it.
