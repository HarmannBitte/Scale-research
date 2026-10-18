# Raw impedance vs DXA: fresh-cycle replication and sensitivity checks

**Completed 17 October 2026** · Follow-up to the [first executed benchmark](./NHANES-Impedance-DXA-Benchmark.md)

## Executive result

**The main finding replicated:** 50-kHz impedance improved cross-sectional body-composition prediction beyond anthropometry plus waist in a fresh NHANES cycle. The full spectrum again offered only a small additional body-fat gain and inconsistent lean-tissue gains.

- **Primary training:** the same **1,802** eligible 1999–2000 adults as before.
- **Fresh test:** **1,858** eligible adults from **2003–2004**, whose model outcomes had not previously been inspected.
- **Body-fat MAE:** adding 50-kHz features reduced error from **2.727 to 2.256 percentage points for Ridge**, and **2.549 to 2.153 pp for Extra Trees**—approximately **17.3% and 15.5% relative reductions**.
- Gains persisted in each predefined sex/BMI intersection and in the specified eligibility/weight sensitivities.
- **New input-integrity finding:** 80 participants in the downloaded DXA file had inconsistent values across their five released records despite non-imputed flags. An independent decoder confirmed the discrepancy. They were conservatively excluded; the cause is not established.

**Important qualification:** the 50-kHz models were evaluated in a cohort quality-screened using the full impedance spectrum. This supports investigating the information in 50-kHz R/X; it does **not** establish that a single-frequency instrument without equivalent quality checks will perform the same way.

This is still historical, selected-cohort prediction research—not home-device validation, longitudinal muscle-change validation, a population accuracy estimate or bone-density measurement.

---

## 1. What stayed fixed, and what changed

Before downloading/evaluating the fresh cycle, I saved a new protocol specifying:

- The same eight predictor sets, four DXA outcomes and two fixed model families.
- Ridge with standardized features and `alpha=10`.
- Extra Trees with 160 trees, minimum leaf size 5, all features available at a split and seed `20261017`.
- The same multi-output fitting approach, without test-driven tuning, frequency selection or model selection.
- A primary 1999–2000 → 2003–2004 replication, followed by four explicitly secondary checks.
- Paired participant-bootstrap intervals and descriptive subgroup auditing.

The cohort loader was extended to the third cycle. It was required to reproduce **exactly** the earlier two cycles' participant IDs, feature values, feature maps and targets before new evaluation. Those checks passed. Original scripts and results remain unchanged.

### Documented eligibility amendment—not an untouched protocol

The first attempt stopped **before model fitting** because a target-copy consistency assertion failed. I investigated the inputs, cross-checked with a second decoder, and amended eligibility to exclude inconsistent participants in all cycles. No model outcomes had been inspected at that point.

This is a **transparent post-input-inspection amendment**, not an independently preregistered study or an entirely unchanged protocol. Model settings and endpoints were not changed. The amendment has no effect on the earlier cohorts, which had zero such inconsistencies.

## 2. The input discrepancy

The DXA documentation states that `DXAEXSTS=1` and `DXITOT=0` identify complete, non-imputed measurements. The release has five records per participant. Those should not be counted as five independent people. [1](https://wwwn.cdc.gov/nchs/data/nhanes/public/2003/datafiles/dxx_c.pdf)

In the downloaded file:

| Check among complete/non-imputed flagged participants | 1999–2000 | 2001–2002 | 2003–2004 |
|---|---:|---:|---:|
| Unique participants | 4,671 | 6,425 | 5,877 |
| Participants whose target values differ across copies | **0** | **0** | **80** |

The discrepancy is not merely floating-point rounding: among the 80, maximum within-person ranges included **4.6 pp body fat**, **12.302 kg fat mass** and **9.257 kg lean soft tissue**. These maxima need not belong to the same participant.

I checked the same original transport bytes with **pyreadstat 1.3.6**, independent of the pandas XPT reader. IDs, version/status/imputation flags and target values agreed, allowing for the already documented tiny-zero decoding artifact. Both decoders identified the same 80 inconsistent participants. Their regional imputation flags were also zero in the pandas inspection.

**Action:** excluded inconsistent target copies rather than choosing the first, averaging them or asserting they were truly measured. Of the 80, **39** reached the fresh-cycle adult/nonpregnant/complete-DXA stage and were excluded there. No causal explanation, CDC error diagnosis or claim about clinical measurement failure is justified from this observation alone. The exact downloaded file hash, IDs, ranges and independent-reader receipt are saved.

### Fresh-cycle strict cohort flow

| Sequential stage | Participants |
|---|---:|
| Joined unique participants | 5,329 |
| Ages 18–49 | 2,976 |
| Not known pregnant | 2,723 |
| Complete DXA, flagged no regions imputed | 2,185 |
| Exclude inconsistent target copies | 2,146 |
| All target components present | 2,146 |
| Complete BIA, excellent/good Cole fit | 1,882 |
| All 100 raw channels finite; resistance positive | 1,882 |
| Complete positive expanded anthropometry | **1,858** |

The source protocol still uses a Hydra whole-body hand/foot measurement with 50 frequencies from 5 kHz to 1 MHz; preparation, exclusions and fit-quality rules matter. [1](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2003/DataFiles/BIX_C.htm)

## 3. Primary results: train 1999–2000, test 2003–2004

**Mean absolute error; lower is better.** Body-fat error is in **percentage points**, all mass errors in **kg**. Lean soft tissue and appendicular lean are DXA compartments, not isolated skeletal-muscle measurements.

### Ridge

| Predictors | Body fat, pp | Fat, kg | Lean soft tissue, kg | Appendicular lean, kg |
|---|---:|---:|---:|---:|
| Basic anthropometry | 2.959 | 2.362 | 2.336 | 1.581 |
| Anthropometry + waist | 2.727 | 2.223 | 2.228 | 1.414 |
| Basic + 50 kHz | 2.410 | 1.746 | 1.740 | 1.315 |
| Waist + 50 kHz | **2.256** | **1.686** | **1.709** | **1.204** |
| Waist + full spectra | 2.205 | 1.660 | 1.698 | 1.199 |
| Expanded anthropometry | 2.704 | 2.205 | 2.207 | 1.363 |
| Expanded + 50 kHz | 2.204 | 1.646 | 1.688 | 1.162 |
| Expanded + full spectra | 2.158 | 1.628 | 1.683 | 1.163 |

### Extra Trees

| Predictors | Body fat, pp | Fat, kg | Lean soft tissue, kg | Appendicular lean, kg |
|---|---:|---:|---:|---:|
| Basic anthropometry | 2.938 | 2.278 | 2.234 | 1.590 |
| Anthropometry + waist | 2.549 | 1.969 | 1.986 | 1.347 |
| Basic + 50 kHz | 2.371 | 1.863 | 1.799 | 1.401 |
| Waist + 50 kHz | **2.153** | **1.700** | **1.690** | **1.262** |
| Waist + full spectra | 2.121 | 1.676 | 1.739 | 1.294 |
| Expanded anthropometry | 2.513 | 1.952 | 1.967 | 1.306 |
| Expanded + 50 kHz | 2.151 | 1.703 | 1.696 | 1.239 |
| Expanded + full spectra | 2.103 | 1.660 | 1.737 | 1.274 |

Bold identifies the common waist + 50-kHz comparison, not a model selected after seeing its results. Basic anthropometry includes age, recorded sex, height, weight and BMI. The waist set adds circumference and waist/height. Expanded adds arm/calf/thigh circumferences and arm/leg lengths. Impedance features are measured R/X and their specified transforms, not vendor-derived fat/lean/water values.

### Paired body-fat MAE improvements

Positive values mean the augmented model performed better on the same participants.

| Added information | Ridge improvement [conditional 95% interval] | Extra Trees improvement [conditional 95% interval] |
|---|---:|---:|
| 50 kHz added to waist baseline | **0.471 pp [0.393, 0.548]** | **0.396 pp [0.339, 0.452]** |
| Full spectra added beyond waist + 50 kHz | **0.051 pp [0.033, 0.068]** | **0.032 pp [0.007, 0.056]** |

The fresh-cycle spectrum gains for body fat are positive in both model families, unlike the less-clear Extra Trees interval in the first test. They remain **small in absolute magnitude**: about three to five hundredths of a percentage point in this primary comparison. No threshold of clinical importance was established.

For lean soft tissue, adding the spectrum beyond 50 kHz changed MAE by:

- Ridge: **+0.011 kg improvement**, interval **−0.002 to +0.024 kg**.
- Extra Trees: **−0.048 kg improvement**, i.e. worse error, interval **−0.073 to −0.022 kg**.

For appendicular lean, the corresponding changes were approximately **+0.005 kg** and **−0.032 kg**. Full spectra therefore did **not** consistently improve all composition endpoints.

The intervals use 2,000 paired test-participant bootstrap resamples. They condition on fitted models and selected cases, omit training uncertainty and survey clustering, and are not multiplicity-adjusted. They are not device-validation confidence bounds or causal effects of buying more frequencies.

## 4. Did the result survive the planned sensitivity checks?

The four secondary experiments used pooled 1999–2002 training, not just the 1999 cycle. Changing training size and eligibility makes them **sensitivity checks, not directly interchangeable absolute-accuracy comparisons**.

### Body-fat MAE improvement from adding 50 kHz to waist

| Analysis | Training n | Test n | Ridge gain, pp | Extra Trees gain, pp |
|---|---:|---:|---:|---:|
| Primary: original 1999 training | 1,802 | 1,858 | **0.471** | **0.396** |
| Pooled strict training | 3,868 | 1,858 | **0.447** | **0.408** |
| Allow marginal Cole fits | 3,904 | 1,909 | **0.450** | **0.414** |
| Do not require expanded anthropometry | 3,880 | 1,865 | **0.446** | **0.402** |
| MEC-weight-sensitive training, evaluated unweighted | 3,868 | 1,858 | **0.461** | **0.409** |

All these gains were positive with their conditional overall bootstrap intervals above zero. Full results, including negative spectrum gains, are retained rather than suppressed.

**MEC-weight sensitivity:** training weights were normalized to mean 1 separately within each training cycle. In this arm, also weighting test absolute errors gave waist → waist+50-kHz improvements of **0.456 pp for Ridge** and **0.427 pp for Extra Trees**. This is a limited predictive weighting sensitivity. It is **not** a survey-design-corrected population result: there is no PSU/stratum variance estimation or correction for the non-random measured-only subset.

Allowing marginal fits is not the same as validating unreliable measurements: questionable, bad and unfitted spectra remained excluded. Relaxing the extra-anthropometry requirement gained only seven fresh test participants, so it says little about populations with widespread missing core measurements.

## 5. Subgroups and individual errors

### Body-fat MAE reduction from adding 50 kHz: primary experiment

| Recorded sex × BMI | Test n | Ridge gain, pp | Extra Trees gain, pp |
|---|---:|---:|---:|
| Male, BMI <25 | 396 | 0.349 | 0.132 |
| Male, BMI 25–<30 | 362 | 0.256 | 0.344 |
| Male, BMI ≥30 | 217 | 0.594 | 0.384 |
| Female, BMI <25 | 390 | 0.593 | 0.512 |
| Female, BMI 25–<30 | 228 | 0.586 | 0.721 |
| Female, BMI ≥30 | 265 | 0.564 | 0.420 |

Every predefined intersection showed a positive gain, and its conditional interval was above zero. These descriptive comparisons still do not certify fairness, universal performance or accuracy in demographic groups absent from the cohort. Recorded sex is the historical dataset variable, not an inferred gender identity.

Ethnicity-specific calibration differences persisted. For the 435 test participants coded Non-Hispanic Black, waist+50-kHz body-fat mean bias was approximately **+1.08 pp for Ridge and +0.96 pp for Extra Trees**, compared with negative mean biases in several other recorded groups. Cause was not investigated; these are model/cohort residuals, not an intrinsic biological explanation. Race/ethnicity was not a predictor. NHANES describes the self-report-derived categories in its documentation. [2](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2003/DataFiles/DEMO_C.htm)

### Absolute errors still limit interpretation

For waist + 50 kHz:

| Primary model / target | MAE | Bias, prediction−reference | Conventional agreement limits |
|---|---:|---:|---:|
| Ridge body fat | 2.256 pp | −0.178 pp | **−5.745 to +5.390 pp** |
| Extra Trees body fat | 2.153 pp | −0.095 pp | **−5.428 to +5.238 pp** |
| Ridge lean soft tissue | 1.709 kg | +0.394 kg | −3.772 to +4.560 kg |
| Extra Trees lean soft tissue | 1.690 kg | +0.298 kg | −4.006 to +4.601 kg |
| Ridge appendicular lean | 1.204 kg | +0.400 kg | −2.466 to +3.267 kg |
| Extra Trees appendicular lean | 1.262 kg | +0.405 kg | −2.624 to +3.434 kg |

Agreement limits are bias ±1.96 residual SD, not individual prediction guarantees or confidence intervals. Empirical residual quantiles are saved separately.

The Extra Trees appendicular-lean mean bias changed from about **+0.10 kg in the earlier cycle test to +0.41 kg here**, despite broadly similar MAE. Different cohorts/reference conditions can change calibration; this observation alone cannot identify hardware drift. It is another reason not to infer that one personal baseline offset will stay valid forever.

## 6. Engineering implications—now with stronger evidence and a new caveat

### Supported direction

1. **Keep raw R/X acquisition in the architecture.** The predictive increment replicated on another cycle and was not confined to one sex/BMI group.
2. **Use 50 kHz as the first information baseline.** A candidate multifrequency model should demonstrate incremental value beyond it on defined endpoints.
3. **Keep geometry and contact quality explicit.** Anthropometry and preparation remain real inputs, not nuisances to hide behind a score.
4. **Budget for measurement repeatability and paired validation before more biomarkers.** These model errors are not small enough to validate subtle personal muscle changes.

### The quality-screening qualification

Both the strict cohort and the marginal-fit sensitivity use **Cole-fit quality derived from multifrequency measurements**, and every arm requires all raw channels to be valid. The 50-kHz-only predictor arms therefore benefit from screening information that a truly single-frequency product might not possess.

Consequently, the defensible claim is **“50-kHz features add information among these spectrum-screened participants,” not “we can discard spectrum acquisition and preserve performance.”** A future pilot needs its own contact/repeatability checks and an explicit plan for failed or poor-quality acquisitions. Fluid-compartment targets and other applications may also benefit from frequencies not justified by this body-fat benchmark.

### What I recommend next

Move from additional historical regression to a **bench-only acquisition specification and impedance-phantom acceptance tests**, reusing the hardware dossier. Define desired R/X accuracy, repeatability, calibration method, phase-error budget, electrode/contact checks, raw-data format and drift logging. This can be done without human connection or a clinical claim.

Only after electrical safety review and a suitable acquisition system should we plan a prospective, geometry-matched pilot with reference measurements and repeat sessions. A single paired scan is not enough to validate longitudinal tracking.

## 7. Saved evidence and execution status

Directory: **`/home/user/dexa-benchmark-followup/`**

- `PROTOCOL.md`: initial settings plus the explicit pre-model eligibility amendment.
- `download-manifest.json`, four compressed `*_C.xpt.gz` files: actual CDC downloads, hashes, dimensions and columns.
- `input-consistency-audit.json`: all-cycle copy-consistency counts, excluded IDs and maximum target ranges.
- `independent-reader-check.json`, `verify_independent_reader.py`: independent decoder check and a repeatable verification script.
- `cohort_loader.py`, `run_followup.py`: amended eligibility and fixed-model execution; depends on the retained first benchmark module/inputs.
- `results/cohorts.json`, `splits.json`: all exclusions and exact participant splits.
- `results/metrics.csv`: **296** complete model/feature/target metric rows across five analyses.
- `results/paired_comparisons.csv`: overall and sex/BMI/intersection gains and conditional intervals.
- `results/subgroups.csv`: full absolute-error and bias audits, including recorded race/ethnicity.
- `results/predictions.csv.gz`: **553,512 prediction records across arms**, not 553,512 different people.
- `results/metadata.json`: library versions, script/protocol hashes and source-cohort equality check.
- `test_followup.py`, `integrity-tests.txt`: **8 passing integrity tests**. These verify computation consistency, not physiological or medical-device validity.
- `execution.log`, `documentation/`: successful run log and selected source documentation.

Original 1999–2002 benchmark inputs/results are preserved. Large, unexamined openScale documentation photographs were pruned from the older source-evidence tree to keep the growing workspace within retention limits; their paths, sizes and hashes are saved in `research-pass-5/openScale-large-photo-pruning.json`. No audited source code or earlier report was removed.

To rerun with compatible dependencies:

```bash
cd /home/user/dexa-benchmark-followup
python verify_independent_reader.py   # requires pyreadstat
OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 python run_followup.py
python -m pytest -o addopts='' -ra test_followup.py
```

### Remaining limits

All model performance is selected-cohort cross-sectional prediction against processed DXA outputs. Age coverage is 18–49; clinical exclusions and measured-only selection narrow generalizability. The new cycle is within the same historical survey/device family. No prospective participant measurement, new hardware build, imaging-model inference, complex-survey analysis, longitudinal repeatability study or bone-density validation was performed. After this pass, the 2003–2004 outcomes have been inspected and are no longer an untouched test set for future tuning.

**Bottom line:** the impedance increment is more credible after replication, but the right next move is calibrated acquisition and quality-control engineering—not a stronger “DEXA-equivalent” marketing claim.
