# Pass 5 — alternatives when you have no Withings account

**October 17, 2026.** User-specific constraint: you do not have a Withings account. Under the currently announced policy, a new account does not qualify for grandfathered free automatic third-party sync. This report concentrates on practical alternatives rather than repeating the research-instrument catalogue.

**No physical hardware, phone pairing or WHOOP integration was tested.** Evidence below separates released source, vendor documentation, supplied-fixture tests and experimental compatibility claims.

## Executive result

The shortlist improves materially in this pass:

1. **Beurer BF1000 + openScale is a concrete released regional-composition route.** I inspected both the current code and the actual v3.1.3 release tag: five regional fat percentages and five regional muscle percentages are decoded and attached to records. This is not merely a generic segmental data model or an unmerged Hume proposal.
2. **Tanita BC-601/603 SD-card scales offer a simpler account-free alternative.** They preserve manufacturer-derived regional results on removable storage. This bypasses both cloud accounts and BLE reverse engineering, at the expense of automatic syncing and broad-band/raw impedance access.
3. **Hume has a newer local Home Assistant dashboard, but its regional calculations are not what they appear.** I ran its nine standalone protocol/model tests successfully, then confirmed by counterfactual execution that changing high-frequency impedance or redistributing arm impedances while preserving their sum changes none of its 39 composition outputs. It is also restrictively source-available, not unrestricted open source.
4. **Keep S3 and Dr.Trust have further protocol leads in openScale.** They demonstrate more implemented acquisition than a brand-only list reveals, but do not establish a complete open BodyScan replacement.

My recommendation now distinguishes **owning regional vendor results** from **owning raw regional signals and the physiological model**. The former is substantially easier.

---

## 1. Beurer BF1000 + openScale: strongest new released Android candidate

### Hardware

Manufacturer identifies **BF 1000 Super Precision**, article **74860**, EAN **4211125748609**:

- eight electrodes for hands/feet and cross-body measurements;
- segmented fat and muscle percentage display;
- weight, body water, bone estimates, visceral-fat indicator and calculated energy requirements;
- Bluetooth transfer;
- 200-kg capacity and 50-g weight graduation;
- raised column/display, rather than the compact retractable-handle form of BodyScan. [1](https://www.beurer.com/global/p/74860/)

These are manufacturer specifications, not independent accuracy findings. Graduation is not an accuracy guarantee. No verified excitation-frequency count is asserted here.

### What I verified in the released software

openScale **v3.1.3**, released September 6, lists BF1000 support and segmental data. I fetched the tag and inspected its actual files rather than infer compatibility from those two release-note bullets. [2](https://github.com/oliexdev/openScale/releases/tag/v3.1.3)

Verified tag commit:

```text
7ebb55bea94836cd070a9c2eabed6d4bc2afc73b
```

At that tag:

- `BeurerBf1000Lib.kt` decodes private fat/visceral and muscle packets.
- `StandardBeurerSanitasHandler.kt` subscribes to private characteristics, buffers the values and attaches them to the corresponding measurement.
- Five fat and five muscle values have explicit device-specific percentage keys.
- `BeurerBf1000LibTest.kt` contains captured-packet fixtures for both packet types and malformed packets.

Pinned source:

- [Decoder](https://github.com/oliexdev/openScale/blob/v3.1.3/android_app/app/src/main/java/com/health/openscale/core/bluetooth/libs/BeurerBf1000Lib.kt)
- [Integrated handler](https://github.com/oliexdev/openScale/blob/v3.1.3/android_app/app/src/main/java/com/health/openscale/core/bluetooth/scales/StandardBeurerSanitasHandler.kt)
- [Fixture tests](https://github.com/oliexdev/openScale/blob/v3.1.3/android_app/app/src/test/java/com/health/openscale/core/bluetooth/libs/BeurerBf1000LibTest.kt)

The parser file is byte-identical between the inspected release tag and the current cloned snapshot. The inspected code has GPL licensing headers.

### What this solves—and does not

| Requirement | BF1000 + openScale finding |
|---|---|
| Local collection without Withings | Yes, implemented Bluetooth route |
| Open collector/dashboard | GPL openScale |
| Five regional fat and muscle outputs | Explicitly decoded in released handler |
| Manufacturer-derived composition | Yes; these are results produced by scale firmware |
| Entire physiological model open | No; open collector does not open proprietary scale firmware |
| Ten raw segment × frequency impedances | Not established in this decoder |
| Regional muscle in kilograms | Reviewed private decoder exposes percentages; do not invent kg by multiplying by total weight |
| ECG/ICG/PWV/ESC/SpO2 | Not established for this device |
| Automatic transfer into WHOOP | Not tested or established by this route |

**Setup caveat:** Beurer's user slots/consent-code workflow can matter. openScale documents how to create or link a user, and warns that forgotten codes can require resetting/recreating scale users. That is local pairing state, not necessarily a cloud-account requirement. I have not verified new-out-of-box BF1000 provisioning. [5](https://github.com/oliexdev/openScale/wiki/Frequently-Asked-Questions-(FAQ))

**Testing limitation:** Kotlin/JVM fixtures were inspected, not executed here. This sandbox lacks the appropriate Android build environment; I am not claiming the release APK or live BLE path was tested.

### Purchase context

An Amazon US listing exists, but I did not verify a dependable US delivered price, domestic warranty or inventory. European/UK listings vary widely. Do not treat an imported listing as an equivalent US-warranty offer. Exact BF1000/article identity and a return policy matter more than a nominal discount. [2](https://www.amazon.com/Beurer-Composition-Management-Measurement-Calculator/dp/B07H46XKR5)

**Verdict:** first model I would investigate for **released open Android collection of vendor regional results**. This is a meaningful improvement over the prior engineering-only shortlist—not a full open BodyScan 2 replica.

---

## 2. Tanita BC-601 / BC-603FS: data ownership without BLE or an account

### The unusually useful feature is removable storage

Tanita's official BC-601 documentation identifies single-frequency BIA, five-region fat percentages and muscle masses, and SD-card transfer. The European page identifies model **BC-601 CG**, SKU **BC601CG21**. [9](https://tanita.eu/bc-601)

The US **BC-601FS** page listed **$245.99**, single frequency and SD output, but was **sold out** when fetched. Its linked manual appears mismatched, so use the combined 601FS/603FS manual linked from the 603FS page instead. [2](https://tanita.com/products/bc601fsb)

The US **BC-603FS** page listed **$245.99** with **Add to Cart**, explicitly describes regional fat/muscle and SD-card storage/transfer, and says connectivity is “None.” That is a current page observation, not a stock/shipping guarantee. [Official BC-603FS page](https://tanita.com/products/bc-603f-fitscan-segmental-body-composition-monitor)

### Why it matters for you

```text
Scale -> SD-card files -> local parser/archive/dashboard
```

No Withings account, partner-sync entitlement or proprietary cloud endpoint is required for this file-based route. It is manually operated unless you build additional infrastructure; I am not recommending an unverified wireless SD-card hack.

The official combined manual describes **measurement of weight and impedance** and **estimation** of the composition metrics. It also defines the muscle metric broadly as skeletal and smooth muscle, not simply pure skeletal muscle mass. Preserve that distinction when comparing it with DXA or another app's “muscle” field. [Combined manual](https://cdn.shopify.com/s/files/1/0835/0462/7999/files/BC-601FS_603FS_Manual_R02.pdf?v=1747675039)

### Actual open parsing resources

**gasperinm/tanita-csv-backup — MIT.** Browser-based conversion of the scale's DATA files into a more readable CSV. Small old project, five visible commits, latest in 2020; not a maintained health platform. Its use of JavaScript dependencies means inspect/download the assets for a genuinely offline workflow. I did not execute it on a real SD file. [11](https://github.com/gasperinm/tanita-csv-backup)

**cab938/tanita — format documentation.** Explains per-user data/profile paths and alternating field-key/value rows. Despite the name, the reviewed repository contains README/license, not a complete maintained parsing application. It documents BC-603FS files that identify themselves as BC-601. Several muscle fields are labelled percent in its README; the official manual/product describes muscle mass, so that mapping needs unit verification against a paired display/file sample. [5](https://github.com/cab938/tanita)

**2013 BC-601 shell script — historical reference only.** Shows that file extraction predates cloud apps. It uses positional columns and should not be treated as a reliable universal importer or assumed open-licensed code. [1](https://trinitor.de/tanita_scale_script/)

### Trade-offs

- Closed manufacturer composition algorithms still run inside the scale.
- Single-frequency BC-601 is not a 13-frequency BIS instrument. Do not assume the 603FS has different frequency capability without its specifications.
- The reviewed data mappings do not establish raw resistance/reactance or per-frequency regional impedance export.
- SD extraction is less convenient than automatic Wi-Fi sync.
- No ECG, ICG, vascular age, ESC or oxygen sensing was established.
- Withings/WHOOP branded scores are not reproduced.

**Verdict:** strongest new **low-lock-in regional-results archive** candidate, particularly the US-listed BC-603FS. It may be more useful than a newer cloud scale if file ownership matters more than automation.

---

## 3. Hume Body Pod Home Assistant integration: useful raw-data lead, misleading model richness

Repository: https://github.com/danfulton72/hume_pod_ha

Inspected version **0.4.1**, commit:

```text
4fdf49a5a5b3e2971fee1ec70ad1243f1bd84b7c
```

### What exists

The project implements local BLE acquisition, multi-person matching, diagnostic raw impedances, a measurement event and a supplied Home Assistant dashboard. README says no Hume account/phone is needed for weigh-ins. It supports active ESPHome Bluetooth proxies. Screenshots are explicitly rendered with sample data. [1](https://github.com/danfulton72/hume_pod_ha)

Maturity caveat: nine visible commits, no tags, and recent real-device changes address weight locking and missing impedance when the handle is not held. This is not equivalent to a long-tested consumer release.

### Licensing is restrictive

`NOTICE` identifies protocol handling, composition equations and dashboard portions derived from Blue2Scale. `BLUE2SCALE_LICENSE` restricts production/public/commercial use and grants personal nonproduction use under a revocable license. README acknowledges the restriction.

Therefore classify as **source-available/personal-use**, not unrestricted open source. Do not assume that installing via a HACS custom repository changes the license or implies inclusion in HACS' default store.

### Nine supplied tests passed, but they do not validate the physiology

Executed:

```bash
python -m pytest --noconftest -o addopts='' -ra tests/test_protocol_bia.py
```

Result: **9 passed**, with two unknown asyncio-config warnings. I deliberately bypassed Home Assistant's conftest/plugin because this file loads the pure protocol/BIA modules directly. **No HA integration, dashboard, Bluetooth or full-suite testing was performed.**

Log: `research-pass-5/hume-protocol-tests.txt`.

### The composition function does not use all the measured information

Inspection of `bia.py` establishes:

- `imp_high` is accepted but unused in the composition function.
- Low-frequency limb values are collapsed into an averaged pathway.
- ECW is a fixed fraction of estimated TBW: 0.37 for male or 0.385 for female profiles; ICW is the remainder.
- Segment weights/fat distributions are assigned using fixed sex-specific proportions.
- Segmental muscle is allocated and normalized from those proportions, not independently estimated from each corresponding limb impedance.
- The visceral-fat indicator depends on BMI and sex, rather than an independently determined abdominal-fat volume.

[Audited model](https://github.com/danfulton72/hume_pod_ha/blob/4fdf49a5a5b3e2971fee1ec70ad1243f1bd84b7c/custom_components/hume_pod/bia.py)

### Counterfactual checks I executed

Using the supplied worked-example profile, I ran the actual function twice more:

| Change | Observed output |
|---|---|
| Replace all five high-frequency impedance inputs with different positive values | **All 39 results unchanged** |
| Increase one arm's low-frequency impedance and decrease the other by the same amount | **All 39 results unchanged**, including regional fat/muscle |

Evidence: `research-pass-5/hume-model-sensitivity.txt`.

These are software dependency checks, not simulated clinical validation. They demonstrate that this model cannot use those changes to detect a high-frequency fluid shift or arm asymmetry. **That says nothing conclusive about the scale hardware or the official Hume app's model.**

### Best use

Potentially useful as a **local raw-data acquisition and archiving reference**, subject to its license and exact-unit validation. Do not buy the scale because this particular dashboard displays 39 physiological outputs or a body map.

The earlier openScale Hume PR also remains incomplete: the maintainer specifically says there is no central impedance-to-composition derivation, and requests actual calculation or corrected capability labels. A contributor reports physical captures, but that is not a released integrated workflow. [PR #1537](https://github.com/oliexdev/openScale/pull/1537)

Absolute frequency labels also require caution: the HA README gives approximately 50/250 kHz, whereas vendor materials elsewhere describe different bands. Decode frequency indices as such until exact hardware evidence resolves the labels.

---

## 4. More narrowly scoped openScale leads

### Keep S3 — dual-frequency and phase parsing deserve attention

The current handler decodes final-record impedance fields labelled **50/100 kHz** and phase fields. It publishes the two composition impedance values when available and calculates composition offline with an SDK-compatible routine. In the inspected current handler, phase values are decoded/logged but **not published**.

The handler and tests exist in the v3.1.3 tree, but I have not compared every current line with the tag or executed the Android tests. This is a source-level lead, not a verified retail recommendation or independent validation of the decoded phase units/frequency labels.

[Handler](https://github.com/oliexdev/openScale/blob/8bddcec182e7996f325a1090932e394a8a512ef5/android_app/app/src/main/java/com/health/openscale/core/bluetooth/scales/KeepS3Handler.kt)

### Dr.Trust SSW532 — regional acquisition is not regional composition

The handler documents eight regional impedance channels, uses selected pathways and `StandardImpedanceLib`, and publishes a derived whole-body impedance/composition record. Raw regional channels in a packet do not establish a five-region normal-export workflow or accurate regional fat/muscle estimation.

[Handler](https://github.com/oliexdev/openScale/blob/8bddcec182e7996f325a1090932e394a8a512ef5/android_app/app/src/main/java/com/health/openscale/core/bluetooth/scales/DrTrustSSW532Handler.kt)

### Omron HBF-702T / KRD-703T — warning against hardware-name inference

The reviewed library recognizes these models but explicitly skips part of the record containing segmental values. Thus a supported hand/foot model is not automatically supported for all regional fields.

[Library](https://github.com/oliexdev/openScale/blob/8bddcec182e7996f325a1090932e394a8a512ef5/android_app/app/src/main/java/com/health/openscale/core/bluetooth/libs/OmronLib.kt)

### Clinical Tanita serial / Bluetooth leads

Additional search results include an old SC-240 USB/Node interface and an MC-780 Bluetooth packet-decoding gist with resistance/reactance-like fields. These concern different clinical hardware, not proof of home RD-545/BC-401 support. Licensing, units, transport and current hardware availability remain unverified. They are research references, not promoted consumer alternatives. [2](https://github.com/eightypop/sc240scale) [4](https://gist.github.com/zapkub/350bb90a0aa70d7c3685522e0b83736c)

---

## 5. Revised comparison for your situation

| Option | Subscription dependency for this route | Regional outputs | Raw/model openness | Main compromise |
|---|---|---|---|---|
| **BF1000 + openScale** | No Withings service involved | Five-region fat/muscle percentages in released code | Open collector; closed device composition | Android, pairing/consent, bulky hardware; US sourcing not verified |
| **BC-603FS SD archive** | No cloud subscription for card transfer | Manufacturer regional fat/muscle | Accessible files; closed device model | Manual transfer; not broad-band spectroscopy |
| **Hume + HA integration** | No vendor account claimed for local collection | Derived body map plus raw diagnostics | Restrictive license; model ignores important raw distinctions | Young integration and weak regional modeling |
| **JEETIF/Fitdays codec** | Local MIT codec | Ten raw regional impedance values on documented unit | Vendor composition binary closed | Exact retail compatibility and integration incomplete |
| **New-account BodyScan 2** | Withings+ for newly announced automatic third-party sync policy | Six-zone vendor estimates plus additional modalities | Closed device/model; cloud export | Hardware plus recurring sync/premium-score cost |

The Withings policy is established by its official staff response; the exact WHOOP connector entitlement still has not been tested. [Policy](https://support.withings.com/hc/en-us/community/posts/51887047154577-Unacceptable-Apple-Health-Sync-is-now-behind-a-99-year-paywall-for-new-accounts)

### What none of these composition alternatives supplies as an integrated equivalent

They do not collectively establish BodyScan 2's complete combination of 13-frequency BIS, six-zone output, ECG/AFib workflow, ICG-derived timing, PWV, ESC/Nerve Response, SpO2 and proprietary wellness scores. MG's official wearable capabilities remain separate; a local archive does not automatically feed WHOOP or reproduce its scores.

### My updated recommendation

- **For practical regional tracking with an open application:** investigate **BF1000 + openScale first**, if Android and the physical design work for you.
- **For account-free data ownership with minimal protocol risk:** investigate **BC-603FS/BC-601 SD transfer first**.
- **For raw regional research:** compare Hume protocol captures with the MIT JEETIF route, but separate acquisition from unvalidated composition and respect the different licenses.
- **For the full integrated advanced-sensor package:** BodyScan 2 remains distinct, but your new-account status means the paid-sync condition must be included in the decision.

Before purchasing either practical candidate, require confirmation of exact model/revision, obtainable local results, correct units, setup without mandatory cloud registration, return rights and warranty. Retain original files and display values for a first paired export. Do not treat BIA-derived water, bone or muscle values as direct clinical measurements.

**Bottom line:** the most promising subscription-free alternative may be a less fashionable scale with a genuinely usable local interface—not a newer scale with more calculated metrics. This pass establishes two substantially more concrete regional-results routes, while also showing why a rich local dashboard can still discard the hardware's most valuable information.
