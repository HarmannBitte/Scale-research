# Separate hardware search: Body Scan 2 alternatives and complements

**Research date: 17 October 2026.** Scope: finished commercial instruments **separated from** open hardware, evaluation boards and research builds. This is a new hardware investigation, not a repetition of the software-integration shortlist. No hardware was purchased, electrically tested, connected to a person, or tested over BLE in this pass. Prices are observed listings, not purchase quotes or guarantees of stock.

## Executive findings

1. **There is still no established, open, integrated equivalent across regional body composition, multilead ECG, cardiac impedance cardiography, PWV and electrochemical sudomotor testing.** Modular instruments can cover more of the underlying signals, but lose the convenience and common validation of a finished system.
2. **Tanita MC-780U PLUS S is a credible currently listed segmental instrument**: $6,999.99 with Add to Cart, SD/USB/RS-232 outputs, and advertised resistance/reactance/phase data. Obtain a sample export before purchase: an output connector or a results CSV does not prove every raw segment/frequency is exported. [Tanita product page](https://tanita.com/products/mc-780u-plus-s-multi-frequency-segmental-body-composition-analyzer)
3. **SFB7 is an excellent technical reference but not an ordinary new-device recommendation.** ImpediMed ended standard sales on **1 November 2025**. Residual inventory/used units need separate support and software checks. Its 256-frequency raw impedance capability does not override this purchasing problem. [Discontinuation notice](https://www.impedimed.com/wp-content/uploads/2025/10/M-371-Rev-A-ImpediMed-SFB7-and-ImpediVET-Notice-of-Discontinue.pdf)
4. **seca mBCA 525 deserves a raw-data quotation**, not a blanket subscription-free recommendation: official support explicitly describes raw-impedance CSV export through analytics 115; newer software bundles and annual licences must be checked separately. [seca support](https://www.seca.com/en_gb/support/technical-service/customer-education-portal/525-525c/525/faq.html)
5. **MAX30009 is the strongest engineering starting point found for impedance spectroscopy and dynamic BioZ**, not a ready-made body-composition scale or validated cardiac-output monitor. It provides I/Q acquisition and configurable bipolar/tetrapolar paths; safe complete-system design, calibration, switching and physiological validation remain work. [ADI](https://www.analog.com/en/products/max30009.html)
6. **HealthyPi 6 is interesting genuinely published hardware, but $599 is a preorder listing**, with estimated shipping 30 October 2026, not evidence of a mature currently shipping product. Its impedance channel is for thoracic respiration, not demonstrated body-composition BIS or cardiac ICG. [Crowd Supply](https://www.crowdsupply.com/protocentral/healthypi-6)
7. **The ESC gap is real.** SUDOSCAN is a relevant finished clinical instrument, but its commercial models include pay-per-test and electrode costs. Ordinary EDA boards, potentiostats and GSR-capable BioZ chips are not validated replacements. [US catalog](https://us.sudoscan.com/collections/all)

## 1. What must actually be measured?

| Target capability | Signals needed or relevant | What does **not** establish equivalence |
|---|---|---|
| Weight | Calibrated force/load-cell signal | “24-bit ADC” alone; resolution is not accuracy |
| Regional BIA/BIS | Known excitation, electrode paths, complex impedance by frequency; geometry and an explicitly validated model for composition | Eight metal contacts or many displayed metrics; whole-body estimates divided into fixed regional proportions |
| ECG | Calibrated differential electrical waveform, defined lead vectors, bandwidth and timing | Pulse rate or PPG; three electrodes do not necessarily mean three independent channels |
| Cardiac ICG | Small pulsatile thoracic impedance changes, Z(t)/dZ/dt, suitable bandwidth and usually ECG synchronization | A respiration trace labelled BioZ; slow whole-body frequency sweeps |
| PWV | Vascular wave timing at defined sites, synchronization and path length appropriate to the method | ECG-to-finger delay alone: this is generally pulse-arrival time and includes pre-ejection time |
| ESC/sudomotor | Controlled electrochemical protocol, defined electrode materials/geometry, current/voltage response, reference validation | Generic skin resistance/EDA, a stress score, or nerve-conduction velocity |
| SpO₂ | Red/infrared optical signals plus a validated calibration/algorithm and suitable probe | A raw PPG breakout, or a green-only heart-rate sensor |
| Temperature, respiration, motion | Defined sensor site, response, scale and sampling | Inferring core temperature from an unvalidated skin sensor |

**Calculated quantities remain calculated.** Fat mass, extracellular/intracellular water, cardiac output, vascular age and risk scores are not independent physical sensors. More frequencies or channels improve available information, not automatically accuracy. This report evaluates complements as well as replacements; listing SpO₂ or temperature does not assert that every target product measures them.

# PART A — Finished commercial devices

## 2. Body composition and impedance instruments

### A1. Tanita MC-780U PLUS S — most concrete current segmental purchase lead

- **Maturity/price:** official US listing shows **$6,999.99** and Add to Cart. Commercial finished instrument; delivery and eligibility still need confirmation.
- **Measurement:** segmental multifrequency BIA. The MC-780 family manual documents eight-contact hand/foot measurements at **5, 50 and 250 kHz**; verify the precise US PLUS revision against its supplied manual rather than assuming all MC-780 variants are identical.
- **Data:** official US page advertises bioelectric data, resistance/reactance/phase angle, segmental phase angle, SD, USB and RS-232 outputs. Its “Connectivity None” field appears alongside these physical outputs—do not read it as “no export.”
- **Remaining question:** exactly which segment/frequency R and Xc fields appear in the purchased configuration's exported records? Ask for a de-identified machine-generated file, not just the printout.
- **Calibration:** manufacturer advertises automatic calibration before each analysis. This does not independently validate an individual's body-fat estimate or replace scale metrology checks.
- **Fees:** no compulsory consumer membership established from the examined product page. Confirm software, serial protocol documentation, support, export permissions and updates in writing. “Not established” is not a guarantee of no future fees.
- **Coverage:** regional composition and impedance; **not** ECG, cardiac ICG, PWV, ESC or SpO₂.

Sources: [US device](https://tanita.com/products/mc-780u-plus-s-multi-frequency-segmental-body-composition-analyzer); [MC-780 family manual](https://tanita.eu/media/pdf/products-tanita/professional/MC-780/MC-780MA%20N%20Instruction%20Manual%20(EN)%202018%20(2).pdf).

### A2. seca mBCA 525 / 525c — strong clinical data lead, software-generation caveat

- Supine segmental measurement using a cabled electrode mat and adhesive skin electrodes, rather than a stand-on household scale. Official support identifies validated electrode types and preparation requirements.
- A 525 international specification lists **nine frequencies: 1, 2, 5, 10, 20, 50, 100, 200 and 500 kHz**. Older regional material can differ: confirm model/revision rather than merging specifications.
- Raw-data evidence is stronger than a generic “CSV export” claim: seca support's troubleshooting instructions explicitly request CSV **including raw impedance data** from **seca analytics 115**.
- This evidence belongs to a particular device/software workflow. It does **not** prove that every current 125/cloud package has the same offline export or licence terms.
- One UK distributor listing showed **£3,239.99 including VAT** and explicitly required an **annual seca 125 licence**. Treat that as a specific regional bundle, not a worldwide fixed price or a property of every used 525.
- Get a quote for hardware, mat/cables, electrodes, software generation, local storage, raw export, renewal and what survives cancellation. Budget electrode consumables.
- The 514/515 manuals are additional legacy leads: extended raw-data acquisition may differ from the standard short measurement. Do not extrapolate this to the 525/580 without a manual and sample file.

Sources: [525 technical sheet](https://www.seca.com/fileadmin/documents/product_sheet/seca_pst_525_en_int.pdf); [official FAQ/export workflow](https://www.seca.com/en_gb/support/technical-service/customer-education-portal/525-525c/525/faq.html); [UK bundle](https://www.habdirect.com/product/seca-mbca-525-body-composition-analyser/); [514/515 manual](https://www.seca.com/fileadmin/documents/manual/seca_man_514_515_en.pdf).

### A3. ImpediMed SFB7 — technically attractive, **discontinued**

- Single-channel **tetrapolar** BIS, **256 frequencies, 3–1000 kHz**, under-one-second readings; single, interval and continuous modes; manufacturer explicitly offers **all raw impedance data**.
- A single tetrapolar channel can measure an intentionally selected path; it is **not** automatic simultaneous five-region hand/foot analysis. Changing electrode placement changes the experiment and its validated interpretation.
- Tissue/fluid outputs use Cole modelling and Hanai mixture theory; raw data and model outputs must remain distinct.
- **Critical purchasing correction:** standard sales ended **1 November 2025**, according to the manufacturer. Remaining inventory might briefly exist through distributors; warranty support is limited by the actual agreement. A live informational product page is not evidence of normal availability.
- For a used/residual unit: verify serial-number support, BioImp installer access, licence transfer, cable/electrode availability, calibration/service and current computer compatibility **before paying**.
- SOZO is the named commercial successor, but the discontinuation notice does not establish equivalent unrestricted research raw export, offline operation or pricing. Do not substitute it without those answers.

Sources: [SFB7 capabilities](https://www.impedimed.com/products/research-devices/sfb7/); [binding purchasing qualification](https://www.impedimed.com/wp-content/uploads/2025/10/M-371-Rev-A-ImpediMed-SFB7-and-ImpediVET-Notice-of-Discontinue.pdf).

### A4. Sciospec Medical Research ISX-3 / EIT systems — instrumentation rather than a scale

- The current standard ISX-3 specification lists **100 mHz–10 MHz**, up to **2048 sweep points**. Optional higher-frequency models and multiplexers have separate limitations; do not apply a base analyzer's best specification to every switched path.
- **Use the Medical Research configuration for electrically human-connected research**, not the ordinary laboratory analyzer. Isolation must cover the whole installed system, including communications and attached equipment.
- The EIT family adds configurable electrode injection/measurement arrangements and open reconstruction workflows. EIT16 is specified separately at **100 Hz–1 MHz**. EIT images conductivity changes; it does not automatically deliver accurate five-region fat/muscle mass.
- Closed commercial instruments can have useful APIs and raw data without being open hardware. Obtain example measurements, protocol/API documentation and perpetual/offline rights in the quote.
- Cost is laboratory-class. Distributor listings show roughly five-figure systems and separately priced medical-safety options; **do not buy a cheaper nonisolated configuration for body connection**.

Sources: [ISX-3](https://sciospec.com/product/isx-3/); [EIT option and routing constraints](https://sciospec.com/product/isx-3eit/); [EIT16](https://sciospec.com/product/eit16/); [medical configuration](https://www.saelig.com/product/isx-3.htm). An independent Python interface exists, but its README marks ISX-3 communication as work in progress: [16](https://github.com/EITLabworks/sciopy).

### A5. Myolex mScan / older mView — local muscle quality, not whole-body composition

A useful adjacent category: **electrical impedance myography (EIM)** measures a local muscle with a defined electrode array and orientation. A 2026 mScan study describes **41 frequencies from 1 kHz to 10 MHz**, nested four-electrode arrays, Bluetooth and a proprietary iPad app. This is not a stand-on regional BIA scale, nerve-conduction test or open app ecosystem. Historical mView raw multifrequency studies do not establish current mScan export rights; some older arrays are no longer manufactured. Quote-only purchasing, raw export, electrode costs and software renewal remain unresolved. [3](https://link.springer.com/article/10.1007/s10439-026-04175-w), [1](https://pmc.ncbi.nlm.nih.gov/articles/PMC13438509/).

## 3. ECG, cardiac ICG, PWV and ESC: buyable but separate instruments

| Instrument | Actual capability / electrodes | Raw access and maturity | Cost/fee caveat |
|---|---|---|---|
| **Polar H10** | Wearable chest ECG, HR/RR; not a diagnostic multilead ECG | Official SDK documents **130 Hz ECG in microvolts**. Closed hardware with direct BLE development access | Hardware purchase plus eventual strap/electrode wear; custom SDK collection is not WHOOP integration |
| **BIOPAC NICO100C + acquisition system + ECG** | Thoracic ICG; separate injection/sensing electrodes; Z and dZ/dt; four selectable excitation frequencies spanning **12.5–100 kHz** | Finished research instrumentation; raw analog waveform outputs. Requires a compatible acquisition system, not a standalone USB sensor | Quote complete system, ECG channel, cables, software and analysis add-ons; do not price just the module |
| **BIOPAC EBI100C** | Impedance magnitude and phase | Different outputs from NICO100C; derivative can be computed in software | Same system/accessory/software issues; not an automatic broad-spectrum composition analyzer |
| **PhysioFlow Q-Link / Enduro** | Six thoracic electrodes; signal-morphology ICG; ECG and hemodynamic estimates | Established proprietary clinical/research platform; Q-Link has FDA 510(k) documentation. Raw waveform export not established here | Obtain quote, electrode requirements, software licence and a waveform export sample. Derived CSV alone is insufficient |
| **SphygmoCor XCEL, PWV-capable configuration** | Carotid tonometry plus thigh cuff and measured distance for carotid-femoral PWV | Clinical/research commercial system; not equivalent to ECG-to-finger PAT | Quote-only; confirm PWV configuration, software/export and calibration/service. Not every XCEL bundle necessarily includes PWV |
| **SUDOSCAN 3** | Hand/foot electrochemical skin conductance; defined low-voltage DC electrochemical method | Finished professional sudomotor instrument, not general nerve conduction or a generic EDA stress sensor | US listings: **$17,990 new**, **$13,990 demo**, **$4,195 pay-per-test**. These are different commercial offers, not interchangeable lifetime prices |

Sources: [Polar raw ECG specification](https://github.com/polarofficial/polar-ble-sdk/blob/master/documentation/products/PolarH10.md); [BIOPAC NICO100C](https://www.biopac.com/product/noninvasive-cardiac-output-module/); [BIOPAC output distinction](https://www.biopac.com/knowledge-base/differences-between-the-nico100c-and-ebi100c/); [BIOPAC analysis add-on](https://www.biopac.com/product/impedance-cardiography-analysis-software-module/); [PhysioFlow product details](https://physioflow.com/products_physioflow.php); [FDA Q-Link record](https://www.accessdata.fda.gov/cdrh_docs/pdf14/K140102.pdf); [SphygmoCor](https://atcormedical.com/technology/sphygmocor-xcel/); [US SUDOSCAN prices](https://us.sudoscan.com/collections/all); [US physician indication and method](https://us.sudoscan.com/pages/for_physicians).

**SUDOSCAN ownership deserves special scrutiny:** the catalog also lists renewable sensor plates at **$2,750**, disposable smart electrodes at **$3,500**, and an S version at **$2,750**. Product applicability, test allowances, replacement/recharge rules and cancellation terms need the precise contract. Do not assume “buy the device once” means unlimited future tests. Nor should lower hardware cost be confused with lower lifetime cost. [Catalog](https://us.sudoscan.com/collections/all).

For SpO₂ and blood pressure used for health decisions, a validated finished fingertip oximeter and validated upper-arm cuff are a different purchasing problem from an open optical/pressure research board. This pass does not establish a particular no-account model with raw waveform export; therefore none is presented as a verified integrated solution.

# PART B — Open hardware, evaluation platforms and research builds

## 4. Strongest practical engineering candidates

### B1. MAX30009 EV kit — impedance acquisition foundation

**What is real:** the chip supports two- or four-electrode configurations, simultaneous **I/Q** measurement, selectable sample rates **16 samples/s–4 ksamples/s**, calibration facilities, and synchronization with other AFEs. ADI publishes EV-kit design files, logging software and a no-OS driver. The kit includes separate MCU and sensor boards, battery operation and BLE/Windows GUI access. [Chip](https://www.analog.com/en/products/max30009.html); [kit and design files](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/max30009evkit.html); [driver](https://analogdevicesinc.github.io/no-OS/projects/afe/max30009.html).

**Frequency caveat:** the current product page's feature list gives BIA/BIS **1–806 kHz**, while its descriptive paragraph says a **16 Hz–500 kHz** transmitter range. These should not be silently combined into a guaranteed 16 Hz–806 kHz specification for every mode. Resolve against the current datasheet, clock and register settings for the intended operating mode.

**What remains:** MCU/host software, electrical safety, electrode/cable design, complex calibration over the intended load/frequency range, segment switching if wanted, timing, artefact rejection, a validated tissue model, enclosure and verification. I/Q counts need calibration/scaling; they are not automatically trustworthy R/Xc or fat mass.

**Openness:** published evaluation files and an open driver are useful, but not proof that the whole kit/Windows GUI is OSI-open or licensed as a complete open-hardware product. Check each component's licence. Availability/price evidence was inconsistent across distributors; do not treat a search price as an in-stock offer.

**Recommendation:** top impedance engineering lead, initially on calibrated electrical phantoms. Not a plug-and-play replacement for a consumer scale, SFB7, clinical ICG or SUDOSCAN.

### B2. AD5940 / AD5941 — flexible impedance/electrochemistry alternative

ADI explicitly positions these AFEs for skin/body impedance and electrochemical sensing, with a switch matrix, DFT-based complex measurements and high-speed excitation up to **200 kHz**. This is useful for a custom instrument, but differs from the MAX30009 in architecture and frequency ceiling. Calibration, lead configuration, output scaling, safety and implementation-specific bandwidth still matter. It is not an ESC nerve-function device just because it supports voltammetry or skin impedance. [ADI specification](https://www.analog.com/en/products/ad5940.html).

### B3. ProtoCentral MAX86150 — published ECG + red/IR PPG hardware

Published schematic/board files and software make this a relatively accessible optical/electrical research route. The inspected repository's licence separates **CERN-OHL-P v2 hardware**, **MIT software** and **CC-BY-SA documentation**. This is materially stronger evidence than an “open” marketing label. [Repository](https://github.com/Protocentral/protocentral_max86150_ecg_ppg); [product](https://protocentral.com/product/protocentral-max86150-ppg-and-ecg-breakout-with-qwiic-v2/).

It supplies ECG/optical signals, **not** regional impedance, ESC or cardiac ICG. Red/IR PPG is not by itself a clinically validated SpO₂ algorithm. Touch/contact artefacts and timing must be characterized. A small board is not a protected finished patient monitor.

### B4. MAX86176 — newer synchronized ECG/PPG design route

This AFE explicitly targets synchronous ECG and PPG, with dedicated acquisition paths. It is a promising companion to MAX30009 where common timing matters. It is a component/development route, not a complete open, medically validated system. Even perfectly synchronized ECG and PPG do **not** by themselves establish PWV, central pressure or reliable cuffless blood pressure. [ADI](https://www.analog.com/en/products/max86176.html).

### B5. MAX30001 / ADS1292R / ADS1293 breakouts — useful, but different modalities

- **MAX30001 / tinyECG:** single-lead ECG and BioZ **respiration**, plus R–R detection. A respiration demonstration is not evidence of validated cardiac-output ICG or broad composition spectroscopy.
- **ADS1292R:** ECG/respiration acquisition route.
- **ADS1293:** three simultaneous ECG-channel breakout route; clarify actual lead connections and calculated leads.
- **AFE4490:** red/IR optical acquisition route; clinical SpO₂ still depends on implementation and calibration.

ProtoCentral lists these separately in its viewer compatibility table—do not collapse them into one all-sensor board. [MAX30001 device](https://protocentral.com/product/protocentral-max30001/); [viewer/hardware compatibility](https://protocentral.com/openview/).

## 5. HealthyPi family: closest integrated *research monitor*, not Body Scan parity

### HealthyPi 6 — open design with preorder risk

- **Listing:** **$599 preorder**, estimated ship **30 October 2026**. The campaign's 8 September update describes waiting on batteries. Estimates can change; the date is after this report's research date.
- **Core sensing:** advertised three-channel/five-lead ECG, red/IR PPG, thoracic impedance respiration, temperature and motion; storage/export workflows advertised via microSD and HealthyPi Studio, including CSV/EDF.
- **Published electrical design:** separate hardware repository identifies **ADS1294R**, **AFE4400**, **BMI323**, STM32H757 and ESP32-C6; isolated supply/USB, microSD and HealthyLink expansion. The current README describes KiCad 10 files and notes some missing external 3D-model paths.
- **Licensing correction:** current hardware is **CERN-OHL-P v2**. The current firmware licence says project code is **MIT**, with Apache-2.0 upstream-derived files, OFL fonts and separately governed dependencies. Older campaign shorthand is less authoritative than current per-file terms. Optional compute-module firmware has separate terms; do not assume an expansion's NPU runtime is also open merely because the base monitor is.
- **Medical status:** the hardware README expressly says research/education/evaluation only. Its CE/UKCA declarations cover electronic-product safety/EMC, **not medical diagnostic clearance**.
- **No demonstrated parity:** not regional composition BIS, not validated cardiac ICG, not validated PWV, not ESC. Expansion sockets are not presently delivered sensors.
- **Unverified:** no firmware build, electrical safety verification, timestamp test, real export round-trip, or shipment verification was performed here.

Sources: [campaign/status](https://www.crowdsupply.com/protocentral/healthypi-6); [hardware and explicit safety/status statement](https://github.com/Protocentral/protocentral_healthypi6_hardware); [firmware](https://github.com/Protocentral/healthypi-6-fw); [actual firmware licence](https://github.com/Protocentral/healthypi-6-fw/blob/main/LICENSE.md).

### HealthyPi 5 and Move

HealthyPi 5's documented front ends are MAX30001 for ECG/BioZ, AFE4400 for red/IR PPG, and an I²C temperature sensor, with RP2040/ESP32-C3 processing. It is an older integrated acquisition lead; current stock and complete kit cost were not established here. [Documentation](https://protocentral.com/product/healthypi-5-vital-signs-monitoring-hat-kit/docs/introduction/).

Move is an adjacent wearable candidate, but open schematics/firmware do not imply that every sensor-hub algorithm, especially SpO₂/BP-related processing, is open or independently validated. Inspect the particular firmware, hub and algorithm licences before committing. Neither product should be relabelled an open Body Scan equivalent.

## 6. Other open/research projects: useful leads and important exclusions

| Project | Hardware/source evidence | Role and limitation |
|---|---|---|
| **uECG** | Official firmware MIT; separate PCB repository **CERN-OHL-P-2.0**, KiCad | Small ECG wearable with raw/processed radio data. Match PCB, firmware, receiver and app versions; current stock and full build not verified. GSR support does not mean ESC |
| **HeartyPatch** | Published ESP32 single-lead ECG hardware/firmware project | Useful historical open wearable route. Do not infer current product stock or active support from its old crowdfunding page |
| **Card/IO** | Public KiCad 7 main-board/front-end designs, enclosure | Single-lead card-format ECG. No explicit licence surfaced in the examined hardware root/README; “public” and “called open source” are not sufficient licensing confirmation |
| **BioGAP** | Local source inspection: hardware **Solderpad 0.51**, firmware **Apache-2.0**; hardware directories for main board, ExG/EMG/PPG shields | Advanced multichannel ExG/EMG + PPG research platform; not composition BIS, ESC or a clinical all-in-one |
| **OpenCardiographySignalMeasuringDevice** | Local inspection: root **GPL-3.0** text, custom board/design files, Pico W firmware, Python GUI and analysis, CSV recording | ECG, PPG, cuff pressure and stethoscope—not proof of cardiac ICG. **Unresolved protection/isolation faults explicitly documented; do not use as a ready safe body-connected device** |
| **OpenEIT / EIT_EE** | Published EIT electronics research route | Reconstructed conductivity/respiration imaging is not automatically body composition or ICG. Full design/licence/safety reproduction not established in this pass |
| **BIMMS** | Public research-control repository; Digilent WaveForms dependency and hardware TODOs | Interesting measurement-system lead, not a complete validated turnkey body analyzer |
| **WULPUS** | Local inspection: hardware **Solderpad 0.51**, host software **Apache-2.0**; acquisition/HV CAD, MCU firmware and host software | Eight time-multiplexed ultrasound channels, raw acquisition. Possible structural/vascular research complement, not BIA/ESC or a ready clinical scanner |
| **TinyProbe** | Current public hardware, MCU firmware and host code; README says **FPGA gateware release planned** | 32-channel ultrasound with raw RF modes. Missing gateware prevents calling the entire published system fully reproducible from source today |
| **SparkFun OpenScale / HX711** | Published load-cell board and firmware; not the Android openScale app | An account-free **weight** subsystem. A 10/80 samples/s load-cell ADC does not, without mechanics/noise/timing validation, establish useful ballistocardiography or PWV |
| **DStat / UWED / other potentiostats** | Electrochemistry research instruments | Not verified medical ESC or neuropathy-test replacements. Do not attach a general lab potentiostat to a person |

Sources: [uECG firmware](https://github.com/ultimaterobotics/uECG), [7](https://github.com/ultimaterobotics/uECG_pcb); [HeartyPatch](https://www.crowdsupply.com/protocentral/heartypatch); [Card/IO](https://github.com/card-io-ecg/card-io-hw); [BioGAP](https://github.com/pulp-bio/BioGAP); [open cardiography prototype](https://github.com/MilosRasic98/OpenCardiographySignalMeasuringDevice); [OpenEIT](https://github.com/OpenEIT/EIT_EE); [BIMMS](https://github.com/fkolbl/BIMMS); [WULPUS](https://github.com/pulp-bio/wulpus); [TinyProbe including gateware qualification](https://github.com/pulp-bio/TinyProbe); [SparkFun OpenScale](https://github.com/sparkfun/OpenScale).

### Why the open cardiography prototype is not on the recommended build list

Its README's **ERRORS** section reports an unvalidated protection circuit, an isolated power supply not working as intended and a wrong pressure-sensor pinout. Charging is also described as unvalidated. These are not cosmetic bugs. A root GPL file and published Gerbers do not establish electrical safety. Its limited comparison against a commercial cuff is not a standards-based population validation. Its broad claims about cuff-monitor validation should not be treated as authoritative clinical guidance. Retain it as a design/analysis reference only until competent engineering remediation and appropriate independent verification.

### Ultrasound is a genuinely different complement

WULPUS and TinyProbe can expose measurements unavailable from a household scale, but ultrasound needs acoustic-output characterization, a suitable transducer/coupling arrangement, qualified operation and an independently validated analysis. Neither is an easy method for obtaining equivalent visceral-fat mass, nerve function or a validated PWV number. TinyProbe's unpublished gateware is a particularly concrete reproducibility limitation—not merely a missing shopping link.

# 7. Calibration and verification: where the hard work actually is

**For impedance:** verify known resistive and RC loads across the entire frequency/load envelope; determine gain/phase error, cable parasitics, repeatability, drift and electrode/contact effects. Validate every switched path, not only an internal calibration resistor. In a tetrapolar design, separate current and voltage electrodes reduce some contact effects but do not eliminate all geometry and interface error.

**For cardiac ICG:** verify small dynamic signals on a large baseline, analogue/digital filtering, derivative polarity, sample timing and ECG synchronization. Agreement in resting heart rate does not validate stroke volume, cardiac output or valve timing.

**For ECG/PPG timing:** quantify clock drift, sample alignment, buffering and timestamp semantics. Same BLE connection or matching nominal sample rates are not proof of simultaneous acquisition. Avoid presenting PAT as PWV or cuffless BP.

**For optical oxygenation:** obtain a validated algorithm/probe combination and evidence across relevant saturation, motion and skin-pigmentation conditions. A plausible value near 98% is not meaningful calibration validation.

**For ESC:** electrode chemistry and clinical reference validation are integral. A matching conductance unit is insufficient; neither ordinary EDA nor peripheral nerve electrical conduction measures the same construct.

**For weight:** check known masses, repeatability, corner loading, temperature and mechanical creep. A 24-bit converter's theoretical count resolution is not the scale's practical accuracy.

**Safety:** body-connected current sources and multiple simultaneous instruments require qualified assessment of leakage/current limits, isolation, faults, USB/charging paths, electrode interactions and device-specific contraindications. Battery power alone does not prove safety. Follow each finished device's instructions; do not combine or modify patient-connected equipment casually. Start custom work on electrical phantoms, not people.

# 8. Subscriptions, consumables and data ownership

## Why companies choose recurring revenue

Some recurring charges pay for genuinely recurring work: cloud storage/security, app maintenance, clinical support, interpretation, regulatory upkeep and service. Others monetize a dependency created by the vendor: mandatory cloud analysis, export gating, metered tests, account-controlled accessories, or features that the owned hardware could otherwise perform locally. Both motivations can coexist. No public material examined here establishes the internal cost/profit allocation for any particular company's fee.

## Five different costs to keep separate

1. **Hardware:** device, electrodes/leads, stand, host computer, acquisition chassis.
2. **Software:** one-time vs annual; raw acquisition vs analysis add-on; local vs cloud.
3. **Consumables/meters:** adhesive electrodes, optical probes, replacement straps, smart-electrode/test credits. These can recur without being called subscriptions.
4. **Service:** calibration, battery replacement, repair, support and shipping.
5. **Exit costs:** loss of export, installer access, cloud shutdown, unsupported operating systems or inability to transfer a used-device licence.

| Route | Account/subscription position established here |
|---|---|
| Tanita professional SD/serial route | Physical local-output routes exist; exact software/export licence and fee terms still require confirmation |
| seca | Local analytics 115 raw export documented; specific newer bundles may require annual 125 licensing |
| SFB7 used/residual | No ordinary new-sale route; installer, transfer, service and warranty availability are purchase conditions |
| SUDOSCAN | Explicit pay-per-test offer and separately priced electrodes; compare the exact contract, not just purchase price |
| BIOPAC / PhysioFlow / SphygmoCor / Sciospec | Obtain a complete quote covering acquisition, analysis, raw export, offline/perpetual use, maintenance and accessories |
| Open designs | No vendor membership inherently required to read your own locally implemented acquisition, but fabrication, batteries, electrodes, toolchains, engineering time and validation are not free |
| Polar H10 SDK route | Direct raw collection is a development route; it does not imply automatic ingestion into another vendor's app |

**Your specific Withings situation:** you do not have a Withings account, so prior-account grandfathering is not a relevant escape route. The earlier no-account/subscription audit remains separate. Nothing here requires opening a Withings account. Also, independent collection does not mean WHOOP MG can ingest these raw streams or substitute them for its own proprietary derived metrics; no such automatic route was demonstrated.

# 9. Ranked recommendations by goal

## If you want to buy a finished instrument

1. **Segmental composition with local data:** request a Tanita MC-780U PLUS S sample export and total quote first; compare against a specifically quoted seca package with raw export and renewal terms.
2. **Research-grade raw impedance:** consider a properly configured Medical Research ISX-3; consider SFB7 only if a supported residual/used unit and transferable software are independently confirmed.
3. **Low-friction raw wearable ECG:** Polar H10 plus a direct collection application/SDK workflow. Not multilead diagnostic ECG.
4. **True cardiac ICG:** BIOPAC is the clearest examined raw-waveform research path; PhysioFlow is the finished hemodynamic alternative, subject to raw export and complete-price checks.
5. **Validated carotid-femoral PWV:** a PWV-equipped SphygmoCor XCEL-class instrument, not an ECG/PPG timing shortcut.
6. **Sudomotor/ESC:** professional SUDOSCAN access, with explicit lifetime/test costs. For occasional health questions, paying a qualified provider for a test may make more sense than buying a five-figure system.

## If you want an open/research build

1. **Impedance:** MAX30009 + calibrated phantom + host acquisition first. Add body connection only after qualified safety assessment; physiological interpretation is a separate phase.
2. **ECG/PPG:** published MAX86150 hardware or a MAX86176-based synchronized design; uECG for a small wearable ECG path.
3. **Integrated acquisition:** HealthyPi 5 if a complete available kit is confirmed; HealthyPi 6 if you accept preorder and verification risks. Neither provides demonstrated BIS/ICG/PWV/ESC parity.
4. **Multichannel experimental biosignals:** BioGAP for a team able to fabricate/debug research hardware.
5. **Ultrasound:** WULPUS as a substantial research project; TinyProbe only after resolving gateware availability and the full build chain.
6. **Weight:** published load-cell hardware is feasible, but keep it a weight project until dynamic/cardiovascular claims are separately validated.

**Not recommended:** a generic potentiostat as an ESC substitute; treating respiration BioZ as validated cardiac ICG; treating a public repository as licensed without checking; the unresolved-isolation cardiography prototype for human use.

# 10. Send this checklist before buying

> Please identify the exact hardware/firmware/software revision and provide:
>
> 1. A de-identified export containing actual raw R/Xc or I/Q, ECG/PPG/Z(t) as applicable—not only physiological estimates or a PDF.
> 2. Electrode paths, excitation frequencies/current modes, sampling bandwidth, and synchronization/timestamp documentation.
> 3. Calibration procedure, service interval, supported electrodes/probes, and current validation for the intended population/use.
> 4. Complete price including software, host/chassis, leads, calibration loads, electrodes and service.
> 5. All annual, cloud, per-test, consumable and licence-transfer costs.
> 6. What still works offline and after cancellation, and whether raw files/installers can be retained indefinitely.
> 7. Current stock/lead time, serial-number support and applicable regulatory/intended-use documentation.

# 11. Evidence and reproducibility of this pass

Four repositories were downloaded and inspected locally, **not built or electrically tested**:

| Repository | Pinned commit | Inspection outcome |
|---|---|---|
| pulp-bio/BioGAP | `3cfb6719ab780f094fc892f25de727bb86341fa8` | Hardware/firmware licensing and hardware directory structure inspected |
| pulp-bio/wulpus | `d052666902aea8f33dc5baef47c861b189aa9a16` | Hardware and host-software licences; CAD/firmware/software presence inspected |
| Protocentral/protocentral_max86150_ecg_ppg | `361ec56d97554b961bd26448a01e825e62b64da5` | Schematic presence and separate hardware/software/documentation licence terms inspected |
| MilosRasic98/OpenCardiographySignalMeasuringDevice | `5493a566030ed0c20bd5d2fabfd093e0d71ce67b` | GPL text, actual signal modalities, CSV workflow and explicitly documented power/protection/isolation problems inspected |

Source identifiers are saved in `hardware-search/source-manifest.json`. Selected inspected source/licence files are retained under `hardware-search/`; large mechanical, image and other assets were omitted after inspection to stay within workspace limits. These retained subsets are evidence snapshots, not complete build packages; source presence is not build reproducibility. HealthyPi 6 licence/hardware claims and TinyProbe's gateware gap were checked against their public pages, not through a complete source build. Other specifications are manufacturer documentation or cited research; their study existence is not an independent validation performed here.

**Bottom line:** commercial lab/clinical instruments can cover the individual modalities, at substantially greater cost and complexity. Open projects can expose useful underlying signals, but the strongest candidates still require engineering and validation. The difficult missing piece is not merely an app—it is a safe, reproducible, calibrated, clinically defensible integrated hardware system with durable local data access.
