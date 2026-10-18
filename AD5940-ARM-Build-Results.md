# AD5940: real ARM cross-build completed

**17 October 2026 — compile/link gate passed; physical-board gate not performed**

The next step is now complete: the hardened application **compiles and links as real Cortex-M3 ARM firmware using the actual ADuCM3029 device headers, vendor startup code and vendor linker script**. This is no longer only a native/mock build.

**Important distinction:** this is an experimental **GNU Arm/newlib integration**, not a successful build with the original proprietary Keil Arm Compiler 5 project. Neither image has been executed on a board, flashed, or cleared for acquisition.

## Deliverables

- [Download the ARM build/reproduction package](AD5940-ARM-Build-Package.zip)
- [Build instructions and profile warnings](ad5940-target-build/README.md)
- [Compiler/linker receipt](ad5940-target-build/receipts/target-build.txt)
- [Machine-readable ELF/startup/memory checks](ad5940-target-build/receipts/artifact-checks.json)
- [Independent clean-rebuild comparison](ad5940-target-build/receipts/clean-target-rebuild.json)
- [78 common regression tests](ad5940-target-build/receipts/common-regression-tests.txt)
- [10 new target-integration host tests](ad5940-target-build/receipts/target-io-tests.txt)

The previous audit and host-only fork/package remain unchanged. The new work is in `ad5940-target-build/`.

## What actually built

| Component | Used for this build |
|---|---|
| Processor target | ADuCM3029, Cortex-M3, Thumb, software floating point |
| Compiler | Debian-packaged `arm-none-eabi-gcc` 14.2.1, release 20241119 |
| C library | Full newlib, Debian package 4.5.0.20241231-1; not newlib-nano |
| Device pack | **AnalogDevices.ADuCM302x_DFP 3.2.1** |
| CMSIS | Core headers from **CMSIS 5.2.0**, commit `80cc44bba16cb4c8f495b7aa9709d41ac50e9529` |
| Startup/linker | The selected device pack's GCC ADuCM3029 startup and linker files, unmodified |
| Application | Separate copy of the hardened fixed-frequency BIA fork, with additional MCU/GNU integration changes |
| Hardware substitute in ARM build | **None:** fake register headers are used only by separately labeled host tests |

The historical device-pack release is listed by Keil, and ADI documents the device-pack installation workflow. This build deliberately uses the pinned project-era dependency rather than silently migrating to a different SDK. [1](https://www.keil.arm.com/packs/aducm302x_dfp-analogdevices/versions/) [2](https://wiki.analog.com/resources/eval/user-guides/eval-adicup3029/software/aducm302x)

The downloaded device-pack archive SHA256 is `845c537cac31a8f1a7e745e7c89970ad222e18aa5079e961cd17485dc89b7f7e`. The retained vendor subset, CMSIS files, licenses, source changes, tools and final artifacts have a delivery manifest.

### Two build profiles, neither cleared for flashing

1. **`unarmed`** — `BIA_BENCH_ARMED=0`, run ID `UNSET`, current floor 0 and RCAL 0.
2. **`fullpath-linkcheck`** — acquisition code compiled with `BIA_BENCH_ARMED=1` so the linker cannot hide its resource requirements merely by discarding the disabled path. **Run ID remains `UNSET`, current floor remains 0, and RCAL remains 0.** The application must therefore refuse acquisition.

The second profile is a link/resource check, **not a characterized or ready-to-run measurement configuration**. Both profiles are included for inspection as ELF files; no flashing script, HEX or BIN is supplied. ELF files can themselves be flashed by some tools, so the absence of a HEX file is not a safety barrier.

## Integration problems found and addressed

### 1. The original default stack was too small for the logger

The vendor GCC startup defaults to **1,024 bytes of stack**. The compiled `AppBIABenchExportFrames` function alone requires **2,416 bytes**, before nested C-library calls or interrupt context.

This integration reserves **8,192 bytes of stack** and **4,096 bytes of heap** through the startup's supported configuration macros. ELF checks confirm those reservations and the initial stack vector.

**This fixes the obviously insufficient reservation; it does not prove an 8 KB worst-case stack bound.** The precompiled C library has no matching `.su` analysis here. Actual stack high-water, formatter behavior, exception nesting and fault paths must still be measured or otherwise bounded.

### 2. GNU/newlib needs a real output backend

Overriding the original port's `fputc` is not sufficient to retarget newlib's `fwrite`/`printf` path. I added:

- `_write` forwarding to the bounded UART transmitter, with error propagation.
- A bounded `_sbrk` using the actual linker-reserved heap, rather than an unchecked heap-growing stub.
- Character-stream metadata initialization and explicit unsupported-operation failures.
- A terminal `_exit` path with best-effort AFE reset-latch clear and CPU halt.
- Unbuffered stdout/stderr initialization, while retaining per-frame write/flush checks.

The linked ELF resolves these functions to the new adapter. Disassembly also shows the adapter calling the selected UART `fputc`. Host tests exercise the actual adapter and MCU transmitter against fake registers; **real serial output remains untested**.

### 3. The original UART setup enabled an unhandled receive interrupt

This integration has a TX-only logger and no receive-command protocol. UART RX/status interrupt enables are now off, and the corresponding NVIC interrupt is disabled. The unused startup UART vector remains a default weak handler; it is not advertised as an implemented receiver.

The AFE external interrupt vector resolves to the real port handler, not the weak default.

### 4. Startup should not release AFE reset before application gates

MCU resource initialization now clears the configured reset-pin latch before enabling its output and leaves it asserted. Only the later, gated AFE initialization calls `AD5940_HWReset` to release reset.

This is checked in source and fake-register probes. **It is not proof of the physical reset voltage or power-on behavior**, including the interval before firmware reaches this routine. Independent electrical review remains necessary.

### 5. Reject invalid UART setup before unsafe arithmetic

The integration accepts its intended **230,400 baud** profile only. Unsupported baud requests and a nonpositive computed divider fail rather than reaching a division by zero. Other baud rates have not been qualified.

### 6. Fail-stop on sequence-generation failure

Review of initialization also found two sequence-generation error returns that bypassed the common stop/invalidation helper. The top-level application already aborted on these errors, but a direct API caller should not have to provide that cleanup. The stop helper also disables the software sequence generator first, so shutdown register writes reach hardware rather than being recorded as more sequence instructions. Both returns now stop/invalidate acquisition state; an injected generation failure is covered by the additional regression.

## Memory-map results

All values below come from the actual linked images, not native `sizeof` estimates.

| Resource | Unarmed | Full-path link check |
|---|---:|---:|
| Flash load bytes, including initialized RAM data | 39,280 | 63,216 |
| Static data + BSS in the selected 16 KB DSRAM_B region | 8,068 | 8,172 |
| Remaining space in that DSRAM_B region | 8,316 | 8,212 |
| Reserved stack in DSRAM_A | 8,192 | 8,192 |
| Reserved heap in DSRAM_A | 4,096 | 4,096 |
| Unallocated gap between heap and stack reservations | 4,096 | 4,096 |

The gap is **not a configured hardware guard**. Free space in the other RAM bank is not automatically available to `_sbrk`.

The GNU memory-usage summary alone omits the initialized-data flash load from its explicitly addressed load-image accounting. The artifact checker separately totals ELF load segments and checks the flash high-water address against 256 KB, avoiding that misleadingly low flash figure.

## Verification performed

- Both ARM images compile and link, with no unresolved symbols.
- ARM ELF architecture, initial stack pointer, reset vector/entry, security-options location, heap/stack reservations and RAM/flash limits checked.
- Compiler dependency files confirm use of real device/CMSIS headers, not the mock-header directory.
- Full-path image retains the real BIA decode, ISR and HSRtia calibration implementation.
- Selected semihosting-backend indicators were not found; output is explicitly retargeted to UART.
- **All 77 earlier common regressions pass again, plus one new initialization-failure regression (78 total).**
- **10 additional host integration tests pass under AddressSanitizer/UndefinedBehaviorSanitizer:** write routing, UART stall, heap boundaries, invalid writes, initialized stream metadata, RX-interrupt suppression, oscillator timeout, baud/divider rejection and reset-hold initialization.
- A separate clean directory rebuilt both ARM images from source/vendor inputs with no copied objects. **Both resulting ELF files were byte-identical** to the first build using the same installed compiler/libraries. Checkout-path debug information is normalized by the build flags.

No Cortex-M3 instructions were executed here. Static artifact inspection and host tests are different evidence from target execution.

### Warnings were triaged, not hidden

The build emits **13 warnings per profile**, mostly inherited signedness, unused-parameter/declaration style and compressed-code indentation warnings. The shared library also warns that `HSDACCode` may be uninitialized in `AD5940_ADCPGACal`.

That separate ADC-PGA calibration routine is **absent from both linked BIA images**; the artifact check enforces that observation. It remains an unresolved issue for users of that other API. This is not an all-library audit or a warning-free build. Full diagnostics are retained in the receipt and warning-triage file.

## What remains before a real passive-fixture test

1. **Hardware inventory:** exact ADICUP3029/BIOZ board revisions, manufacturer-approved Z-Test interface/cables, host/programmer setup and available reference instrument.
2. **Independent target/code review:** particularly reset sequencing, security options, clock assumptions, UART routing, memory map and polling budgets. The iteration budgets have not been calibrated into wall-clock deadlines.
3. **A reviewed characterization procedure:** RCAL must come from an independently characterized standard. The DFT current-floor policy needs actual noise characterization; the package does not invent that threshold or provide a validated noise-characterization mode.
4. Only after those gates, explicit authorization and a manufacturer-approved passive setup: controlled board execution, serial-format checks, measured clock/timing and stack/heap high-water checks.
5. Then comparison of fixed-frequency R/RC measurements against the calibrated reference, including uncertainty, drift, settling and loss/fault behavior.

The earlier [bench acquisition specification](Impedance-Bench-Acquisition-Specification.md) remains the requirements document, not a claim that those measurements have happened.

**Still unavailable:** qualified clipping/compliance/contact diagnostics, acquisition timestamps, independently measured frequency, sweep operation and accuracy/uncertainty evidence. Records remain unqualified; the parser cannot convert unknown flags into passes.

**Do not connect this evaluation board to people. No purchases, flashing, external contact or physical tests were performed.**
