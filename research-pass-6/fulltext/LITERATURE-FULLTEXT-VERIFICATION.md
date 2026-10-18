# Literature full-text verification (pass 6, item b)

Method: full texts fetched directly (PMC efetch XML for PMC IDs; Nature article HTML for s41598/s41387/s41430), tags stripped, and each number searched in the text. Raw text saved next to this file (`*.txt`). Verified means the number appears in the full text in the stated context.

## Verified in full text

| Paper | Claim | Full-text result |
|---|---|---|
| PMC11649400 (Looney 2024) | 14 adults, five visits over three weeks | Confirmed |
| PMC11649400 | %BF bias −4.0 ± 2.8% | Confirmed |
| PMC11649400 | FFM bias +2.8 ± 2.1 kg; FM bias −2.9 ± 2.0 kg | Confirmed (MF-BIA minus DXA; "underprediction of fat mass") |
| PMC4475745 (Wang & Hui 2015) | InBody 520 rc = 0.926 (boys), 0.912 (girls) | Confirmed. Described in the text as "moderate agreement" |
| PMC9813632 (Potter 2022) | MAE FFM 2.8 and 3.1 kg; %BF MAE 3.4% and 3.9% | Numbers present, but see inconsistency below |
| PMC9813632 | InBody %BF bias −3.4 | Confirmed (Table 3, InBody 770 All row) |
| s41598-023-44217-0 (Sci Rep 2023) | ICC/CCC 0.902–0.972 for FM, FFM, LBM | Confirmed |
| s41598-023-44217-0 | %BF underestimated −8.9 to −0.8% | Confirmed |
| s41387-022-00223-1 (Nutr Diabetes 2022) | Leg lean mass 14.76 vs 15.19 kg; difference p = 0.353 | Confirmed (Bland–Altman p) |
| s41387-022-00223-1 | ASMI ICC 0.965 | Confirmed |
| s41387-022-00223-1 | Trunk limits of agreement (previously unverified) | Lean trunk mass: difference −1.29 kg, LoA −4.80 to +2.21 kg (DSMF-BIA underestimates). Arm fat: +2.32 kg, LoA −1.15 to +5.79 kg |
| s41430-025-01664-4 (Eur J Clin Nutr 2025) | FM bias men −3.7 ± 2.6, women −1.9 ± 1.8 kg | Confirmed |
| s41430-025-01664-4 | %BF bias men −4.2 ± 3.0, women −2.8 ± 2.6 | Confirmed |
| s41430-025-01664-4 | FFM bias men +3.4 ± 2.8, women +2.0 ± 2.2 kg | Confirmed |
| s41430-025-01664-4 | VAT CCC 0.34–0.68 | Confirmed (women 0.34, men 0.68) |
| s41598-022-05887-4 (Sci Rep 2022, COPD) | FM ρc = 0.95 | Confirmed |
| s41598-022-05887-4 | FM mean difference 2.7 ± 3.2 kg | Confirmed. Direction now stated: BIA underestimated FM (DXA minus BIA = +2.7) |
| s41598-022-05887-4 | %fat ρc 0.67; FFM ρc 0.74 | Confirmed. %fat mean difference: BIA underestimated by 4.5 ± 3.5% (new) |

## Corrections to earlier notes

- **s41430-025-01664-4 reliability.** The earlier note "ICC 0.987–0.998" combined two ranges. The paper gives DXA ICC 0.990–0.998 and MF-BIA ICC 0.987–0.995.
- **s41598-022-05887-4 direction.** Earlier notes said the direction was not stated. It is stated: BIA underestimates both fat mass (2.7 kg) and percent body fat (4.5%).

## Internal inconsistency found

- **PMC9813632 (Potter 2022).** The abstract gives %BF MAE as 3.4% and 3.9% "respectively" for RJL and InBody. Table 3 gives RJL %BF MAE 2.7 (All) and InBody 3.9. The 3.4 figure in the abstract does not match the table. The table values are used in this record. The discrepancy is noted for anyone citing this paper.

## Added in this pass (full text)

| Paper | Claim | Full-text result |
|---|---|---|
| PubMed 41567330 / PMC12815710 (Wahrlich 2026) | 945 Brazilian adults; FFM bias +3.1 kg; FM −2.9 kg | Confirmed: FFM +3.1 kg (+7.2%), FM −2.9 kg (−13.0%), r = 0.97, CCC ≥ 0.93, n = 945 |
| Frontiers frans.2026.1767078 (2026, InBody 970S) | R² 0.72–0.97 | Confirmed (R² 0.72–0.97; sarcopenia sensitivity 95.1%) |

## Round 2 (abstracts and tables read from publisher and PubMed pages)

| Paper | Source | Result |
|---|---|---|
| Springer s40520-021-02000-z (Aging Clin Exp Res 2022) | Springer article page, full abstract | Confirmed: n = 73 (19 men, 54 women), BMI 27.1. ASMM 21.61 ± 5.82 vs 18.82 ± 4.81 kg; FFM 49.57 ± 9.94 vs 46.22 ± 10.11 kg; FM 24.59 ± 8.28 vs 27.13 ± 10.01 kg; all p < 0.001. Wide limits of agreement |
| Sensors 25/16/5037 (Zaplatosch 2025, open access) | MDPI article page, full abstract | Confirmed. Note: this is a study of **55 women aged 21.1**, not a general adult sample. IB770 vs DXA FM MD −0.22 kg (CCC 0.99); FFM MD +3.15 kg (CCC 0.91). IB770 vs D2O TBW MD 0.34 L (CCC 0.98) |
| PubMed 42437547 (Campos 2026, severe obesity, MACRO trial) | PubMed page, full abstract | Confirmed: n = 49 (39 women), BMI > 40. FM bias 1.1 kg (LoA −6.9 to 9.0). FFM bias −0.22 kg (LoA −6.6 to 6.2). Verdich equation FFM bias −2.9 kg (LoA −11.4 to 5.6). ALST underestimated by all equations |
| PubMed 23388666 (Eur J Clin Nutr 2013, frail women) | PubMed page, full abstract | Confirmed: n = 129, mean age 80.9. Bland–Altman bias defined as DXA minus SMF-BIA: whole-body FM bias −1.2 kg (BIA overestimates FM); whole-body LM bias +2.1 kg (BIA underestimates LM). Appendicular FM bias −0.3 kg. Direction now stated |
| ScienceDirect S2667268526000409 (Hjort 2026, Clinical Nutrition Open Science, open access) | Article page, Table 1 | Table confirmed: n = 316 (209 women, 107 men). FM DXA 26.16 vs BIA 24.95 kg, mean difference 1.21 kg, LoA −3.35 to 5.76; FFM difference −1.28 kg, LoA −6.04 to 3.48; ICC FM 0.97, FFM 0.97, FM arms 0.69, FM legs 0.76 |

### Internal inconsistency found in Hjort 2026

The Results text and Table 1 disagree on sign and size:
- Text: BIA "underestimate[s] total FM by 1.2 kg" (consistent with table). But "individual differences ranging from −5.7 kg to 3.8 kg (FM)" and "−3.6 kg to 6.1 kg (FFM)". Table 1 gives FM −3.35 to 5.76 and FFM −6.04 to 3.48. The text's limits are not the table's limits, even with sign flipped.
- Text: BIA overestimates FM arms by 1.5 kg and underestimates FM legs by 1.1 kg. Table 1: FM arms −1.23 kg (DXA minus BIA, i.e. BIA higher by 1.23), FM legs +1.34 kg (BIA lower by 1.34).

The table values are used in this record. The text figures are not.


### Sillanpää 2014 (Obesity; PubMed 23894111)

- PubMed abstract confirmed: 882 adults aged 18–88, eight-polar BIA vs DXA. Compared with DXA, BIA gave **larger** lean mass (+2.9 kg women, +1.6 kg men) and **smaller** fat mass (−3.1 kg women, −2.6 kg men).
- **Correction:** the earlier note "LM 2.9 kg lower (women) and 1.6 kg lower (men)" had the sign wrong. BIA overestimated lean mass.
- Limits of agreement (LM −6.7 to 1.9 kg women, −7.0 to 3.7 kg men) come from a publisher search snippet, not the full paper. Not checked in full text.
- A second snippet (ResearchGate) reports a different analysis: BIA "systematically underestimated" %BF (bias −1.96%) and FM (bias −0.72 kg). This conflicts with the abstract's FM result and is unresolved. Do not cite it without reading the full paper.


### JEN article 206 (Brown et al. 2025, J Exerc Nutr; full text read from the journal PDF)

Reachable via the journal site (the earlier failure was the host name, not the paper). Sample: 42 men, 35 women. %BF bias, DXA minus device (sign as the paper reports), and LoA:

| Device | Type | Bias (%BF) | LoA (%BF) |
|---|---|---|---|
| Omron | single-frequency | −2.21 | −9.88 to +5.46 |
| Renpho ES-CS20M | single-frequency | +2.38 | −7.95 to +12.74 |
| Tanita BF-679W | single-frequency | +3.18 | tighter than Renpho (figure only) |
| Triomph EMSC91 | single-frequency | +2.88 | −10.25 to +16.01 (widest) |
| InBody H20 | multi-frequency | +2.72 | +5.73 to +11.17 (text range) |
| InBody S10 | multi-frequency | +4.36 | −2.25 to +11.07 (text range) |

ICCs: four devices 0.66–0.73; two devices 0.25 and 0.43. Methods table lists single-point, single-frequency devices for the four non-InBody models.

**Inconsistency in the paper:** the Conclusions say "the Omron had the highest LoA with DXA". The Results give Triomph the widest LoA (−10.25 to 16.01). Omron has the narrowest LoA of the single-frequency devices in the table. The Conclusions claim is not supported by the Results and is not used here.

**Also:** the two InBody results are text ranges and the paper gives no table row for them in the text extract. Figure values were not read.

### MAX30001 datasheet (ADI, Rev. 3)

- ADI product page (`analog.com/en/products/max30001.html`) reached and confirmed the Rev. 3 datasheet link.
- Direct PDF fetch: HTTP/2 INTERNAL_ERROR with curl; HTTP/1.1 timed out after 180 s. Fetch tool: failed. The official PDF is still not retrieved. Mirror pages remain the source for the registers quoted in sections 9–11.

### Not reached in this round

- None of the papers in section 10 remain unread. Sources still limited to snippets: Greek 8-point MF-BIA (healthcare 14/1807), Frontiers 10.3389/fnut.2025.1499752, MDPI nutrients 10/6/738.


## Abstract-level only (superseded by round 2 above where marked)

- Campos 2026 (PubMed 42437547): not in PMC. Abstract value stays: FM bias 1.1 kg (LoA −6.9 to 9.0), n = 49, BMI > 40.
- Springer s40520-021-02000-z: publisher page returned a 48-word stub. Abstract values stay: FFM 49.57 vs 46.22 kg; FM 24.59 vs 27.13 kg.
- MDPI Sensors 25/16/5037: page returned a 17-word stub. Abstract values stay: FM MD −0.22 kg; FFM MD +3.15 kg.
- ScienceDirect S2667268526000409 (2026): not fetched.
- Eur J Clin Nutr 2013 (PubMed 23388666): no PMC copy. Abstract only.
- JEN article 206: not fetched.
