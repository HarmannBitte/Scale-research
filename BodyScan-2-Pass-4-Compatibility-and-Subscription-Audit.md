# BodyScan 2 alternatives — pass 4: compatibility, formulas and subscription audit

**Research date: October 17, 2026.** This supplements the earlier expanded and pass-3 reports. It does not replace their broader hardware/library catalogues. No physical scales, human measurements or account integrations were tested.

## Decision-changing results

1. **Withings changed its automatic third-party sync policy this week.** An official staff response says accounts created from October 13, 2026 require Withings+ for automatic third-party sync. Accounts created on/before October 12 retain free automatic sync, including after buying new devices. CSV/PDF export remains free for everyone. This supersedes any earlier blanket claim that Withings automatic export is subscription-free.
2. **The biggest open-scale pitfall is data provenance, not the number of displayed metrics.** Source inspection finds BMI-only fallbacks, fixed-fraction water/bone estimates and a computed visceral-fat index. A supported device can produce a rich record without supplying impedance or vendor composition.
3. **I ran 522 targeted BLE Scale Sync tests across eight files: all passed.** This confirms the supplied software expectations, including deliberate fallbacks; it does not establish physiological accuracy or prove live device support.
4. **Glucose Resilience is not glucose measurement.** Withings' October explanation explicitly says it does not measure blood glucose, HbA1c or insulin resistance. It combines visceral-fat estimation with the Nerve Response Score.
5. **ESC has published technical detail but is not established as a turnkey open build.** It also has a mixed diagnostic evidence base; published Sudoscan findings cannot simply be transferred to a consumer wellness score.

---

## 1. Newly verified subscription change

### What Withings itself says

In the official response by **Markus, From Withings**, to the October 13 community thread:

> “If you created your account on or before October 12, 2026, automatic third-party sync stays free.”

> “For accounts created from October 13, 2026, automatic sync to third-party apps is part of Withings+.”

The response also says:

- eligibility is tied to the **account**, not the particular device;
- all users retain full-history CSV/PDF export, incoming imports and doctor sharing;
- when membership ends, automatic sync pauses; data is not lost and sync resumes with membership;
- Withings+ includes exclusive scores, physician ECG reviews, an AI assistant and an MCP connector. [1](https://support.withings.com/hc/en-us/community/posts/51887047154577-Unacceptable-Apple-Health-Sync-is-now-behind-a-99-year-paywall-for-new-accounts)

This is an official staff statement on a community page, not merely the thread author's complaint. Independent coverage corroborates it. [10](https://www.heise.de/en/news/Withings-charges-extra-for-Apple-Health-sync-but-only-for-new-users-11491217.html)

### What this means for your MG + scale decision

| Your situation | Consequence |
|---|---|
| Existing Withings account created by October 12 | Company says automatic sync remains free, even with a newly bought scale |
| New Withings account from October 13 | Budget for Withings+ if automatic third-party sync is required |
| Manual archive is sufficient | CSV/PDF export remains available without membership |
| Want a fully local setup | Cloud export, even when free, is not local acquisition |
| Want WHOOP integration specifically | General policy creates a potential paid dependency; verify the exact connector/account entitlement before buying |

**Unresolved:** the staff response is broad; I have not tested the direct WHOOP connector, a new-account OAuth flow, or the developer API under the new rule. Do not claim either a WHOOP exemption or a universal block on every API client without that testing.

Withings' July WHOOP article describes a cloud-based integration forwarding weight, muscle mass and fat percentage. It does not demonstrate raw impedance/ECG/ICG export into WHOOP. Its publication also predates this week's sync policy. [Withings integration article](https://www.withings.com/en-us/blogs/withings-blog/the-best-scale-for-whoop-2026-your-complete-guide)

### Cost illustration, not a price guarantee

July US launch materials list BodyScan 2 at **$599.95** and Withings+ at **$99.50/year or $9.95/month**. WHOOP's official Life page lists **$359/year**. [3](https://www.prnewswire.com/news-releases/withings-bodyscan-2-now-available-in-the-us-setting-a-standard-in-preventive-health-and-longevity-monitoring-302825384.html) [1](https://www.whoop.com/us/en/life/)

At unchanged annual prices, three years of BodyScan 2 + three full annual Withings+ payments is **$898.45**; adding three years of Life totals **$1,975.45**. This arithmetic ignores trials, discounts, taxes and price changes. Since you already own MG, its existing cost is not necessarily an incremental scale cost. Grandfathered sync does not make premium scores free.

### Why companies push subscriptions

**Company explanation:** Withings says membership funds services around the data. Its bundle includes ongoing interpretation, physician reviews and AI-related services. [1](https://support.withings.com/hc/en-us/community/posts/51887047154577-Unacceptable-Apple-Health-Sync-is-now-behind-a-99-year-paywall-for-new-accounts)

**Business interpretation, not an audited financial finding:** recurring revenue extends income beyond infrequent hardware replacement, increases lifetime customer value and makes the service bundle a retention mechanism. Moving automatic export into that bundle also monetizes convenience/interoperability. A local phone-to-health-store write is not the same workload as physician review or a cloud AI service, so those features should not be treated as having identical marginal costs.

Ownership of a downloadable archive, uninterrupted automatic interoperability and access to proprietary scores are **three different rights/capabilities**.

---

## 2. Source-level audit: BLE Scale Sync

Repository: https://github.com/KristianP26/ble-scale-sync

Reviewed snapshot:

```text
version: 1.33.0
commit: a4751aa8d813691530a7628eced18c481622d212
license: GPL-3.0 (LICENSE inspected)
```

Its local collectors/exporters remain a strong automation starting point. But “Yes” under body composition is not enough to decide which scale to buy.

### Exact-model findings

All rows describe **this software snapshot**, not every firmware or alternative app for the device. Source files and the support guide were read locally.

| Device/protocol | What the reviewed implementation actually establishes | Recommendation |
|---|---|---|
| **Robi S9** | Final weight decoded; impedance deliberately zero because captured final frame did not establish a usable field; composition falls back to BMI | Do not buy for open raw segmental BIA based on this adapter |
| **Speediance FG2211WBF** | Full captured handshake, final weight; captured candidate impedance 3022 rejected as implausible, possible scaling still unresolved; part-01 segmental fields not decoded | Treat body-composition “Yes” in the table cautiously; current supplied captured example falls back to BMI |
| **Renpho R-MSC04 / MorphoScan Nova** | Weight path plus composition/segment diagnostics; ten segment impedances debug-logged; profile uncertainty prevents use of vendor composition; guide says current changes lack hardware confirmation | Not yet a normal raw-segmental export recommendation |
| **Arboleaf QN 19-byte dialect** | Vendor fat/water/muscle/bone/visceral values can be used after accepted profile and exact matching; otherwise BMI fallback; segment impedances debug-only | Stronger conditional local vendor-result route; preserve profile and per-reading provenance |
| **Hutbit 218008 / WL292, AC02 family** | Documented raw impedance frame on a related Juniper unit, checksum/contact checks and time pairing; usable impedance feeds an open estimate | Better raw-scalar lead, not five-region composition |
| **Xiaomi S400 MJTZC01YM** | Guide lists composition; requires device bind key from Mi cloud and scale MAC | Local collection after credential provisioning is not a zero-cloud setup claim |
| **Xiaomi S800 ms116** | Guide lists weight only; still needs bind key | Do not confuse richer hardware marketing with implemented local fields |
| **Eufy P2 T9148 / P2 Pro T9149** | Active GATT path for composition; advertisements give weight only | Connection mode matters |
| **Xiaomi XMTZC04HM** | Weight only | Useful weight bridge, not an impedance alternative |

Primary code references:

- [Support guide](https://github.com/KristianP26/ble-scale-sync/blob/a4751aa8d813691530a7628eced18c481622d212/docs/guide/supported-scales.md)
- [Robi adapter](https://github.com/KristianP26/ble-scale-sync/blob/a4751aa8d813691530a7628eced18c481622d212/src/scales/robi-s9.ts)
- [Speediance adapter](https://github.com/KristianP26/ble-scale-sync/blob/a4751aa8d813691530a7628eced18c481622d212/src/scales/speediance.ts)
- [Renpho adapter](https://github.com/KristianP26/ble-scale-sync/blob/a4751aa8d813691530a7628eced18c481622d212/src/scales/renpho-msc04.ts)
- [Hutbit adapter](https://github.com/KristianP26/ble-scale-sync/blob/a4751aa8d813691530a7628eced18c481622d212/src/scales/hutbit.ts)

### Why a shared OEM name or BLE service is not enough

These families use different handshakes, framing, result types and byte ordering. Robi/Speediance and the prior pass's JEETIF codec share an OEM/service family but do not therefore share complete decoders. Hutbit's fixed AC02 frames differ again. Transplanting offsets without frame evidence risks silently wrong values.

The prior pass's **MIT JEETIF/Fitdays codec remains the strongest documented ten-value local acquisition lead**, but it is not a broadly verified retail-model purchase recommendation. Its proprietary WLA37 composition dependency remains. [Repository](https://github.com/dandwhelan/fitdays-lefu-scale)

---

## 3. What the open formulas actually calculate

Audited file: [body-comp-helpers.ts](https://github.com/KristianP26/ble-scale-sync/blob/a4751aa8d813691530a7628eced18c481622d212/src/scales/body-comp-helpers.ts).

### BMI fallback

For adults the implementation uses:

```text
body fat % = 1.20 × BMI + 0.23 × age − 10.8 × sex − 5.4
sex: male = 1, female = 0
```

It also applies an athlete adjustment and bounds the result. This is explicitly a demographic/BMI estimate, not BIA. Two same-age, same-height, same-weight people with the same profile will get the same result even if their true muscle/fat distribution differs.

### Impedance-based route

`computeBiaFat` uses height²/impedance, weight, age and sex/athlete-specific coefficients. The equation is inspectable and modifiable. That transparency does not itself establish its population calibration, clinical accuracy or parity with the vendor model.

### Secondary metrics

Where the scale did not supply corresponding values, the helper calculates:

- water from lean mass using **0.73**, or **0.74** for the athlete branch;
- bone mass from **0.042 × lean mass**;
- “muscle mass” as lean mass minus bone, distinct from a separately used skeletal-muscle heuristic;
- a visceral-fat index from fat percentage and age;
- BMR from a Mifflin–St Jeor-style equation, with an athlete multiplier;
- metabolic age from the BMR comparison.

**Do not mistake these for independent sensors.** An index named visceral fat is not necessarily a measured abdominal-fat compartment. A field named muscle mass may not mean skeletal muscle mass.

### A revealing algebraic limitation

For the non-athlete metabolic-age branch, the BMR reference uses the same height, weight and sex at age 25. Subtracting the two BMR equations cancels height, weight and sex. Before the minimum-age bound, this simplifies to:

```text
metabolicAge = age + trunc((5 × age − 125) / 15)
```

This is my algebraic analysis of the reviewed source, not a project claim. In this branch it cannot independently track improvement in body composition at a fixed chronological age. It is certainly not a substitute for Withings' ICG-based Heart Age or a measured cellular-aging process.

### Data-model limitation

The central `BodyComposition` interface contains one impedance scalar plus whole-body results, not a segment × frequency array or per-field model-origin labels. Debug-logged regional values are therefore not the same as preserved normal exports. A proper segmental archive requires an explicit schema/export addition, not simply connecting MQTT.

Suggested field-level origins:

```text
raw_sensor_decoded
vendor_derived
open_impedance_estimate
bmi_only_estimate
fixed_fraction_estimate
unavailable
```

Also store formula/version, source device/firmware, profile, frequency/pathway, calibration, timestamps and quality flags. Prefer null over an apparently precise fabricated measurement.

---

## 4. Software testing performed

I installed dependencies with lifecycle scripts disabled and ran selected included tests. No Bluetooth device, vendor credentials or human measurements were used.

| Run | Files that actually ran | Passed |
|---|---|---:|
| Targeted adapters | Robi S9, Speediance, Hutbit | 55 |
| Composition and QN/Xiaomi | body-comp helpers, QN 19-byte, general QN, Xiaomi S400 | 382 |
| Renpho | R-MSC04 | 85 |
| **Total, eight distinct files** | | **522** |

Saved logs:

- `research-pass-4/targeted-tests.txt`
- `research-pass-4/composition-tests.txt`
- `research-pass-4/renpho-tests.txt`

Caveats:

- First invocation also named two nonexistent file filters; only the three files listed above ran. Correct helper/Renpho tests were run subsequently and are included in the totals.
- Environment Node was **20.20.2**, while package engines request **Node ≥22**. Tests ran successfully, but this is not a supported-runtime deployment certification.
- Installation emitted deprecation warnings. This was not a dependency-security audit; native BLE lifecycle scripts were not enabled.
- I did not run the full suite or hardware transport tests. Vitest reported no type errors in these runs; I did not independently run a complete production build/typecheck.
- Passing tests can correctly verify a BMI fallback. Passing count is not measurement validity.

---

## 5. Nerve-response investigation: closer to the method, not to a finished open device

### Important public technical source

The 2024 review **From Sudoscan to bedside** describes ESC principles, electrode electrochemistry and analysis. Its authors are affiliated with **Withings**. It explicitly distinguishes ESC from ordinary GSR/EDA. This is useful public technical disclosure, but not a complete open-hardware/firmware release or independent endorsement. [Review](https://www.frontiersin.org/journals/neuroanatomy/articles/10.3389/fnana.2024.1454095/full)

This pass searched for Sudoscan/ESC/sudomotor source repositories and did **not** establish a licensed, maintained, end-to-end open ESC device with human reference validation. One prominent GitHub “sudoscan” result is a Sudoku solver—a false match, not another health project. [1](https://github.com/pintowar/sudoscan)

### The evidence is not uniformly strong

A blinded retrospective study of 210 patients reported weight-adjusted ESC sensitivity/specificity of **64%/77% for abnormal sweat-gland nerve-fiber density**, with ROC AUC **0.73**; the authors describe modest accuracy. This is a particular clinical study, not a BodyScan 2 performance estimate. [8](https://pmc.ncbi.nlm.nih.gov/articles/PMC7212463/)

A skeptical systematic review questioned consistency of normative values and manufacturer-supported evidence; a published response disputes that interpretation. This debate should be disclosed rather than replacing all uncertainty with “clinically validated.” [4](https://www.proquest.com/scholarly-journals/sudomotor-function-testing-electrochemical-skin/docview/2061225568/se-2) [6](https://link.springer.com/article/10.1007/s10286-018-0562-7)

**Conclusion:** neither a cheap EDA board nor an open EMG board is an equivalent nerve-response replacement. Electrochemical hardware, protocol fidelity, reference validation and the clinical interpretation all remain separate tasks. This is not a recommendation to construct a human-connected electrical stimulator.

---

## 6. Glucose investigation: correct the target before trying to replicate it

### Current Withings description

The October 6 Withings article says Glucose Resilience:

- is a long-term wellness score requiring BodyScan 2 and Withings+;
- combines visceral-fat analysis with a feet-based sudomotor/Nerve Response Score;
- **does not measure blood glucose, HbA1c or insulin resistance**;
- is not a diabetes diagnostic tool. [October explanation](https://www.withings.com/en-us/blogs/withings-blog/glucose-resilience-score-what-it-is-and-how-to-read-it)

The current product FAQ likewise says the score does not measure or estimate blood glucose. [4](https://www.withings.com/en-us/products/bodyscan-2-black)

Thus there are three different goals:

| Goal | Appropriate category |
|---|---|
| Reproduce the branded Glucose Resilience score | Exact model and appropriate inputs; neither established as open here |
| Assess metabolic risk | Validated clinical evaluation/risk tools, not a cloned branding score |
| Observe glucose concentrations | Appropriate validated glucose testing/CGM, not a scale proxy |

### Non-invasive optical project found—and why I would not recommend it for care

A Scientific Reports paper and repository call their device an “open-source multi-wavelength non-invasive blood glucose sensing system.” The repository's detailed limitations are more informative than its headline:

- decisive venous-plasma comparison involved **three non-diabetic volunteers**;
- 150 measurements reflect repeated fingertips/time points, not 150 independent participants;
- earlier healthy-volunteer evaluation covered a limited glucose range;
- reflection strategies failed in the reported error-grid assessment;
- drift and warm-up affect reproducibility;
- hardware/algorithms are shared under **CC BY-NC-ND 4.0**—not an unrestricted open-source license. [1](https://www.nature.com/articles/s41598-025-28673-4) [2](https://github.com/HoangNhutHuynh/Blood_glucose)

**Verdict:** research reading, not a replacement glucometer, a validated diabetes detector or a route to recreating Withings' different score. Do not use DIY predictions for treatment or insulin decisions.

Another repository/paper implementation reports MIT code but only an R² around 0.51 across 25 subjects; that statistic does not establish clinical safety or accuracy. [3](https://github.com/dippaul-dp/non-invasive-glucose-monitoring-nir)

### More transparent risk software is possible, but not equivalent

New search leads include **Elucenia/tool-findrisc** (Apache-2.0) and **romebkkk/diabrisk** (MIT). These implement questionnaire-based diabetes risk approaches, not physical glucose sensing. I did not execute or validate either implementation. [2](https://github.com/Elucenia/tool-findrisc) [1](https://github.com/romebkkk/diabrisk)

The underlying FINDRISC tool has external evidence, but calibration/cutoffs vary by population; a Norwegian follow-up illustrates this. A validated published score does not automatically validate a newly written app or justify a personal diagnosis. [20](https://pmc.ncbi.nlm.nih.gov/articles/PMC6887494/)

---

## 7. Regulatory and current-feature corrections

Do not bundle all WHOOP outputs into one medical claim:

- **WHOOP ECG feature:** FDA database records clearance K243236, April 4, 2025. The indication is a software feature producing a single-channel ECG qualitatively similar to Lead I, with specified rhythm classifications. [1](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K243236) [2](https://www.accessdata.fda.gov/cdrh_docs/pdf24/K243236.pdf)
- **WHOOP Blood Pressure Insights:** June 17, 2026 FDA letter says the agency does not intend to enforce device requirements for the modified product under wellness policy. That is **not medical BP clearance**. [5](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/whoop-inc-709755-06172026)
- **BodyScan 2:** Withings' current support FAQ distinguishes EU medical hypertension notifications from US wellness Blood Pressure Insights and identifies regulated ECG/AFib functionality. Launch materials distinguish cleared ECG software from other wellness claims. Regional/version-specific status matters. [10](https://support.withings.com/hc/en-us/articles/42653646388625-BodyScan-2-Frequently-asked-questions-FAQ) [3](https://www.prnewswire.com/news-releases/withings-bodyscan-2-now-available-in-the-us-setting-a-standard-in-preventive-health-and-longevity-monitoring-302825384.html)

The July FAQ still labels some functions “coming soon”; the October Glucose Resilience article describes availability. Do not preserve old availability statements as current without checking the newer source. Conversely, a public article does not verify rollout on every account/region.

---

## 8. Updated recommendation for an MG owner

### Practical path

1. **Determine whether you already have a grandfathered Withings account.** This now materially affects the subscription comparison.
2. **If local data is the priority, require a raw-data sample before purchasing a handle scale.** Exact retail model, firmware, BLE service and result-frame match matter more than OEM family.
3. **Do not buy Robi S9 or Speediance solely because the bridge lists body composition.** The audited paths have explicit missing/rejected impedance evidence.
4. **For immediate local automation, accept a well-supported scalar-impedance scale if segmental ownership is not essential.** Clearly label open-model estimates; do not present them as 30 independent measurements.
5. **For regional data, keep the JEETIF codec as an engineering lead, not yet a broad retail recommendation.** Vendor-equivalent composition remains closed; normal export needs careful verification.
6. **Keep MG's official ECG workflow if that capability matters.** No open clone with equivalent medical functionality was established.
7. **If the main concern is metabolic disease, prioritize appropriate clinical evaluation over collecting branded wellness scores.** That answers a different question from reproducing a score.

### What is genuinely still missing

| Requirement | Status after this pass |
|---|---|
| Open local weight and scalar impedance acquisition | Established software routes, exact-model dependent |
| Ten regional impedance readings from a documented unit | Strong specific codec lead; not broadly hardware-verified |
| Released integrated segmental archive/model/dashboard | Pieces exist; integration and provenance still need work |
| Open calibrated multi-frequency hardware | Research designs exist; not a consumer-equivalent system |
| Open consumer ESC device with appropriate human validation | Not established |
| Exact open Glucose Resilience/Heart Age implementation | Not established |
| End-to-end validated BodyScan 2 replacement | Not established |
| Subscription-free export for every new Withings account | No longer a defensible blanket claim |

**Bottom line:** deeper inspection improved the case for local data ownership but weakened several apparent scale-compatibility claims. The most useful next step is not another broad repository count—it is a matched-device capture and a provenance-preserving exporter. Until that exists, buy based on verified fields and the actual account-level subscription policy, not metric counts.
