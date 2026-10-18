# Withings BodyScan 2 — Every Biomarker, How It's Measured & What's Behind Withings+

> **Correction / supersession notice — 17 October 2026:** Read the separate [DXA Capabilities and Open Alternatives Investigation](./DEXA-Capabilities-and-Open-Alternatives-Investigation.md) for the corrected technical comparison. This older document overstates DXA as equation-free “ground truth,” equates lean soft tissue with muscle, wrongly implies DXA is the only accepted BMD method, and does not adequately separate whole-body composition from diagnostic hip/spine examinations. Its generic precision figures, fixed repeat-scan schedule, “BIS protects muscle” wording and permanent personal-offset advice are not supported as universal recommendations. Composition scores are not raw impedance; categorical frequency/“cellular health” explanations should not be treated as validated diagnoses. The new investigation supersedes those passages. **You have no Withings account:** creating one now cannot obtain pre-13-October grandfathering; follow the later pass-4/pass-5 subscription audits instead. Other vendor-specific assertions below have not all been revalidated by the DXA investigation.

### Plus: 13-Frequency Bioimpedance Spectroscopy (800 kHz) Explained + Honest DEXA Comparison
*For BodyScan 2 Longevity Station — Current as of Oct 17, 2026 | EU launch June 9, 2026 · US July 15-20, 2026 · $599.95 / €499.95*

> This is the companion to the full [BodyScan-2-Dissection.md](./BodyScan-2-Dissection.md). That doc covers hardware, competitors, and subscription strategy. This one answers: *what exactly does it track, how, and do I have to pay monthly to see it?*

---

## 1. The Master List — All 60+ Biomarkers

Withings advertises "60+ biomarkers in ~90 seconds." That number counts **segmental repeats** (e.g., fat in 6 body zones = 6 biomarkers) + scores + trends. Below is the complete inventory reconstructed from Withings product pages, support FAQ (article 42653646388625), PR releases (CES 302652358, US 302825384), Wired/Tom's Guide/TechRadar hands-ons, and Withings staff clarifications.

**Legend:** 🟢 = FREE forever, no subscription · 🔒 = **Withings+ required ($9.95/mo or $99.50/yr)** · ⚠️ = Contested / rollout-dependent

### A. Weight & Basic Anthropometrics — *Direct Measurement*

| # | Biomarker | How It's Measured | Sensor | Withings+? |
|---|-----------|-------------------|--------|------------|
| 1 | **Weight** (50g / 0.1 lb precision, 5–200 kg) | Direct load | 4 load cells + Position Control™ detector | 🟢 Free |
| 2 | **Weight Trend / Weight Trajectory** | Calculated from history | Software | 🟢 Free |
| 3 | **BMI** | Weight / height² (height entered in app) | Formula | 🟢 Free |
| 4 | **BMI Category / Trend** | WHO classification overlay | Formula | 🟢 Free |

### B. Body Composition — *13-Frequency BIS Derived* — The Core Promise

All of these come from **one 13-frequency impedance spectrum** (see Section 2). The scale fires imperceptible currents between hands and feet, measures resistance (R) and reactance (Xc) at each frequency, and runs segmental Cole-model algorithms.

| # | Biomarker | What It Actually Is | Zones | Withings+? |
|---|-----------|---------------------|-------|------------|
| 5 | **Fat Mass (kg)** | Total fat, "99% DEXA correlation" claim | Whole body | 🟢 Free |
| 6 | **Fat Mass (%)** | Fat / weight ×100 | Whole body | 🟢 Free |
| 7–12 | **Segmental Fat Mass** (6 zones) | Fat in **R arm, L arm, Trunk, R leg, L leg, Core/Abdomen** | 6 zones counted separately = Withings' "6-zone" brag | 🟢 Free |
| 13 | **Fat Mass Trend** | Time series | Software | 🟢 Free |
| 14 | **Muscle Mass (kg)** | Total skeletal + smooth muscle estimate | Whole body | 🟢 Free |
| 15 | **Muscle Mass (%)** | Muscle / weight ×100 | Whole body | 🟢 Free |
| 16–21 | **Segmental Muscle Mass** (6 zones) | Muscle per zone | 6 zones | 🟢 Free |
| 22 | **Skeletal Muscle Mass** | Subset of muscle (the trainable kind) | Whole body | 🟢 Free |
| 23 | **Lean Mass / Fat-Free Mass** | Everything that isn't fat | Whole body | 🟢 Free |
| 24 | **Bone Mass (kg)** | Mineral estimate — *not* DEXA bone density, it's impedance-derived | Whole body + segmental | 🟢 Free |
| 25 | **Body Water — Total Body Water (kg & %)** | Total water from impedance | Whole body | 🟢 Free |
| 26 | **Extracellular Water (ECW)** | Water *outside* cells — low frequencies can't enter cells | Derived from low-freq impedance | 🟢 Free |
| 27 | **Intracellular Water (ICW)** | Water *inside* cells — only high frequencies (up to 800kHz) penetrate membrane | Derived from high-freq impedance | 🟢 Free |
| 28 | **ECW/ICW Ratio — Body Fluid Balance** | Hydration distribution marker; shifts with inflammation, overtraining, cycle | Ratio | 🟢 Free |
| 29 | **Hydration Level** | Simplified fluid-balance status | Score | 🟢 Free |
| 30 | **Visceral Fat Index** | Fat around organs — *estimated* from trunk impedance + anthropometrics, not imaged | Trunk algorithm | 🟢 Free |
| 31 | **Visceral Fat Trend** | Historical visceral trajectory | Software | 🟢 Free |
| 32 | **Subcutaneous Fat** | Fat under skin (as opposed to visceral) | Derived | 🟢 Free |
| 33 | **Protein Mass** | Body protein estimate | Derived from FFM | 🟢 Free |
| 34 | **Basal Metabolic Rate (BMR)** | Calories burned at rest (kcal/day) | Harris-Benedict-style formula + FFM | 🟢 Free |
| 35 | **Daily Calorie Budget / Caloric Intake Optimization** | BMR × activity factor | Formula | 🟢 Free |
| 36 | **Body Composition History Graphs** | All above trended daily/weekly/monthly | App | 🟢 Free |

> **Bottom line:** Every gram/%/zone of fat/muscle/water/bone is **FREE**. Withings does not gate composition itself — that's the honest part.

### C. Cardiovascular — *The Differentiator* — Mix of Measured + AI

| # | Biomarker | How It's Measured | Sensor / Method | Withings+? |
|---|-----------|-------------------|-----------------|------------|
| 37 | **Standing Heart Rate (bpm)** | R-R intervals from ECG circuit | ECG electrodes | 🟢 Free |
| 38 | **Heart Rate Trend** | Historical resting HR | Software | 🟢 Free |
| 39 | **6-Lead ECG Trace (12-second strip)** | Electrical heart rhythm | 12 electrodes (handle + feet) in limb-lead config | 🟢 Free — you get the trace + basic labels |
| 40 | **AFib Detection (Atrial Fibrillation)** | FDA-cleared algorithm on ECG | Withings Scan Monitor 2.0 software (510k K230812) — *software* is cleared, not the scale hardware | 🟢 Free — detection itself is free (medically regulated in EU + US) |
| 41 | **QRS / Sinus Rhythm Notification** | Rhythm classification | Same ECG software | 🟢 Free |
| 42 | **Pulse Wave Velocity (PWV)** | Time for pressure wave to travel arm → leg | Impedance plethysmography via electrodes (same tech as Body Scan 1, FDA-cleared there) | 🟢 Free |
| 43 | **Vascular Age** | PWV mapped to age-matched arterial stiffness norms | PWV algorithm | 🟢 Free |
| 44 | **Arterial Stiffness / Elasticity Score** | Inverse of PWV, zoned across body | PWV algorithm | 🟢 Free |
| 45 | **Cardio Responsiveness Score** | How fast heart *reacts* to each beat (pre-ejection period) | **Impedance Cardiography (ICG)** — first time on a home scale, measures mechanical timing vs electrical | 🟢 Free |
| 46 | **Cardio Efficiency Score** | How long heart spends *pumping* vs resting per beat (LVET) | ICG | 🟢 Free |
| 47 | **Heart Age** ⭐ | Composite of ICG Responsiveness + Efficiency vs age norms — the CES headline feature | ICG algorithm | **🔒 Withings+ ONLY** — product pages: *"only available with Withings+ subscription"* |
| 48 | **Hypertension Risk Notification / Blood Pressure Insights** | AI risk model — *not* a cuff measurement. EU: medical-grade score. US: wellness "Insights" | AI model (no BP sensor) | 🟢 Free — the notification itself is free |
| 49 | **Cardio Check-Up (Human Review)** | Your ECG strip reviewed by a **board-certified cardiologist within ~24h**, 4×/year included | Telehealth service | **🔒 Withings+ ONLY** (4 included/yr) |

### D. Respiratory / Oxygen

| # | Biomarker | How | Sensor | Withings+? |
|---|-----------|-----|--------|------------|
| 50 | **SpO₂ — Blood Oxygen Saturation (%)** | Red + infrared light absorption through thumb vessels (oxyhemoglobin vs deoxyhemoglobin) | **Multi-wave PPG** on handle (new, BodyScan 2 exclusive) | 🟢 Free — the % reading is free |

### E. Nerve Health — *Electrodermal*

| # | Biomarker | How | Sensor | Withings+? |
|---|-----------|-----|--------|-------------|
| 51 | **Nerve Response Score — Feet** | Tiny current stimulates **foot sweat glands**, measures peak galvanic skin conductance; low response = possible small-fiber neuropathy correlate (validated vs diabetes in Withings research) | **ESC / sudomotor test** (foot electrodes) | 🟢 Free |
| 52 | **Nerve Response Score — Hands** | Same on hands via handle | ESC | 🟢 Free |
| *Note* | *Wired's verdict: "I'm still not sure how my nerve response score could possibly be of any real, clinical use." Withings labels this **wellness tier**, not diagnostic.* | | | |

### F. Metabolic / Cellular — *The 800 kHz Payoff*

These are where the 13-frequency upgrade matters — ultra-high frequencies (above ~200 kHz) probe cell membrane integrity.

| # | Biomarker | Inputs | Withings+? |
|---|-----------|--------|------------|
| 53 | **Metabolic Age** | BMR + composition vs age-matched norms | 🟢 Free (per app; some retailers list as +) |
| 54 | **Cellular Age** | Ultra-high-freq BIS markers of cell membrane health (reactance) | 🟢 Free (marketed as core BS2 feature, not footnoted as +) |
| 55 | **Active Cell Mass (ACM)** | Metabolically active tissue estimate from high-freq BIS | 🟢 Free |
| 56 | **Metabolic Efficiency Score** | Cellular + composition synthesis | 🟢 Free |
| 57 | **Glucose Resilience Score** ⭐ | **Visceral Fat Index + ESC Nerve Response** → early glycemic dysregulation risk. **Does NOT measure blood glucose. No CGM. No finger prick.** Wellness-only. | **🔒 Withings+ ONLY** — rolling out **H2 2026** (before end of 2026). Launch pillar, shipped on promise. |

### G. Composite Scores, AI & Software — *Where the Paywall Lives*

| # | Feature | What It Is | Withings+? |
|---|---------|------------|------------|
| 58 | **Health Trajectory / Healthy Years Score** | Single "predicted years of healthy life" synthesizing all biomarkers — the longevity headline | **🔒 Withings+** (listed as + on retailer pages; Withings wording has shifted — assume gated) |
| 59 | **Health Improvement Score** | Overall health trend score | **🔒 Withings+** |
| 60 | **Readiness Score / Daily Energy Score** | Readiness-to-train/recover | **🔒 Withings+** |
| 61 | **BodyPath** | Metabolic journey visualization over time | **🔒 Withings+** (per Withings staff on Reddit) |
| 62 | **Body Profile** | Segmental evolution view | **🔒 Withings+** (per Withings staff) |
| 63 | **Body Intelligence** | Health Tab intelligence tier | **🔒 Withings+** |
| 64 | **Lifestyle Intelligence** | Health Tab intelligence tier (activity, nutrition, sleep coaching) | **🔒 Withings+** |
| 65 | **Longevity Intelligence** | Health Tab intelligence tier — *BodyScan 2 exclusive* (BodyFit doesn't get it) | **🔒 Withings+** |
| 66 | **AI Health Assistant — Withings Intelligence (24/7)** | Chatbot that remembers your profile, trends, answers questions | **🔒 Withings+** |
| 67 | **AI Coaching & Insights (HealthSense)** | Personalized nudges, in-scan lifestyle surveys via handle thumb buttons, haptic guidance | **🔒 Partial** — guidance free, intelligence insights gated |
| 68 | **Clinical Add-ons: Nutritionist (1 video session) + Sleep Clinic Assessment** | Human services | **🔒 Withings+** |
| 69 | **Withings+ Protect — Premium Warranty ("Lifetime Guarantee" in US PR)** | Extended warranty | **🔒 Withings+** |
| 70 | **⚠️ Automatic Third-Party Sync — Apple Health, Google Health Connect, MyFitnessPal, Samsung Health** | The data *pipe* out | **🔒 Withings+ for accounts created Oct 13, 2026 or later** — see Section 4 |

**Count:** ~70 distinct data points/scores/features when you count segments + trends + intelligence tiers. Withings rounds to "60+ biomarkers in ~90 sec."

---

## 2. Bioimpedance Tech Deep Dive — Why 13 Frequencies to 800 kHz Matters

### How BIA Works in 30 Seconds
Your body is mostly water with electrolytes — it conducts electricity. Fat is anhydrous (poor conductor). Muscle is ~73% water (good conductor). Bone and air are poor conductors.

A scale injects a tiny, safe, imperceptible AC current (microamps) between electrodes and measures **impedance (Z)** — the opposition to current flow:

- **Resistance (R):** friction from water/electrolytes — more water = lower R
- **Reactance (Xc):** capacitance of cell membranes acting like tiny capacitors — healthier membranes = higher Xc

Algorithms (Cole model, Hanai mixture theory) convert R+Xc at multiple frequencies + your height/weight/age/sex into fat/muscle/water compartments.

### The Frequency Ladder — What Each Band Sees

```
Low (1–5 kHz):     Current flows AROUND cells → measures Extracellular Water (ECW) only
                   Cell membranes block low-freq current.

Mid (50 kHz):      The classic single-frequency BIA — mixture. This is what every
                   $30 Amazon scale uses. One number. Lots of guessing.

High (100–250 kHz): Current starts penetrating membranes → mixture shifts toward
                   Intracellular Water (ICW). Body Scan 1 stopped here (3 freqs ≤250kHz).

Ultra-high (250–800 kHz): Current fully penetrates cells → independent ECW vs ICW,
                   membrane capacitance (reactance), phase angle. This is BodyScan 2's
                   new territory. Powers Cellular Age, ACM, Metabolic Efficiency, hydration balance.
```

| Generation | Frequencies | Max | What You Get | Example Device |
|------------|-------------|-----|--------------|----------------|
| **Budget BIA** | 1–2 | 50 kHz | Foot-to-foot estimate, whole body only, heavy extrapolation | Renpho Elis $29, Eufy P2 Pro $50 |
| **Dual-frequency** | 2 | ~100 kHz | Slightly better water split | Wyze Scale Ultra $120 (dual-freq) |
| **Withings Body Scan 1** | 3 | 250 kHz | Segmental (6 zones), basic ECW/ICW | $399–499 |
| **Clinical multi-freq (e.g., InBody 580 lab unit $17k+)** | 6 | ~1,000 kHz | Independent ECW/ICW, segmental, phase angle | InBody lab |
| **Withings BodyScan 2** | **13** | **800 kHz** | **6-zone segmental, independent ECW/ICW, membrane health, ACM, cellular age, hydration balance** | **$599.95** |

### Why "More Frequencies = More Precise" Is Half-True

**True part:**
- 13 points define the impedance spectrum curve (Cole plot) far better than 3. Less interpolation, more measured.
- Segmental hand-to-foot circuit measures each limb/trunk *through actual current path* vs foot-only scales that only measure legs and *estimate* upper body from demographics.
- 8 ITO electrodes on glass (vs 4 metal pads on cheap scales) = larger contact, less sensitive to foot placement/size (Withings claims "all foot sizes").
- Ultra-high frequencies genuinely unlock *new* biomarkers that lower-freq scales cannot: Cellular Age, ACM, ECW/ICW balance — whether those biomarkers are *clinically useful* is a separate question.

**Marketing-stretch part:**
- Precision ≠ accuracy. A precise BIA can be precisely wrong for an individual if the underlying prediction equations (trained on population data) don't fit you. Athletes, very lean (<15% fat), very obese, elderly, and dehydrated users all break the equations.
- Wyze claims ≥0.98 DEXA correlation for fat / ≥0.99 for lean at $120 with dual-frequency. Withings claims 99% DEXA correlation at $600 with 13 frequencies. Both use **correlation** (see Section 3) — the spec doesn't prove 5× accuracy for 5× price.
- Independent reality: **Tom's Guide** saw body fat swing **6.8% → 8.7% across 5 consecutive weigh-ins** on BodyScan 2. **TechRadar** got Vascular Age "4 years older" then "1 year older" a week apart. Hydration, meals, exercise, skin moisture, and room temp all move readings day-to-day — at *any* frequency.

### Metabolic Insights — What the 800 kHz Unlocks

| Insight | Input Signals | What It Claims | Gated? | Evidence Level |
|---------|---------------|----------------|--------|----------------|
| **Cellular Age** | Ultra-high-freq reactance (membrane capacitance) + norms | Biological age of your cells vs chronological age | Free | Proprietary, no peer-reviewed validation published |
| **Active Cell Mass (ACM)** | High-freq BIS estimate of metabolically active tissue | How much of you is "working" tissue | Free | Clinical concept, BIA implementation proprietary |
| **Metabolic Efficiency** | ACM + composition + BMR synthesis | How efficiently you burn | Free | Proprietary score |
| **Metabolic Age** | BMR + composition vs age norms | Younger/older metabolically | Free | Standard aging-curve idea, proprietary equation |
| **Glucose Resilience** | **Visceral Fat + ESC (nerve) → glycemic risk proxy** | Early signs your glucose regulation is slipping | **Withings+** | Wellness-tier proxy; no blood glucose measured; correlation shown in Withings diabetic cohort, not a diagnostic |

> **Honest translation:** The 800 kHz spectroscopy is a real hardware upgrade — it lets the scale *measure* cell-level electrical properties that cheaper scales *guess at*. Whether the **scores built on top** (Cellular Age, Glucose Resilience) change behavior or predict outcomes better than weight + waist + A1c is unproven. Think of them as "interesting trend signals," not medical facts.

---

## 3. BodyScan 2 vs. DEXA Scan — The Honest Comparison

DEXA (Dual-Energy X-ray Absorptiometry) is the reference method Withings benchmarks against with its "99% DEXA correlation" claim. Here's what that claim means — and doesn't.

### The Two Technologies Side-by-Side

| | **Withings BodyScan 2 (BIS)** | **DEXA (e.g., Hologic Horizon, GE Lunar iDXA)** |
|---|-------------------------------|--------------------------------------------------|
| **Principle** | Electrical: current resistance + cell capacitance at 13 frequencies | Radiographic: two X-ray beams at different energies; fat, lean, and bone attenuate X-rays differently (direct physics, not equation) |
| **What it directly images** | Nothing — *estimates* compartments from impedance + height/weight/age/sex equations | **Pixels of your body** — actually images fat vs lean vs bone mineral per region |
| **Fat measurement** | Estimated from total water + FFM equations | Measured from X-ray attenuation (fat has distinct coefficient) |
| **Lean/muscle** | Estimated (FFM = weight − fat) | Measured: lean soft tissue directly |
| **Bone** | Estimated impedance number — **not bone mineral density (BMD)** | **Gold standard for BMD / osteoporosis diagnosis** — the only one FDA-accepted for BMD |
| **Visceral fat** | Estimated via trunk impedance + waist model | Estimated via software (DEXA visceral is also a model, not CT — but from imaged data) |
| **Segmental detail** | 6 zones (R/L arm, trunk, R/L leg, core) via hand-foot current paths | Full-pixel regional: arms, legs, trunk, android/gynoid, with **bone density per site** |
| **Precision (repeatability)** | Manufacturer: 50g weight; body fat: **volatile in reviews — ±1–2% day-to-day**, Tom's Guide 6.8–8.7% across 5 weigh-ins | **Weight: ±0.1 kg; body fat: ~1% precision; bone BMD ~1% CV** — far more repeatable |
| **Accuracy vs truth** | Population-tuned equations; systematic errors for lean/athletic (+20–35% fat overestimation in <15% fat), obese, elderly, dehydrated; affected by meals, exercise, hydration, skin temp, dry skin | Considered reference for body comp; errors: hydration extremes, very large bodies, beam hardening — but fundamentally imaging, not predicting |
| **Radiation** | None | **Very low: ~1–10 µSv per scan** (1–4 days of natural background; a chest X-ray is ~100 µSv; a transatlantic flight is ~40 µSv). Not zero, but negligible for periodic scans. Not for pregnancy. |
| **Duration** | 30 sec (Daily) / 90 sec (Longevity) at home, daily | 6–12 min on a table, at a clinic/lab. Stays still, arms positioned. |
| **Cost** | $599.95 device + optional $99.50/yr W+; unlimited scans | **$49–$150 typical** in US (university labs, Bodyspec, Dexafit); $150–$300 at hospitals; sometimes covered for osteoporosis screening |
| **Availability** | Bathroom, daily | Appointment; not every city has low-cost option |
| **Regulatory** | ECG software FDA-cleared (K230812); scale itself: *wellness device, not diagnostic* | FDA-cleared medical device for body composition + BMD diagnosis |
| **Data you get** | Weight, segmented fat/muscle/water/bone estimates, Vascular Age, ECG, SpO₂, Nerve Score, + AI scores (Heart Age, Glucose Resilience, Health Trajectory) | **Weight + full fat/lean/BMD breakdown, regional fat distribution, visceral fat, BMD T-score/Z-score, bone health report, often RMR comparison**; no ECG/heart/nerve/SpO₂ |
| **Best for** | **Daily trends at home**, cardio screening (ECG/AFib/PWV), motivation, GLP-1 muscle-preservation tracking | **Ground-truth benchmark** (get one every 6–12 months), bone density screening, precise fat/lean verification |

### What "99% DEXA Correlation" Really Means

Withings says fat mass has a **99% correlation** with DEXA. **Correlation (r = 0.99)** measures whether two methods *move together* — not whether they *agree*.

- If the scale always reads **5% fat higher** than DEXA but tracks perfectly, correlation is still 99%. **Agreement** (Bland-Altman limits) is what matters — and Withings doesn't publish that in marketing.
- **Wyze claims the same thing** at $120: ≥0.98 correlation for fat mass, ≥0.99 for fat-free mass. A correlation claim is not a moat.
- Independent literature (see Honest Notes below): BIA vs DEXA mean absolute differences are **2–4% fat** for typical users, **worse for extremes**. That's useful for trends, not lab-grade absolute numbers.

### Practical Protocol — How Smart Users Combine Them

> **Best practice from longevity clinics (Function Health, Superpower, etc.):**
> 1. **Daily:** Step on BodyScan 2 (or any handle scale) for weight + trend lines — ignore any single day's fat%.
> 2. **Every 6–12 months:** Get a **DEXA** ($75–150) for ground-truth fat/lean/BMD and recalibrate your mental offset ("my scale reads ~2% high vs DEXA").
> 3. **For osteoporosis risk (50+, postmenopausal):** DEXA is *required* — no BIA scale measures BMD. Don't substitute.
> 4. **GLP-1 / cutting / bulking:** Daily BIS + periodic DEXA is the gold combo — BIS protects muscle daily, DEXA verifies quarterly.

---

## 4. The Paywall — What You Actually Pay Subscription For

**Withings+ price:** $9.95/month or $99.50/year (website; App Store $9.99/$99.99). 1 month free with device purchase; 14-day trial in-app. 5-year ownership math: **~$1,100** if you keep it ($600 + 5×$99.50). Lifetime storage + CSV/PDF export stays free.

### ✅ Everything FREE Without Subscription (No Trick)

- All raw measurements: weight, every fat/muscle/water/bone number, all 6 zones, visceral fat, BMR, protein, hydration/fluid balance, PWV/Vascular Age, heart rate, ECG trace + AFib detection, SpO₂, Nerve Response Score
- Unlimited lifetime history, trends, goals, symptom logging
- **CSV + PDF export of full history** (manual)
- HealthLink doctor sharing dashboard
- Data **import** from other apps (Apple Health → Withings stays free)
- 8 users, all special modes (Athlete/Pregnancy/Baby/Pet/Luggage/Weight-Only/Eyes-Closed)

### 🔒 Locked Behind Withings+ (Confirmed by Withings Product Pages + Staff)

| Feature | Why It Stings |
|---------|---------------|
| **Heart Age** | *One of the 5 CES launch pillars* — gated. The scale measures ICG either way; the score is withheld. |
| **Glucose Resilience** | *Second launch pillar* — gated + still rolling out H2 2026. You bought the longevity station; the metabolic longevity score is à la carte. |
| **Health Trajectory (Healthspan Years)** | The single-number longevity score — gated per retailer Withings+ lists |
| **BodyPath & Body Profile** | Journey visualizations — staff confirmed as + exclusive |
| **Body / Lifestyle / Longevity Intelligence (Health Tab tiers)** | All three intelligence tiers — Longevity Intelligence doesn't even exist on the cheaper BodyFit |
| **AI Health Assistant (Withings Intelligence 24/7) + Health Improvement Score + Readiness Score** | Interpretation layer — the "meaning" behind your numbers |
| **Cardio Check-Up (cardiologist ECG review, 4×/yr)** | The most defensible paywall — real doctor, real cost |
| **1× Nutritionist Video Session + Sleep Clinic Assessment** | Human clinical services |
| **Withings+ Protect — Premium / "Lifetime Guarantee" Warranty** | Warranty bundling as retention |
| **⚠️ Automatic Third-Party Sync (Apple Health, Google Health Connect, MyFitnessPal, Samsung Health)** | **NEW Oct 13, 2026 — 4 days ago.** Accounts created **Oct 13, 2026+** must have Withings+ for auto-sync. **Accounts created Oct 12, 2026 or earlier are grandfathered free forever** (tied to account, survives new hardware). Manual CSV/PDF export stays free; import into Withings stays free. Developer API "Start for Free" plan also now requires W+. One outlet called it *"egress fees for your body."* |

### ⚠️ The One Inconsistency to Know Before Buying

Some US reviewers saw **Heart Age appear without a "+" marker** after ECG activation — before subscribing. Withings' official pages (US, FR, DE) and staff replies say Heart Age + Glucose Resilience are **Withings+ exclusive**. Budget as if you'll need the sub for year one to get the headline AI scores + sync. If you buy, **create your Withings account immediately** to lock the pre-Oct-13 free-sync grandfathering via your account date (if you already had an account Oct 12 or earlier, you're safe).

---

## 5. Quick Verdict — Should the Tech Sell You?

| Your Goal | Recommendation |
|-----------|----------------|
| **Daily composition trends + cardio screen (AFib, vascular age, ICG) + longevity curiosity** | BodyScan 2 is the broadest at-home station that exists — but budget $699 for year one ($600 + $99.50 W+) if you want the scores + Apple Health sync |
| **Just accurate weight + solid segmental fat/muscle trends** | **Wyze Scale Ultra BodyScan ($120, no sub, ≥0.98 DEXA correlation claimed) or Hume Body Pod 2.0 ($249 sale, optional $9.99/mo)** — 80–90% of the composition value at 20–40% of price; no ECG/ICG/PWV |
| **Ground-truth body fat + bone density** | **Periodic DEXA ($49–150) beats any home scale** — pair with a cheap handle scale for daily trends |
| **Serious composition, no heart features, no subscription ever** | **InBody Dial H30 (~$379, pro-grade BIA) + periodic DEXA** |
| **You hate subscriptions on principle** | Garmin Index S2, Wyze, Renpho, Eufy, InBody — all no-sub. And if you create a Withings account today, you'll be paying to sync it. |
| **GLP-1 / Ozempic muscle preservation** | BodyScan 2's 6-zone daily muscle tracking is genuinely useful here — but Wyze/Hume do segmental too for far less |

### The One-Move Advice If You Buy
1. Create/register your **Withings account immediately** (even before unboxing) — free-sync grandfathering keys off account creation date.
2. Use Daily Scan most days; Longevity Scan (ECG + Heart Age + Nerve Score) **weekly**.
3. Get a **baseline DEXA within month one**, then every 6–12 months — learn your scale's personal offset and track bone health for real.

---

## Sources (Oct 17, 2026 cut)

Withings BodyScan 2 product pages (withings.com/products/bodyscan-2-black, support article 42653646388625, withings.com/pages/withings-plus), PR Newswire CES 302652358 / US 302825384 / TIME 302910547, The Verge Oct 13 2026 sync-paywall coverage, Wired 9/10 review, Tom's Guide, TechRadar, CNET, MacRumors, PCMag, Wareable, Reddit r/withings (Withings staff), BodySpec/DexaFit pricing, Hologic/GE DEXA specs.

*This doc lives at `/home/user/BodyScan-2-Biomarkers-DEXA-Deep-Dive.md` alongside the full [Dissection](./BodyScan-2-Dissection.md).*

```
BodyScan 2 Sensors: 4 load cells (50g) | 12 electrodes (8 ITO glass + 4 steel handle)
                    13-freq BIS ≤800kHz | 6-lead ECG (K230812) | ICG | PWV | PPG SpO2 | ESC
Scan: Daily ~30s | Longevity ~90s | 60+ biomarkers | 6 body zones
Body: 325×357×18.5mm | ~5.4kg | 5–200kg | aluminum + tempered glass | 640×172 LCD in handle
Power: USB-C Li-ion, 12–15 mo claimed | Wi-Fi + BT | 8 users | iOS18+/A12+
Price: $599.95 / €499.95 / £449.95 / AU$899 | FSA/HSA US
Sub: Withings+ $9.95/mo or $99.50/yr → Heart Age, Glucose Resilience, Health Trajectory,
     BodyPath/Profile, Intelligence tiers, AI Assistant, Cardio Check-Up, + (from Oct 13 2026) auto-sync
```

