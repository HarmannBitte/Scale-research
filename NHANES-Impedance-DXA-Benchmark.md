# Does raw impedance add information beyond body measurements?
## First executed NHANES–DXA benchmark

> **Follow-up completed:** see [Fresh-Cycle Validation and Sensitivity Checks](./NHANES-Impedance-DXA-Fresh-Cycle-Validation.md). The main impedance gain replicated in 2003–2004. That pass also found and independently checked inconsistent target copies in the fresh file, documented an eligibility amendment, and clarified that the 50-kHz predictor arms were evaluated within a full-spectrum-quality-screened cohort. The original results below remain unchanged.

**Completed 17 October 2026 · exploratory research, not a medical device evaluation**

### Answer

**Yes, in this selected historical dataset, adding 50-kHz impedance improved prediction beyond age, sex, height, weight, BMI and waist. But full-spectrum impedance did not deliver a consistent, practically large further gain.** Individual errors remain substantial, and these results do not establish home-device accuracy, muscle-change tracking, or bone-density measurement.

This moves our project beyond a literature search: the benchmark, participant-level predictions, input files, protocol and integrity tests are saved and reproducible.

## 1. What was actually run

The primary experiment trained on **1,802 adults from NHANES 1999–2000**, then tested on **2,066 different adults from NHANES 2001–2002**. A secondary fixed 70/30 split within 1999–2000 used **1,261 training and 541 test participants**.

The two cycles use the same general NHANES measurement ecosystem. This is **cross-cycle transfer**, not independent validation across a new instrument, clinic, population, or home protocol.

### Safeguards

- Ages **18–49**, excluding known pregnancy.
- **DXA scan complete and `DXITOT=0`: no region imputed.** I verified that measured target values agree across the five released copies before retaining one record per participant.
- BIA complete, with an **excellent or good Cole-model fit**.
- All **50 resistance and 50 reactance channels** finite, resistance positive, and required anthropometry present.
- Every feature-set comparison uses **the same participants**, rather than gaining or losing subjects when features change.
- No DXA values, participant IDs, Hydra-predicted fat/lean, fitted body-water volumes, or fitted Cole parameters entered the predictors. The Cole-fit quality code was used only for eligibility.
- Race/ethnicity was retained for subgroup auditing, **not** used as a predictor.
- A written protocol specified cohort rules, models, feature sets, outcomes, splits and bootstrap comparisons before model results were inspected.
- **No tuning against test outcomes and no selection of a preferred split.** All 128 metric rows are retained, not just a favorable result.

CDC's documentation distinguishes completely measured scans from completed scans with some imputed regions. Selecting `DXAEXSTS=1` alone would not have been sufficient. [1](https://wwwn.cdc.gov/nchs/data/nhanes/public/1999/datafiles/dxx.pdf) [2](https://wwwn.cdc.gov/nchs/data/nhanes/public/2001/datafiles/dxx_b.pdf)

### Important scope decision: unweighted, measured-only prediction

This is an **unweighted engineering benchmark on selected complete cases**, not a survey analysis. CDC recommends examination weights and appropriate multiple-imputation/survey methods for NHANES population analyses. Here I deliberately excluded imputed labels to avoid testing against statistical reconstructions, and did not claim population representativeness.

This sacrifices generalizability: valid measured cases are not a random subset. The results are **not US-population accuracy estimates**, prevalence estimates, or a substitute for a properly designed survey-weighted analysis. The bootstrap intervals below also ignore survey clustering and selection effects.

## 2. Cohort construction

| Sequential stage | 1999–2000 | 2001–2002 |
|---|---:|---:|
| Unique participants after joining DXA, BIX, demographics and body measures | 4,079 | 5,949 |
| Ages 18–49 | 2,820 | 3,299 |
| Not known pregnant | 2,540 | 2,973 |
| Complete DXA, no imputed regions | 2,047 | 2,406 |
| All target components present | 2,047 | 2,406 |
| BIA complete, excellent/good fit | 1,816 | 2,089 |
| All 100 raw channels finite; resistance positive | 1,816 | 2,089 |
| Complete positive expanded anthropometry | **1,802** | **2,066** |
| Recorded sex present | **1,802** | **2,066** |

The training cohort contains 936 participants coded male and 866 coded female; the cross-cycle test cohort contains 1,077 and 989 respectively. These are the dataset's recorded sex categories, not inferred gender identities.

The original 4,079-ID overlap therefore became **1,802 eligible adults**, not 4,079 automatically valid training examples. Negative reactance was not transformed to an absolute value; there were no negative raw reactance entries in either final cohort.

### A transport-file issue caught before filtering

Some SAS/XPT zeros decoded through pandas as about **5.4 × 10⁻⁷⁹**, including excellent-fit and non-imputed codes. A literal equality-to-zero test would have incorrectly discarded them. The loader normalizes finite absolute values below **10⁻⁵⁰** to zero and logs correction counts. Original compressed input files and hashes are preserved. This normalization is a file-decoding safeguard, not alteration of meaningful physiological values.

## 3. Predictors and fixed models

Eight feature sets were evaluated:

| Feature set | Included observations/features |
|---|---|
| Basic | Age, recorded sex, height, weight, calculated BMI |
| Waist | Basic + waist circumference + waist/height |
| Basic + 50 kHz | Basic + R, X, calculated phase angle and height²/R at 50 kHz |
| Waist + 50 kHz | Waist + the same 50-kHz features |
| Waist + spectra | Waist + all 100 raw R/X channels; height²/R and phase angle at 5, 50, 200, 500 kHz and 1 MHz |
| Expanded | Waist + arm, calf and thigh circumferences, plus arm and leg lengths |
| Expanded + 50 kHz | Expanded + the same 50-kHz features |
| Expanded + spectra | Expanded + the full-spectrum features above |

Neither skinfolds nor a camera model were included. Phase angle and height²/R are calculated from measured channels; they are not vendor fat/lean predictions.

Models were fixed in advance:

- **Ridge:** standardized features, regularization `alpha=10`.
- **Extra Trees:** 160 trees, minimum leaf size 5, all features available at a split, fixed seed `20261017`.

Both were fitted as **multi-output regressors**. For Extra Trees, split decisions are shared across targets and influenced by target variances; this was not a separately optimized model for each endpoint. No claim of optimal algorithm performance or optimal frequency selection is made.

## 4. Primary cross-cycle results

**Mean absolute error; lower is better. Body-fat percentage errors are percentage points, not relative percent.** The lean columns are kilograms of DXA lean soft tissue, not directly isolated skeletal muscle.

### Ridge

| Predictors | Body fat, pp | Fat mass, kg | Lean soft tissue, kg | Appendicular lean, kg |
|---|---:|---:|---:|---:|
| Basic | 2.933 | 2.255 | 2.205 | 1.515 |
| Waist | 2.729 | 2.142 | 2.115 | 1.387 |
| Basic + 50 kHz | 2.482 | 1.781 | 1.731 | 1.311 |
| Waist + 50 kHz | **2.364** | **1.738** | **1.710** | **1.232** |
| Waist + spectra | 2.321 | 1.721 | 1.702 | 1.230 |
| Expanded | 2.723 | 2.137 | 2.100 | 1.344 |
| Expanded + 50 kHz | 2.282 | 1.705 | 1.687 | 1.190 |
| Expanded + spectra | 2.238 | 1.691 | 1.681 | 1.185 |

### Extra Trees

| Predictors | Body fat, pp | Fat mass, kg | Lean soft tissue, kg | Appendicular lean, kg |
|---|---:|---:|---:|---:|
| Basic | 2.892 | 2.195 | 2.163 | 1.546 |
| Waist | 2.524 | 1.916 | 1.926 | 1.336 |
| Basic + 50 kHz | 2.374 | 1.819 | 1.788 | 1.374 |
| Waist + 50 kHz | **2.197** | **1.696** | **1.679** | **1.258** |
| Waist + spectra | 2.182 | 1.676 | 1.759 | 1.292 |
| Expanded | 2.517 | 1.907 | 1.931 | 1.307 |
| Expanded + 50 kHz | 2.183 | 1.687 | 1.694 | 1.242 |
| Expanded + spectra | 2.163 | 1.659 | 1.764 | 1.280 |

Bold marks the common **waist + 50-kHz comparison**, not a selected winning model. Full precision, RMSE, bias and residual distributions are in [metrics.csv](./dexa-benchmark/results/metrics.csv).

### How much did impedance add?

Positive improvement means lower test MAE after adding the features. Intervals are percentile intervals from **2,000 paired participant-bootstrap resamples**, conditional on the already fitted models and selected test cohort.

| Comparison / endpoint | Ridge improvement [conditional 95% interval] | Extra Trees improvement [conditional 95% interval] |
|---|---:|---:|
| Waist → waist + 50 kHz: body fat | **0.365 pp [0.289, 0.436]** | **0.328 pp [0.274, 0.379]** |
| Waist → waist + 50 kHz: appendicular lean | **0.155 kg [0.115, 0.195]** | **0.078 kg [0.051, 0.106]** |
| Waist + 50 kHz → waist + spectra: body fat | 0.043 pp [0.027, 0.059] | 0.015 pp [−0.010, 0.039] |
| Waist + 50 kHz → waist + spectra: appendicular lean | 0.002 kg [−0.007, 0.011] | **−0.034 kg [−0.048, −0.020]** |

For body-fat percentage, adding 50-kHz features reduced MAE by about **13% relative to the waist baseline** in both model families. That is a real information-gain result within this benchmark, not a 13-percentage-point improvement or a claim of diagnostic equivalence.

The full spectrum made only a small further improvement for Ridge body fat and did not show a clear improvement for Extra Trees body fat under this conditional interval. For Extra Trees, it **worsened** both lean endpoints. Expanded anthropometry comparisons show the same broad pattern: adding 50 kHz helps, while the further spectrum benefit is small or model-dependent.

**Do not overinterpret the intervals.** They ignore training-sample variability, survey clustering, non-random eligibility and instrument-transfer uncertainty. They are not adjusted for the many comparisons and do not establish clinical significance. Correlated frequency channels plus a fixed model can obscure useful information; these results do not prove that every additional frequency is physiologically useless.

## 5. Average error is not an individual accuracy guarantee

For **waist + 50 kHz**, the primary test results were:

| Model / target | MAE | RMSE | Mean bias | Conventional limits of agreement |
|---|---:|---:|---:|---:|
| Ridge: body fat | 2.364 pp | 2.979 pp | +0.184 pp | **−5.645 to +6.013 pp** |
| Extra Trees: body fat | 2.197 pp | 2.767 pp | +0.230 pp | **−5.175 to +5.635 pp** |
| Ridge: fat mass | 1.738 kg | 2.196 kg | +0.203 kg | −4.083 to +4.489 kg |
| Extra Trees: fat mass | 1.696 kg | 2.205 kg | +0.255 kg | −4.039 to +4.548 kg |
| Ridge: lean soft tissue | 1.710 kg | 2.164 kg | +0.004 kg | −4.238 to +4.247 kg |
| Extra Trees: lean soft tissue | 1.679 kg | 2.178 kg | −0.032 kg | −4.301 to +4.236 kg |
| Ridge: appendicular lean | 1.232 kg | 1.579 kg | +0.100 kg | −2.988 to +3.189 kg |
| Extra Trees: appendicular lean | 1.258 kg | 1.622 kg | +0.103 kg | −3.069 to +3.276 kg |

Bias is **prediction minus DXA reference**. Conventional agreement limits are bias ±1.96 residual SD. They summarize observed agreement under distributional assumptions; they are not confidence intervals or guaranteed individual prediction bounds. Empirical 2.5th/97.5th residual percentiles are separately retained in the results.

The practical warning is clear: **a roughly 2.2-pp body-fat MAE coexists with errors spanning approximately −5.2 to +5.6 pp in the conventional agreement summary.** Small mean bias does not mean small individual errors. A model should not reassure a person that a small apparent muscle change is real on this basis.

## 6. Secondary split and subgroup checks

### Within-1999 test: body-fat MAE

| Feature set | Ridge, pp | Extra Trees, pp |
|---|---:|---:|
| Waist | 2.838 | 2.609 |
| Waist + 50 kHz | 2.432 | 2.366 |
| Waist + spectra | 2.437 | 2.319 |
| Expanded | 2.842 | 2.611 |
| Expanded + 50 kHz | 2.364 | 2.334 |
| Expanded + spectra | 2.377 | 2.299 |

The basic impedance gain appeared here too. The spectrum pattern was not identical: for example, Ridge's body-fat MAE slightly worsened after adding spectra in this split. That strengthens the case against presenting one favorable spectrum result as a general hardware requirement.

### Primary subgroup audit: waist + 50 kHz body-fat prediction

| Recorded subgroup | Test n | Ridge MAE / bias, pp | Extra Trees MAE / bias, pp |
|---|---:|---:|---:|
| Male | 1,077 | 2.190 / +0.004 | 2.017 / +0.064 |
| Female | 989 | 2.553 / +0.381 | 2.393 / +0.411 |
| Ages 18–29 | 954 | 2.369 / +0.287 | 2.227 / +0.298 |
| Ages 30–39 | 514 | 2.363 / −0.045 | 2.162 / +0.121 |
| Ages 40–49 | 598 | 2.356 / +0.218 | 2.177 / +0.216 |
| BMI <25 | 907 | 2.381 / +0.576 | 2.226 / +0.284 |
| BMI 25–<30 | 702 | 2.250 / −0.726 | 2.131 / +0.262 |
| BMI ≥30 | 457 | 2.504 / +0.806 | 2.238 / +0.074 |

Race/ethnicity auditing also revealed uneven residuals. For example, participants in **RIDRETH1 code 4 (Non-Hispanic Black)** had a body-fat mean bias of approximately **+1.59 pp for Ridge and +1.35 pp for Extra Trees**, with 450 test participants. These are observed cohort/model residuals, not intrinsic biological claims or explanations of their cause. They warrant investigation before deployment; excluding race as a predictor does not automatically make a model equally calibrated across groups. Code definitions come from the NHANES demographics documentation. [3](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/DEMO.htm)

Every predefined subgroup for every feature/model/target is saved in [subgroups.csv](./dexa-benchmark/results/subgroups.csv). These are descriptive, unweighted audits, not a fairness certification or stable estimates for every intersectional subgroup.

## 7. What this changes about our build plan

### Supported by these results

1. **Raw impedance deserves a place in the research architecture.** It added predictive information beyond basic measurements and waist; the project need not depend entirely on demographic equations.
2. **A properly calibrated 50-kHz R/X baseline should be the first hurdle.** It is a stronger starting comparison than counting frequencies or adding more opaque scores.
3. **Waist remains useful.** It improves the non-impedance baseline and is a cheap direct observation; do not discard it because a device can output fat percentage.
4. **Validate incremental information before paying for complexity.** A candidate BIS system should beat the same model with only its 50-kHz inputs, under compatible reference conditions.
5. **Track subgroup bias and individual agreement, not just overall MAE or correlation.** Those can change the design and data-collection priorities.

### Not established

- That a standing dry-electrode home scale will match this accuracy. NHANES used a Hydra whole-body hand/foot protocol, with different contact geometry and conditions. [4](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/BIX.htm) [5](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2001/DataFiles/BIX_B.htm)
- That impedance detects true within-person muscle loss, or separates edema/glycogen/water change from tissue change. These are cross-sectional participants, not repeated longitudinal measurements.
- That a commercial scale with one, eight, thirteen or fifty frequencies performs like either benchmark model.
- That more frequencies are unnecessary for fluid compartments, difficult populations, contact-quality checks or other targets not tested here.
- That appendicular lean prediction validates separate left/right segments or local electrical impedance myography.
- That any non-ionizing home configuration measures bone mineral content or clinical hip/spine BMD.
- That these fixed algorithms are optimal. More careful training, alternate models, calibration and feature design could change the gains; those changes require a genuinely new held-out evaluation.

### Recommended next experiment

**Use this benchmark as the software baseline, not as a model ready for people.** Before human-connected custom hardware:

1. Specify and verify phantom R/X accuracy, repeatability, drift and contact-quality behavior at 50 kHz; add frequencies only with a clear experimental purpose.
2. Decide electrode geometry and acquisition posture; demonstrate compatibility or explicitly collect new paired data for the chosen geometry.
3. Arrange a safety-reviewed measurement system and a prospectively specified paired-reference pilot with trained acquisition and informed consent as applicable.
4. Include repeated placements and separate-day repeats, not only a single baseline scan.
5. Freeze the reference definitions, primary endpoint and evaluation plan before looking at results.

For further public-data work, a useful next analysis is a **predeclared additional-cycle test or robust survey-aware sensitivity analysis**. Existing test cycles have now been inspected: reusing them to tune a new model would make them development data, not a fresh confirmatory test.

## 8. Reproducibility and saved evidence

Project directory: **`/home/user/dexa-benchmark/`**

| File | Purpose |
|---|---|
| `PROTOCOL.md` | Pre-result cohort/features/model/evaluation specification |
| `run_benchmark.py` | Complete deterministic cohort construction, training and evaluation |
| `download-manifest.json` | Download URLs and SHA-256 hashes for newly obtained XPT files |
| `DEMO.xpt.gz`, `BMX.xpt.gz`, and corresponding four `*_B.xpt.gz` files | Compressed public CDC input files |
| `../dexa-investigation/data/BIX.xpt.gz`, `DXX.xpt.gz` | Previously retained 1999–2000 inputs; original hashes in that investigation's manifest |
| `results/cohort.json` | Sequential exclusions, target distributions, zero-decoding correction counts |
| `results/features.json` | Exact predictor list for each arm |
| `results/*_split.json` | Exact train/test participant IDs |
| `results/metrics.csv` | All **128** evaluation/model/feature/target metric rows |
| `results/paired_comparisons.csv` | All **64** prespecified paired comparisons and conditional bootstrap intervals |
| `results/predictions.csv.gz` | **166,848** participant-level prediction records across arms and evaluations; not unique people |
| `results/subgroups.csv` | Complete predefined subgroup audit |
| `results/run-metadata.json` | Library versions, random seed and script/protocol hashes |
| `test_benchmark.py`, `integrity-tests.txt` | **6 passing integrity tests** |
| `benchmark.log` | Completed training/evaluation log |
| `documentation/` | Saved original DXA codebook PDFs and selected documentation text |

The integrity tests check cohort/label eligibility, disjoint splits, predictor leakage guards, equal test participants across arms, recomputation of every metric row, and paired-improvement arithmetic/units. **They validate the computation's consistency, not a medical device or physiological measurement.**

Execution environment: Python **3.13.16**, pandas **2.2.3**, scikit-learn **1.6.1**; complete metadata also records NumPy. No external account, paid API or Withings subscription was required. Saved outputs contain public NHANES participant IDs, not identified personal records. Fitted models were not serialized or packaged as a consumer prediction app.

To rerun in a compatible Python environment with NumPy, pandas, scikit-learn and pytest installed:

```bash
cd /home/user/dexa-benchmark
python run_benchmark.py
python -m pytest -o addopts='' -ra test_benchmark.py
```

Model outcomes were not changed after inspection. The execution script's output format was changed from uncompressed to gzipped predictions for storage efficiency, followed by a deterministic rerun; the final script hash is recorded in metadata.

### Bottom line

**We now have empirical justification to investigate calibrated raw impedance, but not to promise DXA-equivalent home measurements.** In this benchmark, most of the demonstrated extra value arrived with a carefully measured 50-kHz channel; the full spectrum did not consistently justify itself for these composition endpoints. Our next investment should be measurement quality, safety and matched validation—not simply a larger frequency count.

Related: [DXA capabilities and open alternatives](./DEXA-Capabilities-and-Open-Alternatives-Investigation.md) · [Separate hardware search](./BodyScan-2-Separate-Hardware-Search.md)
