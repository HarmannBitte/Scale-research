# Withings BodyScan 2 — Complete Dissection
### Hardware, sensors, every biomarker, the subscription anatomy, and how it stacks up against everything else on the market
*Compiled October 17, 2026. Sources: Withings (product pages, support FAQ, press releases), The Verge, Wired, Tom's Guide, TechRadar, CNET, Engadget, MacRumors, PCMag, Wareable, PR Newswire, and others.*

---

## 1. What it is, exactly

The BodyScan 2 is Withings' flagship "Longevity Station" — a bathroom scale with a retractable, wired handle that turns a 30–90 second weigh-in into a multi-system health assessment. Announced at **CES 2026** (Jan 5), released in the **EU June 9, 2026** and the **US July 15–20, 2026**. It is a CES 2026 Innovation Award honoree and was named one of **TIME's Best Inventions of 2026** (Oct 2026). FSA/HSA eligible in the US.

| | |
|---|---|
| **Price** | $599.95 US / €499.95 / £449.95 / AU$899 |
| **Positioning** | "World's first science-backed longevity station"; explicitly marketed for the **GLP-1 era** (muscle preservation on Ozempic et al.), perimenopause/menopause, midlife visceral fat gain, stress, athletic training |
| **Claim** | 60+ biomarkers in ~90 seconds, "99% DEXA correlation" on fat mass, developed with cardiometabolic research centers |
| **Lineup context** | Replaces/above Body Scan 1 (2023, 40+ biomarkers). Sits above new **BodyFit** (2026, 40+ biomarkers, handle, no ECG/SpO2), Body Comp (~$210), Body Smart (~$100–130) |

---

## 2. Hardware dissection — every sensor and component

### Physical build
| Component | Detail |
|---|---|
| Platform | Single sheet of high-strength **tempered glass** with large-format **ITO (indium tin oxide) electrode** layer; black/blue striped pattern with foot-placement grid |
| Chassis | **Reinforced aluminum** frame |
| Dimensions | 325 × 357 × 18.5 mm (12.8 × 14.1 × 0.7 in) |
| Weight | ~5.4 kg / 11.9 lb (per TechRadar) |
| Capacity | **5–200 kg (up to 440 lb)** |
| Weight precision | **50 g / 0.1 lb** increments |
| Handle | **Smart retractable handle** on a cable with **automatic locking mechanism**, **auto-stopper** (tangle-free), **haptic guidance** (vibrates to guide hand placement), built-in display + buttons |
| Display | **Color LCD in the handle**, 640×172 px, ~3.2–3.5" ultra-wide (sources vary on diagonal); results visible live during the scan (display moved from base, where it was on Body Scan 1, up to the handle) |
| Controls | **2 thumb buttons** on the handle — double as electrode contacts and interactive buttons for **in-scan lifestyle surveys** and measurement control |
| Battery | Rechargeable **Li-ion, USB-C**; "up to 15 months" per press/CNET, "up to 1 year" per product page |
| Connectivity | **Wi-Fi + Bluetooth** (auto-sync to Withings app); iOS 18+, Android 12+; 100+ partner apps incl. Apple Health, Google Health Connect |
| Users | **8 users**, automatic recognition; Athlete, Pregnancy, Baby (weigh-hold), Pet, Luggage, Weight-Only, and Eyes-Closed modes |
| Privacy | GDPR + HIPAA compliant; **ISO 27001 and ISO 27701** certified |

### The sensor stack — 5 measurement technologies + position system

**1. Electrodes — 12 total (8 + 4)**
- **8 ITO electrodes** embedded in the glass platform (foot contact, "all foot sizes")
- **4 stainless-steel electrodes** in the handle (hand/thumb contact)
- Together they create a **full-body current circuit (hands → feet)**, which is the core accuracy claim vs. foot-only scales: foot-to-foot BIA only measures the lower body and extrapolates; hand+foot measures each segment through the actual current path.

**2. Four weight sensors (load cells)** — precise weight to 50 g, plus the **patented Position Control™ body-position detector** (verifies you're standing correctly before weighing — a Withings staple since 2009).

**3. Multi-frequency Bioimpedance Spectroscopy (BIS) — the big upgrade**
- **13 frequencies, up to 800 kHz** (proprietary). For comparison: Body Scan 1 = 3 frequencies to 250 kHz; typical $30 scales = 1–2 frequencies at 50 kHz; clinical multi-frequency body-composition devices (6-frequency, e.g. InBody lab units) cost **$17,000+**.
- Low frequencies flow around cell membranes (extracellular water); high frequencies penetrate cells (intracellular water) → independent fat mass, muscle mass, and water readings **per body segment**.
- Powers: segmental body composition, hydration, body-fluid balance, visceral fat index, and the "cellular health" outputs (cellular age, active cell mass/ACM, metabolic efficiency).

**4. 6-lead ECG (electrocardiogram)**
- Taken via handle + foot electrodes (limb leads configuration). 12-second rhythm strip.
- **AFib detection** — a *medically regulated* feature, live in EU and US. Enabled by **Withings Scan Monitor 2.0**, the FDA-cleared **software** (510(k) **K230812**) — note: the clearance covers the software, not the BodyScan 2 hardware itself. ECG was ~24h post-setup before activation in one US review (device provisioning/verification).

**5. Impedance Cardiography (ICG) — first time on a home scale**
- Captures the **mechanical** signal of each heartbeat (timing of electrical vs. mechanical events): how fast the heart reacts to each beat (**Cardio Responsiveness**) and how long it spends pumping (**Cardio Efficiency**).
- Used for: Cardio Responsiveness score, Cardio Efficiency score, and the subscription-gated **Heart Age**.
- This is the "heart pumping performance" pillar — stroke-volume-ish mechanics rather than just rhythm.

**6. Pulse Wave Velocity (PWV)** — the same principle as the original Body Scan's FDA-cleared vascular-age measurement: times the pressure wave between arm and leg electrodes → **arterial stiffness, arterial elasticity, Vascular Age** (mapped across body zones on BS2).

**7. Multi-wave PPG (photoplethysmography) — new, handle-mounted**
- Red + infrared LEDs shine through the **thumb** vessels; oxygen-rich vs. oxygen-poor blood absorbs light differently → **SpO₂ (blood oxygen)**. Same principle as smartwatch pulse ox. ~30-second measurement. Exclusive to BodyScan 2.

**8. Electrodermal Skin Conductance (ESC / EDA) — sudomotor testing**
- A tiny safe current **stimulates the sweat glands in the feet**; the scale measures the maximum activity response (galvanic skin response).
- High gland activity = healthy small-nerve function; low activity can indicate early small-fiber neuropathy (relevant to diabetes — Withings says they've seen correlation in users with poorly controlled diabetes).
- Powers the **Nerve Response Score** (hands and feet) and feeds **Glucose Resilience**.
- Withings is careful to call this a *wellness-tier* score, not a diagnostic (it's a neuropathy-screen adjacent idea; FDA would treat a diagnostic claim very differently).

**What is NOT in the box:** no cuff-based blood pressure (the "hypertension" feature is an AI risk model, not a BP measurement), no continuous glucose sensing (Glucose Resilience is not blood glucose), no direct body temperature, no scale-based sleep tracking.

---

## 3. The complete biomarker & feature inventory

### What is *directly measured*
| Measurement | How |
|---|---|
| Weight (50 g) | 4 load cells |
| Body position | Position Control™ detector |
| Impedance spectra (13 freqs, 800 kHz) | 12-electrode BIS |
| 6-lead ECG rhythm strip | Handle + foot electrodes |
| SpO₂ | Multi-wave PPG (thumb) |
| Pulse wave transit time | PWV (arm–leg) |
| Standing heart rate | ECG/BIA circuit |
| Electrodermal skin conductance (feet) | ESC stimulation |
| Air quality & weather | Environmental/feed data shown on-device (not body sensors) |

### What is *derived* (algorithms on top of the raw signals)
**Body composition (whole body + 6 segments: right arm, left arm, trunk, right leg, left leg, core/abdomen):**
- Fat mass (kg, %) — "99% DEXA correlation" claim
- Muscle mass (kg, %), skeletal muscle mass
- Body water / total body water %, body-fluid balance, hydration level
- Bone mass
- Visceral Fat Index + trend
- BMI
- Basal Metabolic Rate (BMR), caloric intake optimization
- Protein, subcutaneous fat (standard BIA-derived set)

**Cardiovascular:**
- Vascular Age + arterial elasticity / early arterial stiffness (PWV)
- Heart Age (ICG timing markers: Responsiveness + Efficiency) — *Withings+ gated*
- Cardio Responsiveness (score), Cardio Efficiency (score)
- AFib detection + rhythm analysis (6-lead ECG)
- **Hypertension risk notifications** — exclusive clinically-validated AI model (no cuff). **EU: medical-grade score. US: "Blood Pressure Insights" wellness score** (regulatory path differs)
- Standing heart rate

**Metabolic & cellular:**
- Metabolic Age
- Cellular age, Active Cell Mass (ACM), metabolic efficiency (ultra-high-frequency BIS)
- **Glucose Resilience score** — early signs of glycemic dysregulation. Built from **two inputs: visceral fat level + electrodermal skin conductance** (nerve health). *Explicitly does NOT measure blood glucose.* Wellness-only claim. Withings+ exclusive, rolling out H2 2026 (before end of 2026)

**Nerve health:**
- **Nerve Response Score (NRS)** — hands and feet, wellness tier, EU + US

**Composite scores & software features:**
- **Health Trajectory** — single "predicted years of healthy life" / healthspan score synthesizing all biomarkers
- **BodyPath** & **Body Profile** — metabolic journey/segmental evolution views (Withings+ exclusive per Withings staff)
- **Longevity Intelligence, Body Intelligence, Lifestyle Intelligence** — the new "Health Tab" intelligence tiers (all three on BodyScan 2; BodyFit lacks Longevity Intelligence) — Withings+ unlocked
- AI-powered coaching & insights (HealthSense/Withings Intelligence 24/7 Health Assistant), in-scan lifestyle surveys via handle buttons
- Daily Scan vs. Longevity Scan workflows (below)
- PDF/CSV export, HealthLink doctor-sharing dashboard, lifetime data storage (free)

### Scan modes
| Mode | Duration | Contents |
|---|---|---|
| **Daily Scan** | ~30 s | Weight (50 g), fat/muscle/water (kg, %, trends), Visceral Fat Index + trend, heart rate, Vascular Age (PWV) — some also list SpO₂ here; metrics customizable in-app |
| **Longevity Scan** | ~90 s | Everything in Daily Scan **+ 6-lead ECG, Heart Age, SpO₂, Nerve Response Score** — designed as a **weekly** deep assessment |
| Custom | — | User chooses which metrics the automatic scan collects |

---

## 4. Free vs. Withings+ — the paywall anatomy

**Withings+: $9.95/month or $99.50/year** (website; App Store lists $9.99/$99.99 — pricing varies slightly by channel). 1 month free with device purchase (14-day trial if subscribing in-app). Includes "Withings+ Protect" premium warranty — the US PR goes as far as calling it a **"Lifetime Guarantee"** for BodyScan 2 buyers.

### Free, forever (no sub):
All raw measurements and recordings — weight, all body composition incl. 6-zone segmental, ECG recordings with basic rhythm labels, SpO₂, NRS, Vascular Age, PWV, heart rate, trends/visualizations, unlimited lifetime storage, Health goals, symptom logging, **CSV & PDF export of full history**, HealthLink doctor sharing, product sharing, and **import** from other apps.

### Locked behind Withings+ (per Withings' own product pages & staff):
| Gated feature | What it actually is |
|---|---|
| **Heart Age** | ICG-derived headline score (product page footnote: "only available with a Withings+ subscription") |
| **Glucose Resilience** | The metabolic score (launching H2 2026) |
| **BodyPath / Body Profile** | Journey views (per Withings staff on Reddit) |
| **Health Tab Intelligence tiers** | Longevity / Body / Lifestyle Intelligence |
| **AI Health Assistant** | "Withings Intelligence" 24/7 assistant that remembers your profile & trends |
| **Health Improvement Score, Readiness (daily energy) score** | Aggregate scores |
| **Cardio Check-Up** | **Your ECG reviewed by a board-certified cardiologist within ~24h** (4 included per year on device product pages) |
| **Clinical extras** | 1 live nutritionist video session; Sleep Clinic assessment (upon eligibility) |
| **Health Trajectory** | The longevity score (listed as Withings+ on reseller/retailer pages; wording has shifted — verify at purchase) |
| **Withings+ Protect** | Extended/premium warranty |
| **⚠️ Automatic third-party sync** | **NEW as of Oct 13, 2026** — see below |

### The October 13, 2026 bombshell (4 days old)
Withings now requires Withings+ for **automatic sync to Apple Health, Google Health/Health Connect, MyFitnessPal, Samsung Health, etc.** for **any account created on or after Oct 13, 2026**. Details:

- Accounts created **on or before Oct 12, 2026 keep free sync forever** — and it's tied to the *account*, so old users can buy new hardware and keep it.
- New users' sync **pauses** (not deletes) after the 1-month trial; data already exported stays in Apple Health.
- Manual **CSV/PDF export stays free**; data *import* into Withings stays free ("Your data stays free" is the marketing line — the *pipe* is not).
- Withings' justification: the rollout of its "AI Connector" and API/privacy changes; the Partner Hub says Withings+ "becomes required on the Start for Free API plan" — meaning **third-party app developers** also face the paywall (or must buy an Enterprise plan). A Strava exception was reported in France.
- Reception: exactly what you'd expect — user forums, MacRumors, The Verge, PCMag, Android Authority all ran "users are rightfully mad" coverage. One outlet's phrase: **"egress fees for your body."**

**Genuine ambiguity to know before buying:** Heart Age's gating has been inconsistent in the wild — some US reviewers saw Heart Age appear without a "+" marker once their ECG activated. Withings' official word (product pages, German site, staff replies) is Heart Age + Glucose Resilience are **Withings+ exclusive scores**. Budget as if you'll want the sub for year one.

---

## 5. Competitive landscape

### Smart scales (the direct field)

| Device | Price | Handle / segmental | Electrodes | BIA freq. | ECG | SpO₂ | Other standout | Subscription |
|---|---|---|---|---|---|---|---|---|
| **Withings BodyScan 2** | $599.95 | Yes, 6 zones | 12 (8 ITO + 4 steel) | 13, ≤800 kHz | 6-lead + AFib (regulated) | ✅ PPG | ICG, PWV, ESC/nerve score, hypertension AI, Health Trajectory | Optional **Withings+ $99.50/yr**; key scores gated; **sync paywalled for new accounts** |
| Withings Body Scan 1 | $399–499.95 | Yes, 6 zones | 8 | 3, ≤250 kHz | 6-lead + AFib | ❌ | PWV, NRS | Same W+ story |
| Withings BodyFit (2026) | ~$200s (see site) | Yes, 6 zones | handle + base | multi-freq | ❌ | ❌ | 40+ biomarkers, PWV, GLP-1-era marketing; no Longevity Intelligence | W+ for intelligence tiers |
| Withings Body Comp | ~$210 | ❌ foot-only | 4 | multi-freq | ❌ | ❌ | NRS, Vascular Age | Same |
| **Hume Health Body Pod 2.0** | $249 (sale) / $379 | Yes (4 foot + 4 handle) | 8 | multi-freq | ❌ | ❌ | 45 metrics, 3D body scan "digital twin", 24 users, Bluetooth only | Optional **Hume Plus $9.99/mo** (coaching, weekly report, nutrition) |
| **Wyze Scale Ultra BodyScan** | $119.98 | Yes, arms/legs/torso | 8 (handle) | dual-freq | ❌ | ❌ | 4.3" color TFT, Wi-Fi + BT, 13 metrics, DEXA correlation claims ≥0.98/0.99, FSA/HSA | **None** |
| **Wyze Scale BodyScan** | $79.98 | Yes | 8 (handle) | dual-freq | ❌ | ❌ | 17 metrics, 4.7" LED, BT only | None |
| InBody Dial H20 / H30 | ~$299 / ~$379 | Yes | 8 | multi-freq (pro-grade) | ❌ | ❌ | Clinical-lineage accuracy; limited app/eco | None |
| Renpho MorphoScan Nova | $199.99 | Yes (8-electrode) | 8 | multi-freq | ❌ | ❌ | Renpho's flagship | None (app free) |
| Arboleaf CS10P | $129.99 | Yes | 8 | multi-freq | ❌ | ❌ | Value segmental | None |
| Garmin Index S2 | $149.99 | ❌ foot-only | 4 | basic | ❌ | ❌ | Garmin Connect ecosystem, Wi-Fi. **No Index S3 yet** (missed expected 2025 refresh; still nothing at CES 2026) | None |
| Eufy Smart Scale P3 / P2 Pro | ~$80–99 / ~$50 | ❌ foot-only | 4 (full-plate ITO) | basic | ❌ | ❌ | Big display, 3D body model, unlimited users | None |
| Renpho Elis / ES-CS20M | $25–50 | ❌ | 4 | basic | ❌ | ❌ | Best-seller budget; 13 metrics | None |
| QardiioBase X, Omron, Tanita, Fitbit Aria 2 | $100–250 | ❌ | 4 | basic–multi | ❌ | ❌ | Various | None |

**Takeaway:** Nobody else combines **ICG + 6-lead ECG + PWV + SpO₂ + ESC + 13-frequency BIS** in one home device. But on the *body composition* half alone, **Wyze at $120 and Hume at $249 deliver the same handle-based segmental idea**, and InBody delivers lab-lineage composition without any cardio features. Withings' true moat is the **cardiometabolic breadth** and the **regulated ECG/AFib software** — not the fat/muscle numbers.

### Adjacent wearables & the "longevity stack" (what people cross-shop)

| Device | Hardware | Subscription | What's locked behind it |
|---|---|---|---|
| Oura Ring 5 | $399–499 | **$5.99/mo, $69.99/yr** | ~Everything insightful: detailed sleep stages, HRV trends, temperature illness detection, Oura Advisor. ~94% of ring buyers convert. Free tier = 3 daily scores only |
| WHOOP 5.0 / MG | Included in sub | **$199 / $239 / $359 per year** (One/Peak/Life) | The membership *is* the product. ECG + Blood Pressure Insights only on the $359 Life tier. Stop paying → band is a bracelet |
| Google Health Premium (ex-Fitbit Premium) | Pixel Watch 5 $399, Fitbit Air $99 | **$9.99/mo, $99.99/yr** (up $20 in 2026) | Gemini Health Coach, adaptive plans, deep sleep insights, Sleep Profile. Free tier relatively generous (stages, HR, steps) |
| Eight Sleep Pod 5/6 | $2,999+ (cover) | **$199–399/yr Autopilot, REQUIRED 12 months** | Temperature automation, sleep reports, HRV; warranty tied to active plan. Without it: manual controls only |
| Apple Watch Series 11/12 | $329–449 | **None** | — |
| Garmin watches | $300–1,200 | **None** for core (Connect+ optional $6.99/mo for AI extras) | — |
| Samsung Galaxy Ring/Watch | $399 | **None** | — |
| Withings ScanWatch 2 / Sleep pad | $370 / $200 | **None required** (W+ optional) | — |
| Huawei watches | varies | Health+ €7.99/mo (France-first) | Premium insights/content |
| CGM programs (Levels, Nutrisense, January AI) | sensor consumables | ~$89–400/mo | The glucose data itself |
| Lab panels (Function Health $365/yr, Superpower $349/yr) | blood draws | annual | 150–160+ biomarkers, care team |

---

## 6. What "they" want people to pay subscriptions for

Across the industry, the recurring revenue is extracted from **seven plays** — roughly in order of how legitimate the cost behind them is:

**1. The interpretation layer (the big one).** Raw numbers are free; *meaning* costs money. Scores, biological/heart/vascular/cellular age, readiness, healthspan trajectories, AI coaches (Withings Intelligence, Oura Advisor, Gemini Health Coach, WHOOP coaching). This is the highest-margin layer — a model on top of data you generated — and it's exactly where BodyScan 2 puts Heart Age, Glucose Resilience, BodyPath, and Health Trajectory. It's also genuinely where ongoing cost lives: model development, AI inference, clinical validation.

**2. The headline features of hardware you already bought.** The harshest pattern: Oura locks sleep-stage detail behind $6/mo; WHOOP puts ECG/BP on the $359 tier; Withings puts *two of the five CES-launch pillars* (Heart Age, Glucose Resilience) behind W+. You paid $600 for a "longevity station"; the longevity score is à la carte.

**3. Clinical services — the most defensible.** A **board-certified cardiologist reading your ECG within 24 hours** (Withings Cardio Check-Up), nutritionist video sessions, sleep-clinic triage, clinician-reviewed blood panels (WHOOP Advanced Labs, Function, Superpower), prescription-adjacent CGM programs. Real humans, real liability, real cost. If you're paying a health-tech subscription, this is the part with clear counterparty value.

**4. Data egress & ecosystem access — the newest and ugliest.** Withings' Oct 13, 2026 move: **$99.50/year to push your own weigh-ins into Apple Health.** Not new measurement, not interpretation — a sync pipe that has been free for 15 years, now rent-seeking behind an "AI Connector" justification. Third-party app developers face the same toll (free API plan requires W+, or buy Enterprise). This is the play to watch: if it sticks for Withings, expect Garmin/Samsung holdouts to look noble and expect others to copy it. (Apple Health *import* into Withings stays free — the data flows toward them for free and away for cash.)

**5. Warranty & insurance bundling.** Withings+ Protect ("Lifetime Guarantee" on BodyScan 2), Eight Sleep tying warranty tiers to Autopilot. Turns a support cost into recurring revenue while sounding like a perk.

**6. Hardware-as-a-service.** WHOOP's pure subscription model and Eight Sleep's mandatory first-year Autopilot reframe the device as an ongoing service. Useful for affordability (no big upfront), but the 3-year math is brutal: WHOOP Life = $1,077 and you own nothing; Oura Ring 5 + membership = ~$609 over 3 years.

**7. Content & community.** Workout libraries, mindfulness, challenges (Google Health Premium, Peloton App+, Apple Fitness+ at $9.99/mo). Cheap to marginalize; mostly filler padding the price justification of tiers above.

**Why the industry does this:** hardware margins are one-time; Wall Street pays for recurring revenue; "longevity/prevention" is a narrative that *implies* ongoing service (you don't prevent once); AI + clinical review + regulatory work (FDA/CE) are real ongoing costs; and a locked data silo raises switching costs — the longer your history is in Health Mate/Oura/Whoop, the more painful leaving gets. The Oct 13 sync paywall is the purest expression yet: **your historical data gravity is the product.**

**Where the market is pushing back:** Garmin, Apple, and Samsung remain subscription-free for core tracking; Google's free tier is still decent; Wyze/Renpho/Eufy/InBody scales have no subs at all; Ultrahuman/Samsung rings market "no membership" explicitly. There's a real segment of buyers now filtering on "no subscription" first.

---

## 7. Honest critical notes (what the marketing glosses over)

1. **"99% DEXA correlation" ≠ DEXA agreement.** Correlation measures whether numbers move together, not whether they match. Wyze claims ≥0.98/0.99 DEXA correlation at $120. Independent testing shows BIA body fat runs within ~2–4% of DEXA for typical users but **overestimates by 20–35% for very lean (<15% fat) athletes** — structural to BIA, not calibration. Treat composition as **trend data**, not absolute truth.
2. **Volatile readings.** Tom's Guide saw body fat swing 6.8–8.7% across five weigh-ins; TechRadar got Vascular Age "4 years older" then "1 year older" a week apart. Hydration, meals, exercise, skin temp, and dry skin all move BIA (moist hands/feet help).
3. **Several "biomarkers" are model outputs, not measurements.** Heart Age, Vascular/Metabolic/Cellular Age, Glucose Resilience (visceral fat + foot sweat conductance!), NRS, Health Trajectory — algorithmic, mostly proprietary, with limited published peer-reviewed validation. Wired's reviewer on the NRS: *"I'm still not sure how my nerve response score could possibly be of any real, clinical use."*
4. **Regulatory split-dressing.** The FDA clearance is for the **Scan Monitor 2.0 software** (K230812), not the scale. Hypertension is a *risk notification* (EU medical / US wellness), not a BP measurement. Glucose Resilience explicitly is **not** blood glucose. Fine print: "not a medical device for diagnostic purposes."
5. **Features shipped on a promise.** Glucose Resilience and parts of the intelligence suite rolled out (or are still rolling out) through H2 2026 after launch; early adopters bought ahead of features. Firmware v1161 post-launch fixed sync/accuracy issues.
6. **Battery claims vs. reality.** 15 months/1 year rated; the Body Scan 1 was rated ~12 months but some users reported 3–4 weeks in real use. Wait for owner reports before trusting BS2 longevity.
7. **The subscription math on a $600 scale.** If you want Heart Age + Glucose Resilience + sync to Apple Health (new account): **$600 + $99.50/yr forever.** 5-year ownership ≈ $1,100. That's Oura/WHOOP money for a device that lives on the floor.

---

## 8. Bottom line — who should buy what

| You are... | Buy |
|---|---|
| Cardiometabolic risk (family history, AFib worry, midlife, GLP-1 user protecting muscle) and want the broadest at-home screen that exists | **BodyScan 2**, ideally creating your account with eyes open about W+ ($600 + ~$99/yr if you want the scores and sync) |
| Just want accurate weight + solid segmental composition trends | **Wyze Scale Ultra BodyScan ($120)** or **Hume Body Pod ($249)** — 80–90% of the body-comp value at 20–40% of the price; Hume's sub is optional |
| Serious about composition accuracy and don't care about heart metrics | **InBody Dial H30** (or a periodic clinical DEXA at $49–200 for benchmarks) |
| Deep in Garmin/Apple/Samsung ecosystems | **Garmin Index S2 / any scale that syncs free** — and beware: a Withings account created today pays to reach Apple Health |
| Want longevity/recovery insight, not a scale | Oura Ring 5 ($70/yr) or WHOOP ($199–359/yr, hardware included) — or Apple Watch/Garmin/Apple Watch with zero sub |
| Hate subscriptions on principle | Garmin Index S2, Wyze, Renpho, Eufy, InBody, Samsung, Apple — the market has never had more credible no-sub options |

**The one-move advice if you buy the BodyScan 2:** create your Withings account and register the device immediately (even before unboxing the scale), so your account exists — the free-sync grandfathering and the free month of W+ both key off account/device setup timing; and set a calendar reminder to decide on W+ before the trial converts.

---

### Quick spec recap
```
Sensors:    4 load cells (50g) | 12 electrodes (8 ITO + 4 steel) | 13-freq BIS ≤800kHz
            6-lead ECG | ICG | PWV | multi-wave PPG (SpO2) | ESC (foot sweat glands)
            Position Control™ detector | haptics in handle
Scan:       Daily ~30s | Longevity ~90s | customizable | 60+ biomarkers, 6 body zones
Body:       325×357×18.5mm | ~5.4kg | 5–200kg capacity | aluminum + tempered glass
            3.2–3.5" 640×172 color LCD in handle | 2 buttons | retractable locking handle
Power:      USB-C Li-ion, up to 12–15 months
Connect:    Wi-Fi + BT | 8 users | iOS 18+/Android 12+ | GDPR/HIPAA/ISO 27001/27701
Price:      $599.95 / €499.95 / £449.95 / AU$899 | FSA/HSA (US)
Sub:        Withings+ $9.95/mo or $99.50/yr — gates Heart Age, Glucose Resilience,
            BodyPath/Profile, AI Assistant, Intelligence tiers, Cardio Check-Up,
            and (for accounts from Oct 13, 2026) automatic Apple Health/Google sync
```
