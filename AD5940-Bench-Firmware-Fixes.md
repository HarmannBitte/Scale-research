# AD5940 bench firmware: hardened fork and regression results

**17 October 2026 · Experimental source changes, not qualified hardware firmware**

## Delivered

I created a **separate, conspicuously marked fork**, preserving the audited upstream snapshot. It fixes the reproduced buffer/count/calibration/numerical failures, adds a raw/configuration/calibration export path, and supplies a strict offline parser.

**77 regression tests passed**, running native C probes under **AddressSanitizer and UndefinedBehaviorSanitizer**, plus Python stream tests. The tests now require safe rejection or explicit invalid records rather than reproducing the old unsafe behavior. They include **100 seeded complex-arithmetic comparisons**.

- [Download source, patch, parser and tests](AD5940-Fixed-Bench-Package.zip)
- [Build/reproduction instructions](ad5940-fixed/README.md)
- [Regression receipt](ad5940-fixed/tests/test-receipt.txt)
- [Change-status matrix](ad5940-fixed/fix-status.csv)
- [Strict stream parser](ad5940-fixed/parse_bia_stream.py)
- [Synthetic normal stream](ad5940-fixed/tests/synthetic-stream.bia) and [parsed result](ad5940-fixed/tests/synthetic-stream-parsed.json)
- [Synthetic fault stream](ad5940-fixed/tests/synthetic-fault-stream.bia) and [parsed result](ad5940-fixed/tests/synthetic-fault-stream-parsed.json)

**No board was connected, no embedded image was built or flashed, and no electrical measurement was made.** This is not a deployable prequalified binary. Do not connect the evaluation board to people.

## What changed

| Audited problem | Implemented behavior |
|---|---|
| FIFO read could exceed the caller's buffer | Reject before reading when the count exceeds capacity, is not a complete four-word frame, is empty at a threshold event, or exceeds the bounded 32-frame internal batch. No silent truncation |
| ISR error left the capacity as an output count | Output count is cleared before early errors. Caller checks the return status and does not reinterpret the raw buffer as an array of polar results |
| Calibration failures ignored | Propagate the calibration return code; reject zero, negative or nonfinite coefficients; invalidate old coefficients before recalibration; refuse start without valid matching calibration |
| Changed settings could reuse stale calibration | Bind calibration to an explicit configuration signature and protected coefficient copy. Changes, recalibration requests and coefficient tampering invalidate it |
| Zero current produced infinity/NaN with success | Require a positive configured DFT-current floor; reject results below it and nonfinite/overflowing calculations; wrap phase with atan2(sin, cos) |
| Processing destroyed raw words | Decode into a separate frame structure. Preserve original full FIFO words, signed channel counts and derived values separately |
| Sweep table/count hazards | **Fail closed:** this first integration accepts fixed nominal 50 kHz only and refuses all application sweeps. Generic library sweep input validation also latches errors for invalid inputs |
| Unbounded waits on the selected BIA path | Bounded interrupt/register polls and selected ADICUP3029 SPI, delay, oscillator and UART waits; latched I/O fault handling. Attempt shutdown and hold AFE reset on a latched bus/timing fault |
| Polar-only unframed UART text | Length-delimited, CRC32-protected JSON records for session, configuration, calibration, measurement, fault and finite-run end events |
| Missing diagnostic evidence could look clean | Electrical/transport quality flags remain **null/unknown** and every measurement remains `qualification_eligible: false` |

The capacity policy deliberately stops a run rather than trying to recover an ambiguous backlog. A partial frame can arise from real sequence timing, so rejecting it may be conservative; physical testing is needed before introducing a safe frame-assembly/recovery scheme.

### Scope of timeout changes

The modified shared library covers the oscillator/initialization and HSRtiaCal waits used by this BIA path. The port changes target **ADICUP3029**. Other library applications still contain waits and have not been hardened or qualified. A polling-iteration budget is **not a measured millisecond timeout**; its appropriate value and fault latency require target measurements.

On a hardware fault, a software reset-pin assertion is an attempted safe stop, not independently verified proof that excitation ceased. GPIO behavior and all normal/fault conditions still require bench verification.

## Export and provenance

Each transport line has this structure:

```text
BIA1 <payload-byte-length> <8-hex-digit-CRC32> <JSON payload>\n
```

The parser validates framing, payload length, CRC, JSON structure, session identity, configuration/calibration linkage, sample sequencing, raw sign decoding and consistency of calibrated values with raw channels and RTIA calibration. It rejects corruption, duplicates, gaps, reordering, mismatched provenance, nonfinite values and unsupported qualification claims. A missing end record is reported as incomplete—not silently promoted to a complete run.

### Records now available

- **Session:** schema, run ID, hardware/synthetic origin declaration, explicit unqualified status.
- **Configuration:** application settings, actual readback of chip ID and frequency word, assumed clocks, clock-derived frequency estimate, effective ODR, gain/filter/DFT/window settings and configured current-floor policy.
- **Calibration:** configured RCAL value, complex RTIA result, identifiers and original calibration DFT words when available. The certificate field remains null; a configured value is not a certificate.
- **Measurement:** original four FIFO words; signed current-related and voltage DFT counts; R, signed X, magnitude and wrapped phase; IDs, sequence, raw interrupt flags and numerical status.
- **Fault:** error, last observed FIFO/interrupt/capacity state and available calibration trace; loss extent explicitly unknown.
- **End:** decoded-frame total for a finite requested run; still not proof of no upstream acquisition loss.

Raw channel values are **DFT counts**, not amperes or volts. Frequency readback plus an assumed clock is an estimate, not an independently measured frequency.

A fault detected after a successful FIFO transfer preserves the captured raw frames but marks their results invalid. The supplied synthetic fault example demonstrates this path; it is not a real ADC clipping experiment.

CRC protects framing against ordinary corruption; it is not authentication, an analog accuracy test, or a guarantee that the AFE acquired every intended sample.

## Conservative startup gates

The delivered source is **unarmed by default**. Its main application refuses acquisition unless all of these are deliberately configured:

1. `BIA_BENCH_ARMED=1` for an approved **passive electrical fixture only**.
2. A non-placeholder, run-unique `BIA_BENCH_RUN_ID`.
3. A characterized positive `BIA_BENCH_MIN_CURRENT_COUNTS` threshold.
4. A positive `BIA_BENCH_RCAL_OHM` representing the selected independently characterized standard.

The last two default to zero. The host tests use synthetic values solely to exercise code. **Do not copy their threshold or calibration number into hardware as if they were measured.** Supplying a positive value does not itself establish traceability; the source remains unqualified.

The accepted software profile is intentionally narrow: nominal 50 kHz, the reviewed 16 MHz clock configuration, selected 1 kΩ RTIA/gain/filter settings, and requested ODR no higher than 20 Hz. These are software compatibility bounds, **not guarantees of analog accuracy or adequate settling**.

The Keil project has C99 enabled and unframed debug printing disabled. The common application includes the new logger implementation from its existing translation unit, avoiding a missing additional-source-file entry in the project. The actual legacy toolchain/device packs must still be installed, licensed and tested before any target build is claimed.

## What the tests establish

The native harness compiles the modified common BIA application and exercises its real initialization/control/processing/ISR paths using mocked peripherals. Selected library helpers are extracted exactly from the modified library. Separate probes execute the actual modified SPI/delay port functions against explicitly fake, stalled register storage.

Regression coverage includes:

- Real 512-word host backing buffers, with sanitizers checking the oversized-FIFO rejection path.
- Zero/small capacities, partial/oversized batches, maximum supported batches, null pointers and wakeup failures.
- Calibration failure propagation, invalid coefficients, configuration changes and invalid reinitialization.
- Zero/noise-floor current, raw sign boundaries, raw-word preservation, wrapped phase and numerical parity.
- Bounded interrupt/register polling, stalled SPI and delay behavior, and invalid waveform inputs.
- Normal and invalid-record export pipelines; caller behavior on FIFO failure.
- CRC reference vector and strict parsing/rejection tests for corrupted, truncated, reordered, duplicate and misleading records.
- A separately compiled **unarmed** application that refuses initialization.

The whole modified common application, main application and library also compile to native GCC object files. **Neither that nor sanitizer success establishes an ARM target build, timing behavior, peripheral correctness, stack/RAM fit or measurement accuracy.** Fake register storage is not an MCU simulator.

## Remaining work—not silently declared fixed

| Item | Status |
|---|---|
| Complete electrical diagnostic coverage: clipping, compliance, lead/contact validity | **Not implemented/validated**; fields stay unknown and block qualification |
| Hardware acquisition timestamps and independently checked actual frequency | **Not available**; timestamp fields are null and frequency is labeled an estimate |
| Full register/board/build provenance and reference certificates in the stream | Partial configuration capture only; complete archive/manifest and certificate linkage remain required |
| Sweep operation, frequency-transition settling and contact-QC classification | **Disabled**, not qualified or replaced by a reduced-frequency assumption |
| Nonblocking/DMA/ring-buffer transport and autonomous reconnect/recovery | Not implemented; bounded blocking output and fail-stop limits are used instead |
| Target compiler, device-pack licenses, link map, memory/stack usage, floating-point printf and UART behavior | **Unverified on the actual embedded target** |
| Reference-fixture accuracy, uncertainty, drift, cable/contact behavior and long-duration integrity | **Not performed** |
| Human-connected design or clinical/body-composition validation | **Not authorized or performed** |

The parser deliberately cannot turn this telemetry into a “passed” bench qualification by filling unknown flags with zeros. Both synthetic parsed results keep `device_qualified: false` and `human_connection_authorized: false`.

## Source and licensing

The fork derives from the pinned [audit](AD5940-Firmware-and-Export-Audit.md): examples commit `ae917b69b4f71214c7f19ae3eef563b9c547d48f`, library commit `d4c2ba01f0c1f8cb47264905407a4a3f7bf1cd47`.

Upstream license files and notices are retained. Modified upstream C/header files and the changed project are marked. The package contains a [unified source patch](ad5940-fixed/bench-hardening.patch), [upstream provenance](ad5940-fixed/upstream-manifest.json) and a delivery hash manifest. ADI-product and third-party license restrictions still apply; this work does not convert the original firmware to an unrestricted license.

**Next gate:** review the patch, then reproduce a target build with the exact toolchain/device packs and inspect its memory map. Only after that, manufacturer-approved passive-fixture connection and independent reference measurements can establish whether these software changes work correctly on the board.
