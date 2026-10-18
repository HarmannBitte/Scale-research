# Deep impedance-software audit: how to read and rerun this folder

Date: 17 October 2026. Scope: deep-dive on the impedance and biosensing repositories in the collection (see `../open-projects-collection/`). This is research on software and source files. It is not a hardware qualification, a safety assessment or a validation of body-composition or physiological measurements.

## Start here
- `DEEP-FINDINGS.md`: the human-readable report (headline results, findings table, open items, scope limits).
- `findings.json`: the same findings in machine-readable form (29 findings, 5 open items), each with evidence levels.
- `MANIFEST.json`: SHA-256 and size of every file in this folder (regenerate after any edit).

## Evidence levels
- **S**: source observation at a pinned file and line.
- **H**: host probe. Upstream C code compiled with GCC on the host, with simulated peripherals. Not target silicon.
- **D**: Dart probe. Upstream Dart run with synthetic data (Dart 3.13.5).
- **DS**: vendor datasheet or vendor header, with the cited chunk or file.
- **T**: upstream test run in this sandbox.
- **U**: unverified; needs hardware, producer firmware or a register map not retrieved.

## Files
| File | Purpose |
|---|---|
| `run_native_probes.py` | Extracts upstream C functions from the collected sources, compiles them with GCC (and AddressSanitizer where used) with stubbed peripherals, and writes results. Needs `--sources PATH/TO/COLLECTION/sources`. |
| `native-probe-results.json`, `native-run.log` | Output of the probes. |
| `native-source-provenance.json` | SHA-256 of each extracted source region and the upstream file it came from (20 entries). |
| `dart-runtime-provenance.json` | Dart SDK version and download source used for the Dart probes. |
| `dart-probe/`, `biosig_probe.dart`, `biosig_value_check.dart`, `biosig-crc-probe.log` | Dart probes of the OpenView framer and the `.hpd` reader (F16, F17). |
| `producer-probe/`, `producer-probe.log` | Dart probe that feeds the real OpenView packet-type-2 framer and decoder with frames built as the Arduino example producer builds them (F15, F20, F21). |
| `impedance-test_circuit_fit-long.log` | Log of the long `test_circuit_fit` run (1 passed in 158.86 s). |
| `openebi-*.log`, `uprm-*.log`, `spectra-*.log`, `openeit-*.log` | Per-probe outputs and compile logs. |
| `generated/` | Extracted C sources compiled by the probes. |

## Rerun the native probes
```
python3 run_native_probes.py --sources /path/to/Open-Source-Projects-Collection/sources
```
Requires GCC and a sanitizer-capable libc. The compiled binaries go to `~/.cache/open-projects/deep-audit/native/`, which is not kept in snapshots. Expected: the same 20 provenance hashes, and results identical except ASan process IDs and stack addresses (verified 17 October 2026).

## Rerun the Dart probes
Install Dart 3.13.5 or later (the SDK is not stored here). Then from `producer-probe/`:
```
dart run lib/producer_probe.dart
```
Expected output: six lines with heartRate `0,255,0,255,0,255` and rr `0`, and `FramerStats(ok=6, ...)`.

## What is not settled
- F05: MAX30009 BIOZ_ADC_OSR bit table (not decoded from the fetched chunks).
- F22: whether a real MAX30009 FIFO count is in samples (the vendor driver implies it; not tested).
- F20: intended HR/RR contract for OpenView packet type 2. This is a question for the maintainer; no contact was made.
- Hardware reachability of F01, F08 and F09. No device was connected.
- Upstream fixes in F24 (pubspec.lock and assets missing from the snapshot) and F26 (melazab licence).
- Not run: Zephyr, Android, MATLAB, AVR runtime (see pass4/PASS4-RECEIPT.json).

## Pass 4 receipts
`pass4/` holds the AVR compile logs, the OpenView test and build logs, and `PASS4-RECEIPT.json`. Rerun the OpenView tests on a stripped working copy: see `openview_strip_assets.py` (copied into `pass4/`).

## Limits
- No device was purchased, connected, flashed or used on a person.
- No calibration against reference resistors or phantoms was performed.
- GCC host builds are not ARM target builds of the probed functions.
- A probe result is a statement about the code as pinned, not about the product built from it.
