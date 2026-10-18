# Open impedance and biosensing projects: collection and engineering investigation

**17 October 2026 · Research collection, not a hardware qualification**

## 1. Scope and outcome

All **15 project families** from the preceding survey remain in scope. **Licensing was not used to exclude or downgrade any candidate.** OpenEIT/Spectra is investigated on its technical merits alongside the others. Licence/attribution texts are retained as provenance, not treated as a reason to stop investigating.

The collection covers **25 distinct repositories and 26 commit-pinned snapshots**. The extra snapshot preserves the exact AD5940 library revision required by the examples, in addition to the library's current default-branch revision. Companion repositories were added where the original project depended on them or its README pointed to outdated software.

### What is delivered

- A compact, offline **source/design collection**, including available CAD, fabrication files, schematic PDFs, licences, selected documentation, and the investigated Arduino thesis.
- Per-file SHA-256 manifests, repository commit IDs, original upstream archive URLs and recorded archive hashes where downloaded.
- A searchable CSV catalogue and source-level findings register.
- Actual software/build receipts, including failures, timeouts and corrected research-environment problems.
- This engineering dossier, including data formats, calibration, missing pieces, dependencies and limits.

**Collection boundary:** these are not full Git mirrors. Large binaries, media, many manuals/datasets and generated files are selectively omitted and individually listed in the manifests. ADI no-OS is a **scoped MAX30009 source snapshot**, not the entire framework/SDK. Existing submodule relationships are not assumed to be included automatically: the AD5940 examples' exact library dependency was collected separately.

**No boards were purchased, connected or flashed. No human measurements were made.** Software tests, source inspection and successful linking do not establish electrical accuracy, physiological validity, or human safety. The AD5940 evaluation-board never-human-connected restriction remains unchanged.

## 2. What was verified in this investigation

| Area | Actual result | Boundary |
|---|---|---|
| Collection | 25 repositories, 26 pinned snapshots; file/archive hashes and omission inventories | Not full histories or a mirror of every binary/dependency |
| pyEIT | **62 upstream tests passed** | Software tests only; not an EIT hardware benchmark |
| pyimpspec | **139 selected upstream tests passed using unittest**, the upstream runner style | Four selected modules, not the entire suite; a pytest capture-related assertion failed in an earlier run |
| DearEIS | Installed from collected source; **43 selected project/utility tests passed** | No interactive GUI/rendering or full fitting/DRT suite validation |
| impedance.py | **34 upstream tests passed**, one expensive fitting test excluded from that run; a labelled synthetic RC fit also passed | Full-suite attempt timed out at 180 s. The isolated global-fit test then passed on its own (1 passed, 158.9 s, thread caps); the earlier 90 s run was a time limit, not a failure |
| BioScale | **4 upstream tests passed, 1 failed** | Failure is a missing argument in a test/API call; not evidence that physiological outputs are accurate or inaccurate |
| melazab AD5940 GUI | **5 upstream tests passed** | Mocked flash-target behavior; no device was flashed |
| melazab firmware | **All five programs built and linked with genuine GNU ARM tools** | Linker warnings remain; no execution, stack/noise testing or safety qualification |
| OpenEIT parser | Seven isolated input probes executed against the exact upstream function | No serial/BLE connection or full dashboard execution |
| Hardware files | Inventory/parsing of available schematics/CAD/PDFs; fabrication files preserved | No CAD DRC/ERC, production readiness review or physical verification |

The frozen environments and full command logs are in `verification/` inside the collection. Results are not silently combined into a blanket “all tests passed.”

### Important research-environment corrections

- Two impedance.py tests initially could not find fixtures because of a hard-coded repository-directory name. After supplying the expected directory alias, all 34 tests in the bounded selection passed without modifying upstream source.
- An early pyimpspec packaging attempt used the compact working copy and exposed a missing `COPYRIGHT` file in our collection filter. That filter was corrected. Subsequent checks used complete upstream source archives; both pyimpspec and DearEIS installed successfully. This was **not an upstream packaging defect**.
- Under pytest, one pyimpspec test expecting text on redirected stderr failed. The same four modules passed **139/139** with upstream-style unittest execution. This is recorded as runner/capture sensitivity, not a confirmed numerical defect.

## 3. Project dossiers

### 3.1 OpenEIT / Spectra — full inclusion, with four repositories

**Collected:** [electronics](https://github.com/OpenEIT/EIT_EE), [official firmware](https://github.com/OpenEIT/EIT_Firmware), [dashboard](https://github.com/OpenEIT/OpenEIT), and [dioptre GCC firmware fork](https://github.com/dioptre/EIT_Firmware).

**Architecture.** An ADuCM350-based impedance front end, external electrode switching, firmware measurement modes, and Python reconstruction/dashboard software. The documented system supports time-series impedance, spectroscopy and multi-electrode EIT. This is the closest collected end-to-end precedent for a multiplexed impedance imaging instrument—not a finished body-composition scale.

**Hardware collected.** Older editable Eagle board/schematic files, an electrode-flex KiCad board, fabrication Gerbers and their auxiliary files, a BOM spreadsheet, a flex manufacturing ZIP, and the newer `Spectra.PDF`. The newer PDF parsed as **11 pages** and identifies the ADuCM350 and supporting circuitry. The older editable design and newer Spectra schematic must be treated as **different revisions**, not one fabrication-ready matched set. Editable layout/BOM/assembly completeness for the newer revision was not established.

**Firmware findings.** In the inspected official `modes.h`, the spectroscopy array has **15 requested frequencies from 200 Hz to 70 kHz**. The common `FREQ` macro is **25 kHz**, whereas README descriptions also discuss 50 kHz examples. Those facts need to be reconciled with the selected sequence and actual clock/register settings; neither is a measured output-frequency guarantee.

Most importantly, the inspected `bioimpedance_spectroscopy()` path converts DFT results to magnitudes and emits `magnitudes:<frequency>;<value>`. The presence of phase functions elsewhere does **not** establish that this path exports signed R/X or calibrated phase. For our raw-complex-data goal, a firmware/export change may be needed.

**Data/analysis.** The dashboard contains its own older pyEIT code and reconstruction wrappers. Do not assume substituting current standalone pyEIT is API-compatible. The serial parser accepts comma-separated time-series/EIT data and semicolon-separated spectroscopy data. Its isolated probes rejected nonnumeric text but accepted NaN/infinity, empty frames, and dropped empty fields without a quality flag. A downstream adapter must enforce finite values, expected lengths and acquisition metadata.

**Maintenance work identified.** Root `setup.py` still pins much older dependencies than root `requirements.txt`; dashboard modules import old Dash shim packages; older reconstruction modules use removed NumPy aliases. The source explicitly comments out a macOS BLE path using `darwin_xx`. A clean compatibility environment and BLE migration are technical tasks, not reasons to discard the project.

**Configuration review item.** `SINE_AMPLITUDE_BIPOLAR` references `VPEAK * 40`, despite a separate `VPEAK_BIPOLAR` definition; the macro is used in firmware. This requires schematic/register review and passive measurement before interpreting or using that mode. No actual excitation amplitude is inferred from the macro alone.

**GCC fork.** The fork contains alternate startup/linker/source arrangements, support scripts, and mixed licence notices. Scripts such as `serve.sh` invoke J-Link; they are not a complete portable build recipe. No genuine Spectra firmware build or dashboard runtime was established during this investigation.

**Useful contribution to our research:** multiplexing, stimulation order, reference measurements, end-to-end acquisition/reconstruction, firmware/dashboard separation, and realistic legacy-integration lessons. EIT conductivity images are not DXA/CT tissue measurements.

**Licence provenance:** official repositories contain CC BY-NC-SA 4.0; the GCC fork has mixed per-file/third-party terms. Retained, with no licence-based exclusion.

### 3.2 OpenEBI — four-electrode spectrometer with editable hardware

**Collected:** [hardware](https://github.com/openebi/hardware) and [firmware](https://github.com/openebi/software).

**Architecture.** AD5933 spectrometer with an external four-electrode front end. Hardware includes legacy Eagle schematic/layout/CAM materials, BOM and schematic/assembly PDFs. The schematic did not parse as XML in our lightweight inspection, consistent with a legacy CAD format; this is not proof of file corruption or successful import into a modern CAD package.

**Acquisition.** Firmware defaults request a start near 4 kHz with 2 kHz increments and 48 increments, nominally reaching 100 kHz. The UART command interface exposes sweep, free-run and configuration functions. The sweep output is two numeric columns labelled `R I`.

**Critical distinction:** those columns are averaged **AD5933 real/imaginary register values**, not automatically calibrated resistance/reactance in ohms. The instrument front end and frequency response must be calibrated before converting them into physical complex impedance. We must not import them into our canonical ohm-valued schema without a documented transformation.

**Quality review items.** `main.c` contains polling loops waiting for valid data. Its configuration parser does not validate all conversion results, and `average` is not visibly constrained to a nonzero value before division. Interrupted hardware responses and malformed parameters need bounded behavior. These are source findings, not observed hardware failures.

**Evidence.** A 2012 paper is linked by the project and reports electrical-load experiments. The current collection establishes the design files and firmware, not a replicated measurement campaign or a clinical validation study. Old hardware/software dates mean CAD/toolchain and component lifecycle work remain.

**Build status.** Source reviewed; AVR build not executed because an AVR toolchain was not present. Licences retained: CC BY-SA 3.0 hardware, MIT software.

**Useful contribution:** a clear four-electrode architecture and low-level data path we can compare with the newer AFEs.

### 3.3 ADI AD5940 examples and libraries — dependency provenance matters

**Collected:** [examples](https://github.com/analogdevicesinc/ad5940-examples) and [library](https://github.com/analogdevicesinc/ad5940lib), including **two library revisions**.

The examples are pinned at `ae917b69…`. Their Git submodule explicitly requires library revision `d4c2ba01…`. The current library default branch resolved to a different revision, `818c5482…`. Both are preserved. A ZIP of the examples alone does not contain the submodule's source, and combining arbitrary latest revisions would not reproduce the intended project.

**Capabilities.** The ecosystem includes BIA, two-wire impedance, EDA and other applications. It provides switch-matrix/sequencer/DFT/calibration mechanisms, not independently validated body-fat, hydration, nerve-health or cardiac-health interpretations.

**Data.** The application examples have their own output structures and presentation functions. Preserve the underlying DFT/configuration/calibration context; do not assume every printed number from every example represents the same physical quantity.

**Verification status.** The collection resolves the dependency relationship. We did not rerun the already delivered hardened ARM program in this investigation. Its prior 78 common and 10 integration tests belong to **our existing package**, not these unmodified upstream snapshots.

**Useful contribution:** manufacturer reference code, especially for understanding calibration and register semantics. The evaluation board remains never-human-connected; no upstream example changes that restriction.

### 3.4 melazab/AD5940-BIOZ — actual GNU builds succeeded

**Collected:** [repository](https://github.com/melazab/AD5940-BIOZ), pinned at `dcd50963…`.

**Architecture.** ADICUP3029/ADuCM3029 with AD5940-BIOZ; hand-written startup/linker/register access, vendored ADI application/driver code, and a Tkinter GUI. Five firmware programs cover LED bring-up, two-/four-wire sweeps, and two-/four-wire time-series acquisition.

**Acquisition/data.** Sweeps default to 40 linear points from 1–200 kHz. Human-readable output includes requested frequency, complex impedance, magnitude and phase. The GUI streams received measurements to CSV separately from its bounded plot buffers. Zero-baseline subtraction is distinct from RTIA calibration, and baselines are volatile. Four-wire time-series is documented at a nominal 5 Hz; higher two-wire trigger settings do not prove achieved throughput.

**Build evidence:**

| Program | Text bytes | Initialized data | BSS | Build/link |
|---|---:|---:|---:|---|
| blink-led | 548 | 0 | 0 | Passed |
| measure-2wire-bioz | 48,880 | 2,764 | 2,784 | Passed |
| measure-4wire-bioz | 53,992 | 2,756 | 2,784 | Passed |
| time-series-bioz | 76,628 | 2,756 | 2,464 | Passed |
| time-series-bioz-2wire | 73,076 | 2,764 | 2,480 | Passed |

These are GNU `size` sections, **not** a complete runtime RAM budget: stack, heap and interrupt behavior are not proven by BSS totals. The measurement builds emitted linker warnings for unimplemented newlib/nosys functions. The code supplies a UART `_write`, so those warnings must be interpreted individually rather than declaring all output broken.

**GUI evidence.** All five upstream flash-target tests passed using mocked subprocesses and temporary directories. They test selection/identity behavior, not actual flashing, transport robustness or measurement accuracy.

**Open questions.** Full reset/timeout/error handling, throughput and calibration performance need additional review and passive testing. A project-wide licence for original application/GUI code was not located; vendored library licences are separate. This is documented but does not remove the project from the research collection.

### 3.5 ADI no-OS MAX30009 — structured driver, not a finished instrument

**Collected:** [MAX30009 project](https://github.com/analogdevicesinc/no-OS/tree/bdd9427af10c767f6bf3aa9a61100317d1192b44/projects/max30009) and associated driver, core headers/utilities, Maxim platform files and build scripts: **a scoped snapshot**.

**Architecture.** SPI/I²C register-access implementations, device initialization/configuration functions, FIFO/I-Q decoding, lock/status and lead-off mechanisms. The basic example documents 50 kHz stimulation and a 100-sample/s setting with tetrapolar MUX configuration. These are requested settings, not an independent performance measurement.

**Dependency/build.** It uses the no-OS platform/build abstraction and a MAX32655FTHR example target. The entire SDK, all transitive framework/platform components and a reproducible toolchain bundle were not collected. Therefore this snapshot is not presented as a self-contained successful build. Driver/example headers carry BSD-3-Clause identifiers.

**Data/calibration.** Register/FIFO access is useful for preserving raw counts and quality state. It does not by itself supply a full instrument calibration, per-frequency complex error budget, fixture de-embedding or population-specific composition model.

**Useful contribution:** an upstream codebase against which to compare custom MAX30009 drivers. The generated documentation endpoint previously found in search returned 404, but source and documentation-source files exist in the collection.

### 3.6 ADI MAX32655/MAX30009 example — GSR/EDA ancestry

**Collected:** [repository](https://github.com/analogdevicesinc/MAX32655_MAX30009).

The README targets GSR/EDA and prints quadrature, in-phase, BioZ and adjusted-BioZ columns. It is the ancestry of the UPRM project, not a general body-composition platform. A project-level custom Maxim permission notice is retained.

**Technical concerns.** Fixed setup/calculation assumptions need to be separated from general chip capabilities. The README has inconsistent jumper-state text. It also describes specific evaluation-board changes and human connections, which we did not perform or adopt as qualified instructions.

**Build status.** Source/documentation reviewed; no MSDK build or hardware test. Use it for baseline register/configuration provenance and comparison, not as evidence that later multi-frequency/BLE modifications are correct.

### 3.7 UPRM Multi-Frequency BioZ — acquisition, BLE, SD and movement handling

**Collected:** [repository](https://github.com/oscaroflores/UPRM-Multi_Frq-BioZ-Research), pinned at `b3a8844a…`.

**Architecture.** MAX30009/MAX32655 firmware, BLE service code, Python GUIs, SD/FatFs logging, IMU-related service logic and analysis scripts. The inspected `setFreq()` supports approximately 4 kHz and 131 kHz; the main loop alternates them and discards seven samples between accepted acquisitions. This is more specific than “multi-frequency”: it is not a general arbitrary sweep in the inspected implementation.

**Data format.** `calcBioZ()` decodes tagged I/Q words, handles negative ADC values, applies a cached counts-to-ohms coefficient and formats a row as `timestamp,Q_ohm,I_ohm,frequency`. It calls BLE transmission and SD writing from this path. Timestamps are reconstructed from sample index and rate; they are not automatically an independently measured host/device clock timeline.

**Hardening questions.** Sign/scaling conventions, overflow reporting, frequency-switch settling, coefficient validity, dropped notifications, storage failure and timebase behavior should be tested explicitly. The source calls `datsSendData()` before checking `snprintf()` length validity. That order merits correction/review before relying on bounded data transmission; we did not demonstrate an exploit or an overrun in operation.

**Calibration.** Scaling from gain/current/reference quantities is not the same as a measured complex calibration over load and frequency. Seven discarded samples must be justified experimentally for each configuration.

**Build status.** No MSDK/BLE/SD hardware build was reproduced here. Original and SDK dependency notices are retained. Useful for system organization and acquisition trade-offs, not a validated composition output.

### 3.8 AD5933 Arduino body-composition project — thesis distinguishes electrical testing from physiology

**Collected:** [code and thesis](https://github.com/dyarleniber/AD5933-arduino-bioimpedance).

**Architecture.** Arduino firmware, AD5933, external analogue front end, Bluetooth/mobile workflow, personal attributes and derived TBW/FFM/FM. Firmware scans 50–100 kHz and retains magnitudes at the endpoints for calculations. The 55-page Portuguese thesis describes the analogue circuitry and mobile application; a complete editable PCB/mobile-app source set was not established in this repository.

**What the thesis actually validates.** The reported validation table contains three resistor loads and one 2R1C network at two frequencies—**eight electrical comparisons**, not a DXA study of people. The precision resistor used for calibration is described as 1 kΩ with 1% tolerance. There is no demonstrated full uncertainty budget or independently replicated phase characterization in this review.

Recomputing the table's absolute percentage differences gives approximately **0.61–2.53%**, rather than turning the thesis's approximate “2% worst case” phrase into a universal specification. Reference-component tolerances and fixture effects also matter. These results concern the thesis's device/load conditions, not our future instrument.

**Equation implementation.** A fixed 0.73 relation converts TBW to FFM; FM is weight minus FFM. The firmware then applies absolute values to the estimates, which can hide impossible negative outputs rather than flagging invalid conditions. The AD5933 gain factors and magnitude handling require reconciliation with the actual analogue transfer function.

**Build status.** Source/thesis reviewed; no Arduino build or human testing. GPLv3 software retained. Useful as a transparent end-to-end educational example, with particularly important limits on what its published validation supports.

### 3.9 impedance.py — useful backend with bounded verification

**Collected:** [upstream](https://github.com/ECSHackWeek/impedance.py), pinned at `e175ad2b…`.

**Capabilities.** Preprocessing, multiple file readers, equivalent-circuit definitions, local/global fitting, validation methods, Bode/Nyquist and related plots. It is an EIS analysis library, not a body-composition model.

**Tests.** The initial full upstream test run reached the expensive fitting test and exceeded 180 seconds. A bounded run excluding that test passed **34 tests** after resolving the repository-name fixture path. A narrower follow-up ran only the expensive fitting test with BLAS/OMP threads limited to one. It timed out at 90 seconds, which was a time limit, not a failure. A rerun with a 1,500-second limit passed (1 test, 158.9 s; receipt `verification/impedance-py-test_circuit_fit-long-timeout.json`).

**Independent software check.** A noiseless synthetic `R0 + (R1 || C1)` spectrum at our six proposed frequencies—5, 10, 20, 50, 100 and 200 kHz—was generated with parameters 100 Ω, 500 Ω and 10 nF. The fitted parameters recovered those values within the check's tolerances; maximum complex residual was approximately **9.43 × 10⁻⁷ Ω**. This is numerical consistency on known synthetic data, **not measured instrument accuracy**, robustness to noise or proof of physiological identifiability.

**Integration considerations.** Maintain our own raw/calibrated schema, quality gating, units/sign conventions and uncertainty reporting around the library. A circuit fit can be non-unique; passing a fit or consistency test does not establish a unique tissue model. Sparse bandwidth limits what validation methods can conclude.

**Licence:** MIT. No licence-based exclusion or special preference was applied.

### 3.10 DearEIS and pyimpspec — installed, with selected tests executed

**Collected:** [DearEIS](https://github.com/vyrjana/DearEIS) and [pyimpspec](https://github.com/vyrjana/pyimpspec).

**Architecture.** DearEIS supplies a desktop workbench and batch interfaces; pyimpspec supplies much of the parsing, circuit, fitting, validation and simulation machinery. Features include project files, equivalent-circuit construction, Kramers–Kronig/Z-HIT methods and relaxation-time analysis. Treat them as a linked stack, not unrelated duplicate plotting tools.

**Build/runtime.** Both collected source revisions successfully built/installed in a separate Python 3.13 environment. DearEIS 5.1.3 and pyimpspec 5.2.0 were installed together; exact dependency versions are frozen in the receipts. A successful installation is not an interactive GUI test.

**Tests.** Selected pyimpspec circuit, connection, element and data modules passed **139 tests** using unittest. An earlier pytest run produced 138 passes and one stderr-message assertion failure, which disappeared under upstream-style unittest execution. DearEIS project/utility modules passed **43 tests**. The complete fitting, DRT, GUI and all-platform suites were not run.

**Risks/limits.** Runtime/dependency versions are materially newer than legacy OpenEIT's, so they should not share a guessed universal environment. Some analyses are computationally expensive or rely on data assumptions not met by a moving biological load or a six-point sweep. Versioned imports/project serialization need explicit adapter tests.

**Useful contribution:** a serious analysis workbench and backend we can inspect and evaluate without writing everything ourselves. GPLv3-or-later notices retained.

### 3.11 pyEIT — strongest complete upstream test result in the tomography branch

**Collected:** [standalone current toolkit](https://github.com/eitcom/pyEIT).

**Architecture.** Mesh generation, forward finite-element models, inverse/reconstruction methods, import/render utilities, EIT system/performance analysis and examples. Current source structures differ from the older bundled implementation in OpenEIT.

**Verification.** **62 upstream tests passed**, with warnings recorded. The full upstream archive was used for these tests so sample-data omissions in the compact collection were not mistaken for upstream defects.

**Data/model.** Reconstruction depends on electrode order, stimulation/measurement pattern, mesh geometry, boundary model and reference data. A successful synthetic reconstruction or unit test does not validate an electrode belt or recover DXA tissue compartments.

**Integration work.** Compare the exact ordering and sign of the Spectra measurements with the protocol supplied to pyEIT, then verify on a conductive phantom. Current pyEIT cannot simply be substituted into old OpenEIT wrappers based on a shared project name.

**Build/dependencies.** Python scientific stack, with additional geometry/image/performance packages. BSD-style licence text retained; this was not a selection criterion.

### 3.12 openScale and openScale-sync — personal tracking, not a raw-spectrum archive

**Collected:** [openScale](https://github.com/oliexdev/openScale) and [sync companion](https://github.com/oliexdev/openScale-sync).

**Architecture.** Android local-first measurement storage, Bluetooth device handlers, custom-scale integration, charts/exports, and a separate external-sync companion. Account-free local tracking and optional external transfers are separate concerns. Neither is an impedance AFE.

**Custom protocol finding.** The current custom handler uses an HM-10-style service/characteristic and newline-delimited records. The `$D$` payload contains index, date/time, weight, fat, water, muscle and an integer-XOR checksum. It is not a native multi-frequency R/X/configuration/calibration schema.

**Important behavior.** On a `$F$` completion message, the handler sends an EEPROM-clear command and disconnects. Any bridge for our instrument must understand this lifecycle; the consumer app should not be the sole research archive. Keep immutable acquisition records separately, rather than discarding raw samples after deriving four body metrics.

**Build requirements.** The inspected Android app specifies SDK 37, minimum SDK 31, Java 21 and Gradle 9.4.1. That is substantially different from older app setup guides. Android builds/instrumented tests were not performed because a corresponding SDK/device environment was not prepared.

**Compatibility limit.** No BodyScan 2 support or raw per-frequency export from a particular commercial scale was established. Supported protocols are model-specific. GPL notices retained; all candidates remain included regardless of licence.

### 3.13 BioScale / OKOK alternative — protocol/UI value, unsupported physiological shortcuts

**Collected:** [repository](https://github.com/eayrenk/bioscale-okok-alternative).

**Architecture.** Chipsea BLE parsing, Python application/storage/calculations, Flutter mobile code and tests. It offers an inspectable alternative to an opaque vendor app, not an independent measurement modality.

**Test result.** Four upstream tests passed; one failed because `get_classifications()` now expects `height_cm`, while the test calls it without that argument. This is an actual source/test mismatch in the collected revision; we did not patch it or generalize it to all application functionality.

**Scientific source findings.** Water percentage is derived from fat-free fraction using a fixed hydration relationship and clamping. The bone-mass helper contains an accuracy claim in its docstring, but no matching device-level DXA validation was established. The visceral-fat helper explicitly describes itself as empirical and says no published validated formula exists for that implementation. Metabolic-age output is another derived heuristic, not a direct biological-age sensor.

**Useful contribution.** BLE parsing examples, a visible calculation layer and app organization. Reuse of its display/protocol components can be studied independently from endorsement of the equations. Preserve raw impedance definitions and don't equate an arbitrary scale integer with calibrated resistance in ohms.

**Build status.** Python tests executed; Flutter app not built and BLE measurements not exercised. MIT notice retained.

### 3.14 BioZPulse simulation platform — pulse-wave/electrode sensitivity research

**Collected:** [repository](https://github.com/TAMU-ESP/BioZPulse-Sim-Platform).

**Architecture.** MATLAB functions generate a time-varying three-dimensional circuit grid, run LTspice, parse output, calculate sensed voltages/delays and visualize results. The README cites associated research and describes a MATLAB 2019b-era workflow.

**Dependency findings.** Example code includes a Windows LTspice executable path that must be changed. The runner can retry the external simulator until success; resource limits and bounded failure handling need attention before batch execution. MATLAB and LTspice have their own installation/licensing requirements even though the project code is public/GPL.

**Physical meaning.** The model is useful for exploring electrode sensitivity and pulse transit effects under its tissue/circuit assumptions. It does not establish a working sensor, a measured PWV/path length, cardiac output or cuffless blood-pressure accuracy.

**Verification.** Source inspected; no MATLAB/LTspice execution. Neither the needed simulation stack nor a validated substitute was prepared. The project is fully retained, not rejected for these dependencies.

### 3.15 ProtoCentral MAX30001 ecosystem — hardware, two firmware options, current viewer

**Collected:** [hardware repository](https://github.com/Protocentral/protocentral_max30001), [actual Arduino library](https://github.com/Protocentral/protocentral_max30001_arduino_library), [Zephyr driver](https://github.com/Protocentral/protocentral_max30001_zephyr_driver), and [OpenView](https://github.com/Protocentral/protocentral_openview).

**Important correction to older documentation.** The original hardware README claims a software directory and describes a Processing/Java viewer. The inspected hardware snapshot is essentially hardware/docs; the Arduino firmware is in a **separate repository**. Current OpenView is **Flutter-based**, not the old Processing application. Those companions were collected rather than treating stale README instructions as a dead end.

**Hardware.** Eagle board/schematic and schematic PDF are present. XML parsing found 71 schematic `part` objects, including supply symbols/frames—not 71 physical BOM components. This verifies file structure and inspectability, not routing correctness, safety, current production revision or a ready-to-order BOM.

**Arduino firmware.** Source and five examples cover ECG/BioZ streaming, R-R detection, lead-off, interrupts and configuration. It includes raw sample/timestamp/status structures and OpenView-compatible output. The library README specifies at least **8 KB SRAM** and **16 KB flash**, excluding classic 2 KB-SRAM Uno/Nano-class boards; it recommends newer boards. Its example table separately cites roughly **47 KB program / 5.5 KB RAM**, so the small headline flash minimum must not be treated as an example-build guarantee. Do not assume compatibility from old wiring tables. Arduino compilation was not performed.

**Zephyr firmware.** An out-of-tree driver with Kconfig/devicetree integration and documented older Zephyr targets. The README's example west manifest follows moving branches. For reproduction, pin Zephyr/modules/toolchains rather than interpreting those branches as a complete lockfile. No Zephyr build was performed.

**Current OpenView.** Source describes separated transport → framer → router → buffers → recording/replay layers, descriptor-based board support, USB/BLE/TCP transports gated by board capabilities, and `.hpd` recordings with a custom BIOSIG-v1-style structure. It is a relevant reference for a research acquisition viewer. MAX30001 is listed as USB-supported; broad app BLE support is not proof of MAX30001 BLE support.

**Limits.** ECG/impedance respiration is not broadband complex BIS, a six-lead ECG, a composition model or a full Withings sensor replacement. Flutter rendering, physical transports, firmware update functions and recording round trips were not exercised.

**Licence provenance:** hardware CERN-OHL-P v2, Arduino software MIT, documentation CC BY-SA 4.0; companion licences are retained separately. No licence-based exclusion.

## 4. Cross-project engineering conclusions

### 4.1 “Raw data” means different things in these projects

| Project/path | Data exposed or described | Transformation/metadata still required |
|---|---|---|
| OpenEBI UART | Averaged AD5933 real/imaginary registers | Frequency/path-aware complex calibration; raw-count vs ohm distinction |
| Spectra inspected spectroscopy | Frequency-labelled magnitude | Signed complex export if needed; quality flags and actual clock-derived frequency |
| Spectra EIT | Pattern-ordered magnitude vectors | Frame validation, electrode ordering, reconstruction reference and geometry |
| melazab sweep | Complex Z, magnitude, phase text; GUI CSV | Validate sign/calibration, actual frequencies, error state and throughput |
| ADI no-OS MAX30009 | FIFO/register/status access | Instrument-level calibration, persistent acquisition schema and export tooling |
| UPRM | Timestamp, scaled Q/I and frequency rows; BLE/SD path | Timebase/loss characterization, coefficient provenance, flags and settling validation |
| Arduino AD5933 BIA | Derived composition over Bluetooth | Preserve raw complex data instead of only demographic-model outputs |
| openScale custom handler | Consumer body-metric records | Separate raw spectrum/configuration/calibration archive |
| OpenView | Framed board-specific signals and recordings | Define and test a BioZ descriptor/payload; verify recording round trip |
| Analysis packages | Physical complex spectra in their expected formats | Unit/sign/ordering/import validation; not direct hardware compatibility |

A common adapter must not silently equate Q counts, reactance in ohms, magnitude, a vendor's impedance index and a body-fat percentage.

### 4.2 Calibration is not one interchangeable operation

Different projects use register/reference scaling, RTIA calibration, zero-baseline subtraction, resistor-derived gain factors, reference-frame normalization or fitted equations. These solve different problems. In particular:

- A short/zero check does not establish gain and phase accuracy across frequency/load.
- On-board reference calibration does not automatically characterize leads, switching paths or electrode contacts.
- A reconstruction reference frame does not establish absolute conductivity accuracy.
- A physiological equation cannot repair uncharacterized electrical errors.
- Calibration and verification should use appropriately independent references.

### 4.3 Sampling claims need a unit and a measurement point

ADC sample rate, DFT update rate, configured trigger rate, accepted sample rate after settling, UART/BLE throughput and complete EIT frames per second are different quantities. Spectra's ADC rate must not be reported as its imaging frame rate. UPRM's discarded samples and alternating frequencies reduce accepted per-frequency output. No achieved rate was independently measured here.

### 4.4 The collection covers different sensor modalities, not a unified validated device

The strongest direct coverage is impedance acquisition/analysis and EIT. ECG and impedance respiration are represented separately; EDA examples and pulse-wave simulation are present. The collection does not establish a unified validated system for body composition, clinical bone density, PWV, blood pressure, oxygen saturation, nerve diagnosis or glucose-related interpretation. Those claims need their own sensors/protocols/reference studies.

### 4.5 Software reproducibility is a separate achievement from measurement validity

The successful builds/tests materially improve our understanding of the projects' usability. They do not transfer clinical validation from one repository, population or instrument to another. Likewise, a legacy dependency or failing unit test does not make an otherwise useful architecture unworthy of research.

## 5. Open questions retained for each family

| Family | Highest-value remaining investigation |
|---|---|
| OpenEIT/Spectra | Matched newer hardware manufacturing set; actual complex export; bounded sequence failures; validated current/voltage behavior; clean dashboard environment |
| OpenEBI | Legacy CAD import/DRC; exact front-end calibration; UART timeout/parameter hardening; AVR build |
| ADI AD5940 | Keep exact library/API alignment; characterize selected configuration on passive references |
| melazab AD5940 | Runtime/linker/heap/stack review; calibration/sign/throughput tests; original-code licence clarification documented separately |
| ADI no-OS MAX30009 | Complete target-specific dependency lock/build; instrument calibration/export/status contract |
| ADI MAX example | Reconcile setup text and assumptions; distinguish EDA settings from BIS requirements |
| UPRM | Verify scaling, timebase, settling, notification loss, SD failure paths and bounds-check ordering |
| Arduino AD5933 | Equation applicability and invalid-result handling; reproduce electrical table with independent references |
| impedance.py | Benchmark the global-fitting test (now passing, 158.9 s); noisy-data conditioning and sparse-spectrum limitations |
| DearEIS/pyimpspec | Broader fitting/DRT tests and interactive GUI; versioned import/adapter integration |
| pyEIT | Verified Spectra protocol mapping and phantom reconstruction; no assumed API interchangeability |
| openScale/sync | Android builds and bridge behavior; preserve independent raw research archive |
| BioScale | Test/API mismatch; distinguish protocol correctness from unsupported physiological shortcuts |
| BioZPulse | Reproducible simulation environment and bounded external-process execution; validate model assumptions |
| MAX30001/OpenView | Arduino/Zephyr/Flutter build matrix; sample units, framing and recording round-trip checks |

These are open research tasks, not licence-based rejections. No purchase or implementation platform was selected.

## 6. How to use the collection

The archive contains:

- `sources/<snapshot>/`: collected source, design and notice files.
- `manifests/`: original commit/URL metadata, hashes for every included file, and every omitted upstream file observed during collection.
- `collection-index.json` and `project-catalog.csv`: machine-readable inventory.
- `research/`: hardware inventory and technical findings.
- `verification/`: commands, raw output, environment freezes, successes, failures and timeouts.
- `tools/verify_collection.py`: offline hash verification.
- `tools/fetch_upstream.py`: optional retrieval of a selected complete upstream archive by pinned URL/hash; no checkout execution or flashing.
- This dossier and a README.

After extracting, run `python tools/verify_collection.py`. Verification confirms file integrity against our manifest, **not authorship, safety, licensing completeness or measurement accuracy**. Large omitted files remain obtainable from the recorded original upstream URLs. SDK/toolchain/package dependencies are not all vendored.

### Bottom line

We now have a **versioned research collection of every candidate from the survey, including OpenEIT/Spectra**, with meaningful source investigation and several real build/test results. The projects are complementary: hardware acquisition, firmware, local data handling, numerical analysis, tomography and physiological simulation are all represented. We have not prematurely selected one or mistaken public source for a validated human instrument.

## Deep-dive addendum (17 October 2026, pass 1)

*Superseded in part by passes 3 and 4 below: F02 (FIFO count) is resolved, F12 is resolved from the ADuCM350 manual, and the OpenView producer is in the Arduino library.*

Full detail: `deep-impedance-audit/DEEP-FINDINGS.md`. Evidence levels: source reading, host probes with simulated peripherals, Dart probe, and unverified items.

- **UPRM FIFO parser (host probe):** upstream `spiBurst` writes out of bounds for FIFO counts 0–1 and reads out of bounds for a truncated trailing word. Reachability on hardware is unverified.
- **UPRM scaling (host probe):** 45.25 µA excitation, 0.00662 Ω/count, 4104 Hz and 131 328 Hz excitation, and a seconds-to-µs truncation bug in an unused timing variable.
- **OpenEBI (host probe):** average=0 yields NaN; valid-data wait has no timeout.
- **Spectra fixed-point (host probe):** an open/zero denominator reports magnitude 0; values ≥2³¹ raw wrap negative. The bipolar amplitude macro (61 320 codes from VPEAK×40) conflicts with the unused 12.73 mV constant and needs review before any hardware work. No hazard claim is made.
- **MAX30001 (source):** Arduino BioZ is 20-bit; OpenView documents 19-bit. OpenView packet-type-2 producer firmware is not in the collection, so its units are unverified.
- **OpenView framer (Dart probe):** frames with and without the `0x00` pad both decode.
- **OpenView .hpd reader (source):** CRC-32 is written but not checked, and read errors end the file silently.

Unchanged: no device was connected, flashed or used on a person, and no purchase or maintainer contact was made.

## Pass 2 deep audit (17 October 2026, continued)

*Superseded in part by passes 3 and 4 below.*

The full evidence table is in `deep-impedance-audit/findings.json` (19 findings, 4 open items). Report: `deep-impedance-audit/DEEP-FINDINGS.md`. Each claim is tagged by evidence level: S (source), H (host probe), D (Dart probe), DS (datasheet), T (test run), U (unverified).

**Changes to earlier statements**
- **impedance.py global-fit test:** the isolated run passed (1 test, 158.9 s with BLAS/OMP caps). The earlier 90 s result was a time limit, not a failure.
- **MAX30009 datasheet:** now retrieved (chunks 0, 4, 5, 8, 9 of 10). It confirms the BioZ sample-rate and stimulus-frequency formulas used by the UPRM firmware, a 20-bit ADC, a 256-word FIFO, and a vendor-stated 60601-1 lockout on high-current, low-frequency drive. The register map (FIFO-count layout) was not retrieved.

**New findings (highest priority first)**
- **OpenEIT bipolar amplitude (F12, review before any hardware use):** the macro gives 61,323 DAC codes, but the 11-bit amplitude field keeps 1,931 codes (about 754 mV equivalent) instead of the roughly 23.96 V the macro implies. The defined 12.73 mV constant is unused in that path. Whether bits above bit 10 are ignored by the register write is unverified. No hazard claim is made.
- **UPRM FIFO parser (F01, F02):** out-of-bounds access for FIFO counts of 0 or 1 and for a truncated trailing word (confirmed with AddressSanitizer in host probes). The FIFO-count formula conflicts with the ADI no-OS driver; the register map is needed to resolve it.
- **OpenView `.hpd` recordings (F17):** the CRC-32 written per block is never checked, and read errors end the file silently. In a Dart probe, one corrupted byte changed a sample with no error, and a 200-byte truncation silently dropped 4 of 30 samples.
- **Spectra open-circuit ambiguity (F10, F11):** a zero denominator reports magnitude 0, which can be mistaken for a 0 Ω reading; values in [2³¹, 2³²) wrap negative.
- **OpenEBI (F08, F09):** average=0 yields NaN; the valid-data wait has no timeout.
- **UPRM units (F03–F07):** 45.25 µA is a peak value (the datasheet's equivalent is 32 µA RMS). Sample-rate and frequency formulas match the datasheet. Some comments are stale.
- **OpenView packet type 2 (F14, F15):** the BioZ bit-width is documented as 19 bits, while the Arduino library in the same family extracts 20 bits. The producer firmware is not in the collection, so RR units are unverified.
- **OpenView framer (F16):** frames with and without the 0x00 pad both decode.

**Still open:** FIFO-count register layout (F02); amplitude-register write behaviour and the intended bipolar drive (F12); OpenView packet-type-2 producer firmware (F15); hardware reachability of F01, F08 and F09. None of these was tested on hardware, and no device was connected or flashed.

**Not changed:** no device was purchased, connected, flashed or used on a person, and no maintainer was contacted.

## Pass 3 deep audit (17 October 2026)

Full detail: `deep-impedance-audit/DEEP-FINDINGS.md` and `findings.json` (23 findings, 4 open items). Each claim keeps its evidence level.

**Corrections to earlier statements**
- **FIFO-count formula (F02) is resolved against vendor sources.** The MAX30009 count is bit 7 of register 0x0A times 256, plus register 0x0B (ADI MAX32655_MAX30009 header and driver, and no-OS). UPRM's `(c1&0x7F)*2+c2` does not match. The earlier "register map needed" statement is superseded.
- **OpenView packet-type-2 producer is in the collection (F15).** It is `Example01_BasicECGBioZ.ino` in the Arduino MAX30001 library. The earlier statement that the producer was absent was wrong.

**New findings**
- **OpenView heart rate and RR are wrong for the Arduino producer (F20, Dart probe).** The real `packet_framer_v3.dart` and `max30001_decoders.dart`, run on six producer-format frames, report heartRate `0, 255, 0, 255, 0, 255` and rr `0`. The producer sends no HR or RR; byte 8 is a BioZ skip flag, which the decoder reads as HR. This is a mismatch between producer and decoder, not a validated HR measurement.
- **BioZ rate label (F21).** OpenView labels BioZ 128 samples/s, but the producer changes BioZ about every other frame, so the effective change rate is about half that.
- **UPRM FIFO burst size (F22, inference).** UPRM reads `fifoCount` bytes and parses 3-byte samples from them. If the count is in samples, as the vendor driver implies, each burst is one third of the data it should be. Needs a hardware test.

**Verification in this pass:** the native probes reproduce from the archived sources (20 provenance hashes identical; only ASan process IDs and stack addresses differ). The long `test_circuit_fit` run passed (1 test, 158.86 s).

**Still open:** the bipolar amplitude register behaviour (F12; ADuCM350 register table not retrieved); the MAX30009 ADC OSR table (F05); hardware FIFO semantics (F22); the intended HR/RR contract (F20, a maintainer question, not contacted).

**Not changed:** no device was purchased, connected, flashed or used on a person, and no maintainer was contacted.


## Pass 4: outstanding items worked (17 October 2026)

Full receipts: `deep-impedance-audit/pass4/PASS4-RECEIPT.json`. Findings: `deep-impedance-audit/findings.json` (29 findings, 5 open items).

- **F12 is now resolved from the chip manual.** On the ADuCM350, the amplitude register's bits above bit 10 are read-only reserved. The 61,323-code bipolar macro is therefore most likely masked to 1,931 codes, about 754 mV equivalent. Still not measured on hardware.
- **F05 is still open.** The MAX30009 OSR bit table was not decoded from the fetched chunks.
- **melazab/AD5940-BIOZ licence (F26).** No root licence; the GitHub licence API returns 404. The vendored ADI library licence limits use to ADI products and forbids combining with differently licensed code. Recorded as a difference; not excluded.
- **AVR compile-only (F25).** `protocentral_max30001.cpp` compiles for ATmega328P (0 errors, 13 warnings). The AD5933 sketch compiles (0 errors, 0 warnings). Stub headers, not the Arduino core; nothing ran on a microcontroller.
- **OpenView (F28, F24).** 42 Flutter tests in 5 files pass, and the Linux debug build succeeds. The collected snapshot has no `pubspec.lock` and omits fonts and branding assets, so the tests ran on a working copy with the asset declarations removed and dependencies freshly resolved.

Not run: Zephyr (multi-GB SDK on a 2 GB machine), Android (no SDK), MATLAB (no licence), AVR runtime and any hardware work (not authorised).
