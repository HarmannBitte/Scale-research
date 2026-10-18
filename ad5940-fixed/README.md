# Experimental AD5940 passive-bench hardening fork

Read `../AD5940-Bench-Firmware-Fixes.md` for the change summary and limitations.

**Source only. No ARM firmware image, board test, electrical accuracy claim or human-use authorization.** The default application is unarmed. Do not connect the evaluation board to people.

## Reproduce the host tests

Linux-like environment with GCC (including AddressSanitizer/UndefinedBehaviorSanitizer) and Python 3; no extra Python packages, network access, account or vendor IDE needed for these host tests:

```sh
cd ad5940-fixed
sh tests/build.sh
python tests/test_fixed.py
```

Tested with GCC 14.2.0 / Python 3.13.16. The build script:
- Compiles the modified common application, application main and shared library into **native object files**, not an embedded executable.
- Generates exact selected library-function extracts and explicit no-op peripheral mocks.
- Builds armed **synthetic** and unarmed native probes with ASan/UBSan.
- Builds a separate probe of actual modified port code against fake stalled registers.

All simulated standard values, counters and raw DFT words in these probes are synthetic. The tests do not emulate analog acquisition, oscillator accuracy, MCU timing or the entire processor. `tests/mockhardware/ADuCM3029.h` is deliberately fake host register storage. **Never use it in an embedded target include path.**

The pinned audit source is preserved separately at `../ad5940-audit/source` in the workspace. This fork retains the same curated scope: root documents/licenses, BIA directory and library, not every upstream example or external device pack.

## Parse the new protocol

```sh
python parse_bia_stream.py tests/synthetic-stream.bia --output my-parsed.json
```

Output must be a new file; existing files and source overwrite are refused. The parser is for **this fork's BIA1 framed JSON**, not the original vendor magnitude/phase UART or SensorPal format. Framing errors are fatal; it does not quietly skip corrupt lines and return a clean run. It preserves raw records in the parsed result and hashes the original input.

Format: `BIA1 <decimal ASCII payload byte count> <CRC32 hex> <ASCII JSON>\n`. CRC32 uses the standard reflected polynomial (check vector `123456789` -> `cbf43926`). CRLF transport endings are also accepted outside the payload. Payload maximum is 2,048 bytes. No debug/boot chatter is permitted in the framed stream.

Sessions require a non-placeholder run ID, schema 1, explicit synthetic/hardware kind and unqualified status. Records include configuration, calibration, measurement and fault/end events. Measurement sequences start at zero within a new firmware session; loss/gaps/duplicates/reordering in emitted records are rejected. The parser cannot detect every upstream acquisition loss or authenticate the source-kind declaration. Do not restart device sequence numbering under a reused run ID.

A valid frame/CRC is not a qualified measurement. Missing/unknown diagnostics remain null. No automatic conversion to the prior bench checker's mandatory clear/failed quality flags is supplied. Never fabricate clear flags to make a file pass.

## Target integration — not verified here

Selected target: **ADICUP3029 only**. The shared application/logger and selected Keil project are modified; other MCU ports/projects are not offered as hardened targets. The Keil project enables C99 and disables `ADI_DEBUG`. The logger implementation is included from the existing common application unit, so it does not need an extra project source entry.

A real target build still requires the exact Arm Compiler 5 / Keil device-pack setup and license review described in the audit. IAR dependencies and alternative targets were not rebuilt or qualified. Validate `snprintf`, `isfinite`, float formatting, stdio/UART error propagation, stack usage, RAM/link map and debug/programming behavior on the target.

Before any approved passive-fixture acquisition, deliberately supply:
- `BIA_BENCH_ARMED=1` (default 0).
- `BIA_BENCH_RUN_ID` as a unique 1–48 character alphanumeric/hyphen/underscore session ID, not `UNSET`.
- `BIA_BENCH_MIN_CURRENT_COUNTS` from the intended configuration's measured noise-floor policy (default 0, refuses startup).
- `BIA_BENCH_RCAL_OHM` from the independently characterized calibration standard (default 0, refuses startup).

**Do not copy the native harness defines into hardware.** Its floor 1 and RCAL 10,000 are synthetic test inputs, not measured recommendations or certificates. Manufacturer-approved passive interface/packing list, reference instrumentation, stimulus/current/compliance review and target build review remain prerequisites.

The first hardened integration accepts only nominal 50 kHz with the reviewed 16 MHz AFE clock, selected gain/RTIA/filter settings and requested ODR <=20 Hz. Sweeps and configuration variants fail closed. Iteration-based polling budgets must be validated for the real hardware; they do not express calibrated elapsed time. A bus fault latches and requests AFE reset; no autonomous rearm/recovery is implemented.

Blocking framed output remains: there is no DMA or producer-consumer transport queue. The bounded batch policy stops on excess backlog rather than overrunning memory. Throughput, sustained operation and actual stop/reset behavior are not tested.

## Archive/provenance and licensing

- `bench-hardening.patch`: complete diff against the preserved audited source subset. Apply from a copy of that subset using `patch -p1`; it includes new logger files.
- `upstream-manifest.json`: original repository/submodule pins and original worktree hashes.
- `delivery-manifest.json`: final delivered file hashes and scope.
- `fix-status.csv`: implemented, disabled and unresolved items.
- `tests/build-receipt.txt`, `test-receipt.txt`: executed build/test receipts.
- `tests/synthetic*.bia`, matching parsed JSON: examples generated by the native mocks, not hardware logs.

Original ADI license files and notices remain under `source/`. Modified files carry conspicuous notices. ADI-product, combination, third-party/toolchain restrictions and disclaimers remain applicable; this is not an unrestricted MIT/BSD relicensing. The new host tooling and modifications do not alter the upstream license obligations. Review the exact intended integration before redistribution.

The delivered archive omits generated native binaries, object files and Python caches; rebuild them with the commands above. Neither licenses nor hashes establish hardware safety, calibration traceability or fitness for clinical use.
