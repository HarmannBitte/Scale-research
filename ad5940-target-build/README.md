# Experimental AD5940 GNU Arm target integration

**Real ARM compile/link completed; no target execution or hardware qualification. Do not flash these artifacts or connect the evaluation board to people.**

See `../AD5940-ARM-Build-Results.md` for results and limits. This directory is separate from the unchanged `ad5940-fixed` host-only delivery.

## What is included

- `source/`: the curated hardened BIA source/library, plus additional marked ADICUP3029 MCU changes.
- `gnu/`: newlib adapter, reproducible cross-build script and independent ELF/startup/memory inspection script.
- `vendor/`: actual ADuCM302x DFP 3.2.1 headers/GCC startup/linker/system source and full pack licenses; CMSIS 5.2.0 Core headers and license. No fake headers enter an ARM build.
- `tests/`: common native regressions and additional explicitly fake-register integration probes.
- `receipts/`: executed compiler/test/ELF checks, toolchain versions and clean-rebuild comparison.
- `artifacts/`: **UNVERIFIED, DO NOT FLASH** ARM ELFs, maps, compiled gates and stack-frame reports.
- `integration-source.patch`: source changes and GNU integration additions relative to the previously delivered host fork; vendor/test dependencies are supplied by this complete package, not embedded into this review patch.
- `delivery-manifest.json`: hashes of delivered files, including both ARM ELF artifacts.

The device-pack files are not relabeled as unrestricted open source. Original ADI/ARM notices, full device-pack licenses and CMSIS license remain. Linked toolchain/newlib package license notices are under `licenses/`. No paid Keil/Arm compiler was installed or claimed to work.

## Rebuild with GNU Arm tools

Tested on Debian Linux with:

```text
gcc-arm-none-eabi       15:14.2.rel1-1
binutils-arm-none-eabi  2.44-3+23+b1
libnewlib-arm-none-eabi 4.5.0.20241231-1
libnewlib-dev          4.5.0.20241231-1
Python                3.13.16
```

A Debian-family installation can use `sudo apt-get install --no-install-recommends gcc-arm-none-eabi libnewlib-arm-none-eabi`; exact versions depend on its package repository. Different compiler/library versions require rechecking results and may not produce identical images.

From this directory:

```sh
sh gnu/build.sh
python gnu/check_artifacts.py
```

No network downloads are needed for these commands after the compiler/libraries are installed. The retained vendor files are provided. Build paths should not contain spaces. Outputs go under `build/`, not over the delivered artifacts.

The script targets Cortex-M3/Thumb/soft-float C99, uses full newlib/libm and the vendor GCC linker/startup, without LTO or fast-math. It compiles the real MCU main/port, common application and complete library translation units. Section garbage collection keeps the linked subset; the artifact checker ensures the full-path image retains real BIA decode/ISR/HSRtia calibration code.

`-ffile-prefix-map` normalizes checkout-path debug information. With the same installed tools/libraries, rebuilding from a separate clean directory produced **byte-identical ELF files for both profiles**. This is not a claim of reproducibility across different toolchains or independently rebuilt compiler libraries.

### Profile gates—read carefully

| Profile | ARMED | Run ID | Current threshold | RCAL |
|---|---:|---|---:|---:|
| `unarmed` | 0 | `UNSET` | 0 | 0 |
| `fullpath-linkcheck` | 1 | `UNSET` | 0 | 0 |

The second profile compiles acquisition code for honest link/resource inspection. **It is not a valid measurement configuration.** Startup is intended to refuse acquisition in both delivered profiles. No guessed threshold or calibration number is inserted to make a demo run.

The source-kind default is hardware, but no hardware data were generated here. Native test streams explicitly declare synthetic origin.

Neither ELF is cleared for flashing. No flashing command is included. A debugger may program ELF files directly, so lack of HEX/BIN output does not make them intrinsically non-flashable.

### Do not confuse this with a Keil build

The historical `.uvprojx` and IAR project remain within the retained source subset for provenance. The old Keil project has not been compiled or brought into equivalence with these GNU stack/newlib/interrupt settings. **Use the GNU script only to reproduce these receipts.** Do not open the legacy project and assume it inherits the GNU stack reservation or C-library adapter.

## Reproduce host regression tests

Native GCC with ASan/UBSan and Python 3:

```sh
sh tests/build_common.sh
python tests/test_fixed.py
sh tests/build_host.sh
python tests/test_target_io.py
```

The executed results are **78 common tests (77 earlier tests plus a new initialization-failure regression) and 10 integration tests**, including 100 seeded numerical cases inside the common suite. These execute native code, not Cortex-M3 firmware. Fake register storage is regenerated using the real DFP bit-mask values; it does not simulate electrical/peripheral behavior or timing. **Never put `tests/mockhardware` into a target build include path.**

The adapter tests call actual `_write`, `_sbrk`, MCU UART initialization/transmission and MCU clock-wait source against fake registers. They do not prove real UART baud, oscillator startup, GPIO polarity, MCU memory behavior or on-board stdio output.

The common suite's `tests/build_common.sh` is the earlier host build with mock-header regeneration added. It does not produce target firmware. `parse_bia_stream.py` is unchanged from the strict host-fork parser; it accepts this fork's BIA1 framed stream, not vendor SensorPal text.

## What changed for GNU integration

- Real device headers and vendor startup/linker, with 8 KB stack and 4 KB bounded heap reservations.
- Explicit newlib write/syscall adapter and initialized character-stream metadata.
- Unbuffered UART stdout/stderr.
- UART RX/status interrupt disabled because no receive handler/protocol exists.
- Unsupported baud and invalid divider rejection before unsafe arithmetic.
- Sequence-generation initialization errors now take the fail-stop/invalidation path.
- MCU resource setup keeps the AFE reset pin asserted until the gated application performs its hardware-reset sequence.

The reset change is an intended GPIO operation, not a measured guarantee that the physical AFE is held off during power-up or a clock failure. Early failures before GPIO initialization can only clear a latch best-effort. Hardware safety must not depend solely on these software gates.

## Known limits

The compiler emits 13 warnings per profile, retained and triaged in `receipts/warning-triage.json`; this is not a warning-free build. One warns of an uninitialized DAC-code path in the separate `AD5940_ADCPGACal` API, which is absent from both linked images. Other library APIs are not qualified merely because their translation unit compiled.

The largest reported application stack frame is 2,416 bytes. Reserving 8 KB corrects the vendor default's obvious 1 KB insufficiency but does **not** prove the complete call-chain/interrupt/library maximum. Actual stack/heap high-water and all formatter/error behavior remain untested.

Sweeps remain disabled, electrical diagnostic fields remain unknown, and every record remains unqualified. No validated noise-characterization mode is included. Actual RCAL/threshold inputs, accuracy, settling, timing, drift, loss behavior, fixture uncertainty and long-duration behavior require a reviewed passive-bench procedure and reference instrumentation.

No board was connected, no image was flashed, no purchases/contact were made, and no physical or human measurements were performed.
