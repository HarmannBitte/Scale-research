# Open-source projects relevant to our DIY impedance platform

**Research date: 18 October 2026**  
**Scope:** reusable measurement hardware/firmware, impedance analysis, local scale-data collection, and adjacent physiological research. This is a repository/documentation and selected-source review, not a build, electrical test, security audit, legal opinion, or human-safety assessment.

## Executive decision

**There is substantial work to reuse, but I did not establish a complete, openly reusable, independently validated Withings BodyScan 2 replacement.** The useful projects solve different layers of the problem:

1. **OpenEBI:** the closest published open-hardware precedent for four-electrode impedance spectroscopy.
2. **ADI no-OS MAX30009 + UPRM research firmware:** the most relevant MAX30009 acquisition references.
3. **melazab/AD5940-BIOZ:** unusually close overlap with our existing GNU/ADICUP3029 firmware work, but an unresolved licence for original project code prevents treating it as a drop-in dependency.
4. **impedance.py and DearEIS:** existing analysis tools to evaluate before writing a fitting/plotting application from scratch.
5. **openScale:** a strong local-first personal-tracking and Bluetooth integration reference—not an impedance instrument.
6. **OpenEIT/Spectra:** technically relevant, but non-commercial licensing and hardware-file completeness require particular caution.

**Recommended direction:** keep our acquisition/qualification core, investigate a small number of upstream components, and avoid building a monolithic “open Withings clone.” Open data and reproducibility are achievable goals before physiological superiority is established.

## 1. What was actually checked

- Downloaded public metadata and recursive file inventories for **16 repositories**.
- Read their root README/licence materials where available.
- Examined selected firmware, GUI, calculation and test sources for the closest candidates.
- Separately retrieved the MAX30009 driver, example and documentation directly from ADI no-OS.
- Recorded default-branch commit IDs for four priority repositories, and SHA-256 hashes for the saved evidence files.
- Used the previously reviewed AD5940 manufacturer examples as an additional reference; did not rebuild our completed ARM package.

Evidence is under `open-source-survey/`. Metadata `pushed_at` is repository-wide activity, **not necessarily a default-branch code change**. For example, UPRM has September repository activity but the inspected default-branch tip is dated July 4. API licence classifications such as `NOASSERTION` are not a legal conclusion: actual texts were read where practical.

**Not done:** hardware purchases, board construction, third-party firmware execution/builds, human measurements, maintainer contact, comprehensive licence provenance, or clinical validation. No claims of reproducibility or safety follow merely from finding public source.

## 2. Closest hardware and firmware projects

### A. OpenEBI — the most directly relevant open-hardware precedent

**Sources:** [hardware repository](https://github.com/openebi/hardware), [software repository](https://github.com/openebi/software), [2012 paper](https://ieeexplore.ieee.org/document/6376851/).

**What exists:** an AD5933-based four-electrode electrical-bioimpedance spectrometer. Its documentation describes magnitude and phase acquisition from a few kilohertz to 100 kHz. The hardware repository includes editable Eagle schematic/layout files and supporting exports/BOM material; the software is separate. [5](https://github.com/openebi/hardware) [8](https://github.com/openebi/software)

**Licence:** hardware is declared **CC BY-SA 3.0**; firmware/software is declared **MIT**. Retain attribution and applicable share-alike obligations; confirm component/library and export provenance before redistribution.

**Evidence:** there is a published measurement paper, rather than just a project description. Its abstract reports experiments on an RC network and individual components, with materially different errors for different loads. That is a reason to study the test conditions, not adopt one universal accuracy number. [1](https://ieeexplore.ieee.org/document/6376851/)

**Maturity:** inspected hardware tip is from July 2016; software repository activity is from 2013. Expect legacy CAD/toolchain and component-availability work.

**Use for us:** learn from four-electrode topology, front-end design, separation of current and voltage paths, and their validation approach.

**Do not assume:** its AD5933 calibration, frequency envelope or physiological equations transfer to AD5940/MAX30009. Its authors explicitly require medical-electronics training and good engineering practice. Publication is not certification.

**Verdict: high-priority architectural reference; not an automatic platform switch.**

### B. Analog Devices no-OS MAX30009 — a stronger upstream starting point than a random driver

**Inspected source:** [MAX30009 driver](https://github.com/analogdevicesinc/no-OS/blob/bdd9427af10c767f6bf3aa9a61100317d1192b44/drivers/afe/max30009/max30009.c), [example README](https://github.com/analogdevicesinc/no-OS/blob/bdd9427af10c767f6bf3aa9a61100317d1192b44/projects/max30009/README.rst), [basic example](https://github.com/analogdevicesinc/no-OS/blob/bdd9427af10c767f6bf3aa9a61100317d1192b44/projects/max30009/src/examples/basic/basic_example.c).

**What exists:** a structured no-OS driver with SPI/I²C register-access implementations and a basic project. The README describes a 50 kHz, 100-sample/s configuration, I/Q FIFO acquisition, tetrapolar MUX configuration, lead-off and lock/status monitoring. These are documented example settings—not throughput, electrical-accuracy or human-safety results independently verified here.

**Licence:** inspected driver and basic-example headers use **BSD-3-Clause**. Other framework/platform dependencies still need a normal file-level licence inventory.

**Maturity:** inspected repository tip `bdd9427…`, dated October 14, 2026. This date is for the repository tip, not proof of the MAX30009 driver's release history or qualification.

**Use for us:** compare driver architecture, status handling, decoding, configuration and error propagation before writing another MAX30009 driver.

**Important limitation:** the generated documentation URL found in search returned **404**. The actual source, project README and documentation source were retrievable, so use those instead. Do not use the README's application list as evidence that body composition, hydration or cardiac outputs have been validated.

**Verdict: first upstream codebase to assess if we choose MAX30009. No build was attempted.**

### C. UPRM Multi-Frequency BioZ Research — close to the system we want to assemble

**Source:** [repository](https://github.com/oscaroflores/UPRM-Multi_Frq-BioZ-Research).

**What exists:** MAX30009 acquisition using MAX32655, with Python GUI/logging code and BLE-related development. The repository is derived from ADI's MAX32655/MAX30009 example. Its README describes multi-frequency recording, Bluetooth, SD logging and a user interface as project goals; not every goal should be counted as finished. [1](https://github.com/oscaroflores/UPRM-Multi_Frq-BioZ-Research)

**Useful source-level finding:** the inspected `src/bioZ.c` documents two supported frequency selections, approximately **4 kHz and 131 kHz**; `main.c` alternates selections and discards seven samples between acquisitions. This is a concrete example of frequency switching and settling management—not a general-purpose validated broadband sweep. The discard count must not be copied as a universal settling criterion.

**Licence:** root text gives broad permission to use, modify and distribute with notices, plus Maxim-specific clauses. Call it a **custom permissive vendor notice**, not simply MIT; confirm coverage of later contributions and SDK/BLE dependencies.

**Maturity:** default-branch tip `b3a8844…`, July 4, 2026. This is substantially more than a conceptual block diagram, but I did not reproduce its build, conversion to ohms, BLE integrity, or measurement performance.

**Use for us:** investigate multi-frequency scheduling, GUI organization, packet/logging structure and movement-data integration.

**Verdict: high-priority comparative source review alongside the vendor no-OS code.**

### D. melazab/AD5940-BIOZ — the closest overlap with our completed GNU firmware work

**Source:** [repository](https://github.com/melazab/AD5940-BIOZ).

**What exists:** bare-metal GNU firmware for ADICUP3029/ADuCM3029 plus an AD5940-BIOZ shield; separate two-wire and four-wire sweep/time-series programs; startup/linker code; a Tkinter GUI with live plots and CSV recording. Its sweep defaults are 40 points from 1–200 kHz; the four-wire time-series mode is documented at a nominal 5 Hz. These are configurations, not verified performance specifications. [2](https://github.com/melazab/AD5940-BIOZ)

**Maturity:** inspected tip `dcd5096…`, September 21, 2026. A GUI flash-target test file exists, but this is not evidence of comprehensive acquisition testing or a successful build in our environment.

**Licence blocker:** no project-wide licence was located in the inspected root/tree or original main/GUI material. Vendored `ad5940lib` has its own licence, but that **does not automatically license the author's GUI, startup or application code**. Public visibility is not permission to copy/redistribute original code.

**Use for us:** compare interfaces and documented design choices; seek explicit permission/licence before incorporating original code. This research did not contact the maintainer.

**Why not replace our code immediately?** We already have a pinned, tested, genuinely GNU-built package with explicit limits. This candidate may save GUI/interface work after licence clarification; it does not erase our work or constitute a demonstrated upgrade.

**Verdict: very relevant comparison; reuse blocked pending licence clarification.**

### E. Analog Devices AD5940 examples — already part of our foundation

**Source:** [manufacturer repository](https://github.com/analogdevicesinc/ad5940-examples).

Includes BIA, two-wire bioimpedance, EDA and other examples. We have already built on this ecosystem and preserved pinned dependencies/provenance. It remains the baseline for comparisons—not a newly discovered finished body-composition product. [2](https://github.com/analogdevicesinc/ad5940-examples)

Keep manufacturer/library licence notices and dependencies distinct. The evaluation-board restriction remains decisive: **never connect the AD5940 evaluation board to the human body**, irrespective of what a third-party project demonstrates or suggests. [1](https://www.analog.com/en/resources/app-notes/an-1557.html)

### F. ADI MAX32655/MAX30009 example — useful ancestry, narrower application

**Source:** [repository](https://github.com/analogdevicesinc/MAX32655_MAX30009).

The README targets **GSR/EDA**, with I-phase, Q-phase and derived BioZ output. It is not itself a body-composition platform. Its root notice is the custom permissive vendor text also found in the UPRM project. Repository activity inspected here is from 2023. [2](https://github.com/analogdevicesinc/MAX32655_MAX30009)

The README's jumper instructions are internally inconsistent about one jumper's state. That alone is a reason not to treat them as an executable setup procedure without reconciliation. We will not reproduce its human-connection instructions.

**Verdict: useful for provenance and low-level comparison; not the primary finished solution.**

### G. AD5933 Arduino bioimpedance — explicit composition estimates, but not validated truth

**Source:** [repository](https://github.com/dyarleniber/AD5933-arduino-bioimpedance).

Arduino firmware acquires impedance magnitude at 50/100 kHz, accepts personal attributes over Bluetooth, and calculates total body water, fat-free mass and fat mass. A Portuguese-language undergraduate thesis is linked. Software licence: **GPLv3**; repository activity inspected here is from 2020. [1](https://github.com/dyarleniber/AD5933-arduino-bioimpedance)

**Source-level caution:** the calculation uses a fixed 0.73 relationship to derive FFM from TBW, then takes absolute values of FM, FFM and TBW. Taking an absolute value can conceal an impossible negative estimate instead of rejecting it. For our system, invalid inputs/results should remain explicit errors or flagged estimates.

**Use for us:** an educational example of the acquisition → demographics → equation → app workflow.

**Verdict: educational reference, not our physiological model or calibration standard.**

## 3. Existing analysis software we should evaluate before writing our own

### H. impedance.py — strongest initial candidate for a scripted analysis backend

**Source:** [upstream repository](https://github.com/ECSHackWeek/impedance.py).

Python package for preprocessing, validation, equivalent-circuit fitting and visualization of electrochemical impedance data; includes documentation, examples and tests. Licence: **MIT**. Inspected tip `e175ad2…`, October 11, 2026. [Repository](https://github.com/ECSHackWeek/impedance.py)

**Use for us:** compare against our passive-phantom calculations, fit known circuits, inspect residuals, and generate reproducible plots. Preserve our own raw-data schema and quality gating around it.

**Limits:** it is not a physiological body-composition model. A successful circuit fit does not establish a unique physical interpretation. Kramers–Kronig-style checks depend on assumptions and adequate data; our proposed sparse frequency set may be insufficient for strong conclusions.

**Verdict: first software dependency to test, using pinned versions and synthetic/passive fixtures.**

### I. DearEIS — an existing desktop workbench

**Source:** [repository](https://github.com/vyrjana/DearEIS).

GUI and batch API for spectrum import, visualization, equivalent-circuit construction/fitting, simulations, Kramers–Kronig/Z-HIT checks and relaxation-time analysis. Some core functionality is in `pyimpspec`. Licence: **GPLv3-or-later**; inspected repository activity is April 2026. [13](https://github.com/vyrjana/DearEIS)

**Use for us:** evaluate it as an external analysis workbench before building a custom desktop GUI. Our export format could be adapted to its supported imports.

**Limits:** same scientific interpretation cautions as impedance.py. Using a GPL program separately and distributing a combined derivative are different licence situations; plan integration deliberately. No GUI was installed or exercised here.

**Verdict: promising ready-made workbench; custom UI should solve only demonstrable gaps.**

### J. pyEIT — reserve for a later tomography branch

**Source:** [repository](https://github.com/eitcom/pyEIT).

Python toolkit with forward/inverse EIT methods, meshing and examples/tests. The current inspected licence text is **BSD-3-Clause-style**, with exceptions for example code; older descriptions referring to Apache should not override the current files. Repository activity inspected here is December 2025. [Repository](https://github.com/eitcom/pyEIT)

**Use for us:** simulations and reconstruction if we deliberately develop a multi-electrode tomography experiment.

**Limits:** tomography is a different and more difficult inverse problem than recording four-electrode impedance. It is not required for our first instrument and is not an impedance-based DXA replacement.

**Verdict: useful later, not a dependency for the baseline.**

## 4. Local-first scale/app projects

### K. openScale — strongest application-layer reference

**Source:** [repository](https://github.com/oliexdev/openScale).

Android weight/body-metrics application with Bluetooth-scale integrations, local data handling, CSV import/export, manual entry, multiple users and configurable metrics. It does not require a user account for its core local workflow. The repository includes a custom-scale integration path and an older Arduino MCU directory. Licence: **GPLv3**. Activity was visible on October 17, 2026. [11](https://github.com/oliexdev/openscale)

**Use for us:** consider a custom integration or export bridge instead of writing an entire personal-tracking app. Its current custom-scale handler would need review before promising compatibility.

**Critical limits:** supported-device lists must be checked per model. This review did **not** establish BodyScan 2 support, raw multi-frequency R/X access from any given scale, or scientific validity of every displayed metric. An app that displays “bone mass” is not measuring bone density.

**Verdict: high-priority local-first data/app reference, not measurement hardware.**

### L. BioScale / OKOK alternative — interesting, but do not adopt its accuracy claims

**Source:** [repository](https://github.com/eayrenk/bioscale-okok-alternative).

Advertises an offline Chipsea-scale workflow, Python desktop/web and Flutter mobile code, local storage and CSV export. Licence: **MIT**; inspected repository activity is October 2026. [22](https://github.com/eayrenk/bioscale-okok-alternative)

The repository has calculation code and unit tests. The selected tests check arithmetic, presence of outputs and basic result behavior—not device-level agreement against DXA or MRI. The code references published equations and derives multiple outputs from shared inputs.

**Use for us:** app/UI ideas, BLE organization and explicit equation inspection.

**Limits:** “validated scientific formulas” is not proof that a formula is appropriate to this scale's impedance definition, electrode geometry, population or acquisition conditions. More output metrics do not imply more independent measured quantities.

**Verdict: watch/reference; no physiological endorsement.**

## 5. Adjacent physiological directions

### M. BioZPulse simulation platform — useful for the pulse-wave branch

**Source:** [repository](https://github.com/TAMU-ESP/BioZPulse-Sim-Platform).

Models tissue, arterial pulse waves and electrode configurations using a time-varying 3D circuit grid simulated in SPICE. Licence: **GPLv3**. The documented workflow uses MATLAB and LTspice, which have separate licensing/runtime requirements; open project code does not make the entire toolchain open source. Inspected repository activity is from 2020. [16](https://github.com/TAMU-ESP/BioZPulse-Sim-Platform)

**Use for us:** study sensitivity to electrode placement before a future pulsatile-impedance experiment.

**Limits:** not body composition, not a validated blood-pressure/PWV instrument, and not proof that a proposed sensor captures the modeled signal.

**Verdict: a later simulation reference, not an immediate dependency.**

### N. ProtoCentral MAX30001 — ECG/respiration, not a replacement BIS platform

**Source:** [repository](https://github.com/Protocentral/protocentral_max30001).

Publishes Eagle hardware files, Arduino software and a linked visualization tool for single-lead ECG and impedance-respiration acquisition. Declared licences: hardware **CERN-OHL-P v2**, software **MIT**, documentation **CC BY-SA 4.0**. Inspected repository activity is from 2022; current product advertising does not by itself establish current firmware maintenance. [11](https://github.com/Protocentral/protocentral_max30001)

**Use for us:** a separate ECG/respiration module reference if that scope becomes a priority.

**Limits:** single-lead ECG/respiration is not multi-frequency body-composition spectroscopy or a six-lead ECG. Marketing “clinical-grade” language is not certification of an assembled DIY instrument. Disconnecting a laptop charger is not a complete electrical-safety case.

**Verdict: adjacent module only; require the same professional safety review.**

## 6. OpenEIT/Spectra: useful engineering, important openness caveats

**Sources:** [firmware](https://github.com/OpenEIT/EIT_Firmware), [electronics](https://github.com/OpenEIT/EIT_EE), [dashboard](https://github.com/OpenEIT/OpenEIT).

The project describes ADuCM350-based impedance acquisition, spectroscopy/time-series modes, electrode multiplexing and EIT reconstructions. That makes it technically relevant to a future multi-electrode platform. [1](https://github.com/OpenEIT/EIT_Firmware) [2](https://github.com/OpenEIT/OpenEIT)

However:

1. **The inspected repositories use CC BY-NC-SA 4.0.** The non-commercial condition means they are not unrestricted open-source building blocks. GPL copyleft and non-commercial restrictions are not the same: GPL permits commercial use subject to its obligations.
2. **Hardware completeness varies by revision.** The electronics README distinguishes older editable eight-electrode Eagle materials from a newer 32-electrode schematic PDF. A PDF is not a complete editable manufacturing package for that newer revision. [5](https://github.com/OpenEIT/EIT_EE)
3. **Toolchain/history matters.** Firmware documentation references IAR and a GCC branch; no build or cross-branch compatibility was established here. Hardware/firmware activity inspected is from 2021, while dashboard repository activity is later.
4. **It does not become CT or DXA because it reconstructs an image.** Conductivity reconstruction has different resolution, physics and limitations. We do not adopt promotional claims of safety or image equivalence.

**Verdict: useful technical reading; not the default foundation for a broadly reusable/commercial-capable platform.**

## 7. Coverage of the wider Withings-like feature set

| Measurement/output | Relevant projects found | What remains missing for our project |
|---|---|---|
| Weight and personal tracking | openScale; BioScale; custom-scale paths | A qualified physical scale, verified protocol and integration |
| Complex impedance/spectroscopy | OpenEBI; ADI examples; no-OS MAX30009; UPRM; melazab | Our own electrical qualification, configuration/export contract and uncertainty budget |
| Segmental/multi-path acquisition | OpenEBI four-electrode precedent; EIT multiplexing references | A reviewed segmental design, path/contact control and segment-specific validation |
| Fat/lean/water estimates | Arduino BIA; scale-app equations | Device/population-specific validation; valid handling of uncertainty and changes |
| Bone density | No suitable impedance project established | An impedance estimate cannot substitute for clinical BMD measurement |
| ECG | ProtoCentral; AD5940 ecosystem | Correct lead architecture, safety, signal quality and claim-specific validation |
| EDA/skin conductance | ADI MAX30009/AD5940 examples | Electrode/protocol validation and justified interpretation; not proof of generalized nerve health |
| Respiration/pulsatile impedance | MAX30001; BioZPulse simulation | Fit-for-purpose acquisition and physiological validation |
| PWV/blood pressure | Pulse-wave simulation is adjacent only | Valid sensor timing/path definitions and independent reference validation |
| SpO₂ and glucose-related scores | Not established by the shortlisted impedance projects | Separate sensing/validation; impedance-only scores are not direct oxygen or glucose measurements |

This is a bounded survey, not proof that no other project exists. I did not verify a comprehensive unrestricted clone of the full Withings sensor/feature set, nor a complete published human-safety dossier for these candidates.

## 8. What this changes in our DIY plan

### Reuse or evaluate first

- **Analysis backend:** test impedance.py on known synthetic/passive circuits before writing another fitter.
- **External workbench:** assess DearEIS imports and report usefulness before building a rich analysis UI.
- **MAX30009 acquisition:** compare the current no-OS driver and UPRM source against our acquisition requirements.
- **Hardware architecture:** use OpenEBI as a design-review reference, not a ready human-connected assembly instruction.
- **Personal tracking:** evaluate an openScale bridge only after deciding what data should reach the app.

### Keep our distinctive work

- Conservative passive-bench scope and explicit never-human-connected evaluation-board boundary.
- Pinned builds, manifests and automated failure-path tests already delivered.
- Preservation of signed complex data, actual frequency, raw counts, calibration IDs and configuration.
- Quality gating that rejects missing/invalid state instead of manufacturing plausible physiology.
- A transparent uncertainty and qualification report.

### Do not copy blindly

- Body-composition equations tied to another geometry/instrument/population.
- Zero-offset subtraction as a substitute for full gain/phase calibration.
- Fixed settling counts without an experiment establishing adequacy.
- Sampling-rate settings as proof of achieved throughput or loss-free logging.
- “Safe,” “clinical-grade,” “validated formulas,” or high metric counts as demonstrated safety/accuracy.
- Code without clear reuse rights, or non-commercial code into a broadly reusable product.

## 9. Recommended next decision

**Do not change hardware or discard our current firmware based on this survey alone.** The most useful next deliverable is a small, evidence-led reuse assessment:

1. Pin and compare **ADI no-OS MAX30009 vs UPRM** for raw-data access, frequency configuration, calibration, quality/status reporting, SDK requirements and licence coverage.
2. Evaluate **impedance.py vs DearEIS** on the same labelled synthetic/passive reference datasets, including whether our sparse sweep is sufficient for each proposed analysis.
3. Compare **OpenEBI's front-end and test methodology** against our electrical requirements.
4. Treat **melazab's GUI as a permission/licensing question first**, not an integration task.

The resulting choice could be “reuse an analysis library, keep our acquisition core, and write only adapters and qualification tooling.” That would preserve the project's strongest purpose: **an inspectable measurement system with evidence behind each claim**, rather than a large number of opaque health scores.

---

### Saved evidence and limitations

- `open-source-survey/inventory.json`: repository metadata summary and interesting paths.
- `open-source-survey/project-comparison.csv`: curated decision matrix.
- `open-source-survey/selected-heads.json`: four inspected default-branch commit observations.
- Per-repository directories: metadata, file trees, README/licence snapshots, selected source files.
- `open-source-survey/manifest.json`: content hashes; does not authenticate authorship or establish licence correctness.

Snapshots were retrieved from public endpoints during the review. They are a research record, **not a complete vendor distribution, endorsed release, or licence-cleared source bundle**. No third-party builds/tests were executed during this survey. Existing DIY deliverables were not modified.
