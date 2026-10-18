# Beyond a smart scale: DXA capabilities and reusable open alternatives

**Separate investigation · 17 October 2026**  
**Scope:** what DXA actually provides; what can be reproduced, estimated, or improved using existing open technology; what remains closed or unvalidated. No DIY X-ray generator or home radiographic scanner is proposed.

## Executive finding

**There is enough existing technology to build an open, modular body-composition research system. There is not a verified, turnkey, entirely open home replacement for all DXA capabilities.** The useful architecture is not “one sensor replaces DXA.” It is:

1. **Frequent local measurements:** calibrated weight, standardized circumferences/shape, optionally research-grade raw impedance and local ultrasound.
2. **Periodic external references:** appropriately acquired DXA for composition or clinical bone assessment; MRI when anatomical muscle/VAT detail is the question. These are different examinations, not interchangeable labels.
3. **An open data and analysis layer:** original observations, quality flags, model versions, uncertainty, and portable exports—not dozens of opaque derived scores.

The strongest immediately reusable components are **NHANES reference data, report ingestion, existing CT/MRI analysis, and local ultrasound analysis**. Optical models are promising but require particular care over what was actually validated. **Bone density remains a separate workstream.** A camera, impedance scale, or synthetic bone-looking image does not measure clinical hip/spine BMD.

### Most consequential discoveries

- **A real impedance–DXA dataset bridge exists.** I downloaded the 1999–2000 NHANES BIX and DXX files. They share **4,079 unique participant IDs**. BIX contains **50 resistance and 50 reactance frequency channels**. This establishes a useful research starting point, not 4,079 automatically valid training cases. DXA validity, imputation, age, survey design and impedance quality still require filtering and appropriate analysis.
- **Pseudo-DXA is not a fully open quantitative pipeline.** GPL-3.0 code exists, but weights/test meshes are request-only; standardized meshes use Meshcapade; conversion into proprietary DXA files is explicitly nonpublic; downstream composition analysis uses DXA software.
- **The `bodycomp` photo project's headline end-to-end error is simulated.** Its two stages use separate BodyM and NHANES cohorts. The “end-to-end” evaluation adds Gaussian measurement noise to NHANES anthropometry. It is not a direct test of phone photographs paired with those participants' DXA scans.
- **Open code can still do useful work.** I reproduced `bodycomp`'s JavaScript parity check: **440 predictions, zero disagreement with its supplied Python reference outputs**. That verifies a software port—not physiological accuracy or live-camera performance.
- **The PDF extractor needs hardening.** Synthetic checks reproduced numerical corruption in its repeated-character cleanup, and non-parsing of comma-separated masses. It is a useful MIT-licensed starting point, not safe to trust unattended.
- **Current versions matter.** Comp2Comp's inspected root licence is Apache-2.0. Current `fohofmann/BodyComposition` documentation explicitly avoids the separately licensed TotalSegmentator tissue tasks; an older description of that dependency would be misleading.

These conclusions come from source inspection, primary documentation, selected bounded software checks, and an actual public-data download. **No new imaging inference, human measurement, hardware build, or clinical validation was performed.**

---

## 1. Corrections to the earlier DXA comparison

The earlier `BodyScan-2-Biomarkers-DEXA-Deep-Dive.md` overstated several points. This investigation supersedes its DXA comparison, “ground truth,” fixed scan schedule, and muscle-protection recommendations.

| Earlier simplification | Correct interpretation |
|---|---|
| DXA is “direct physics, not equation” | DXA measures X-ray attenuation and derives composition using calibration, tissue assumptions, algorithms and region definitions. Being imaging-based does not make its estimates assumption-free. |
| DXA directly measures “muscle” | **Lean soft tissue is not skeletal muscle.** It includes water and non-muscle lean tissues. Appendicular lean mass is a useful proxy, not isolated muscle mass. Fat-free mass also includes bone mineral. |
| DXA is “the only FDA-accepted” BMD method | Unsupported and too categorical. Central DXA is preferred for many clinical decisions, but QCT, pQCT, peripheral DXA, validated heel QUS and other methods have distinct roles and limitations. Regulatory authorization belongs to a particular device/intended use. |
| Whole-body DXA gives diagnostic BMD “per site” | Whole-body regional BMD/BMC is not automatically a diagnostic lumbar-spine or hip acquisition. Ask explicitly which examination and interpretation are provided. |
| DXA gives ground-truth body fat and has a universal ~1% precision | DXA is a valuable reference, not error-free truth. Precision is metric-, facility-, operator-, positioning- and system-dependent; cross-manufacturer results can differ. |
| Daily BIS “protects muscle”; a baseline DXA establishes a permanent personal offset | Measurement itself prevents nothing. Hydration can change lean estimates. One paired observation does not establish longitudinal accuracy or a stable correction equation. |
| Everyone should obtain DXA every 6–12 months / quarterly when cutting | No universal schedule is justified here. Clinical bone follow-up and elective composition tracking have different indications. Repeat testing should answer a defined question and exceed relevant measurement noise. |
| Composition “raw measurements” include all fat/muscle/bone scores | Those are commonly algorithmic outputs. **Raw impedance means frequency-specific resistance/reactance or equivalent calibrated signals**, not a CSV of final scores. |

Also do not carry forward categorical claims that particular impedance frequencies “measure cellular health” or independently isolate organs. Frequency response depends on the measurement geometry and tissue electrical properties; phase angle and fitted membrane-related parameters are not standalone diagnoses.

The key clinical distinctions and precision requirements are documented by ISCD. Its positions explicitly address QCT/pQCT/QUS as well as DXA, and call for local precision assessments and cross-calibration. [1](https://iscd.org/official-positions-2023/) [2](https://iscd.org/resources/precision-assessment-calculator-faqs/)

**Account correction retained:** you do not have a Withings account. Old advice to create one “now” to obtain pre-13-October grandfathering is inapplicable. The separate pass-4/pass-5 subscription audits remain the relevant purchasing context; this report does not revalidate every Withings claim in the earlier documents.

---

## 2. What DXA can—and cannot—tell us

### 2.1 Whole-body composition

A whole-body composition acquisition can report total and regional **fat mass, lean soft-tissue mass, bone mineral content, projected bone area and areal BMD**, with regions such as left/right arms, left/right legs, trunk and head. Android/gynoid regions and derived indices depend on the scanner's analysis package. NHANES codebooks make the distinction between lean **excluding** BMC and lean **including** BMC explicit. These definitions must survive data import. [1](https://iscd.org/official-positions-2023/) [3](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DXX_J.htm)

Useful derived quantities include:

- Fat percentage and fat mass index: FM/height².
- Lean mass index: lean soft tissue/height², with the exact lean definition recorded.
- Appendicular lean mass: sum of lean soft tissue in both arms and both legs.
- ALMI: appendicular lean mass/height².
- Left/right differences, limb-to-trunk distributions and android/gynoid ratios.

These are **derived from a smaller set of compartment measurements**. A report advertising 150 or 200 metrics has not necessarily added that many independent observations. Low lean mass alone is not a complete sarcopenia diagnosis; strength and function are separate questions.

### 2.2 Visceral fat is a special case

DXA is a projection technique. Commercial VAT packages estimate the visceral component within a defined android region using algorithms that separate or infer subcutaneous contribution. They do not provide a CT-like three-dimensional view of each internal fat depot. Hologic describes estimated VAT area/mass/volume; GE CoreScan similarly describes estimates within the android region. [2](https://continuumofcare.hologic.com/product/horizon-dxa-system/) [2](https://www.gehealthcare.com/content/dam/gehc/global/products/bone-and-metabolic-health/body-composition/documents/body-composition-analysis-br-jb48048xx-en.pdf)

**VAT area in cm², volume in cm³/litres, and mass in grams are not interchangeable without assumptions.** A single CT slice, an abdominal MRI volume and a DXA android estimate also have different anatomical coverage. Match the compartment and region before comparing errors.

### 2.3 Bone assessment is a different branch

- **BMC:** estimated mineral quantity, typically grams. Not total wet bone mass.
- **Areal BMD:** BMC/projected area, typically g/cm². Not volumetric density or a complete measure of bone strength.
- **Clinical hip/spine DXA:** dedicated acquisition, positioning, analysis and appropriate reference database; T- and Z-score interpretation depends on patient context.
- **Whole-body BMD:** useful in appropriate contexts but not a substitute for routine diagnostic hip/spine results.

Additional scanner capabilities can include vertebral fracture assessment/lateral imaging, assessment of atypical femur fractures, and trabecular bone score from appropriate spine images. These require the relevant acquisition/software and interpretation; they are not guaranteed in a fitness composition scan. TBS is a texture-derived risk adjunct, not direct imaging of microscopic trabeculae. Hologic and IOF describe these additional branches. [1](https://www.hologic.com/horizondxa) [3](https://www.hologic.com/sites/default/files/Brochure%20-%20Horizon%20DXA%20-%20PB-00238-EUR-EN%20Rev001_0.pdf) [4](https://www.osteoporosis.foundation/health-professionals/diagnosis/other-diagnostic-tools)

### 2.4 Things DXA does not independently measure

A composition scan does not directly measure ECG, arrhythmias, nerve conduction, glucose, HbA1c, insulin sensitivity, aerobic capacity, strength, muscle function, cellular health, or resting energy expenditure. A BMR/RMR value printed alongside it can be an equation; measured resting metabolism requires a suitable separate method such as indirect calorimetry.

Nor does ordinary whole-body DXA separate individual organs, muscle groups or intramuscular lipid in the way a suitable MRI/CT protocol may. The appropriate reference depends on the question:

| Question | Appropriate reference direction |
|---|---|
| Whole-body fat/FFM estimation | Carefully specified multicomponent model, often 4C; DXA remains a practical comparator |
| Anatomical VAT/SAT or muscle volume | Suitable MRI or CT with defined segmentation and coverage |
| Clinical bone density/fracture management | Appropriate clinical DXA or validated alternative within its intended scope |
| Local muscle thickness/area/architecture | Standardized ultrasound and expert annotation, with MRI comparison when needed |
| Actual muscle preservation/function | Composition plus strength/function and clinical context—not a scale score alone |

A 4C model combines body mass, body volume, body water and mineral-related information, but its component methods and equations introduce uncertainty too. A 2026 systematic review illustrates why small average BIA bias can coexist with wide individual limits of agreement; its included devices and populations do **not** establish the performance of every new instrument. [5](https://www.mdpi.com/2411-5142/11/1/65)

A 2026 DXA/MRI comparison also finds important cross-sectional and longitudinal differences. Do not translate all differences between DXA lean soft tissue and segmented MRI muscle into “DXA muscle error”: these can be different compartments. It reinforces the need to define the target rather than crown one universal gold standard. [6](https://www.nature.com/articles/s43856-026-01440-w)

---

## 3. Capability → open alternative → validation gap matrix

A spreadsheet-friendly copy is saved separately as [DEXA-Capability-Matrix.csv](./DEXA-Capability-Matrix.csv). Read it alongside the source audits and limitations below, not as a standalone clinical equivalence chart.

**Evidence labels:** **established modality** means a recognized measurement approach, not approval of every open implementation; **research** means published/source-supported work requiring validation; **proxy** means indirect prediction; **gap** means no verified reusable equivalent found in this investigation.

| Capability | Reference/acquisition | Reusable open route | Evidence strength | Remaining work / non-equivalence |
|---|---|---|---|---|
| Body weight | Calibrated scale | Load cells + local logging; existing local scale integrations | Established measurement | Traceable calibration, load position, drift, resolution vs accuracy |
| Total fat and FFM | Specified 4C or DXA comparator | NHANES-trained anthropometry/BIS; `bodycomp` regressor | Research/proxy | External paired testing; hydration, population shift; not direct tissue imaging |
| Regional fat and lean | Whole-body DXA; anatomical MRI/CT | Segmental impedance + shape; image segmentation when real scans exist | Imaging strong; home inference proxy | Region alignment; independent limb validation; no presumed equivalence |
| Appendicular lean mass/ALMI | DXA appendicular lean; MRI for actual muscle | NHANES limb labels; `bodycomp`; segmental impedance | Research/proxy | Correct target naming; external validation; strength/function separate |
| Left/right asymmetry | Standardized DXA/MRI or ultrasound | Bilateral ultrasound; segmental raw impedance; shape | Research | Positioning/electrode asymmetry and segmentation error may mimic biology |
| Waist, circumference, surface volume | Standardized anthropometry/validated 3D scan | Tape; camera/depth capture; mesh processing | Direct geometry + research automation | Clothing, pose, camera scale, occlusion, breathing and tracking repeatability |
| VAT and SAT | Defined abdominal MRI/CT region | FatSegNet; Comp2Comp; BodyComposition; licensed TotalSegmentator tasks | Established imaging + research software | Real internal imaging required; ROI/protocol validation and model rights |
| Local fat-layer thickness | Standardized ultrasound | Image export + manual/open analysis | Established technique | Pressure, landmark, fascia identification; local layer ≠ whole-body FM |
| Local muscle ACSA/thickness | Ultrasound/MRI | DeepACSA; DL_Track_US; manual 3D Slicer analysis | Published research | Operator/acquisition precision; no automatic whole-body mass conversion |
| Muscle architecture | Longitudinal ultrasound | DL_Track_US | Research | Probe angle, fascicle extrapolation, scanner/domain differences |
| BMC | Appropriate DXA | Import/report extraction; CT bone analysis is a different construct | Gap for home equivalent | Impedance/camera “bone mass” is not measured mineral |
| Diagnostic hip/spine aBMD | Dedicated clinical DXA | Preserve clinical results; Ogo for properly calibrated CT research | Clinical modality; open CT research | Site-specific validation, calibration, reference norms, clinical interpretation |
| Bone volumetric density/geometry | QCT/pQCT | Ogo, segmentation/FEA toolchains | Established modality + research implementation | Ionizing acquisition, protocol/phantom dependence; not home screening |
| Ultrasound bone-risk alternatives | Validated heel QUS / REMS equipment | No complete unrestricted substitute verified | Commercial clinical/research routes | Generic ultrasound images or RF access alone do not recreate a validated model |
| TBS, VFA, fracture adjuncts | Appropriate spine DXA/lateral imaging | Research analysis possible; no validated open equivalent established here | Gap for interchangeable clinical output | Proprietary models, acquisition and interpretation; not supplied by a scale |
| Longitudinal change | Local precision + suitable repeated reference | Open QC/LSC/trend software | Established statistics | Need actual repeated acquisitions; cross-sectional correlation insufficient |
| Images/raw ownership | Scanner archive + export | DICOM/NIfTI tools; PDF/CSV ingestion | Technically feasible, access variable | DICOM/PDF export may not contain dual-energy detector data or analysis archive |
| Cardiac/nerve/metabolic scores | Separate reference instruments | Earlier hardware dossier | Outside DXA | Do not infer them from composition images or generated DXA previews |

Sources and implementation limits for the open routes are detailed below. **There is no green checkmark here that means a project was tested on people by us.**

---

## 4. Reusable projects: what is actually available

### 4.1 Pseudo-DXA — important research, incomplete open reproduction

**Input:** registered 3D body surface mesh. **Output:** generated DXA-like channels and previews. **Inspected licence:** GPL-3.0.

The paper reports RMSE of **5.32 kg for total fat mass, 6.56 kg for fat-free mass, and 4.15 kg for total mass**. These are different targets; do not compare kilograms with body-fat percentage points. The authors explicitly say the work is not meant to demonstrate a replacement for DXA body composition. [7](https://www.nature.com/articles/s43856-024-00434-w)

The current source documents four substantial reuse barriers:

1. Meshes must be fitted/standardized to a T-pose with 110K points using the Meshcapade API; the example samples 22,061 points.
2. Working trained weights and a fitted test mesh are available **on request**, not verified as a public one-click asset download.
3. Conversion of predicted NPY arrays into proprietary DXA files **cannot be made public**; the lab offers to perform it.
4. Quantitative analysis then uses DXA body-composition software. Training data also include controlled/request-based cohorts.

**Our execution:** 3 lightweight tests passed; 1 TensorFlow-dependent module skipped because TensorFlow was absent. No weights, mesh registration, inference or quantitative composition reproduction was attempted. [8](https://github.com/LambertLeong/Pseudo-DXA)

**Verdict:** retain as a collaboration/research lead, not the foundation of an independent home bone-density product. A generated bone-looking image predicts learned relationships; it is not a measurement of the person's internal mineral distribution.

### 4.2 `rishabcv-eng/bodycomp` — reusable local inference, overstated headline validation

**Inspected licence:** MIT. Useful pieces include a local browser interface, silhouette features, boosted-tree regressors, uncertainty/calibration machinery, and a JavaScript inference implementation. Its headline is approximately **2.84 percentage points MAE** in the photo-available feature setting under simulated favorable conditions; the stored full-feature scenario is approximately **2.82**. Neither is a newly verified phone/DXA trial. [9](https://github.com/rishabcv-eng/bodycomp)

The key source is `src/end_to_end.py`: BodyM supplies silhouette-to-anthropometry information, while NHANES supplies anthropometry-to-DXA labels. The end-to-end calculation perturbs NHANES measures with independent Gaussian errors estimated from the other cohort. It does not capture every error introduced by camera pose, segmentation, clothing, correlated feature errors or population shift.

Its published calibration JSON reports roughly **80.5% coverage with an interval width around 8.79 percentage points** for body fat. That is model/repository evidence, not an independently reproduced live-camera coverage claim. The code's `muscle_pct` target is derived from appendicular lean mass divided by body weight: **do not relabel it as measured total skeletal-muscle percentage**.

**Our execution:** `node parity_test.mjs` compared 440 supplied test predictions across 11 models; maximum difference was exactly 0. This proves the JS tree walker agrees with the supplied reference vectors. No camera test, retraining, cohort reanalysis or external physiological validation was performed.

**Verdict:** good engineering donor for local model execution and transparent data handling. Establish a real paired acquisition study before claiming clinical or DXA-equivalent accuracy. Audit third-party segmentation/pose weights and dataset rights separately from the MIT application licence.

### 4.3 FatSegNet — genuine internal fat segmentation, if you already have Dixon MRI

**Inspected licence:** Apache-2.0. It processes fat/water Dixon MRI and segments abdominal adipose compartments, producing segmentation masks, QC views and quantitative summaries. This is analysis of internal imaging, not prediction of invisible anatomy from a selfie. [10](https://github.com/Deep-MI/FatSegNet)

Reproducibility caveats are concrete: the inspected CPU container uses TensorFlow **1.6.0**, Keras **2.2.4**, NumPy **1.15.4**, and other old pinned dependencies. Its README says the included example fat/water files are **empty illustrative placeholders**, not a real validation dataset. The inspected last commit is April 2022.

**Verdict:** strong scientific/algorithmic reuse lead, but budget for environment restoration or a carefully validated port, compatible MRI acquisition, weight provenance and independent segmentation review. No container build or inference was performed here. Open analysis does not make MRI acquisition open or cheap.

### 4.4 Comp2Comp — broad CT composition toolchain

**Current inspected root licence:** **Apache-2.0**. The repository supports CT-based workflows for muscle/adipose measurements and bone analysis; input is actual CT DICOM data. Cite the current licence rather than blindly repeating the GPL label in an older publication. [11](https://github.com/StanfordMIMI/Comp2Comp)

Regulatory caution: its README includes an “FDA Approved BunkerHill…” BMD heading, while an example explicitly labels predicted Z/T scores **“NOT FDA cleared.”** This investigation did not independently establish the clearance/version/intended-use boundary of each component. **Do not describe the whole GitHub project or all its outputs as FDA approved.** Dependencies and downloaded models also need their own rights audit.

**Verdict:** a practical first CT-analysis candidate if clinically acquired scans already exist. Not a reason to acquire repeated CT solely for hobby composition tracking. No inference/build performed.

### 4.5 TotalSegmentator and BodyComposition — inspect the particular model, not just the wrapper

TotalSegmentator's core and several tasks are Apache-2.0, but **`tissue_types`, `tissue_types_mr`, `tissue_4_types` and certain other tasks require separate licensing**; free non-commercial access is not unrestricted open-source reuse. Its body-statistics prediction command also has a separate licence requirement. [12](https://github.com/wasserth/TotalSegmentator)

An important version correction: the **current** `fohofmann/BodyComposition` README is **1.0.0rc1**, not the older v0.2 lead. Its model documentation explicitly says it **does not use TotalSegmentator's separately licensed `tissue_types` or `vertebrae_body` tasks**. It describes a default compartment model with CC-BY-4.0 weights, optional alternatives, pinned upstream asset hashes, model verification separate from inference, and CSV/Parquet/NIfTI/JSON outputs. Some optional vertebral models have CC-BY-SA-4.0 weights. This improves its reuse prospects; it is not a complete audit of every upstream dependency or a reproduced inference result. [13](https://github.com/fohofmann/BodyComposition) [14](https://github.com/fohofmann/BodyComposition/blob/main/docs/models.md)

I retained the current README/model documentation at commit `638d8e28dcb80aba25233569a1c4786b51221ea4` as additional web evidence. This project was **not** one of the seven locally cloned/tested repositories.

**Verdict:** shortlist current BodyComposition alongside Comp2Comp for a controlled bake-off on existing CT, with independent masks and measurement agreement—not simply screenshot quality—as acceptance criteria.

### 4.6 DeepACSA and DL_Track_US — local muscle measurements, not whole-body DXA

**DeepACSA inspected code:** Apache-2.0. It analyzes anatomical cross-sectional area in muscle ultrasound, with newer tendon/muscle models and acquisition-specific training contexts. The repository references models, training/example data and executables; the March 2026 v0.3.2 software record has Apache-2.0 metadata. The separate older executable/example/models archive has **CC-BY-4.0** metadata. Individual newer assets still need checking at their actual source. [15](https://github.com/PaulRitsche/DeepACSA) [16](https://zenodo.org/records/19130694) [17](https://zenodo.org/records/7568384)

The README itself notes v0.3.2 was not yet available as a Python package and gives clone/environment instructions. No environment installation, model download or ultrasound inference was performed here.

**DL_Track_US:** complementary open analysis for longitudinal ultrasound architecture such as fascicle length and pennation/thickness-related analysis; web-reviewed lead, not locally tested in this pass. [18](https://github.com/PaulRitsche/DL_Track_US)

**UMUD:** useful discovery infrastructure, but its current repository README still warns it is beta and **“No real datasets are integrated yet.”** Do not assume a paper/catalogue announcement means a ready integrated training corpus. Dataset licences are individual. [19](https://github.com/PaulRitsche/UMUD)

**Verdict:** perhaps the best way to add a genuinely different local tissue observation to the scale/shape/BIS stack. Acquisition landmarks, orientation, probe pressure, muscle state and pixel calibration matter at least as much as segmentation. A local cross-sectional area cannot be turned into whole-body muscle kilograms without a separately validated model.

### 4.7 Ogo — open CT bone calibration and analysis

**Inspected licence:** GPL-3.0. Ogo includes CT calibration, segmentation, quantitative bone tools and finite-element-related workflows. This is relevant to genuine bone research, not a home replacement for diagnostic DXA. [20](https://github.com/Bonelab/Ogo)

The standard calibration source explicitly fits density against HU and warns that output units depend on the phantom; the user must know the units. Internal/phantom calibration, contrast, reconstruction, scanner stability and segmentation all need control. A pretty bone mask is not sufficient for valid BMD.

**Our bounded test:** `pytest tests/calib` produced **1 passed, 4 skipped, 4 warnings**. The four skips are **placeholder tests**, not proof of passing calibration validation. This is an important coverage gap in the selected directory; it does not characterize the entire Ogo test suite. No CT calibration, segmentation or finite-element solve was performed.

**Verdict:** retain for bone-specific CT work with qualified collaborators and appropriate existing images. Do not translate every CT HU value directly into a DXA T-score.

### 4.8 `dxa-extractor` — a useful ownership layer, with reproduced parser hazards

**Inspected licence:** MIT. It extracts fields from Hologic PDF reports to CSV, with advertised support for approximately 96 fields. The author reports testing on Horizon W / software 13.6.x; other layouts need validation. **It extracts a report, not raw detector data or a fresh tissue segmentation.** [21](https://github.com/FSUcaplab/dxa-extractor)

I exercised selected parser functions using synthetic text, without launching the GUI or processing patient PDFs:

| Synthetic case | Observed result |
|---|---|
| `L Arm 1000.0 4000.0 5000.0 20.0` | Parsed as expected |
| `L Arm 10000.0 40000.0 50000.0 20.0` | Cleanup changed the three masses to **100.0, 400.0 and 500.0** |
| `L Arm 1,000.0 4,000.0 5,000.0 20.0` | Returned no regional fields |

Reason: a run of four identical characters triggers global doubled-character cleanup; legitimate repeated digits can be collapsed. The regional regex also does not support thousands separators. These are **synthetic robustness findings**, not an estimate of the failure rate on real Hologic PDFs.

**Verdict:** reuse after adding template-specific extraction, numeric normalization, mandatory-field checks, mass/unit consistency tests, explicit review flags and real deidentified PDF regression fixtures. Never silently accept a partial or implausible parse.

### 4.9 General infrastructure

**3D Slicer** is a useful BSD-style, commercially reusable platform for image viewing, manual segmentation and QC; it explicitly is not FDA approved as the general research application. [1](https://www.slicer.org/commercial-use.html)

**MeshLab** is GPL-3.0 mesh-processing infrastructure, not a body-composition model. It can help with surface cleanup/inspection, but does not solve camera calibration, anatomical correspondence or internal composition estimation. [1](https://www.meshlab.net/)

Open MRI console efforts such as **MaRCoS** are real, but a console is not a complete safe human scanner, and neither its console price nor its openness establishes validated whole-body Dixon composition acquisition. This is a specialist research track, not our sensible first build. [1](https://github.com/marcos-mri) [3](https://arxiv.org/abs/2208.01616)

---

## 5. Datasets: genuinely paired information versus a synthetic bridge

### 5.1 NHANES whole-body DXA + anthropometry

Public NHANES releases provide processed DXA measurements and related anthropometry keyed by participant ID. The 2017–2018 whole-body examination targets ages **8–59**; other cycles have different eligibility. Android/gynoid/VAT, femur and spine components can be separate files. **A public numeric XPT file is not evidence that raw scan images or detector data are publicly downloadable.** [3](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DXX_J.htm)

For modeling, preserve:

- Cycle, scanner/analysis details and units.
- Examination status and region-specific validity flags.
- Total/subtotal/head-included definitions and lean-with/without-BMC distinctions.
- Demographics, eligibility, missingness and survey design variables when making population claims.
- Participant-level splits; do not place the same person or their imputed copies in train and test.

### 5.2 The important impedance bridge: downloaded, inspected, retained

The 1999–2000 BIX documentation describes Xitron Hydra 4200 whole-body hand/foot measurements, **50 frequencies from 5 kHz to 1 MHz**, with DXA conducted first, followed by BIA. It includes raw R/X spectra as well as fitted/model-derived outputs, quality codes and important exclusions. The BIA sample was ages **8–49**, so it is not representative of older adults by default. Fasting was not uniform. [1](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/BIX.htm)

Actual local file inspection:

| Item | Observed count |
|---|---:|
| BIX rows / unique IDs | 5,311 / 5,311 |
| DXX rows | 31,175 |
| DXX unique IDs | 6,235 |
| Shared unique BIX–DXX IDs | **4,079** |
| Resistance/reactance columns | **50 / 50** |
| BIX rows with both 50-kHz R and X nonmissing | 4,269 |

The final count is **across BIX**, not the valid paired DXA subgroup. Shared IDs do not prove complete measured labels or acceptable impedance quality.

The DXA file contains **five imputation records per person**. CDC says to analyze the five completed datasets appropriately and combine results, not treat them as independent people, select a convenient imputation, or average them into assumed truth. For a measured-label machine-learning benchmark, define a separate measured/valid cohort and explicitly acknowledge selection bias; do not claim it represents the US population just because the underlying survey does. [4](https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx)

**Why this matters:** we can investigate whether raw frequency features improve on age/sex/height/weight/waist before building custom electronics. But models trained on supine Hydra electrode geometry will not automatically transfer to standing dry-electrode scales, segmental arrays or electrical impedance myography.

**Not done:** no validity-filtered adult cohort, model fitting, survey-weighted statistics or predictive performance estimate was produced. Gzipped original XPT files, SHA-256 values, column inventory, inspection script and aggregate counts are retained locally.

### 5.3 BodyM is not a DXA dataset

The AWS registry describes **8,978 silhouettes from 2,505 subjects**, with height, weight, sex and 14 measurements. It lists no DXA labels. It is useful for geometry/anthropometry, not direct internal-compartment supervision. The registry's licence text says Attribution–NonCommercial 4.0 while its hyperlink points to CC-BY-4.0: **commercial rights are unresolved until the actual terms are clarified**. [22](https://registry.opendata.aws/bodym/)

Combining a BodyM model and an NHANES model can be a legitimate engineering experiment. It does not create a participant-matched photo/DXA dataset.

### 5.4 Paired optical/DXA research does exist—but access is not automatically open

- **Shape Up!** supplied same-day paired 3D optical/DXA data for Pseudo-DXA. The paper directs researchers to requests/data-sharing routes. Health ABC and BMDCS have their own access conditions. [7](https://www.nature.com/articles/s43856-024-00434-w)
- **Fenland / 2024 3D-shape work:** the main model fits meshes to DXA silhouettes plus anthropometry, but importantly the paper also includes a **separate 119-person smartphone validation study with DXA and BODPOD**. It would be wrong to dismiss the entire paper as having no smartphone validation. Its data are available by request, not established here as unrestricted public downloads; its complete deployable model/weight rights were not audited. [23](https://www.nature.com/articles/s41746-024-01289-0)
- Newer optical/body-model publications remain useful follow-up leads, but publication, downloadable code, downloadable weights and reusable paired data are four different questions. No claim that “no public paired dataset exists anywhere” is warranted by this search.

**Best next data action:** prepare one concrete access request with required modalities, raw/export formats, licences, demographic coverage and longitudinal repeat measurements. Separately finish a careful NHANES BIS benchmark. Do not wait for a photorealistic synthetic-DXA model to start useful work.

---

## 6. Acquisition hardware and the subscription/market comparison

The earlier [separate hardware dossier](./BodyScan-2-Separate-Hardware-Search.md) remains the detailed commercial/development/open-hardware inventory. This section adds the acquisition distinctions relevant to DXA-like information.

| Route | What it actually acquires | Open/reuse position | Cost/subscription issue |
|---|---|---|---|
| Clinic whole-body DXA | Projection attenuation and derived composition | Request reports, regional values, images and archive/export details | Pay-per-scan may avoid consumer subscriptions; composition/VAT and diagnostic bone services may be separate |
| Hologic Horizon / GE Lunar iDXA | Clinical DXA platform; available features depend on package | Proprietary acquisition/analysis; DICOM capability does not establish access to raw dual-energy channels | Capital/service/software options; obtain a written scope and export sample |
| MRI + open analysis | Internal 3D anatomy; suitable sequences can distinguish fat/water compartments | Strongest non-ionizing internal-imaging route; acquisition remains a clinical/research service | Scan/protocol and expert QC costs; no verified inexpensive home equivalent |
| Existing clinically acquired CT + open analysis | Internal anatomy and CT attenuation | Useful opportunistic composition/bone research | Do not add routine CT exposure merely to feed an open app |
| Research ultrasound + open local analysis | Actual local tissue interfaces/images; RF access on suitable systems | More directly informative locally than a camera; generally closed acquisition hardware | Probe/software/API/export rights can be separately charged |
| Commercial A-mode body-composition ultrasound | Local thickness with equation-derived whole-body outputs | Not a whole-body DXA image or bone-density system | Current subscriptions and legacy hardware rights differ |
| Commercial optical scanner | External shape; composition predicted by models | Some provide mesh/CSV exports; not internal imaging | Business SaaS, API tiers, credits and cancellation risk |
| Open weight + tape/shape + BIS | Mass, geometry and electrical response | Best match for a modular local-first build | Lowest lock-in if raw export/model execution remain local; validation is the major hidden cost |

### Concrete procurement findings

**Styku:** current first-party business documentation lists **$199/month Access**, **$499/month Elite list**, and **$349/month introductory Elite**. Access includes CSV and OBJ export; API tiers differ by plan, and Health Screen uses separate credits. Hardware is also required. That is materially more informative than repeating competitors' old “$150–800/month” estimates. Access alone is **$2,388/year or $11,940 over five years**, before hardware, tax, price changes or extra credits. This is a business comparison, not a personal-use recommendation. [12](https://help.styku.com/what-are-styku-s-business-pricing-plans/)

**BodyMetrix:** the current North American FAQ says an active subscription is required to operate the BX2K and device/platform are not sold separately. That defeats a simple “buy the older ultrasound wand and escape SaaS” assumption. The public site/legacy seller prices are inconsistent enough that I am **not** treating an indexed hardware price as a verified complete quote. [9](https://bodymetrix.com/pages/faqs)

Its present marketing also says “FDA Class I cleared” and “unaffected” by multiple preparation factors. The FDA document I actually inspected for **legacy BX2000, K082147**, identifies **Class II** and a scope of local fat/muscle thickness and **estimated** total body fat with BodyView; it is not for diagnosis of disease/condition. These are different names/generations and potentially different claims: request the exact current authorization/label, rather than assuming either that marketing is correct or that one old clearance automatically resolves the present product. [24](https://www.accessdata.fda.gov/cdrh_docs/pdf8/K082147.pdf)

**Clarius research:** current material advertises RF/IQ/image access and research APIs, but scope is configuration-specific. The Cast repository says the Clarius app must be running and connected, a licensed probe is needed, and API/app versions must match; raw capture/streaming has mode-specific limitations. Older and newer product pages describe different levels of RF access. Ask for the exact probe, firmware, beamformed versus channel RF, export route, licence duration and behavior after cancellation. Public BSD-licensed example code does **not** make the scanner/SDK service independent of vendor authorization. [1](https://clarius.com/specialties/research/) [25](https://github.com/clariusdev/cast)

### Bone-specific non-X-ray options

Validated **heel QUS** can contribute to fracture-risk assessment, but ISCD says it cannot monitor skeletal effects of osteoporosis treatment. Its outputs and thresholds are not interchangeable with central DXA T-scores. **REMS** is another non-ionizing commercial route; IOF describes proprietary reference spectral models. A generic ultrasound probe plus open RF reader is not an open reimplementation of that reference database and clinical algorithm. No fully open turnkey equivalent was verified here. [1](https://iscd.org/official-positions-2023/) [4](https://www.osteoporosis.foundation/health-professionals/diagnosis/other-diagnostic-tools)

### Why subscriptions keep appearing

Some recurring costs are real: hosting, support, model maintenance, training, regulatory work, integration and human review. But the commercial incentive also includes predictable revenue, tiered analytics, financed hardware, retention and making historical data/workflows expensive to leave. That is an economic interpretation, not a claim about an individual company's private motives.

The key distinction is **optional service versus a remotely revocable measurement instrument**. Before buying, require answers to:

1. Can it acquire and export new measurements offline after cancellation?
2. Can old records, images, meshes and metadata be exported in bulk without another fee?
3. Are raw physical measurements available, or only model scores/PDFs?
4. Are the algorithm, weights and conversion steps independently runnable?
5. What happens if the vendor shuts down, changes terms or stops supporting the OS?
6. Are API, RF, DICOM, analysis modules and research rights perpetual, annual or per-scan?

We should design our own system so local acquisition, history, raw export and ordinary analysis do not depend on a subscription. Paid support or optional hosted collaboration need not revoke access to one's instrument or data.

---

## 7. Longitudinal precision: the feature to build before more scores

A device can rank people well while measuring one person's change poorly. Correlation does not establish agreement, and a smooth app graph does not establish tissue change.

ISCD calls for local precision assessment for relevant composition measures. Its minimum acceptable individual-technologist precision figures are **3% total fat mass, 2% total lean mass and 2% percent fat mass**. These are precision criteria, **not promised absolute accuracy, not universally achievable thresholds for every regional metric, and not automatically percentage-point errors**. [1](https://iscd.org/official-positions-2023/)

For independent repeated measurements under standard assumptions, the familiar 95% least-significant-change calculation is:

**LSC ≈ 2.77 × precision error**

The units follow the precision estimate. If precision SD is 0.40 kg, the corresponding illustrative LSC is about 1.11 kg. If a relative CV is used, the LSC is relative too. Do not put “2%” in a dashboard without saying whether it is percent relative, percentage points, CV or an absolute error. This example is arithmetic, not a performance claim for a particular scanner. [2](https://iscd.org/resources/precision-assessment-calculator-faqs/)

### Required validation, not optional polish

- Same-session repeats **with repositioning** and repeat electrode/probe placement.
- Between-day repeats with time, hydration/food/exercise, posture and environmental conditions logged.
- Phantom/calibration and drift records for the physical instrument.
- Bias, RMSE/MAE, limits of agreement, proportional bias, subgroup performance and uncertainty coverage.
- Tests on **changes**, not only cross-sectional values.
- External device/site/population validation; subject-level splitting and frozen test sets.
- Comparison against simple baselines: weight/height/age/sex, waist, and previous value. Demonstrate that impedance, ultrasound or camera data add information.
- Versioned models and reference definitions; do not conceal a model update as biological progress.

A single personal baseline can be useful context but is not a validation study. Biological adaptation, edema, glycogen changes or aging may alter the relation between a proxy and its reference.

---

## 8. Ranked reuse roadmap

This is a recommended sequence, not an already completed build or a clinical recommendation.

### Rank 1 — Build the local evidence/data layer

**Reuse:** hardened `dxa-extractor`, CSV import, direct entry with source attachments, ordinary DICOM/NIfTI tooling and existing scale integrations.

**Deliverable:** a portable local record with original reports, extracted numbers, units, scanner/software, region definitions, quality/review flags and acquisition conditions. Export JSON/CSV plus original attachments. Separate observed signals, model predictions and clinical interpretations.

**Gate:** deidentified real-report fixtures; every required field either validated or explicitly missing; no silent digit repair; automated unit/mass/region checks plus human review. Start with your own data only if you actually obtain suitable reports; no Withings account is assumed.

### Rank 2 — Benchmark information gain before designing custom electronics

**Reuse:** NHANES BIX + DXX + demographics/body measures; transparent baseline regressors and Cole-spectrum features.

**Deliverable:** a reproducible, validity-aware benchmark showing whether raw impedance improves total fat/lean or limb-lean prediction beyond anthropometry, with participant-level test splits and uncertainty.

**Gate:** correct handling of five imputations and survey/selection issues; honest age/geometry limitations; no claiming phone validation from separate datasets. Try additional compatible NHANES cycles only after codebook alignment.

### Rank 3 — Add low-burden direct geometry

**Reuse:** weight, standardized tape measurements, then local camera/depth capture and mesh tools; reuse `bodycomp` inference/UI patterns without inheriting its headline accuracy claim.

**Deliverable:** repeatable mass/circumference/shape tracking with local image storage or explicit opt-in deletion policies. A tape baseline is useful even if the eventual interface is camera-based.

**Gate:** demonstrate repeatability and external geometry accuracy before reporting tissue composition. Store camera calibration, scale reference, clothing/pose and rejection reasons. Do not buy a specialized SaaS scanner solely to obtain opaque body-fat or bone predictions.

### Rank 4 — Add raw impedance as an engineering module

**Reuse:** the MAX30009/BioGAP and other measurement leads in the hardware dossier, where appropriate; open spectrum logging and phantom tests.

**Deliverable:** frequency-specific calibrated R/X with contact/quality metadata—not just vendor-derived fat percentages.

**Gate:** electrical safety review and bench/phantom performance before any human connection; geometry-specific paired reference testing afterward. Do not equate EIM, whole-body BIS, segmental BIA and EIT; each needs its own protocol and target. A respiration BioZ example is not automatically validated cardiac ICG or composition analysis.

### Rank 5 — Add targeted ultrasound if local muscle/fat change is important

**Reuse:** suitable commercial research/export-capable ultrasound and DeepACSA/DL_Track_US; open hardware from the earlier dossier remains a development path, not a validated finished acquisition system.

**Deliverable:** bilateral local thickness/ACSA/architecture with saved images and acquisition landmarks.

**Gate:** trained acquisition, pixel calibration, repeated-site localization, pressure/angle control, expert comparison and change precision. Validate on the chosen probe and population; do not extrapolate one thigh measurement into a universal muscle-preservation score.

### Rank 6 — Use open internal-image analysis opportunistically

**Reuse:** Comp2Comp/current BodyComposition for existing CT; FatSegNet or a validated maintained alternative for suitable MRI.

**Deliverable:** anatomical masks, defined VAT/SAT/muscle measures, QC and reproducible exports.

**Gate:** actual compatible images, model/dependency rights, independently annotated test cases and acquisition-aware validation. Do not obtain unnecessary CT scans just because the analysis is free. MRI can be an external reference service without owning a scanner.

### Separate bone track — retain clinical assessment, research alternatives cautiously

**Reuse:** appropriate clinical DXA results; Ogo for calibrated CT research; evaluate commercial REMS/QUS only within validated scope.

**Deliverable:** correctly sourced BMD/BMC/risk information separate from home wellness predictions.

**Gate:** correct skeletal site, validated acquisition/calibration/reference population and qualified interpretation. Do not release an osteoporosis diagnosis, DXA-equivalent T-score, or reassuring “bone score” from unvalidated home signals.

### Defer — complete Pseudo-DXA reproduction / open MRI acquisition

Only move these ahead if asset access, preprocessing, licences, model rights and quantitative validation can be resolved with a collaborating lab. They are much larger projects than a modular home tracker, and neither is necessary to start collecting useful open measurements.

---

## 9. Evidence retained and exact execution status

Everything for this pass is under **`/home/user/dexa-investigation/`**.

### Locally inspected repository pins

| Project | Exact commit | Root licence inspected | Last commit at inspected pin |
|---|---|---|---|
| Pseudo-DXA | `196630285aaa3637b4990e0b5ff2d445c10c3544` | GPL-3.0 | 2026-07-09 |
| Comp2Comp | `fa617e2d0d2d02f59c7d8322e4ffc5375213eb7b` | Apache-2.0 | 2026-01-06 |
| DeepACSA | `781cc471aa7197bc8cb32e8d36cfd41493781a12` | Apache-2.0 | 2026-03-31 |
| FatSegNet | `720d36b0cffcc1be42417a538153fde99b2ad4f2` | Apache-2.0 | 2022-04-07 |
| Ogo | `d5bec374608812b1c08a0d0da9cab3ea33cf720e` | GPL-3.0 | 2026-10-14 |
| bodycomp | `00474935fa562b06909cd6d51f1f5d256514788b` | MIT | 2026-10-08 |
| dxa-extractor | `b90af0e48078ed1e1a65ea114b301d0a7295cf2e` | MIT | 2026-08-11 |

Commit dates are evidence of activity, not a maintenance guarantee. Root licences do not automatically cover weights, datasets, dependencies, SDKs or proprietary conversions. GPL permits commercial use but introduces applicable redistribution/source obligations; it is not the same as a non-commercial-only licence.

### Retained artifacts

- `source-manifest.json`: repository URLs, pins, dates and an exact list of pruned files.
- Selected source/licence/configuration subsets in the seven project directories. Git history, large binaries and image/PDF assets were removed to preserve the workspace; **these are evidence subsets, not complete build packages**. Re-fetch the pinned repositories for a full build or to repeat tests requiring omitted assets.
- `pseudo-dxa-tests.txt`: **3 passed, 1 skipped**; no TensorFlow inference.
- `ogo-calibration-tests.txt`: **1 passed, 4 placeholder skips**, 4 warnings.
- `bodycomp-parity-tests.txt`: **440 comparisons, zero disagreement** with supplied reference predictions; not a fresh Python-training run.
- `dxa-extractor-synthetic-checks.json`: the three synthetic parser cases, inputs, cleaned text and parsed outputs.
- `inspect_nhanes_bridge.py`, `nhanes-bridge-inspection.json` and its log: repeatable transport-file inspection and aggregate counts.
- `data/BIX.xpt.gz` and `data/DXX.xpt.gz`: compressed original CDC files; hashes in the inspection JSON refer to decompressed original XPT bytes.
- `web-evidence/`: saved primary-page text, pinned current BodyComposition documents, Zenodo licence metadata and an URL/hash manifest. `preserve_web_evidence.py` records the retrieval method.

### Limit of this investigation

This is a broad, source-audited search, **not proof that every relevant project in the world has been found**. Commercial equipment was not purchased; clinical sites were not contacted; no private dataset request was submitted; no model inference on MRI/CT/DXA/ultrasound was reproduced; no hardware or human testing occurred. The bounded tests above should not be added into a misleading “hundreds of medical validation tests passed” headline.

### Related saved dossiers

- [Separate hardware search](./BodyScan-2-Separate-Hardware-Search.md)
- [Pass 4: compatibility and subscription audit](./BodyScan-2-Pass-4-Compatibility-and-Subscription-Audit.md)
- [Pass 5: no-Withings-account shortlist](./BodyScan-2-Pass-5-No-Withings-Account-Shortlist.md)
- [Earlier biomarkers/DXA deep dive—technical comparison superseded here](./BodyScan-2-Biomarkers-DEXA-Deep-Dive.md)

## Bottom line

**Reuse the existing pieces, but build around measurement provenance and validation—not around the appearance of a DXA report.** Start with portable reference records and the real NHANES impedance/DXA bridge; add direct geometry and calibrated raw impedance; add ultrasound for local tissue questions. Use clinical imaging where it provides information the home sensors cannot. Keep bone diagnosis separate. That is a credible open alternative to a subscription-first wellness platform, without claiming to have built a home DXA scanner.
