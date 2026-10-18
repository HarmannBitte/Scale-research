# Fresh-cycle follow-up protocol — 2026-10-17

Specified before downloading/inspecting 2003–2004 model outcomes. The earlier 1999–2002 results are known and motivated this test; no claim of independent preregistration is made.

## Primary replication
Train on the original eligible 1999–2000 cohort only; test 2003–2004 using unchanged measured-only eligibility, eight feature sets, four targets, fixed Ridge(alpha=10) and ExtraTrees(160 trees,min_leaf=5,max_features=1,seed=20261017), all multioutput. No tuning, model selection, frequency selection, or outcome-driven stopping. Use every fixed arm. Compare waiver of nothing: core primary eligibility remains identical to the first benchmark.

## Prespecified secondary checks
1. Train on pooled 1999–2002 eligible participants and test the same fresh 2003–2004 cohort. No ID overlap; original 2001–2002 test data become training data only for this secondary experiment.
2. Eligibility sensitivity: include marginal Cole fits (BIDFIT 2) in addition to 0/1 in pooled training and fresh testing. No questionable/bad/unfitted spectra.
3. Eligibility sensitivity: require complete positive height, weight and waist, but do not require the extra arm/calf/thigh/length measures; use the five non-expanded feature arms only. Require all 100 valid raw channels in every comparison. Pooled training.
4. Predictive observation-weight sensitivity: original two-year MEC weights renormalized to mean 1 within each training cycle, fixed models and original strict cohort; pooled training. Evaluate unweighted and weight-normalized test MAE. This is NOT a survey-design-corrected estimate and does NOT correct measured-only selection bias.

## Outcomes and uncertainty
Same four DXA targets, MAE/RMSE/bias/empirical residual percentiles/conventional limits of agreement. Positive paired improvement = baseline absolute error minus augmented absolute error. Bootstrap 2000 test participants, same resample for the two predictions; conditional intervals ignore training variability, complex survey clustering and multiple comparisons. No population-accuracy or causal claim.

For every run/model/target: waist→waist+50k; waist+50k→waist+spectra; and expanded counterparts where eligible. Record sex and BMI-group paired improvement and absolute metrics; use sex×BMI intersections as descriptive checks with n<50 flagged. Record race/ethnicity subgroup absolute errors/bias as descriptive auditing, not biological explanations; no race predictor. Do not suppress negative gains.

## Input and integrity checks
Use official CDC 2003–2004 BIX_C, DXX_C, DEMO_C, BMX_C. Confirm protocol/codebook alignment, DXITOT=0, five identical measured copies, uniqueness, and raw channel names. Preserve downloads as compressed originals with hashes, or hash-preserving compressed archives if storage budget requires consolidating prior inputs. Retain earlier reports/results unchanged.

Refactored cohort loader must reproduce exact earlier 1999–2002 participant IDs, targets and feature maps before evaluating new data. Explicitly normalize tiny XPT zero decoding artifacts as in original. Verify n, no target-derived predictors, disjoint train/test IDs, identical test IDs across each arm, and recomputed saved metrics.

## Decision rule and limitations
Treat a small/nonconsistent full-spectrum gain as insufficient evidence for complexity for THESE cross-sectional targets, not proof that higher frequencies are useless. Never infer home-electrode performance, longitudinal precision, water-compartment validity, or bone diagnosis. Report all fixed runs and explain that weight sensitivity lacks PSU/stratum variance estimation and nonresponse correction. The 2003–2004 outcomes become inspected development evidence after this pass and cannot remain a fresh confirmatory set for future tuning.

## Eligibility amendment before any 2003–2004 model outcome — 2026-10-17
The input consistency assertion stopped execution before model evaluation. Among scan-complete/no-region-imputed flagged records, 80 participants in DXX_C had varying target values across the five copies (1999/2001: zero). Independent pyreadstat 1.3.6 decoding agreed with pandas for IDs, flags and targets (absolute tolerance 1e-50 after tiny-zero normalization). Cause not established; do not label them definitively measured or imputed.

Conservative amendment applied to ALL cycles/analyses: drop any participant marked complete/non-imputed whose target copies disagree or who lacks exactly five such copies. Save excluded IDs/ranges; do not select or average a copy to manufacture truth. Recheck earlier-cohort equivalence, then run unchanged model/feature/metric settings. This is a documented post-input-inspection eligibility amendment, not an outcome-driven model change or a wholly untouched protocol.
