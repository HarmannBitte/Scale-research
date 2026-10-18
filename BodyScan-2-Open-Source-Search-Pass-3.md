> **October 17 follow-up:** See [pass 4: compatibility and subscription audit](BodyScan-2-Pass-4-Compatibility-and-Subscription-Audit.md). Withings now says automatic third-party sync requires Withings+ for accounts created from October 13, 2026; older accounts retain free sync and manual CSV/PDF exports remain free. Source inspection also identifies BMI-only fallbacks in several scale adapters. Do not infer measured composition from a generic support-table entry.

# BodyScan 2: third-pass open-source investigation

**October 17, 2026 · New findings beyond the previous expanded dossier**

Scope: commercial-scale protocols, local and cloud ingestion, broad-band and multiplexed research hardware, model fitting, synchronized cardiac signals, imaging/anthropometry alternatives, and implications for an existing WHOOP MG owner.

## Findings in one page

1. **Fitdays/Lefu segmental BLE acquisition is a stronger lead than previously identified.** `dandwhelan/fitdays-lefu-scale` publishes an MIT codec, handshake planner and computer-based acquisition example preserving ten regional impedance readings. I cloned it and ran its tests: **11 passed, one skipped**. No physical scale was available. Its optional vendor-equivalent composition path requires a proprietary binary not distributed in the repository.
2. **A usable self-hosted segmental dashboard need not be built from scratch.** RecompPro-core imports Fitdays CSV/XLSX reports and displays five-zone trends. It is MIT-licensed, but direct cloud integration was documented as an issue/proposal rather than established shipped support.
3. **HealthyPi Move is a substantial wearable research alternative, with an important closed dependency.** Open hardware/app/firmware surround proprietary MAX32664 sensor-hub firmware. This is not an entirely open algorithm chain or evidence of WHOOP-equivalent clinical screening.
4. **The missing analysis layer is partly available.** impedance.py, NeuroKit2, pyPPG, BioSPPy and Lab Streaming Layer cover modeling, filtering, morphology and synchronization. None creates measurements absent from the hardware.
5. **Broader body-composition alternatives exist.** Ultrasound muscle analysis, CT composition analysis and 3D anthropometry are useful adjacent approaches, not daily bathroom-scale replacements.
6. **Still not established:** a single validated open BodyScan 2 replacement; equivalent nerve-response/Glucose Resilience/Heart Age algorithms; reliable independent MG clinical-feature parity.

## Evidence standard

- **Local test:** I executed code against supplied fixtures. This does not validate a physical sensor or physiological accuracy.
- **Primary documentation:** read repository or paper; capabilities remain author claims unless otherwise specified.
- **Search lead:** surfaced in search but not deeply audited; explicitly lower confidence.
- **Proposal:** issue/PR, not assumed merged or released.

Public repository ≠ open license. Open application ≠ open sensor firmware. Vendor report agreement ≠ reference-method accuracy. Historical paper BOM ≠ current complete purchase cost.

---

## 1. Strongest new acquisition lead: Fitdays/Lefu dual-frequency segmental scales

**Repository:** https://github.com/dandwhelan/fitdays-lefu-scale

### What is actually published

The README describes a reverse-engineered eight-electrode scale advertising `JEETIF…`, using vendor BLE service `0xFFB0`. Code includes:

- frame parsing and checksum validation;
- a timestamped profile/handshake planner;
- live weight and stable-result decoding;
- ten impedance values: trunk, both arms and both legs at two frequency indices;
- a complete `bleak` acquisition example;
- tests against captured frames. [1](https://github.com/dandwhelan/fitdays-lefu-scale)

This is closer to the missing regional-impedance layer than a foot-only scale broadcasting a single resistance number.

### Verification performed locally

Cloned commit: `5efdfd62d7ac8ad2a828501d0822095f97367180`.

Executed from the repository root:

```bash
PYTHONPATH=. python -m pytest -o addopts='' -ra tests
```

Result:

```text
collected 12 items
11 passed, 1 skipped
SKIPPED: vendor library not provided — set WLA37_SO_PATH to your own copy
```

The supplied tests exercise corrupted-frame rejection, profile construction, fresh-versus-replayed results, segment decoding, absent electrode-contact data and handshake planning. This verifies behavior against the included fixtures only—not the fixture provenance, BLE behavior on another unit, or clinical accuracy.

**Saved evidence:** `research-pass-3/fitdays-test-results.txt`; source snapshot under `research-pass-3/fitdays-lefu-scale/`.

### Critical closed-source dependency

The optional `wla37.py` route runs Fitdays' `libICBodyFatAlgorithms.so` under Unicorn emulation. The user must supply that library from their own app copy; it is neither included nor covered by the repository's MIT license. The README reports vendor-output comparison on **one paired weigh-in**, not independent validation. It also identifies a fixed user ID and uncertain portability to other units. [1](https://github.com/dandwhelan/fitdays-lefu-scale)

Therefore distinguish:

| Layer | Status |
|---|---|
| BLE frame codec / handshake | MIT source available; supplied tests passed locally |
| Raw regional impedance acquisition | Hardware support claimed for the documented unit; not tested by me |
| Vendor-identical composition | Requires proprietary binary; one paired-sample comparison reported |
| Fully open regional composition model | Not established by this project |
| Calibration against DXA or dilution methods | Not established by this project |
| Compatibility with all Fitdays, Hume or Renpho scales | Not established |

Two frequency indices do not prove their exact values in hertz. Do not assume they are 50/250 kHz without hardware/firmware evidence. This `FFB0` family is also not automatically the same as the Hume Body Pod 2 `FFF0` protocol discussed previously.

### Why this matters with WHOOP MG

**Recommended investigation, not a verified plug-and-play stack:** retain official MG and pair it with a precisely matched handle scale whose regional raw data can be acquired locally. That targets the largest uncovered measurement category without duplicating the wearable.

Before buying, obtain exact model number, BLE advertisement/service UUID, sample capture and confirmation that the repository works on that revision. A shared vendor app or OEM name alone is insufficient.

---

## 2. More practical scale software and export routes

### RecompPro-core — segmental report dashboard

https://github.com/cfassoni/RecompPro-core

**Primary documentation reviewed. MIT license.** Self-hosted Next.js/SQLite application importing Fitdays CSV/XLSX, with five-zone composition trends, original report attachments and access-controlled sharing. Repository showed October 2026 activity and Docker deployment files. [6](https://github.com/cfassoni/RecompPro-core)

**Useful now:** retain and visualize existing composition reports without writing a dashboard.

**Not established:** direct local BLE collection, native WHOOP integration, or a turnkey importer for arbitrary raw impedance JSON. Do not connect those arrows without an explicit adapter.

Issue #119 proposes Fitdays cloud integration and references other clients; the issue is not evidence that the connector shipped. The importer's unit/profile validation work is particularly important because mass, percentage and impedance fields are easy to silently mis-map. [1](https://github.com/cfassoni/RecompPro-core/issues/119) [7](https://github.com/cfassoni/RecompPro-core/pull/120)

### ScaleLink — deliberately small Android bridge

https://github.com/mahmutaunal/ScaleLink

**Primary README reviewed. Apache-2.0.** Local BLE → Health Connect; no account/backend. The reviewed support table lists **Xiaomi Mi Smart Scale 2 XMTZC04HM, weight only**. Its general schema can represent composition fields, but no listed device should be assumed to populate them. Young repository; validation notes still describe release gates. [34](https://github.com/mahmutaunal/ScaleLink)

Best fit: someone wanting a simple weight bridge rather than a full openScale alternative. It does not close the BodyScan advanced-sensing gaps, and Health Connect availability does not establish WHOOP consumption of each field.

### SmartScaleConnect — wider ecosystem bridge

https://github.com/AlexxIT/SmartScaleConnect

**Primary README reviewed.** Imports from Garmin, Home Assistant, Mi Fitness, My TANITA, Picooc, Xiaomi Home, Zepp Life, CSV and JSON; exports a narrower set. Offers multiple users and scripting. README warns of early development; visible latest commit was December 2025. [2](https://github.com/AlexxIT/SmartScaleConnect)

Useful if data already lives in one of these ecosystems. This is not evidence of cloud-free device acquisition, raw segmental impedance support, or WHOOP integration. Inspect its license and adapter-specific limits before redistribution/deployment.

### Fitdays cloud client

https://github.com/AboveColin/fitdays

**Primary repository reviewed.** Async unofficial read-only cloud client handling authentication, region redirects, measurement models and token renewal. Recent test/CI work is visible. This is a cloud extraction route, not the local codec above. License should be checked directly before reuse. [1](https://github.com/AboveColin/fitdays)

Alternative lead: `roquerodrigo/fitdays-api`, referenced by RecompPro issue #119, not independently audited here. [1](https://github.com/cfassoni/RecompPro-core/issues/119)

### Additional model-specific leads — not purchase endorsements

- Local Home Assistant integrations: [Renpho](https://github.com/ronnnnnnnnnnnnn/renpho_fitness_scale_ble) and [Etekcity](https://github.com/ronnnnnnnnnnnnn/etekcity_fitness_scale_ble). Search leads, not independently tested. Check exact model support and whether composition is vendor-provided or calculated.
- [export2garmin](https://github.com/RobertWojtowicz/export2garmin): Xiaomi S400 data/decryption/export lead; optional Garmin destination remains cloud-based.
- [inbody-api-mcp](https://github.com/rwestergren/inbody-api-mcp): cloud-account client, not evidence of direct H20/H30 BLE decoding.
- [inbody-to-sqlite](https://github.com/MarshalX/inbody-to-sqlite): report extraction using an external vision service is not fully local merely because storage is SQLite.

This pass did **not** establish a reliable open raw-segmental BLE collector for InBody H20/H30. Do not infer one from generic BLE libraries or a cloud API wrapper.

---

## 3. Additional impedance hardware beyond MAX30009 and BIMMS

### AFE4300Control

https://github.com/EIT-team/AFE4300Control

Public code to control TI's AFE4300. This chip combines weight and composition front ends and supports multiple tetrapolar configurations. TI publishes calibration/segmental-BIA guidance. **This is an older research/control lead, not a newly verified complete open scale.** License, GUI dependencies and working hardware must be checked. [1](https://github.com/EIT-team/AFE4300Control) [14](https://www.ti.com/product/AFE4300) [7](https://www.ti.com/lit/an/sbaa202/sbaa202.pdf)

### Four-ring, 32-channel AFE4300 EIT design

The HardwareX paper publishes CC BY 4.0 design materials and lists a historical $49.17 hardware BOM. Its reported validation uses saline-tank objects and conductivity/volume changes. That is not a $49 clinically validated human composition scale; exclusions, fabrication and current sourcing affect real cost. Source archive is identified in the paper. [36](https://pmc.ncbi.nlm.nih.gov/articles/PMC10767629/)

Why relevant: additional evidence that programmable electrode multiplexing is openly documented. Why not equivalent: ring-based tomography and segmental hand/foot BIA are different geometries and inverse problems.

### ABI EIT

A wearable GPLv3 research EIT design, source archive available, 25-kHz excitation and 4–32 electrodes. The paper lists roughly $260 hardware cost. Better treated as a lung-monitoring research platform than a fat/muscle scale. [8](https://www.hardware-x.com/article/S2468-0672(24)00015-4/fulltext)

---

## 4. The previously underexplored layer: impedance model fitting

Raw spectroscopy → fitted electrical parameters → estimated physiological compartments are three separate stages.

| Project | Published function | Relevance / limitation |
|---|---|---|
| **impedance.py** | Preprocessing, validation, circuit fitting, visualization | Strong general analysis candidate; electrochemistry origins, not a validated body-composition engine |
| **Cole-Cole-fit** | Complex spectrum fitting | README explicitly calls it old/unused and points elsewhere; do not choose by name alone |
| **ccd_tools** | Cole-Cole/Debye decompositions | Geophysical origins; adaptation and units/conventions matter |
| **cole-fit web** | Local browser import of f,R,X data | Public source but no license visible in reviewed listing; README/file-name inconsistency; not an established open recommendation |

Sources: [9](https://github.com/ECSHackWeek/impedance.py) [30](https://github.com/kbknudsen/PyEIS) [1](https://github.com/m-weigand/Cole-Cole-fit) [2](https://m-weigand.github.io/ccd_tools/) [6](https://github.com/simicm1987/cole-fit)

### What could be implemented transparently

With calibrated complex impedance, one can compute phase, visualize spectra and fit a Cole-style model. Whether those parameters provide valid ICW/ECW or tissue estimates depends on the acquisition, pathway, reference data and chosen equations. A curve fit is not a validated Cellular Age.

**Important for commercial scale selection:** a pair of impedance magnitudes does not automatically give complex resistance/reactance or measured phase. Do not advertise phase angle from data that cannot support it. Even models fitted to sparse magnitudes require explicit assumptions and validation.

Store frequency, units, pathway, raw complex/magnitude status, calibration version, posture, profile and formula version. Preserve raw data separately from calculated values so new models do not rewrite measurement history.

---

## 5. Synchronized cardiovascular sensing: more concrete routes

### HealthyPi Move / NEXT

Hardware: https://github.com/Protocentral/healthypi-move-hw
Firmware: https://github.com/Protocentral/healthypi-move-fw

**Primary firmware history inspected.** Watch-format platform with single-lead ECG, wrist/finger PPG, EDA and other sensing. NEXT documentation identifies open hardware, MIT application firmware and an app/data-protocol path. It is a more integrated research device than a bag of modules. [1](https://github.com/Protocentral/healthypi-move-hw) [13](https://protocentral.com/healthypi-move-next/)

**Significant caveat:** the firmware repository explicitly says proprietary Analog Devices MAX32664 `.msbl` sensor-hub firmware was removed from redistribution and must be provisioned separately. Therefore an open watch/application does **not** mean every shipped physiological algorithm is open. [9](https://github.com/orgs/Protocentral/repositories)

The vendor's BP trending uses a sensor hub, not proof of a fully open clinically validated BP estimator. Availability statements differ between repository and crowdfunding page; verify current revision, price and shipping rather than assume stock. [5](https://www.crowdsupply.com/protocentral/healthypi-move)

**For someone already owning MG:** valuable for raw signals and firmware control, not necessarily useful to buy just to duplicate HR/SpO2/ECG. No WHOOP-equivalent cleared AFib workflow or score equivalence established here.

### SPEC-P6

https://github.com/Andres-Navarro-Torres/spec-p6-retroauricular-system

Multi-site PPG/IMU platform with PCB/CAD/firmware/software and a synchronization trigger. README gives a 50-Hz target rate. Useful acquisition architecture, but no assumption that a 20-ms sample interval plus wireless synchronization meets a particular PWV error target. Hardware timing, buffering, clock drift and filtering delays need measurement. Search lead; license and assembly not audited. [4](https://github.com/Andres-Navarro-Torres/spec-p6-retroauricular-system)

### PulseSensor Playground two-sensor PTT lab proposal

PR #210 describes synchronous two-channel 500-Hz acquisition, quality gates and a web lab. It is a **PR**, not assumed merged/released or physically validated by its software-test results. Promising inexpensive research direction, not vascular-age equivalence. [6](https://github.com/WorldFamousElectronics/PulseSensorPlayground/pull/210)

### Lab Streaming Layer (LSL)

https://github.com/sccn/liblsl
https://github.com/labstreaminglayer/pylsl
https://github.com/labstreaminglayer/App-LabRecorder

MIT core/library ecosystem for time-synchronized streams and recording. Good infrastructure for combining research sensors. **It cannot retroactively remove unmeasured device sampling offsets, BLE buffering or proprietary preprocessing delays.** WHOOP daily API records are not synchronized raw ECG/PPG acquisition. [7](https://github.com/sccn/liblsl) [13](https://github.com/labstreaminglayer/pylsl) [11](https://github.com/labstreaminglayer/App-LabRecorder)

### Datasets before hardware spending

- PhysioNet **Pulse Transit Time PPG**: synchronized multi-site signals, pressure, motion and ECG across 22 participants. Useful to evaluate analysis on existing recordings. [2](https://physionet.org/content/pulse-transit-time-ppg/1.0.0/README.txt)

---

## 6. Biosignal analysis: mature tools, not extra sensors

- **NeuroKit2 — MIT:** ECG/PPG/EDA/EMG/respiration processing and derived metrics. Strong first analysis dependency to evaluate. [2](https://link.springer.com/article/10.3758/s13428-020-01516-y)
- **BioSPPy — BSD-3-Clause:** physiological preprocessing and feature extraction. [7](https://www.sciencedirect.com/science/article/pii/S2352711024000839)
- **pyPPG — AGPLv3:** pulse-wave fiducials/morphology and documented benchmarking. Paper/article license is not the software license. Finger-PPG validation should not be assumed to transfer unchanged to wrist reflectance or low-rate wearable exports. [5](https://pypi.org/project/pyPPG/) [10](https://pmc.ncbi.nlm.nih.gov/articles/PMC11003363/)
- **BIOBSS — MIT:** wearable ECG/PPG/EDA/acceleration processing. [23](https://github.com/obss/BIOBSS)

**tinyGSR** adds an accessible open hardware acquisition path: current documentation identifies CERN-OHL-P hardware, MIT Arduino code and digital skin-conductance output. It remains ordinary EDA/GSR rather than demonstrated ESC neuropathy assessment. [23](https://protocentral.com/product/protocentral-tinygsr-gsr-eda-digital-output-sensor-board-qwiic-stemma-qt/docs/getting-started/)

---

## 7. Alternative modalities: useful but not scale replacements

### 3D body shape / anthropometry

- **SMPL-Anthropometry:** measurements from fitted body meshes.
- **Pose-independent anthropometry:** body measurements from sparse 3D landmarks.
- **SHAPY:** image-to-body-shape/measurement research. [1](https://github.com/DavidBoja/SMPL-Anthropometry) [2](https://github.com/DavidBoja/pose-independent-anthropometry) [9](https://github.com/muelea/shapy)

They can add waist/hip/limb geometry for longitudinal tracking. They do **not** sense internal fat, water compartments, nerve response or cardiac activity. Body-model files/datasets may carry separate research or commercial restrictions; repository code alone is not an unrestricted full stack. Camera, clothing, pose and fitting error can obscure small changes.

### Ultrasound muscle and fat analysis

**DeepACSA** processes muscle cross-sectional area in ultrasound images. Published open segmentation work also targets vastus lateralis muscle and subcutaneous adipose tissue. Useful for localized muscle-size questions that differ from whole-body BIA. Requires appropriate ultrasound images and operator expertise; not a phone-only substitute. [13](https://github.com/PaulRitsche/DeepACSA) [6](https://pmc.ncbi.nlm.nih.gov/articles/PMC12453877/)

### CT-based body composition

**Comp2Comp, BOA, CompositIA** and related pipelines segment muscle and visceral/subcutaneous fat on existing medical scans. This is a genuinely different observation of anatomy, not another impedance formula. [17](https://arxiv.org/abs/2302.06568) [5](https://github.com/UMEssen/Body-and-Organ-Analysis) [9](https://link.springer.com/article/10.1186/s41747-025-00552-7)

Use only appropriately obtained scans and expert interpretation. **Do not obtain repeat CT scans merely for recreational composition tracking.** Model weights/subtasks may have additional licenses. None supplies daily bathroom measurements.

**recomptracker** is another lead for tracking existing DXA results and reference percentiles, not acquiring a DXA scan or replacing its hardware. [2](https://github.com/bmabey/recomptracker)

### BCG / muscle projects intentionally not promoted

Bathroom-scale BCG research shows the concept of measuring cardiac recoil on a weighing platform, but this pass did not establish a convenient maintained open scale implementation equivalent to Withings ICG. Several search hits concern video or under-mattress BCG, not a bathroom scale. [29](https://web.stanford.edu/group/kovacslab/cgi-bin/uploads/PDFs/Dissertations/Dissertation_Inan.pdf)

OpenMuscle and OpenEMG are useful projects for pressure/activation/gesture sensing. **They do not measure muscle mass** and should not inflate a composition-parity list. [5](https://github.com/Open-Muscle/OpenMuscle-Hub) [1](https://github.com/CGrassin/OpenEMG)

---

## 8. Updated shortlist and decision path

### If you want a solution to use rather than a research project

1. **Already have a Fitdays handle scale?** Try a report export with RecompPro-core first. This avoids altering scale behavior.
2. **Want local raw segmental data?** Check exact compatibility with `fitdays-lefu-scale`. Preserve raw records; don't silently replace vendor values with unvalidated estimates.
3. **Want Android weight → Health Connect?** ScaleLink is a narrow option for its listed model; openScale remains broader.
4. **Already have cloud history?** Evaluate the appropriate Fitdays/Renpho/Tanita bridge, recognizing it preserves cloud dependence.
5. **Already own MG?** Keep its official workflow while evaluating scale capture. A combined self-hosted dashboard is a separate adapter/data-model task, not automatically WHOOP-app integration.

### If the goal is an open BodyScan-class engineering platform

Suggested staged architecture, **not an existing validated integrated product**:

```text
Commercial segmental BLE scale OR calibrated broad-band BioZ hardware
  -> raw weight/path/frequency/impedance archive
  -> explicit model fitting and versioned physiological estimates
  -> local time-series/dashboard

Official WHOOP exports/API OR separately verified direct-BLE research
  -> independent wearable archive
  -> daily association with composition trends

Optional synchronized ECG/PPG/ICG research acquisition
  -> source timestamps + measured latency + signal-quality gates
  -> LSL/recording + NeuroKit2/pyPPG/PEP tools
```

Start with acquisition and calibration, not AI interpretation. Passing parser tests does not validate physiology. Multiple separately connected body-contact devices require whole-system electrical-safety review; research boards should not be attached to a person merely because they are battery powered or described as open hardware.

### Where this search leaves the comparison

The **segmental acquisition and software ownership** gaps are narrower than the original report suggested. The **fully open physiological model** gap remains visible even in the best new project, because vendor-equivalent reports require a closed binary. PWV/ICG research components are increasingly accessible; branded age, glucose-resilience and nerve-response replicas remain unestablished.

**Best next step:** validate one exact handle scale and its output fields, rather than buy more sensors or count more repositories. For an MG owner, that is the clearest route to adding genuinely new information.
