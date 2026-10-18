# Locked exploratory benchmark protocol — 2026-10-17

Written before model outcomes were inspected. This is an engineering information-gain benchmark, not a US population estimate or clinical validation.

## Cohort
- NHANES adults aged 18–49 inclusive, not known pregnant (RIDEXPRG != 1).
- DXAEXSTS=1 AND DXITOT=0: all regional DXA data measured and valid, no imputation. Verify five imputation copies agree exactly on targets before retaining _MULT_=1; do not analyze imputed labels or average copies.
- BIAEXSTS=1; BIDFIT in {0,1} (excellent/good). Raw 50 resistance and 50 reactance channels must be finite; all resistance channels positive. Reactance sign convention retained; no absolute-value correction.
- Complete positive selected anthropometry. Use the same complete cohort for all feature sets so feature gains are not different-cohort artifacts.
- XPT tiny numerical zero artifacts (absolute value <1e-50) normalized to zero before flag comparisons. Preserve original compressed files/hashes.

## Outcomes
DXDTOPF (% body fat, error in percentage points); DXDTOFAT/1000 (kg fat); DXDTOLE/1000 (kg lean soft tissue excluding BMC); sum(DXDLALE, DXDRALE, DXDLLLE, DXDRLLE)/1000 (kg appendicular lean soft tissue). Neither lean target is directly isolated skeletal-muscle mass.

## Features
All models get age, recorded sex, standing height, body mass, BMI. No DXA columns, imputation flags, fitted Hydra volumes, derived Hydra fat/lean, or subject IDs enter predictors.
- Basic anthropometry.
- Basic + waist and waist/height.
- Basic + 50-kHz resistance/reactance/phase angle/height² divided by resistance.
- Waist + the same 50-kHz features.
- Waist + all 100 raw spectral channels, plus height²/R and phase angle at 5,50,200,500 kHz and 1 MHz.
- Expanded anthropometry: waist set plus arm/calf/thigh circumferences and arm/leg lengths.
- Expanded + 50-kHz.
- Expanded + full spectra.

## Models and evaluation
- Fixed standardized Ridge(alpha=10); fixed ExtraTreesRegressor(n_estimators=160,min_samples_leaf=5,max_features=1.0,random_state=20261017). No hyperparameter tuning against test results; no selection of a winning feature/model after looking at test errors.
- PRIMARY: train all eligible 1999–2000 cases, test eligible 2001–2002 cases. Distinct participant IDs asserted. This is temporal/cycle transfer within NHANES, not external device/site validation.
- SECONDARY: stratified 70/30 participant split within 1999–2000, seed 20261017, stratified on recorded sex. Same subjects in every feature-set comparison.
- Unweighted engineering performance on the selected measured-only cohort. Survey weights/design not used; do not infer national prevalence, US population accuracy, or causal benefit from extra frequencies.
- Report test MAE, RMSE, bias=prediction-reference, empirical residual 2.5/97.5 percentiles, and conventional bias ±1.96 SD agreement limits. Residual percentiles and limits are not confidence intervals.
- Paired participant bootstrap (2000 replicates, fixed seed) for MAE improvement, comparing waist→waist+50k, waist+50k→waist+spectra, expanded→expanded+50k, expanded+50k→expanded+spectra, separately by model/target. These intervals condition on fitted models and a selected cohort, ignore survey clustering, are not multiplicity-adjusted, and do not include training uncertainty.
- Primary subgroup audit: recorded sex, age groups 18–29/30–39/40–49, BMI <25/25–29.99/≥30, and RIDRETH1. Race/ethnicity is audit-only, not a predictor. Small groups explicitly flagged, not interpreted as stable estimates.

## Limits
Cross-sectional labels only; cannot establish longitudinal tissue-change precision, home-scale performance, safety, commercial product validity, tissue water status or clinical bone density. Frequencies correlated, devices/protocols differ; more channels do not prove they are necessary. Whole-body spectra do not validate segmental or EIM devices. Measured-only selection is non-random and narrows coverage. No person should be reassured or treated based on this research model.
