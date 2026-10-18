# AD5940 BIA firmware and export audit

**17 October 2026 · Pinned source review plus host-only tests · No hardware connected**

## Verdict

**Useful development starting point; not a measurement-grade logger as shipped.**

The four-wire `AD5940_BIA` example has the raw voltage/current DFT data and complex RTIA calibration needed to build a reproducible local acquisition path. However, the stock UART output exposes only **frequency, impedance magnitude and phase**, and several error-handling paths need correction before relying on its records.

**Procurement implication:** keep the AD5940 bundle as a conditional bench candidate, but budget for firmware/export engineering—not just a terminal-to-CSV parser. Do not treat this audit as approval to purchase, connect people, or deploy a body-composition model.

### Most consequential findings

1. **Raw DFT data are available before processing, but processing overwrites the same buffer.** Capture them before that happens.
2. **The FIFO-capacity check does not enforce the supplied buffer limit.** A mocked run requested 516 words despite a declared 512-word capacity.
3. **Calibration errors can be swallowed.** A mocked calibration failure still produced an application-level success return.
4. **Zero current can produce infinity/NaN with a success status.** There is no numerical validity gate in the processing function.
5. **The caller ignores initialization/start/ISR return codes.** An ISR error can leave the input capacity masquerading as an output record count.
6. **Published source is restricted to use with ADI processors/products.** It is not an unrestricted MIT/BSD-style foundation, and the supplied target build depends on external development tools/packs.

**Executed evidence:** 21 host-side tests passed, including 40 synthetic complex-arithmetic comparisons and 12 frequency-word cases. Several tests deliberately assert that an unsafe or invalid behavior occurs: their passing means the finding was reproduced, **not** that the firmware passed qualification.

## 1. Exact scope and reproducibility

| Item | Audited identity |
|---|---|
| Examples repository | `analogdevicesinc/ad5940-examples` |
| Examples commit | `ae917b69b4f71214c7f19ae3eef563b9c547d48f` |
| Required `ad5940lib` submodule commit | `d4c2ba01f0c1f8cb47264905407a4a3f7bf1cd47` |
| Library header version macros | 0.2.1 |
| Application reviewed | `examples/AD5940_BIA`, primarily the ADICUP3029 target |
| Native test environment | GCC 14.2.0; Python 3.13.16 |
| Embedded target build / flashing | **Not performed** |
| SensorPal binary/firmware behavior | **Not audited or executed** |

Artifacts: [source/provenance manifest](ad5940-audit/source-manifest.json), [unaltered BIA implementation](ad5940-audit/source/examples/AD5940_BIA/BodyImpedance.c), [findings table](ad5940-audit/findings.csv), [test receipt](ad5940-audit/tests/test-receipt.txt), [captured probe outputs](ad5940-audit/tests/probe-results.json), [test runner](ad5940-audit/tests/run_audit.py), [reproduction instructions](ad5940-audit/README.md), and [downloadable audit package](AD5940-Audit-Package.zip).

The retained source is a **curated subset**, not a full buildable repository: root documentation/licenses, the complete BIA example directory, and its library worktree. Original worktree file hashes were recorded before pruning unrelated examples/documentation and Git metadata. The test suite verifies that retained upstream files are unchanged. Generated function extracts and test wrappers are identified separately; full applicable upstream licenses are retained.

Pinned upstream references: [examples tree](https://github.com/analogdevicesinc/ad5940-examples/tree/ae917b69b4f71214c7f19ae3eef563b9c547d48f), [library tree](https://github.com/analogdevicesinc/ad5940lib/tree/d4c2ba01f0c1f8cb47264905407a4a3f7bf1cd47).

## 2. Acquisition-to-export trace

### A. Configuration and sequencing

`AD5940Main.c:97–111` and `BodyImpedance.c:20–65` together configure the example:

- Nominal sine frequency: **50,000 Hz**.
- Requested output rate: **20 Hz**, subject to the sequence-time limit.
- HSTIA selection: **1 kΩ**, with complex RTIA calibration.
- Assumed external calibration resistor value: **10,000 Ω**.
- DFT: **8,192 points**, SINC3 source, Hanning window enabled.
- DAC amplitude parameter: **800 mV peak-to-peak**, with separately configured DAC/excitation gains. This is **not a measured current or a human-safe stimulus specification**.
- Sweep disabled by default; dormant defaults are a 100-point logarithmic sweep from **10 to 150 kHz**, not our proposed 5–200 kHz profile.

The amplitude/RCAL defaults must be reconciled with the actual board and selected passive-load range. Do not substitute the preceding MAX30009 current setpoint into this voltage-drive example.

`BodyImpedance.c:308–327` sequences two DFT acquisitions: first the HSTIA current-related voltage, then the differential load voltage at AIN3/AIN2. The conversions are **sequential, not simultaneous**. A changing load during the pair can affect their ratio.

Comments describing a FIFO pair as “RCAL data” are misleading for the normal measurement path: the code actually consumes **current-related and load-voltage DFT pairs**. RCAL is involved separately in RTIA calibration.

### B. FIFO data and complex conversion

`AppBIAISR` reads complete groups of four FIFO words. `AppBIADataProcess`, at `BodyImpedance.c:516–567`, interprets each group as:

1. Current-channel DFT real word.
2. Current-channel DFT imaginary word.
3. Load-voltage DFT real word.
4. Load-voltage DFT imaginary word.

It masks each to 18 bits and sign-extends bit 17. It negates the DFT imaginary component when calculating channel phase:

`phi_V = atan2(−DFT_V_imag, DFT_V_real)`

`phi_I = atan2(−DFT_I_imag, DFT_I_real)`

`|Z| = |DFT_V| / |DFT_I| × |RTIA_cal|`

`phi_Z = phi_V − phi_I + phi_RTIA_cal`

Equivalently, for the audited arithmetic:

`Z = [complex(Vreal, −Vimag) / complex(Ireal, −Iimag)] × complex(RTIA_cal)`.

The internal output phase is **radians**; the UART formatter converts it to degrees. R and signed X can be reconstructed with cosine/sine, but cannot recover discarded raw DFT words, ADC clipping evidence or calibration history from magnitude/phase alone.

The host arithmetic tests agree with an independent Python complex-number calculation for 40 seeded synthetic cases. A synthetic capacitive case gives negative X under the proposed canonical convention. **This does not verify the actual board's wiring, polarity, parasitics or physiological interpretation.**

### C. Calibration

`AppBIARtiaCal`, at `BodyImpedance.c:365–408`, calls the library's `AD5940_HSRtiaCal`. The library measures voltages across RCAL and RTIA, applies its polarity conventions and returns complex RTIA in polar form. Calibration data live in `RtiaCurrValue` and, for sweeps, `RtiaCalTable`.

Calibration runs at initial application setup or when `ReDoRtiaCal` is set. Merely requesting sequence regeneration with `bParaChanged` is **not** the same as invalidating/repeating calibration. A new acquisition layer must bind calibration to all relevant settings.

This is **RTIA calibration**, not proof that all external cables, switches, sense loading and contact errors are corrected. Independently characterized held-out fixtures remain necessary.

### D. UART output

`AD5940Main.c:32–45` prints one frequency prefix per call, then magnitude/phase for each returned record. The exact formatter produced this host-only demonstration:

```text
Freq:50000.00 RzMag: 500.000000 Ohm , RzPhase: 0.000000
RzMag: 600.000000 Ohm , RzPhase: -5.729578
```

That is **not** a self-describing per-record CSV protocol. Frequency is an application configuration/state value, not a measured frequency certificate. No per-record timestamp, sequence number, raw DFT values, status or calibration identifier is printed.

The ADICUP3029 target initializes UART at 230400 baud and transmits through blocking character output. Its MCU interrupt handoff is a Boolean flag, not an event counter. These choices do not prove that data will be lost at the default rate, but they require explicit backlog, overflow and transport testing.

**Debug caveat:** the Keil project enables `ADI_DEBUG`; sweep calibration can print RTIA diagnostic lines. This is not a complete structured calibration export, and fixed-frequency calibration does not use that same sweep print path. Debug and measurement text can mix; do not treat every terminal line as a measurement record.

Sources: [pinned application main](https://github.com/analogdevicesinc/ad5940-examples/blob/ae917b69b4f71214c7f19ae3eef563b9c547d48f/examples/AD5940_BIA/AD5940Main.c), [BIA processing/sequencing](https://github.com/analogdevicesinc/ad5940-examples/blob/ae917b69b4f71214c7f19ae3eef563b9c547d48f/examples/AD5940_BIA/BodyImpedance.c), [library implementation](https://github.com/analogdevicesinc/ad5940lib/blob/d4c2ba01f0c1f8cb47264905407a4a3f7bf1cd47/ad5940.c).

## 3. Reproduced problems and their limits

| Finding | Evidence | Required response |
|---|---|---|
| **FIFO capacity not enforced** | `BodyImpedance.c:589–593` detects `FifoCnt > BuffCount` but executes only a TODO, then reads the full count. Mocked 516-word FIFO / 512-word capacity: success, 516 requested words, 129 results. A 1,024-word case also exceeds that capacity | Enforce capacity before the read; define bounded chunking, alignment and overflow invalidation. Never simply truncate without recording loss |
| **ISR error leaves stale count** | Initialization/wakeup failures return before `*pCount=0`. Mocked wakeup failure: error −9, count still 512. The main loop ignores the return code and passes that count to the formatter | Zero output count before any early return; propagate errors; do not format failed batches |
| **Calibration errors swallowed** | The application ignores `AD5940_HSRtiaCal` return values and returns OK. An injected parameter error leaves the previous 1,000 Ω calibration value and produces success | Propagate failure, invalidate calibration/results, require finite valid coefficients and a new calibration ID before restarting |
| **Zero current accepted** | Stock processing returns OK with infinite magnitude when current DFT is zero; both zero channels yield NaN. Zero calibration magnitude is also accepted | Reject zero/near-noise-floor denominators and invalid calibration; require finite outputs; preserve failure reason |
| **Sweep input not fully guarded** | A one-point logarithmic sweep produces nonfinite output in the extracted library function. Application calibration table has 100 slots, but the calibration loop uses the configured point count without a local table-size guard | Validate sweep endpoints/count, table capacity, supported settings and every generated frequency |
| **Raw provenance overwritten** | Output is written in place into the input buffer after sign/mask conversion | Archive original words/status and signed DFT values before deriving polar results; use separate buffers |
| **Quality metadata absent from output** | Formatter emits only frequency/magnitude/phase. Library defines ADC threshold and FIFO overflow/underflow interrupt sources, but the BIA acquisition/output path does not turn them into an exported validity record | Design and verify actual diagnostic coverage; unknown is not “clear” |

### Important qualifications

- The FIFO tests **did not perform an actual out-of-bounds write**: backing storage was deliberately larger than the advertised capacity. They demonstrate that the function ignores its caller's limit. A real 512-word buffer can be exposed if backlog exceeds it.
- A 512-word buffer holds only 256 two-float polar records. If an error leaves count 512 and the caller formats it, there is a **static out-of-bounds-read risk**. That caller-chain consequence was reviewed, not executed against an undersized buffer.
- Calibration failures were injected through a mock; actual analog calibration failure rates were not measured. The library itself has parameter-error returns, and the application does not propagate them.
- A phase outside ±π is not automatically an invalid impedance: the source does not wrap it, so downstream comparison must use wrapped angular differences.
- FIFO tags/ECC are not validated by this processor; it masks to 18 bits with an ECC TODO. The original full words should be retained, but meaningful validation requires confirming the exact FIFO mode/device documentation.
- Unbounded waits exist in initialization/calibration and MCU transport paths. Add timeouts and fault recovery; their physical timing was not exercised.
- A modest DFT magnitude does not prove that the ADC or analog path never clipped. Threshold/status configuration and stimulus/compliance characterization require separate design and hardware tests.

## 4. Missing-data matrix

| Required evidence | Internally available in reviewed source? | Stock measurement UART? |
|---|---|---|
| Voltage/current raw DFT pairs | Yes, before in-place processing | **No** |
| Original FIFO words and potential tags | Yes, immediately after read | **No** |
| Signed R/X | Derivable from calibrated complex result | **No**, only polar output |
| Calibration RTIA magnitude/phase | RAM; conditional sweep debug print | No complete structured archive |
| Calibration RCAL measurement/uncertainty | Configured nominal RCAL; no traceable certificate embedded | **No** |
| Requested frequency and settings | Application configuration | Frequency only; no complete configuration |
| Programmed frequency word / silicon mode | Library computes it using assumed clock and detected silicon mode | **No** |
| Independently measured actual frequency | Not established here | **No** |
| Monotonic timestamp / session / per-record counter | Not in stock measurement record | **No** |
| ADC/FIFO diagnostic state | Relevant register/interrupt APIs exist; full coverage not implemented here | **No** |
| Compliance/contact/lead validity | No complete exported diagnostic contract found | **No** |
| Transport integrity / drop count | No framed end-to-end record/loss protocol found | **No** |

Availability of register APIs is not evidence that a suitable contact/compliance detector already exists. Some faults may be indistinguishable from real load changes without additional circuitry or procedures.

## 5. Frequency, settling and sample-rate cautions

The library frequency-word calculation uses different widths for its S1/S2 silicon modes. The host tests checked nominal 5–200 kHz values in both branches against an assumed 16 MHz clock. All resulting computed frequencies were within **0.13 Hz** of those targets in these arithmetic tests. That is **quantization arithmetic only**, not oscillator accuracy, spectral quality or proof of supported analog performance at every point.

Export silicon identity, clock source, assumed/measured clock, frequency word and derived frequency—not merely `SinFreq`. Freeze settings separately by frequency. The existing sweep is not automatically our qualification profile.

The measurement sequence contains fixed waits, including 50 µs settling waits and a 250 µs wait marked with a TODO comment. It limits requested ODR using sequence timing, but parts of the timing calculation assume 16 MHz. Neither this review nor the source establishes adequate settling for every passive/contact load, or accuracy across the proposed 5–200 kHz sweep.

Source: library `AD5940_WGFreqWordCal`, lines 1555–1568; BIA sequence/configuration lines 294–348.

## 6. Build dependencies and licensing

### Reproducible target build is not yet established

The repository README recommends Keil and warns that ADuCM3029 needs **Arm Compiler 5.06 update 7**, not simply a standard current Keil installation. The reviewed Keil project identifies that compiler and **AnalogDevices.ADuCM302x_DFP 3.2.1**. It also requires device/CMSIS pack components.

The IAR project references external/generated `RTE` startup/device files and pack settings for **ADuCM302x_DFP 3.2.0** and ARM CMSIS **5.4.0**. Those dependencies and their full licenses were not downloaded or validated. The source tree alone is not a reproducible firmware-build environment.

The application includes both `ad5940.h` and `AD5940.h`; Windows-style paths use case variants too. A Linux/GCC target port must resolve casing and provide appropriate startup/linker/MCU support. The successful native probes compile only selected application paths with peripheral mocks and exact library function extracts. **They are not a successful Keil/IAR, ARM GCC, MCU or SensorPal build.**

No current IDE price, free-license eligibility, pack download availability or compiler activation/offline policy was established. Do not assume either “paid subscription required” or “entire build is free.”

### License findings — engineering reading, not legal advice

The [root license](ad5940-audit/source/LICENSE) permits reproduction, modification and distribution under conditions including:

- Complete license and copyright/proprietary notices retained.
- Modified versions conspicuously marked.
- Use solely with processors/products manufactured by or for ADI.
- Restrictions on combining code in ways that impose conflicting license terms.
- No support/update obligation; substantial warranty and high-risk-use disclaimers.

The [submodule license](ad5940-audit/source/examples/ad5940lib/LICENSE) also has ADI-product and license-combination restrictions. Source availability is **not unrestricted open-source portability**. The restriction is not simply “ADI MCU only”: this repository also provides a non-ADI MCU target using the ADI AFE. Obtain legal/vendor clarification for the intended combination and redistribution rather than inferring a universal ban or permission.

The root appendix contains an IAR source license restricting covered code to use with IAR Embedded Workbench. Device packs, startup files, CMSIS and the GUI have separate terms that require review. Do not assume that converting an IAR project to GCC carries every included runtime/startup component's permission with it, or that the entire package is automatically compatible with a copyleft product.

The source path itself contains no mandatory cloud measurement dependency identified in the reviewed acquisition/processing/printing code. That does not certify the GUI's installer/license, nor remove recurring reference-calibration and maintenance costs.

## 7. Minimum remediation before trustworthy bench logging

**Must fix before accepting qualification data:**

1. Enforce buffer capacity/alignment and bound all FIFO drains; test backlog and overflow.
2. Check initialization, start, ISR and calibration returns. Clear counts on failure, invalidate stale calibration and stop publishing success records.
3. Preserve raw FIFO and channel DFT data before processing, along with calibration inputs/results and configuration identity.
4. Reject nonfinite results and invalid/near-zero denominators; flag invalid calibration and unsupported settings. Preserve failure records rather than silently dropping them.
5. Validate sweep counts/table sizes and couple every frequency/configuration transition to its calibration and settling state.
6. Add a framed export with session/sequence IDs, timestamps, units/sign convention, raw channels, calibrated values and diagnostic/unknown states. Include loss/backlog counters and restart/end summaries.
7. Add timeouts/recovery and independently verify diagnostic behavior with passive fault fixtures.
8. Freeze and successfully build the exact embedded target/toolchain/packs under reviewed licenses, then compare its output against the host reference arithmetic and actual reference loads.

A [proposed export/remediation contract](ad5940-audit/Export-and-Remediation-Contract.md) accompanies this audit. It is **not an implemented firmware patch**.

**Recommended next development step:** create a separate, conspicuously marked bench-logger fork fixing error/buffer handling and adding raw/configuration/calibration capture, initially at one fixed frequency. Keep the unmodified pinned example as a reference. Only after the embedded build and passive bench tests should we add sweep/contact-QC behavior. A parser for the existing magnitude/phase text alone would not close the identified gaps.

## 8. What remains unverified

No board purchase, supplier contact, flashing, real UART capture, electrical test, calibration accuracy, actual sample timing, clipping/compliance coverage, cable/contact robustness or biological validation occurred. This audit covers the pinned four-wire BIA example and selected library paths, **not** every alternative example, current vendor binary or future revision.

The [bench specification](Impedance-Bench-Acquisition-Specification.md), [procurement review](Impedance-Bench-Procurement-Review.md), independent metrology requirements and separate human-safety gates still apply. The manufacturer [AN-1557](https://www.analog.com/en/resources/app-notes/an-1557.html) simulator-only warning remains controlling for this plan: **do not connect the evaluation board to people**.
