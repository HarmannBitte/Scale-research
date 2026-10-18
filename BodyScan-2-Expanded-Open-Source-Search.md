> **October 17 follow-up:** See [pass 4: compatibility and subscription audit](BodyScan-2-Pass-4-Compatibility-and-Subscription-Audit.md). Withings now says automatic third-party sync requires Withings+ for accounts created from October 13, 2026; older accounts retain free sync and manual CSV/PDF exports remain free. Source inspection also identifies BMI-only fallbacks in several scale adapters. Do not infer measured composition from a generic support-table entry.

# BodyScan 2 alternatives: expanded open-source search

**Research date: October 17, 2026.** Includes usable software, experimental hardware, analysis libraries, and WHOOP MG-specific routes. This is a documentation/repository review, not hands-on testing or an electrical-safety audit. Repository claims are identified as such; availability does not establish measurement accuracy.

## Executive finding

The earlier search was too narrow. Open projects exist for broad-band impedance, ICG processing, multi-lead ECG and direct WHOOP access. The remaining obstacle is not that the measurement principles are proprietary: it is combining safe acquisition, calibrated electrode geometry, validated physiological models and a convenient consumer workflow.

**No integrated, clinically validated, open BodyScan 2 equivalent was established by this search.** However, several building blocks substantially narrow the engineering gap.

### Corrections to the earlier dossier

- **800 kHz is not an open-development impossibility.** MAX30009 is advertised for BIS up to 806 kHz, with public drivers and research code. BIMMS offers an open research design extending above 800 kHz. Neither establishes BodyScan-equivalent body composition accuracy. [12](https://www.analog.com/en/products/max30009.html) [1](https://www.sciencedirect.com/science/article/pii/S2468067222001328)
- **AD5940/AD5941 are not limited to 100 kHz.** Their high-speed impedance path supports up to 200 kHz. The earlier report conflated these with the AD5933. [21](https://www.analog.com/media/en/technical-documentation/data-sheets/ad5940-5941.pdf)
- **ICG is not a closed-only modality.** Clifford Lab provides ICG processing; PEPbench provides pre-ejection-period extraction; Biosignal PI published ECG+ICG hardware work. This is not a ready-made open bathroom scale. [2](https://github.com/cliffordlab/ICG_OSToolbox) [16](https://www.authorea.com/doi/full/10.22541/au.176595493.35093262/v1) [7](https://doi.org/10.1109/jbhi.2017.2783949)
- **openScale's segmental data model is not a hardware compatibility guarantee.** Its Hume Body Pod 2 PR provides a particularly useful counterexample: the maintainer states that the submitted handler publishes weight and impedance, not centrally derived composition. Five segments at two frequencies are present, but the implementation does not yet provide a complete validated segmental composition workflow. [6](https://github.com/oliexdev/openScale/pull/1537)
- **Public code is not automatically open source.** Blue2Scale uses a custom restrictive source-available license. Several NOOP-family WHOOP projects use PolyForm Noncommercial. The original Goose repository has licensing questions and is archived. Keep these separate from GPL/MIT/Apache/CERN-OHL projects. [25](https://github.com/JozefJarosciak/Blue2Scale.com/blob/master/README.md) [2](https://github.com/tigercraft4/goose) [8](https://github.com/b-nnett/goose/issues/11)
- The earlier parity percentages, predictions of future BodyScan 2 reverse-engineering support, generic DIY current-limit instructions and statements that ICW is directly measured should not be used as established evidence. No single current number or battery-only power arrangement establishes medical electrical safety.

## 1. Practical scale acquisition and data ownership

### openScale — strongest general-purpose Android starting point

Repository: https://github.com/oliexdev/openScale

**Role:** local collection, charts, exports and body-metric estimation from supported commercial scales. The support table distinguishes supported fields from fields needing reverse engineering. Release 3.1.3 introduces segmental fat/muscle fields and additional devices, but that does not mean every listed device supplies those fields. [1](https://github.com/oliexdev/openscale/wiki/supported-scales-in-openscale) [4](https://github.com/oliexdev/openScale/releases/tag/v3.1.3)

**Practical status:** usable software; compatibility must be checked per exact model, revision and measurement field. Do not buy BF710/BF800 or another foot-only scale expecting independently measured arm composition because an app supports segmental fields.

**New developments worth watching:**

- **Hume Body Pod 2 PR #1537:** five segment impedances at two frequency indices are documented in hardware-capture discussion. The contributor reports physical testing; the maintainer identifies missing composition derivation and problems in the checksum test. Treat as development, not a finished release feature. [6](https://github.com/oliexdev/openScale/pull/1537)
- **Xiaomi S400 PR #1538:** proposes changed composition equations, two-band fluid estimates and hydration warnings. The contributor reports DXA comparisons; these are not independent clinical validation or a guarantee of generalization. Verify sample size, population and actual PR/release status before relying on it. [18](https://github.com/oliexdev/openScale/pull/1538)
- **Multi-segment issue #1532:** active discussion of preserving impedance by body segment and frequency rather than collapsing it into one scalar. This is valuable for future transparent modeling. [5](https://github.com/oliexdev/openScale/issues/1532)

### BLE Scale Sync — stronger automation candidate

Repository: https://github.com/KristianP26/ble-scale-sync

**Role:** local acquisition and exporting to a broader self-hosted workflow. Recent development notes make an important distinction: a Eufy P2 broadcast path can be weight-only while an active GATT path exposes impedance for calculated composition. Supported brand/model does not guarantee every connection mode provides the same data. Hardware confirmation is also explicitly missing for some newly added adapters. [23](https://github.com/KristianP26/ble-scale-sync/pull/468)

**Best fit:** technical user wanting unattended collection and downstream storage; verify exact adapter and field support before purchase.

### Blue2Scale — useful new lead, but NOT unrestricted open source

Repository: https://github.com/JozefJarosciak/Blue2Scale.com

**Claims:** browser BLE access; Hume Body Pod tested; 39 displayed metrics including five-region muscle/fat, ICW/ECW and other estimates. The README says these metrics are calculated from BLE weight/impedance data. This must not be described as 39 independently sensed measurements or proven clinical accuracy. [25](https://github.com/JozefJarosciak/Blue2Scale.com/blob/master/README.md)

**Important limitations found in the primary README:**

- Custom **source-available** license; personal noncommercial self-hosting allowed, commercial/production deployment requires additional permission.
- PHP/MySQL backend with Google sign-in; not universally offline or account-free. Guest measurement is local, saved account measurements use a server.
- Web Bluetooth browser/platform constraints; do not assume iPhone/Safari compatibility.
- Repository snapshot shows a single initial public commit and no tags: weak evidence of sustained maintenance.
- Compatibility/general-service claims should be checked against its own proprietary-protocol document and real hardware, not extrapolated to arbitrary scales.

**Verdict:** a promising protocol/reference lead for Hume owners, not a verified open-source replacement recommendation. The openScale PR cites its protocol document, making it useful to study even if its application license does not meet the user's goal.

## 2. Broad-band impedance: the most important hardware expansion

| Project | What exists | BodyScan gap it addresses | What remains |
|---|---|---|---|
| **OpenEBI** | AD5933 four-electrode hardware and embedded software; magnitude/phase from a few kHz to 100 kHz | Transparent raw complex impedance acquisition | Limited band; no ready consumer composition model or segmental scale workflow |
| **AD5940-BIOZ** | Community bare-metal firmware and desktop GUI; two/four-wire sweeps configured 1–200 kHz | Reproducible sweeps and time-series acquisition | Evaluation-board system; mixed original/vendor licensing; calibration and safety work |
| **MAX30009 no-OS** | Driver and documented tetrapolar acquisition example | Modern BioZ acquisition foundation, potentially near the 800-kHz target | Example uses 50 kHz; must demonstrate full desired sweep, calibration and electrode routing |
| **UPRM Multi_Frq BioZ** | MAX32655/MAX30009 research repository | Multi-frequency research starting point | README describes some functions as intended/future; not a turnkey completed scale |
| **BIMMS** | Published design, hardware archive, Python and calibration approach; spectroscopy up to 10 MHz | Shows open research instrumentation can exceed 800 kHz | Lab instrument, not validated whole-body/segmental bathroom-scale composition |
| **OpenEIT/Spectra** | Dashboard, reconstruction, time series and spectroscopy; up to 32 electrodes | Multiplexed acquisition/imaging research | 80 Hz–80 kHz advertised band; tomography is not a body-fat-scale algorithm |

Sources: [13](https://github.com/openebi/hardware) [17](https://github.com/openebi/software) [3](https://github.com/melazab/AD5940-BIOZ) [2](https://analogdevicesinc.github.io/no-OS/projects/afe/max30009.html) [1](https://github.com/oscaroflores/UPRM-Multi_Frq-BioZ-Research) [1](https://www.sciencedirect.com/science/article/pii/S2468067222001328) [12](https://zenodo.org/records/7148811) [28](https://github.com/OpenEIT/OpenEIT) [14](https://mindseyebiomedical.com/products/spectra-eit-kit)

### Why MAX30009 changes the engineering conclusion

The manufacturer's product page advertises BIS frequencies from 1 kHz to 806 kHz and ICG applications. Public no-OS code provides an implementation route, with a source-file header identifying a BSD license. This is a credible component-level path, not evidence that any project has replicated Withings' internal electronics. [12](https://www.analog.com/en/products/max30009.html) [7](https://analogdevicesinc.github.io/no-OS/drivers/afe/max30009.html)

A real build still needs:

1. Frequency-by-frequency gain and phase calibration against known loads.
2. Appropriate multiplexing for each electrode pathway.
3. Contact detection and repeatable geometry/posture.
4. Electrical safety assessed for the entire system and all attached equipment.
5. Appropriate population-validated composition equations.
6. Repeated-measures and reference-method testing, not merely agreement on resistors.

**13 frequencies is not an uncopyable feature.** The hard part is obtaining useful, stable, validated measurements at the chosen frequencies and translating them into physiological estimates.

### BIMMS: a genuine open research instrument

The HardwareX publication lists approximately $650 hardware cost at publication, CC BY 4.0 licensing and openly archived fabrication/software files. Treat that as historical research BOM context, not a current shopping quote. A proprietary Analog Discovery acquisition platform is part of the design, so an open front-end does not imply every underlying instrument is open hardware. [1](https://www.sciencedirect.com/science/article/pii/S2468067222001328) [12](https://zenodo.org/records/7148811)

## 3. ICG and pumping-related timing

### Clifford Lab ICG_OSToolbox

https://github.com/cliffordlab/ICG_OSToolbox

Includes noisy-beat removal, ECG-synchronized ensemble averaging, manual/automatic fiducial annotation and parameter extraction, with example ECG/ICG recordings. The README requires MATLAB and the PhysioNet cardiovascular toolbox. The repository snapshot's latest visible commit is January 2024. **Usable research processing, not acquisition hardware; open code still has a proprietary runtime dependency.** [2](https://github.com/cliffordlab/ICG_OSToolbox)

### PEPbench

https://github.com/empkins/pepbench

Python package for automated pre-ejection-period extraction. Related work describes MIT licensing and automated ICG fiducial detection. Repository inspection shows recent October 2026 changes. This is particularly relevant to the timing-analysis portion of the gap, but still requires suitable synchronized source recordings; it does not create a Withings Heart Age model. [16](https://www.authorea.com/doi/full/10.22541/au.176595493.35093262/v1)

### Biosignal PI / Z-RPI

The 2017 publication combines Raspberry Pi, ADAS1000 ECG and AD5933 impedance sensing, extracting ejection time, stroke volume and cardiac output. Its documentation statement refers to a **noncommercial share-alike** license, and this search did not establish a currently complete maintained build package. **Research precedent, not a ready recommendation or unrestricted-open project.** [7](https://doi.org/10.1109/jbhi.2017.2783949) [10](https://www.researchgate.net/publication/321841956_Full_Impedance_Cardiography_Measurement_Device_Using_Raspberry_PI3_and_System-on-Chip_Biomedical_Instrumentation_Solutions)

**Revised verdict:** open ICG analysis and research acquisition do exist. No integrated scale replacement or validated replica of Withings' pumping/age scores was established.

## 4. PWV, pulse timing and arterial research

### PulseLab

https://github.com/pulselabteam/pulselab

MATLAB toolbox for ECG/PPG processing and cuffless BP-model research. Useful for experimenting with pulse timing, not proof of clinical PWV accuracy or a replacement for a validated cuff. [21](https://github.com/pulselabteam/pulselab)

### ECG+PPG pulse-arrival-time research hardware

https://github.com/GCY/Continuous-Non-Invasive-Blood-Pressure-Research-Platform---ECG-and-PPG-Pulse-Arrival-Time-Based-

Provides a hardware/software direction for ECG plus MAX3010x PPG acquisition. **Pulse arrival time is not pure arterial transit time:** the ECG-to-peripheral-pulse interval includes pre-ejection timing. This matters when interpreting BP or stiffness results. [14](https://github.com/GCY/Continuous-Non-Invasive-Blood-Pressure-Research-Platform---ECG-and-PPG-Pulse-Arrival-Time-Based-)

### OpenCardiographySignalMeasuringDevice

https://github.com/MilosRasic98/OpenCardiographySignalMeasuringDevice

More substantial than a basic sensor tutorial: project files include PCB Gerbers, schematics, printed parts, firmware and GUI. Acquires cuff pressure, ECG, phonocardiography and PPG with a Pico W-based design. Useful as a multi-signal bench-research starting point; not BodyScan 2's ICG or scale-based PWV implementation. License terms need inspection before reuse. [3](https://github.com/MilosRasic98/OpenCardiographySignalMeasuringDevice)

### Supporting resources

- **Pulse Wave Database / PulseAnalyse:** simulated arterial waveforms and feature algorithms; valuable for tests, not personal measurement. [2](https://peterhcharlton.github.io/pwdb/pwdb.html) [13](https://peterhcharlton.github.io/pwdb/algorithms.html)
- **PulseWaveform:** PPG morphology and component-wave feature pipeline; not automatic validated Vascular Age. [12](https://github.com/stw32/PulseWaveform)
- **cam-bpw-sim / bpwave:** open waveform simulator and validation software; engineering test infrastructure, not a human BP monitor. [4](https://doi.org/10.3390/s25165173)
- **PolyPulse radar research:** published multi-site PTT study with MIT code; a radically different research route, not a practical bathroom-scale substitution. [24](https://www.nature.com/articles/s41467-026-73453-x)

**Revised verdict:** substantial open pulse-analysis infrastructure exists. No convenient, validated, open scale-based vascular-age replacement was demonstrated.

## 5. Multi-signal platforms and ECG

### HealthyPi 5 — strong open hardware starting point

https://github.com/Protocentral/protocentral_healthypi_5

RP2040 + ESP32-C3; MAX30001 ECG/respiration, AFE4400 PPG and temperature support. Hardware is CERN-OHL-P v2 and software MIT. This is a better documented research platform than assembling unrelated low-cost modules with assumed synchronization. **Its respiration BioZ does not make it a broad-band composition spectrometer.** [1](https://github.com/Protocentral/protocentral_healthypi_5)

### BioGAP / BioGAP-Ultra

https://github.com/pulp-bio/BioGAP

Modular low-power biosensing architecture, 16-channel biopotential acquisition and PPG shields; paper demonstrates ECG/PPG PAT estimation. Hardware license is Solderpad 0.51. Advanced research fabrication and firmware effort; no demonstrated whole-body composition model or complete scale-equivalent ICG system should be inferred. [5](https://github.com/pulp-bio/BioGAP) [6](https://arxiv.org/abs/2508.13728)

### Card/IO

https://github.com/card-io-ecg/card-io-hw

KiCad hardware for a single-lead ECG in a compact format. Relevant to open waveform ownership, not an upgrade over the user's MG screening capability. [14](https://github.com/card-io-ecg/card-io-hw)

### MobilECG-II / CardioBit

https://github.com/RobertCsordas/MobilECG-II
https://github.com/kevmasajedi/Cardiobit

Multi-channel/lead research is not limited to AD8232 single-lead tutorials. MobilECG-II describes an open Holter but explicitly warns of a preliminary buggy release with no stable branch. CardioBit describes reduced-lead acquisition and attempted virtual lead reconstruction: reconstructed leads must not be sold as independently recorded diagnostic 12-lead equivalence. [9](https://github.com/RobertCsordas/MobilECG-II) [1](https://github.com/kevmasajedi/Cardiobit)

**With MG already owned:** additional ECG hardware is low priority unless the explicit aim is raw signals, reproducible algorithms or different electrode configurations. Open acquisition is not regulatory clearance for AFib detection.

## 6. EDA is available; a nerve-score replacement was not found

### EmotiBit

https://github.com/EmotiBit/EmotiBit_Docs
https://github.com/EmotiBit/EmotiBit_FeatherWing

Records EDA, multi-wavelength PPG, temperature and motion; open firmware and documentation and published validation work. Hardware licensing and fabrication-file completeness must be checked separately rather than inferred from MIT software. [1](https://github.com/EmotiBit/EmotiBit_Docs) [12](https://www.sciencedirect.com/science/article/pii/S2772569323000567)

### BITalino

https://github.com/BITalinoWorld/firmware-bitalino-revolution
https://github.com/BITalinoWorld/revolution-python-api

Established biosignal ecosystem with ECG/EDA and other sensors; firmware/API repositories provide GPL code. Useful for recording autonomic skin responses, not proof of a sudomotor-neuropathy score. [22](https://github.com/BITalinoWorld/firmware-bitalino-revolution) [24](https://github.com/BITalinoWorld/revolution-python-api)

**Key distinction:** ordinary EDA/GSR and electrochemical skin-conductance protocols are not interchangeable. ESC literature describes specific stimulation/electrochemistry and electrode procedures. This expanded search did not establish a complete validated open Withings Nerve Response or Sudoscan-equivalent implementation. Do not apply clinical ESC thresholds to generic GSR measurements. [6](https://pmc.ncbi.nlm.nih.gov/articles/PMC4601729/)

## 7. Existing WHOOP MG: two very different software routes

### Route A — retain official WHOOP processing, own a downstream copy

**HealthLog:** https://github.com/MBombeck/HealthLog

Self-hosted health timeline with WHOOP and Withings OAuth sync, body composition and other health records. Good candidate to evaluate for a combined dashboard. Local storage does not remove upstream WHOOP/Withings cloud dependencies; scale-to-HealthLog ingestion must be verified separately. [2](https://github.com/MBombeck/HealthLog)

**Open Wearables:** https://github.com/the-momentum/open-wearables

Unified developer-facing ingestion/API layer. WHOOP provider documents recovery, sleep/workout/cycle summaries and body measurements, but no continuous HR stream through the official API. A unified schema supporting many fields does not mean WHOOP supplies every field. [9](https://github.com/the-momentum/open-wearables) [12](https://openwearables.io/docs/providers/whoop-api-integration)

**whoopity:** https://github.com/sjapanwala/whoopity

Browser-side WHOOP export visualization with IndexedDB, avoiding a live API integration. Useful for trying local analysis without changing the strap workflow. Inspect its license before redistribution. [16](https://github.com/sjapanwala/whoopity)

**Python WHOOP client:** https://github.com/hedgertronic/whoop

API-v2/OAuth integration building block, not an independent replacement for WHOOP hardware processing or subscriptions. [11](https://github.com/hedgertronic/whoop)

The official API lists read scopes for recovery, cycles, sleep, workouts, profile and body measurements. This review did not establish public endpoints for raw MG ECG, AFib classifications or Blood Pressure Insights. Do not promise that a third-party dashboard exports all the MG-exclusive features. [18](https://developer.whoop.com/api/)

### Route B — direct BLE from the strap, experimental independent processing

| Project | License/status evidence | MG relevance | Main caution |
|---|---|---|---|
| **whoop-rs** | Apache-2.0 repository; Rust library/CLI/TUI/browser route | Explicitly lists MG and ECG command support | README capability claims need hardware/firmware verification; not cleared screening or official score equivalence |
| **Whoop5Protocol** | MIT; Swift frame/checksum and record decoder | Explicit 5.0/MG protocol target | A decoder library is not a complete wearable app or clinical algorithm |
| **Goose original** | Archived June 2026; licensing unresolved in reviewed evidence | Original README targets 5.0 only | Do not infer MG support from news headlines |
| **NOOP/Goose forks** | Several use PolyForm Noncommercial; evolving forks/archives | Some explicitly claim MG support | Source-available rather than unrestricted open source; conflicting ECG support claims |

Sources: [23](https://github.com/eugenehp/whoop-rs) [20](https://github.com/Rudra5417/whoop5-protocol) [1](https://github.com/b-nnett/goose) [8](https://github.com/b-nnett/goose/issues/11) [16](https://github.com/b-nnett/goose/pulls) [2](https://github.com/tigercraft4/goose) [22](https://github.com/tanarchytan/noop)

**Important unresolved ECG discrepancy:** whoop-rs advertises MG ECG support; a NOOP Android fork says ECG remains gated/unreachable; an MG issue documents success responses without ECG data. These could reflect different firmware, command handling or entitlement. They do not establish reliable clinically useful subscription-free MG ECG. [23](https://github.com/eugenehp/whoop-rs) [22](https://github.com/tanarchytan/noop) [26](https://github.com/ryanbr/noop/issues/891)

**Data-loss caution:** whoop-rs documents that acknowledging offloaded history can let the strap reclaim it. Do not casually switch collectors or run experimental clients against important unsynced history. First sync/export official data, inspect commands, avoid configuration writes and firmware changes, and establish how clients coexist. Battery-only operation is not a universal safety guarantee for external body-connected electronics.

## 8. Revised recommendation for this user

### Practical now

1. Keep the official MG workflow if its ECG/AFib screening and proprietary coaching are important.
2. Choose a commercial scale based on **verified exact-model local acquisition**, not biomarker count.
3. Use openScale for phone-centric collection or evaluate BLE Scale Sync for automation.
4. Evaluate HealthLog as a joint timeline; treat scale ingestion/format mapping as a separate integration task.
5. Archive raw weight/impedance where available, plus the formula/version used for every derived output.

This is an architectural recommendation, not a claim that every arrow is already a one-click supported connector.

### Closest segmental lead to investigate

Hume Body Pod hardware plus the protocol work around openScale #1537. First prove raw regional impedance acquisition, then identify frequencies and calibrate, then choose/validate equations. Blue2Scale can inform that investigation, but its restrictive license, calculated metrics and limited maintenance evidence prevent calling it the finished open answer.

### Advanced engineering path

MAX30009-based acquisition + safe electrode switching + calibrated known-load tests + raw-spectrum storage. Add ECG synchronization and PEPbench/ICG toolbox only if pumping-related research is truly needed. This path can narrow the *measurement engineering* gap; it does not recreate Withings' validated models or medical clearances.

### Updated gap assessment

| Target | Revised finding |
|---|---|
| Weight, logs, export | Practical open software available |
| Basic composition estimates | Practical, hardware/formula dependent |
| Regional impedance | Credible community hardware captures and developing support |
| 800-kHz-class spectroscopy | Credible component/driver path; open higher-band lab design also exists |
| ICG timing analysis | Open research tools available; acquisition required |
| PWV/vascular age | Research components exist; validated turnkey open scale not established |
| ECG/PPG sensing | Multiple open platforms; MG already covers much practical use |
| Direct MG data ownership | Real projects, but experimental and feature-dependent |
| MG ECG/AFib without subscription | Not established by this review |
| ESC nerve-response score | No validated complete open replacement found |
| Glucose Resilience / Heart Age replicas | No validated open replica found |
| Single polished, safe, validated all-in-one scale | Not established |

**Bottom line:** the open ecosystem is considerably richer than my initial search suggested. Its strongest near-term value is local acquisition, transparent estimates and combined data ownership. Its biggest remaining gap is a validated integrated product—not the mere existence of the sensor principles.
