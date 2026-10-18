# Withings BodyScan 2 vs. Open-Source Alternatives

> **Important correction / superseding research:** See `BodyScan-2-Expanded-Open-Source-Search.md` (October 17, 2026). This earlier dossier contains unsupported parity percentages and overstatements about segmental scale support, impedance frequency limits, ICG availability, direct ICW measurement and DIY electrical safety. Do not use those claims as established facts or purchase/build guidance. The expanded report separates open source from restrictive source-available licenses and practical products from research prototypes.
### How close can you get without the cloud, the app, or the $99.50/year?
*Compiled Oct 17, 2026 — anchors to the BodyScan 2 as shipped (EU June 9, US July 15-20, 2026, $599.95 + Withings+ $99.50/yr, incl. Oct 13 sync-paywall)*

> **The question:** Is there an open-source way to get the same 60+ biomarkers, 13-freq BIS, 6-lead ECG, ICG, PWV, PPG SpO₂, and ESC nerve score — without a Withings account, without AI paywalls, without "egress fees for your body"?
>
> **Short answer:** Yes for **weight + basic body composition with full privacy**. Sort-of for **segmental composition**. No, not in one device, for the **cardio/vascular/nerve/SpO₂/longevity stack**. Open source replaces the *scale* and the *data pipe*, not the cardiometabolic lab-in-a-handle.

---

## 1. What "Open Source" Actually Means Here

There are **four distinct layers** people conflate — and BodyScan 2 locks all four:

| Layer | What Withings Locks | Open-Source Equivalent |
|-------|---------------------|------------------------|
| **1. Hardware (the sensors)** | 12 electrodes, 4 load cells, 13-freq BIS to 800kHz, 6-lead ECG, ICG, PWV, PPG, ESC | Cheap BLE scales + DIY AD5933/ESP32 builds + separate ECG/SpO₂ modules |
| **2. App (read & log the data)** | Health Mate app (cloud, account required, sync now paywalled) | **openScale**, **BioScale**, **OpenTara**, **HealthLog** |
| **3. Pipe (get data out)** | Apple Health / Google Health Connect / MQTT / Home Assistant — now Withings+ for new accounts | **BLE Scale Sync**, **ESPHome + ESP32 proxy**, **openScale-sync**, Home Assistant Withings/Withouthings |
| **4. Intelligence (scores, AI, trajectory)** | Heart Age, Glucose Resilience, BodyPath, Health Trajectory, AI Assistant | Self-hosted formulas (Janssen, Kyle, Mifflin-St Jeor), HealthLog AI Insights (local LLM), Nextcloud/InfluxDB/Grafana |

**No single open-source project does all four like BodyScan 2.** You assemble a stack.

---

## 2. The Open-Source Stack — Complete Inventory

### A. Apps That Replace Health Mate — Phone-Side, 100% Offline

#### 1. openScale — The Veteran (GPLv3, 2,273★, 401 forks, since 2014)
**Repo:** `oliexdev/openScale` — Android (F-Droid + Play Beta) · **2,000+ commits**
**What it is:** Fully offline weight + body metrics tracker. No account, no cloud, no ads. Location permission only to find BLE, revokable after. Exports CSV/SQLite.

**Supported hardware (80+ models decoded):**
- **Full list:** Beurer BF105/BF500/BF600/BF700/BF710/BF720/BF800/BF850/BF950/BF1000, Digoo DG-S038H, Excelvan CF369BLE, Exingtech Y1, Hesley/Yunchen, MGB/Vitalmaxx/Vigorun, Medisana BS444/BS440, Runtastic Libra, Sanitas SBF70/SBF72, Silvercrest SBF75/SBF77, Xiaomi Mi Scale v1/v2 + Mi Body Composition Scale 2, Yunmai Mini/SE, iHealth HS3, Easy Home 64050, Huawei Scale 3, Terraillon X-Line, Omron HBF-702T, **Hume Dara 2.0**, Etekcity Fit 8S, A&D UC-352BLE, PICOOC, **Eufy P2/P2 Pro, Eufy C1/C20**, Keep S3, FitTrack Dara, Xiaomi S800/S400, + **Custom-Made Bluetooth Scale** (DIY template) — and 30+ QN-Scale / FITINDEX / RENPHO rebrands.

**Metrics it tracks:**
Weight, BMI, **body fat %, body water %, muscle %, LBM, bone mass, visceral fat**, waist/hip/chest/thigh/biceps/neck circumferences, WHR, WHtR, caliper, **BMR, TDEE, calories**, plus **custom metrics**, **segmental body fat & muscle per arm/leg/torso** + **metabolic age** (new in v3.1.3), goals, charts, multi-user (8+), assisted weighing (baby/pet), amputee mode, 27 languages, dark theme.

**How it gets body comp:** Two paths:
1. **From the scale** (if the scale broadcasts it — Beurer, Yunmai, QN-Scale do)
2. **Estimated locally** from scientific formulas (Durnin & Womersley, Deurenberg, etc.) — useful if scale only sends weight + impedance. The app publishes its estimation code openly.

**Sync out:** `openScale-sync` companion → Google Fit / Health Connect / MQTT. Also `BLE Scale Sync` can read openScale's SQLite.

**Verdict:** The closest drop-in Health Mate replacement for composition. **Beats Withings on privacy** (internet permission literally removed). **Loses on sensors** — it only displays what the cheap scale sends.

#### 2. BioScale — OKOK·International Replacement (MIT, 2025-2026)
**Repo:** `eayrenk/bioscale-okok-alternative` (+ fork `brumathey/...`)
**Niche:** Replaces the notoriously ad-filled, paywalled **OKOK·International app** (Chipsea chipset — the chip inside *hundreds* of $25-60 Amazon/AliExpress BLE body fat scales).

**Stack:** Python/Flask backend + Dash/Plotly frontend + SQLite (desktop: macOS/Win/Linux) + Flutter 3.x (Android/iOS native) + `bleak`/`flutter_blue_plus` BLE.

**Why it matters:**
- OKOK locks ~12 metrics behind paywall + forced video ads. BioScale unlocks **20+ metrics, all free, 100% offline, no login**.
- Metrics: Body Score, BMI, obesity degree, ideal weight, metabolic age, body fat %/kg, visceral fat, subcutaneous fat, muscle %/kg, skeletal muscle mass (Janssen 2000/MRI-validated), FFMI, SMI, LBM, bone mass, body water %/kg, protein %, BMR (Mifflin-St Jeor), + WHR/WHtR/cardiovascular risk (AHA/Ashwell).

**BIA accuracy:** Reverse-engineered OKOK `CsAlgoBuilder` + corrected with peer-reviewed refs: Janssen 2000 (SMM vs MRI), Kyle 2004 (H²/R impedance index), Mifflin-St Jeor (BMR), Pace & Rathbun 1945 (73% hydration), EWGSOP2 (sarcopenia). The README explicitly calls OKOK's stock calculations "questionable" and replaces them.

**Compatible scales:** Any scale mentioning **Chipsea / OKOK** — generic Amazon/AliExpress body fat scales. No BodyScan 2-class hardware, but proves the community *rewrites* vendor BIA math openly.

**Verdict:** Best example of **open-source fixing vendor BIA math**. Template for how BodyScan 2's algorithms *could* be audited — if Withings opened them (they don't).

#### 3. OpenTara (iOS) — The Missing Piece for iPhone
**Repo:** `etlami/opentara` — MIT
**Problem it solves:** openScale is Android-only. iPhone users were stuck with iCloud-bound vendor apps. OpenTara is the iOS equivalent.

**Status (2026):** Xiaomi Mi Body Composition Scale 2 (MIBFS) ✅ verified, Mi Scale v1 🧪 experimental, Bluetooth-SIG standard scales (0x181D/0x181B) 🧪 experimental. Computes full body metrics **locally on iPhone**, no cloud.

**Verdict:** Young but critical — shows iOS local-first is possible, albeit with fewer supported scales.

#### 4. Bodymiscale — Home Assistant Body Composition Engine (Docker, GPL)
**Repo:** `dckiller51/bodymiscale` — Home Assistant custom component
**What it does:** Takes *any* weight + optional impedance sensor (from ESPHome, BLE Monitor, or `input_number`) and runs **three selectable scientific models**:
- **Xiaomi Mode** (original 2017 Zepp Life algorithms for consistency)
- **Scientific models** (peer-reviewed BIA equations)

It then publishes 12+ entities to HA: fat%, water%, muscle, bone, visceral, BMR, etc. — fully local, automatable, dashboard-ready.

**Verdict:** The glue between cheap BLE scales and a self-hosted Health Mate clone. Pair with Xiaomi Mi Scale 2 via ESP32 BLE proxy → Home Assistant → Bodymiscale → Grafana.

#### 5. Self-Hosted Health Clouds — HealthLog, NutriTrace, Withoutings
- **HealthLog** (`MBombeck/HealthLog`, AGPL): Self-hosted health tracker (Docker + Prisma + Next.js PWA). Weight, BP, glucose, mood, meds. **Import from Withings + Apple Health**. Local AI Insights (you bring the LLM). The "self-hosted Health Mate."
- **NutriTrace** (`TraceApps/nutritrace`, AGPL-3.0): Nutrition + health, Withings/Garmin/Fitbit sync, single Docker container, no telemetry.
- **Withoutings** (`roessland/withoutings`, Go): DDD/clean-code web app giving Withings users access to their *own* Withings data — streams to Dropbox/Drive/IFTTT. The "break your data out" escape hatch.
- **Withouthings** (`DavidVentura/withouthings`): **Watch-side** — reverse-engineered ScanWatch 2 firmware (firmware was leaked), local app without Health Mate. Proves Withings wearables are hackable too.

---

### B. The Pipe — Getting Data Out Without Paying Withings+ (or Any Cloud)

This is where the Oct 13, 2026 paywall *hurts* — and where open source shines.

| Tool | Scale → Where | Phone Required? | Headless? | Scales | Output | License |
|------|---------------|-----------------|-----------|--------|--------|---------|
| **BLE Scale Sync** (`KristianP26/ble-scale-sync`) | 25+ scale brands → Garmin Connect, Strava, MQTT (HA), InfluxDB, Webhooks, Ntfy, CSV/JSONL | **No** | **Yes** (RPi/Docker/Linux/macOS/Win) | 35+ adapters: Xiaomi (passive broadcast), Renpho/QN-Scale, Eufy P2/P2 Pro (AES decoded), Yunmai, Beurer BF700-950 incl. BF720, Sanitas, Medisana, Soehnle, Active Era | 10 BIA metrics, auto multi-user by weight, LWT, HA auto-discovery | GPL-3.0 |
| **openScale-sync** | openScale → Health Connect / MQTT | Yes (Android) | No | Via openScale | 4 metrics (weight, fat, muscle, water) | GPL-3.0 |
| **ESPHome Withings Body+ Local** (`didac.dev` Sep 2026) | Withings Body+ → Home Assistant via ESP32 | No | Yes (ESP32) | Withings Body+ (BLE association decoded via decompiled Android app + Codex) | Weight + body comp directly to HA, no Wi-Fi, no cloud | Open (ESPHome) |
| **ESPHome Eufy Bluetooth Proxy** | Eufy C1/P1/P2 Pro → HA via ESP32 | No | Yes | Eufy scales (standard GATT) | Weight + impedance → Bodymiscale | Open |
| **Withings → HA Cloud** (official) | Withings cloud → HA | No | Yes (cloud push) | All Withings via OAuth | Weight, body comp, BP, HR, sleep, temp | Apache 2.0 (HA core) |
| **Prolixium DNS Hack** (2010, still referenced) | Original Withings scales (WS-50/Body) → your own server | No | Yes (Pi + DNS) | WS-50, Nokia Body (unencrypted JSON to `scalews.withings.net`) | Full POST interception — scale thinks your Pi is Withings | Public domain |

**Key win:** `BLE Scale Sync` **explicitly supports scales that broadcast without pairing** (Xiaomi Mi Scale 2 passive) and **decodes encrypted Eufy P2 Pro AES handshakes** (`bdr99/eufylife-ble-client`). Both were community reverse-engineered — the same work Withings would call proprietary.

**For BodyScan 2 owners angry about the Oct 13 paywall:** The cheapest protest is **not replacing the scale**, it's replacing the pipe. Keep the BodyScan 2 for its sensors, but intercept or duplicate the data locally. The Body+ ESP32 hack proves Withings BLE *is* reverse-engineerable; BodyScan 2's 13-freq BIS + handle protocol is newer but follows the same BLE GATT lineage — expect community support within 12-18 months if there's demand.

---

### C. Hardware That Replaces the Scale Itself — DIY BIA

#### 1. Custom Bluetooth Scale (openScale Wiki Template)
**Repo:** `oliexdev/openScale/wiki/Custom-Bluetooth-Scale`
**Recipe:** 4 load cells + HX711 24-bit ADC + ESP32 + tempered glass + BLE GATT profile matching openScale's "Custom made Bluetooth scale." Decode display or read sensors directly, do weight calc on MCU, expose via BLE.

**Cost:** ~$40-80 in parts. **BIA?** Not in the template — weight-only. Add BIA below.

#### 2. AD5933 + ESP32/Aruino BIA Boards — The Workhorse (since 2012)
This is **the** open-source BIA building block — every DIY paper since 2012 uses it.

| Project | MCU | Chip | Frequencies | Electrodes | What It Does | Cost |
|---------|-----|------|-------------|------------|--------------|------|
| **dyarleniber/AD5933-arduino-bioimpedance** (Bachelor thesis) | Arduino + BT | AD5933 | Sweep 50-100kHz (50 increments) | 4-electrode tetrapolar | Sends impedance at 50kHz+100kHz to phone, phone computes FM/FFM/TBW via equations, returns to Arduino | ~$30 |
| **ESP32 IoT Bioimpedance Device** (ResearchGate, April 2025) | ESP32 + BLE/Wi-Fi | AD5933 | 5 Hz–100kHz (AD5933 limit) | 4-electrode | Real-time health monitor, Wi-Fi to cloud + LCD + I²C | ~$35 |
| **Nature 2026: Segmental BIA for Fracture Detection** | LPC2138/ESP32-WROOM + 20×4 LCD | AD5933 eval board | 50kHz (single) + validation 10Ω-1000Ω, 10pF-470pF, <7% error | 4-electrode Ag/AgCl segmental (limbs separately) | Portable segmental BIA — **the closest open equivalent to BodyScan 2's segmental idea** but single-freq. Validated. | ~$80 |
| **A Low-Cost 2D Bioimpedance (EIT) System** (ScienceDirect) | Arduino + LabVIEW + EIDORS | AD5933 | ~50kHz | Up to 16 electrodes, 2D imaging | Electrical Impedance Tomography — research-grade | $80.50 |
| **Hackaday DIY Body Fat Analyzer (2015)** | ATmega1284P | Discrete 50kHz square wave + opto-isolation | 50kHz fixed | Hand-to-opposite-foot (longest path) | 10µA current source, safety-isolated | Student project |

**Also:** `Bioimpedance Measurement` (leybme, ESP32-S3 + AD5941 AFE, STM32H7 + custom DFT, FreeRTOS) — more advanced, AD594x is AD5933's successor (wider band, better SNR, still ≤100kHz without external front end).

**How far vs BodyScan 2's 13-freq to 800kHz?**
- AD5933 **caps at ~100kHz** stock (with external clock hack to ~1MHz but accuracy degrades). You cannot hit **800kHz ultra-high** without a better AFE (AD5940/AD5941, MAX30001, or lab-grade).
- You can **sweep** (e.g., 50-100kHz in 1kHz steps) → multi-frequency, but low-band only. You get ECW vs mixture, **not true ICW** → you cannot derive Cellular Age, ACM, ECW/ICW balance accurately.
- Safety: DIY BIA *must* limit current to <800µA (IEC 60601-1). Commercial scales use isolation, current-setting resistors (1MΩ), and protection diodes — copy them.

**Bottom line:** DIY BIA proves the *principle* is open, but **no DIY project matches 13-freq spectroscopy to 800kHz + segmental 6-zone + medical-grade calibration**. You can build a 1-2 freq foot-to-foot or hand-to-foot scale for ~$60-80 that rivals a $30 Amazon scale — not a $600 longevity station.

#### 3. Off-the-Shelf Open-Ish Hardware
- **SparkFun OpenScale IoT** (ESP32 + HX711 + TMP102, Qwiic, Wi-Fi/BT, OTA, browser terminal, USB-C): Open hardware + firmware, plug-and-play load-cell reader. **Weight-only** (no BIA). Great as the weight base to add AD5933. Not compatible with oliexdev openScale app (name collision).
- **Decent Open Scale** (`decentespresso/openscale`): Full open-source (HW + CAD + FW) BLE scale — ESP32 + HX711 + SSD1306 OLED + MPU6050 gyro — built for coffee (Decent Espresso) but usable as generic. PlatformIO, ESP32-S3. **Weight-only.**
- **Spectra EIT Development Kit** (2019): 32 electrodes, 160kSPS, 16-bit, accelerometer, IEC 60601-1 filtered — the most advanced open biomedical impedance hardware. For hackers wanting **electrical impedance tomography**, not bathroom scales.

---

### D. ECG / PPG / PWV / ICG — The "Impossible" Sensors

BodyScan 2's moat isn't body comp — it's that **one handle contains five extra modalities**. Here's the open status of each:

| BodyScan 2 Sensor | What It Does | Open-Source Equivalent | Match? | Why Not Perfect |
|-------------------|--------------|------------------------|--------|-----------------|
| **6-lead ECG + AFib** (handle + feet, 12 electrodes, Scan Monitor 2.0 K230812) | 12-sec rhythm, AFib detection | **AD8232 single-lead ECG** (SparkFun module, 170µA, 80dB CMRR, 60.8dB gain, 0.5-40Hz bandpass, RLD, lead-off detection) + ESP32 (250Hz, 12-bit) + `XantyagoS/ecg-ad8232-esp32` / `Alpusa/AWECG-Monitor` / `Doenec/ecg-esp32` / `akloster/esp32-ecg` + open 3D-printed case. ~$35 total. | **20%** | Single-lead (Lead I) vs 6-lead. No AFib algorithm (that's regulated, ML-based). You get a trace you must interpret or run through open AFib detectors (e.g., PhysioNet). No medical claim. |
| **Impedance Cardiography (ICG)** — heart pumping efficiency/responsiveness, Heart Age | Times electrical vs mechanical beat, pre-ejection period, LVET | **No open-source ICG scale project exists.** Research ICG uses tetrapolar thoracic bands + high-freq injection + ensemble averaging — not bathroom-scale. You'd need custom electrodes + AD5933-class impedance plethysmography + published ICG equations. | **0%** | This is BodyScan 2's *only-in-this-device* claim. No DIY equivalent. |
| **Pulse Wave Velocity (PWV) / Vascular Age / Arterial stiffness** | Arm→leg pressure wave transit time via impedance plethysmography | **No open DIY PWV scale.** PWV normally requires two synchronized PPG/ECG/pressure sites + known distance. BodyScan 2 cheats by using handle+foot electrodes as timing gates (patented). Closest open: dual MAX30102 PPG on wrist+ankle + ESP32 cross-correlation, but ±10ms jitter kills PWV (~5-10 m/s). | **0%** | Patented, calibrated, age-normed. DIY ± years of error. |
| **Multi-wave PPG → SpO₂** (red+IR LEDs on thumb) | Blood oxygen via light absorption | **MAX30102** (880nm IR + 660nm red, 18-bit ADC, 50-3200Hz, I²C 0x57) + ESP32 — dozens of open projects: `atomic14/max30102-esp32c3-oled-oximeter`, `XantyagoS/pulsioximetro-max30102-esp32` (240×240 GC9A01 round TFT), `how2electronics ESP32 Patient Health Monitor` (ECG+SpO₂+BPM+Temp+DASH). ~$8 sensor + $10 ESP32. SparkFun/Maxim libraries open. | **90%** | The sensor *is* the same principle (and likely same LED pair). Open reports are uncalibrated until fitted — medical accuracy requires FDA-style hypoxia testing. Good for trends. |
| **Electrodermal Skin Conductance (ESC) → Nerve Response Score** | Stimulates foot sweat glands, measures conductance; glucose resilience input | **No open ESC scale.** Closest: GSR/EDA open hardware (see `A Portable Sensor for Skin Bioimpedance` — ESP32-C3 + AD5933 + CD74HC4067 multiplexers, 15 sensors, <90ms acquisition, Wi-Fi, I²C). Used for stress/neuropathy research, not consumer scales. | **5%** | Concept exists in research/open EDA boards; no consumer-scale integration or validated Nerve Score. |
| **13-freq BIS to 800kHz → Cellular Age, ACM, Metabolic Efficiency** | Ultra-high freq membrane capacitance | AD5933/AD5941 DIY caps at 100kHz without exotic front end; **can't reach 800kHz**. No open Cole-model to 800kHz with 12-electrode segmental. | **30%** | You get low/high mix and basic phase angle, not cellular. Published 2019 SBISD paper (3kHz-1MHz, 280µA, NCT04006899) is the closest *research* device — not DIY-friendly cost. |

**TL;DR on ECG/SpO₂ open:** You *can* build an open ECG + SpO₂ vital monitor for ~$30-50 (ESP32 + AD8232 + MAX30102 + BME280 + 2.4" TFT, streaming to web dashboard via Wi-Fi) — multiple open repos do exactly that, with HR, HRV (RMSSD/SDNN/pNN50), SpO₂, respiration from PPG, temperature. **But it's a bedside monitor on your finger/chest, not a 90-second weigh-in.** PWV/ICG/ESC remain BodyScan 2 exclusives.

---

## 3. The Honest Feature-Match Matrix

*🟢 = Achievable open source · 🟡 = Partial / DIY-hard · 🔴 = No open equivalent · 💰 = Requires separate purchase/assembly*

| BodyScan 2 Feature | Sensor Behind It | Open-Source Status | How You Get It Openly | Gap vs Withings |
|--------------------|------------------|--------------------|-----------------------|-----------------|
| **Weight 50g, 5-200kg, Position Control™** | 4 load cells | 🟢 | Any openScale/BLE Sync scale; or SparkFun/Decent Open Scale DIY (HX711+ESP32) | Position Control™ is Withings UX polish — open just trusts you stand still |
| **BMI + trends** | Weight + height | 🟢 | openScale / BioScale / Bodymiscale — all local | None |
| **Fat mass kg/% whole + 6-zone segmental** | 13-freq BIS (12 electrodes) | 🟡 | **Foot-only scales via openScale/BLE Sync**: weight + impedance → open formula (2-4% vs DEXA typical). **Segmental**: *Only* Beurer BF710/800, Huawei Scale 3, Hume Dara 2.0 via openScale v3.1.3 expose arm/leg/torso fat/muscle — but foot-to-foot vs arm/leg split, not 6-zone + trunk + core. DIY segmental AD5933 (Nature 2026) exists but single-freq. | No 13-freq to 800kHz; no true 6-zone; no ITO full-plate precision; equations public but less tuned than Withings' population of millions |
| **Muscle / lean / skeletal muscle / bone / protein** | BIS derived | 🟡 | Same as above — BioScale uses Janssen 2000 (MRI-validated) for SMM; openScale Durnin & Womersley / Deurenberg | BodyScan 2's 13-freq gives better ECW/ICW split → muscle estimates more stable across hydration. Open is 1-2 freq, more hydration-volatile |
| **Body water total / ECW / ICW / fluid balance / hydration** | BIS high-freq | 🔴 (partial 🟡) | AD5933 DIY can do ECW vs mixture, but not clean ICW without >200kHz. Open apps compute water as 73% FFM (Pace & Rathbun) — estimate, not measured. | BodyScan 2 measures ICW directly at 800kHz; open estimates it |
| **Visceral fat index + trend** | Trunk impedance + waist model | 🟡 | openScale/BioScale visceral via trunk impedance + anthropometrics (same class of model as Withings). BioScale visceral is unlocked vs OKOK paywall. | Both sides are models, not imaging (vs CT/DEXA). Comparable. |
| **BMR / TDEE / calorie budget** | FFM + Mifflin-St Jeor etc. | 🟢 | Every open app does this locally | None — formula is public |
| **Vascular Age / PWV / arterial stiffness-elasticity** | PWV (arm→leg timing) | 🔴 | No open DIY. Dual-PPG hack is research, not product. | **Withings exclusive.** Must buy or skip. |
| **6-lead ECG + AFib** | Handle+foot electrodes + K230812 | 🔴 (single-lead 🟡) | AD8232 single-lead ECG + ESP32 (~$35) → trace on OLED/web; AFib via open algorithms (PhysioNet) but not certified | Withings gives *6-lead* + certified AFib + Body+ handle convenience. Open gives 1-lead + DIY electrodes + unverified detection. |
| **SpO₂ %** | Multi-wave PPG (handle) | 🟢 (but 💰 separate) | MAX30102 + ESP32 + open firmware (dozens of repos, $8). Same red/IR physics. | BodyScan 2 integrates it in the 90-sec scan. Open is a separate finger clip, separate step. |
| **Nerve Response Score (hands+feet)** | ESC / sudomotor | 🔴 | Research EDA boards exist (ESP32-C3 + AD5933 + multiplexers) but no scale integration | Withings wellness-tier only anyway; Wired questioned clinical use. Losable. |
| **Cardio Responsiveness / Efficiency** | ICG | 🔴 | None | Same as PWV — exclusive |
| **Heart Age** | ICG → age norms | 🔴 | No open norm tables + no ICG | Gated behind Withings+ anyway |
| **Glucose Resilience** | Visceral fat + ESC | 🔴 | Cannot — requires visceral + nerve + proprietary model; explicitly *not* glucose | Wellness proxy, H2 2026 rollout, unproven. Skip is fine. |
| **Cellular Age / ACM / Metabolic Efficiency / Metabolic Age** | 800kHz ultra-high BIS | 🔴 | No open 800kHz hardware; closest research SBISD 3kHz-1MHz is lab gear | Proprietary scores, no peer-reviewed validation. Interesting, not essential. |
| **Health Trajectory / BodyPath / Intelligence tiers / AI Assistant / Readiness / Improvement Score** | Cloud AI on all above | 🟡 | HealthLog: local AI insights (bring your LLM). Grafana dashboards + own trend logic. | You lose Withings' polish + population comparisons; you gain privacy + no sub |
| **Retractable handle + haptic guidance + in-scan survey + 3.2" LCD + 90-sec workflow** | Industrial design | 🔴 | No open handle-scale exists. DIY would be 3D-printed handle + buttons + OLED | BodyScan 2's *experience* is unmatched — daily 30s / weekly 90s scan is genuinely nicer |
| **8 users auto-recognition + Athlete/Pregnancy/Baby/Pet modes** | Software | 🟢 | openScale: manual user select + auto weight-matching (BLE Sync) + baby/pet assisted weighing | Auto-recognition via weight proximity, not ML — works |
| **Wi-Fi + BT + 8-user + lifetime storage + CSV/PDF + HealthLink sharing** | Cloud | 🟢 | openScale: CSV/SQLite export free forever; BLE Sync: CSV/JSONL + InfluxDB + MQTT; HealthLog: local DB + doctor share | Better — you *own* the DB |
| **API + Apple Health / Health Connect sync (the Oct 13 paywall)** | Withings Partner Hub | 🟢 | **The killer feature of open:** No account, no "AI Connector" toll. BLE Sync → MQTT → HA → Health Connect via openScale-sync = free forever. Withings now charges $99.50/yr for the same pipe. | Open wins on freedom; requires technical setup vs one-tap |

### Summary Score

| Category | Open Coverage | Note |
|----------|--------------|------|
| **Weight, BMI, basic BIA composition, BMR, trends, export, multi-user** | **90-100%** — equal or better (privacy, ownership) | Buy a $40-120 Beurer/Xiaomi/QN-Scale + openScale/BLE Sync = done |
| **Segmental 6-zone composition** | **30-50%** — only premium openScale models do arm/leg/torso, not core/abdomen, not 6-zone | Withings still leads |
| **ECW/ICW balance, hydration** | **20%** — estimated, not measured | Requires 800kHz; DIY can't |
| **Vascular Age / PWV / arterial stiffness** | **0%** | No open equivalent |
| **Heart Age / ICG cardiometabolic** | **0%** | BodyScan 2 world exclusive |
| **6-lead ECG + certified AFib** | **15%** (single-lead DIY) | Open gives trace, not diagnosis |
| **SpO₂** | **90%** but as separate device | MAX30102 is cheap and open |
| **Nerve / ESC / Glucose Resilience / Cellular scores** | **0-5%** | Wellness-tier anyway |
| **AI longevity scores / Trajectory / BodyPath** | **0% Withings-style; DIY via local LLM possible** | Different, not drop-in |
| **Handle/UX/retractable/90s scan** | **0%** | Industrial design moat |
| **Privacy / no subscription / data ownership / sync** | **100%+ — open wins outright** | The actual reason to go open |

**Overall if you count features 1:1:** Open hits **~55-60% of BodyScan 2's bullet list**, but **~85% of what most buyers actually use daily** (weight, fat, muscle, water, trends). The missing 40% is the *longevity station* pitch — heart, vessels, nerves, cellular — which is also the least validated.

---

## 4. Three Concrete Open Stacks You Can Build Today

### Stack A: "I Just Want Private Weight + Composition, No Cloud, No Sub" — $40-120, 30 min
1. Buy **Beurer BF700/800, Xiaomi Mi Body Composition Scale 2, Eufy C1, or any QN-Scale/RENPHO** ($30-120) — all fully reverse-engineered.
2. Install **openScale** (F-Droid) on Android — or **BioScale** if your scale was Chipsea/OKOK.
3. Pair once. Weigh. Done. Graphs, BMR, visceral, bone, multi-user, CSV export — no account ever.
4. Optional headless: Raspberry Pi Zero 2 W ($15) + **BLE Scale Sync** (Docker) + Home Assistant + InfluxDB → auto MQTT on every weigh-in, no phone needed, Garmin/Strava sync free.

**Matches BodyScan 2:** Weight, all basic composition, BMR, trends, export — 100%. **Misses:** No segmental 6-zone (unless you pick BF710/800 or Hume Dara via openScale 3.1.3), no ECG/Vascular/SpO₂/Nerve.

### Stack B: "I Want Segmental + Home Assistant + Local AI" — $80-200, 1-2 hours
1. Same scale but **prioritize segmental models:** Beurer BF710/BF800, Huawei Scale 3, Hume Dara 2.0 — confirmed in openScale 3.1.3 to expose **segmental fat & muscle per arm/leg/torso + metabolic age** with individual CSV columns.
2. **BLE Scale Sync on Pi** + **Bodymiscale** in Home Assistant: the Pi catches passive BLE broadcasts (no pairing), Bodymiscale runs scientific BIA equations locally, HA creates 12+ entities, auto weight-matching for family.
3. **HealthLog (AGPL)** on same Pi/NAS (Docker): Withings/Apple Health import if migrating, long-term DB, mood/meds/BP/glucose, **local LLM insights** (you bring Ollama).
4. Dashboard: Grafana over InfluxDB for 5-year trajectories that rival BodyPath.

**Matches BodyScan 2:** Everything in Stack A + segmental (torso/legs/arms) + self-hosted Health Trajectory approximation. **Still misses:** No 800kHz cellular, no PWV/Vascular Age, no ICG/Heart Age, no handle UX.

### Stack C: "I Want to Replicate the Handles — Full DIY" — $150-300, weekend project, soldering required
1. **Weight base:** SparkFun OpenScale IoT (ESP32+HX711) or Decent Open Scale (ESP32-S3+HX711+OLED) — open HW/FW, calibrated load cells.
2. **BIA add-on:** AD5933 eval board (~$25) + external analog front end (AD8606 op-amps, 1MΩ current limiter, isolation, protection diodes) + **8 ITO-like electrodes** (stainless tape or custom PCB) + CD74HC4067 multiplexers for 6-zone switching — follow the Nature 2026 segmental BIA paper (single-freq, <7% error) and the 3kHz-1MHz SBISD paper (NCT04006899) for high-band compensation.
3. **ECG add-on:** AD8232 module ($10) + 3-electrode chest/hand strap + ESP32-S3 250Hz sampling + `ecg-ad8232-esp32` firmware → trace on OLED + BLE to phone/HA. Not 6-lead, not certified, but real.
4. **SpO₂ add-on:** MAX30102 breakout ($8) on shared I²C bus → same ESP32 → heart rate + calibrated SpO₂ (Maxim algorithm, 25Hz).
5. **Firmware:** ESPHome/Arduino merging weight + BIA + ECG + PPG into one BLE GATT device that mimics the "Custom Bluetooth Scale" openScale expects — so openScale/BLE Sync can ingest it.

**Matches BodyScan 2:** Weight + multi-freq BIA (to ~100kHz) + single-lead ECG + SpO₂ + DIY handle, all local. **Still misses:** No true 800kHz (need AD5941 + wideband front end, ×3 cost), no ICG/PWV/ESC/Cellular Age, no retractable cable/haptics, no FDA/CE, no polished app.

> **Reality check:** Stack C is a *thesis*, not a product. Published cost $80-150 in parts but 40-80 hours of calibration, safety testing, and equation tuning to get within BodyScan 2's accuracy — and you still won't pass regulators. Stacks A/B are the practical "open alternatives" most people mean.

---

## 5. Why No Open Project Equals BodyScan 2 — The Structural Reasons

1. **IP & calibration moat:** 13-freq to 800kHz isn't just a chip — it's *population-specific prediction equations* trained on thousands of DEXA + BIS pairs per demographic (age/sex/ethnicity/BMI). Withings owns that dataset from millions of scales. Open has the *formulas* (Deurenberg, Janssen, Kyle) but not the *coefficients* for 800kHz + 6-zone + ITO. Rebuilding requires a DEXA lab partnership.

2. **Medical regulation tax:** 6-lead ECG + AFib + hypertension risk + (in EU) PWV are *regulated medical claims*. Open can publish code, but cannot publish a certified diagnosis without 510(k)/CE MDR, clinical trials, ISO 13485 QMS. So open ECG stops at "trace" — Withings can say "AFib."

3. **Sensor fusion & UX:** Handle + haptics + auto-locking cable + Position Control™ + air quality + 90-second guided flow is *industrial design* — not schematics you can fork. It's also where BodyScan 2 *feels* premium.

4. **Scale economics:** Withings amortizes firmware, app, cloud, regulatory, and AI across millions of units. DIY amortizes across *you*. A $120 Beurer + openScale beats Withings on price/privacy, but *only* for basic composition — which is exactly the market Wyze ($120) and Hume ($249) also target commercially without subscription.

---

## 6. The Bottom Line — When to Go Open vs. When BodyScan 2 Still Wins

| You Are... | Do This |
|------------|---------|
| **Privacy-first, hate subscriptions, only need weight + fat/muscle/water trends** | **Stack A** — Beurer/Xiaomi/QN-Scale + openScale + BLE Sync. $40-120, no account, no paywall, CSV forever. You lose nothing that matters daily. |
| **Data hoarder who wants HA/Grafana/long-term, maybe segmental** | **Stack B** — Beurer BF710/800 or Hume Dara 2.0 + openScale 3.1.3 + BLE Sync + Bodymiscale + InfluxDB/Grafana/HealthLog. Best open "BodyPath" clone. 80% of the composition story, 100% local. |
| **Maker / researcher / thesis / quantified-self hacker** | Stack C — AD5933/AD5941 + HX711 + AD8232 + MAX30102 + ESP32, build the handle yourself. Genuinely educational, potentially publishable, but months of work to approach BodyScan 2's *composition* half, never its *cardio* half. |
| **Cardiometabolic risk (family AFib, midlife hypertension, GLP-1 muscle guard), want vascular age + ECG + ICG in one weigh-in** | **BodyScan 2** — there is no open alternative for ICG, PWV, Heart Age, or 6-lead. Budget $600 + $99.50/yr if you want Heart Age/Glucose Resilience/Apple Health sync as a new user — or create account now and go open-pipe via HA hack. |
| **Want best accuracy without DIY** | **Cheap handle scale + periodic DEXA** ($120 Wyze Ultra or $250 Hume + $75-150 DEXA every 6-12mo) — more accurate than any open *or* Withings BIA alone. The open community recommends this combo too. |

### The "Protest" Option If You Already Own (or Still Want) BodyScan 2
You don't have to accept the Oct 13 sync paywall to get the hardware:

1. Use Health Mate for the advanced sensors (they're free: Vascular Age, ECG trace, SpO₂, Nerve Score) but treat it as a *staging area*.
2. **ESP32 + ESPHome Body+ hack** lineage (didac.dev Sep 2026, open on GitHub) proves Withings BLE is interceptable — duplicate the weigh-in locally to HA/MQTT before it ever hits the cloud.
3. Keep your **pre-Oct 12, 2026 Withings account** for grandfathered free sync; if you're post-Oct 13, use **BLE Scale Sync → HA → Health Connect** as a parallel pipe — Withings+ becomes optional, not mandatory.

---

## Sources (Oct 17, 2026)

`oliexdev/openScale` (2,273★, GPLv3) + Wiki (Supported scales: 80+ models, Custom Bluetooth Scale, Xiaomi/Beurer pages) + releases 3.1.3/3.1.2; `eayrenk/bioscale-okok-alternative` (MIT) + `brumathey` fork; `etlami/opentara` (iOS, Chipsea/BT-SIG); `dckiller51/bodymiscale` (HA, 3 models); `KristianP26/ble-scale-sync` (35+ adapters, 25+ brands, Garmin/MQTT/InfluxDB); `didac.dev` Sep 3 2026 Withings Body+ ESP32 + HN discussion; Prolixium DNS hack (2010); SparkFun OpenScale IoT (Mar 2026); `decentespresso/openscale` (ESP32-S3); Spectra EIT (32-electrode, 160kSPS); AD5933 EDA/Biomarker DIY papers (dyarleniber GPv3, Nature 2025/2026 segmental BIA, SciDirect SE2DoBID $80.50, Instructables); `leybme/bioimpedance_measurement` (ESP32-S3+AD5941); `XantyagoS/ecg-ad8232-esp32` + `Doenec/ecg-esp32` + `Alpusa/AWECG-Monitor` + `kursancew/ekg-ad8232` (AD8232); `atomic14/max30102-esp32c3-oled-oximeter` + `how2electronics ESP32 Patient Health Monitor` (MAX30102); `MBombeck/HealthLog` (AGPL) + `TraceApps/nutritrace` + `roessland/withoutings` + `DavidVentura/withouthings`; Home Assistant Withings integration (cloud push, 1.5% installs); HA community Xiaomi Mi Scale threads; HardwareRecs cloud-free scales (2019, updated).

*Companion docs:* [Full Dissection](./BodyScan-2-Dissection.md) · [Biomarkers + DEXA Deep Dive](./BodyScan-2-Biomarkers-DEXA-Deep-Dive.md)

```
Open stacks:  A) $40-120 openScale + BLE Sync (30 min) → 90% daily composition, 100% private
              B) $80-200 + segmental scale + HA + Bodymiscale + HealthLog/Grafana → best open BodyPath
              C) $150-300 DIY AD5933/AD5941 + HX711 + AD8232 + MAX30102 + ESP32 → thesis, not product
Coverage:     Weight/BIA/BMR/trends/export: 🟢  Segmental 6-zone: 🟡  ECW/ICW 800kHz cellular: 🔴
              PWV/Vascular/ICG/Heart Age: 🔴 (exclusive)  6-lead ECG: 🔴 (1-lead DIY 🟡)  SpO₂: 🟢 separate  ESC/Nerve: 🔴
```

