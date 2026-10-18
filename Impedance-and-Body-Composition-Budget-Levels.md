# Budget levels: from passive impedance bench to a body-composition research platform

**Planning date: 17 October 2026 · USD · Starting with no hardware**

## The short answer

There are three different purchases hiding inside this project:

1. **A passive electrical bench:** establish that an instrument measures known impedances correctly.
2. **A custom device-development program:** engineer an appropriate complete system before considering human connection.
3. **A physiological validation program:** establish what the measurements predict about real people, for whom, and with what errors.

A more expensive version of (1) does not automatically accomplish (2) or (3). Even an unlimited budget cannot turn an evaluation board, a low-noise ADC or a large number of displayed metrics into validated body-composition measurements.

**My recommendation for you:** plan around a **$12,000–$25,000 owned-reference bench**, with a **$75,000–$100,000 first-phase authorization if professional engineering and independent verification are included**. Release that money against milestones. Do not begin by buying every premium instrument or by commissioning a multi-million-dollar device.

If the ambition really is a new human-connected product, use the larger engineering and validation tiers below as a roadmap—not as permission to connect the existing evaluation board to yourself.

**Companion:** [editable budget workbook](Body-Composition-Budget-Levels.xlsx). The existing [ARM build results](AD5940-ARM-Build-Results.md) and [bench specification](Impedance-Bench-Acquisition-Specification.md) remain relevant. No purchases, supplier messages, reservations, lab bookings or human studies have been made.

## How to read the numbers

- **Listed price:** a retrieved public product-page observation, not a quotation or a landed checkout total.
- **Planning allowance:** my order-of-magnitude estimate, not a supplier quote or a market average.
- Prices are nominal USD as of the planning date. Sales tax, duties and delivery are excluded unless expressly included in a particular allowance.
- Bench setup budgets include equipment, initial fixtures and the described initial external services, but **not your unpaid time or paid engineering**. I show labor separately so a cheap board does not disguise an expensive project.
- Professional-work estimates use an **editable assumption of $150–$250/hour**. This is a budgeting model, not a survey of consultant rates. A team model elsewhere uses **$180,000–$300,000 per full-time-person-year**, including overhead, as another editable assumption. Do not add both rate models for the same people.
- Timelines are rough elapsed planning windows, not delivery promises. Backorders, redesigns, laboratory scheduling and approvals can dominate.
- Bench tiers are **alternative total setups**, not five shopping lists to add together. Engineering tiers are cumulative through their milestones. Validation tiers are alternative overall programs through the stated evidence milestone. Shared equipment/studies must be credited rather than purchased twice.

# Track A — Passive bench only

**No person is connected at any tier of Track A.** ADI's AN-1557 explicitly prohibits connecting the AD5940 evaluation board to the human body. The note describes the kit's test board and simulator workflow; that is the intended starting point here. [23](https://www.analog.com/en/resources/app-notes/an-1557.html)

| Level | Initial setup allowance | Complexity / rough window | What it buys | What it does not buy |
|---|---:|---|---|---|
| **A1 — Learning and bring-up** | **$1,000–$3,000** | Low–moderate; 2–6 weeks | Evaluation kit, basic DMM/power/tools, approved passive test interface, simple loads, logging/debugging | Traceable complex-impedance accuracy; a human-safe instrument |
| **A2 — Reference access without ownership** | **$3,000–$8,000** | Moderate; 4–12 weeks | A1 plus a defined rental/shared-lab/service campaign, better fixtures and independent reference measurements | Unlimited reference access; automatic success if the rental is poorly configured |
| **A3 — Owned-reference engineering bench** | **$12,000–$25,000** | Moderate–high; 1–3 months | Suitable precision LCR reference, correct probe/fixture, calibration/standards, scope, DMM, supply, DUT and reproducible records | Physiological validity or qualified human use |
| **A4 — Premium characterization bench** | **$35,000–$100,000** | High; 2–6 months | More capable analyzer/control workflow, programmable passive fixtures, temperature experiments, better timing/debug tools and uncertainty work | Better body-fat predictions merely because the analyzer is expensive |
| **A5 — Automated metrology/verification lab** | **$100,000–$300,000+** | Very high; 4–12 months | Automated regression fixtures, environmental coverage, multiple units, independent cross-checks and repeatable verification infrastructure | Product clearance or a clinically validated model |

These are estimates, not quotes. A5 can exceed its band if custom automation or environmental facilities become substantial. Internal engineering labor remains separate; externally purchased fixture fabrication is included only to the extent of the chosen equipment allowance.

## What belongs at each level

### A1 — Learn cheaply, without pretending to certify accuracy

- One complete EVAL-AD5940BIOZ kit, **after confirming the packing list**. Do not automatically buy a second controller; the manufacturer describes the kit stack as including ADICUP3029, BIOZ and Z-Test boards. [23](https://www.analog.com/en/resources/app-notes/an-1557.html)
- A basic DMM, appropriate bench power source, ESD supplies and the exact required programming/debug route.
- Manufacturer-approved passive connection and test loads.
- Local computer and data storage; assume an existing computer, or add one explicitly.
- Raw-stream and parser verification, reset/timeout checks and initial noise observations using a reviewed diagnostic procedure.

A DC DMM is useful for resistance checks. It is not an AC phase reference. A nominal 0.01% resistor is not automatically a calibrated complex impedance standard at 50 kHz.

**Exit gate:** board revision and programming path confirmed, repeatable passive-only startup/logging demonstrated, and faults do not masquerade as measurements. No accuracy claim follows merely from this gate.

### A2 — Pay for evidence instead of owning every instrument

Use a qualified lab, properly configured rental or supervised shared facility to characterize the specific R/RC standards and your DUT. Require frequency, amplitude, fixture/reference plane, phase convention, uncertainty and environmental conditions in the deliverable.

A rental lead exists for the Hioki IM3536. Search extraction advertised **$649/month**, but the detailed page retrieved did **not** substantiate that rate. Treat it as a quote lead only; transport, insurance, calibration, probe choice and minimum term remain unknown. The advertised SMD tweezer accessory is not automatically the right fixture for this project. [25](https://www.atecorp.com/products/hioki/im3536)

**Exit gate:** an independent reference comparison with applicable uncertainty, not simply a photograph of a calibrated instrument or a DC calibration certificate.

### A3 — The best balance for your current position

Buy one appropriate reference instrument and its correct fixture, not several competing instruments immediately. A practical candidate is the **Hioki IM3536**, whose manufacturer lists 4 Hz–8 MHz operation and representative basic Z/phase accuracy. Actual accuracy depends on conditions; the headline specification is not the full uncertainty of your fixture/DUT comparison. [1](https://www.hioki.com/global/products/lcr-meters/10-mhz/id_6057) [9](https://www.hioki.com/us-en/support/faq/detail/id_227)

The detailed TEquipment page currently shows **$5,186**, separately purchased probe/fixture, and stock **expected October 21**, not confirmed stock on hand. That differs from the search snippet's “in stock/ships tomorrow” wording. Get a written quote. [6](https://www.tequipment.net/Hioki/IM3536/LCR-Meters/)

Add a sensible scope, DMM and supply, characterized standards, approved fixture/interface, and a complete uncertainty/calibration record. More scope bandwidth is not a substitute for an AC impedance reference.

**Exit gate:** guard-banded agreement over the specified passive test matrix, raw/math replay consistency, verified timing/fault behavior, and measured stack/heap/transport margins. The exact tolerances must be declared before interpreting results.

### A4 — Buy capability that answers an actual question

Possible reference choices include:

- **Zurich Instruments MFIA:** manufacturer page displays **$14,490**, region-specific/ex-works, with 500 kHz and 5 MHz variants. The base description is 500 kHz, extended to 5 MHz when upgraded; do not budget the displayed price as an all-options 5 MHz quotation. It includes LabOne, APIs and the MFITF fixture, according to the manufacturer. The MFITF's inclusion still does not prove it suits your custom passive fixture without adaptation/characterization. [1](https://www.zhinst.com/en/products/mfia-impedance-analyzer/)
- **Keysight E4980BL:** the detailed US page displays **$7,391 / $10,839 / $14,264** for its 300 kHz / 500 kHz / 1 MHz configurations. Confirm the exact interface/options/fixture configuration: the page combines generic connectivity features with configuration-specific option lines. These are list observations, not a quotation. [Keysight detailed US listing](https://www.keysight.com/us/en/product/E4980BL/precision-lcr-meter-20-hz-1-mhz.html)

**Procurement correction:** E4980AL is now listed by Keysight as discontinued/currently supported, with E4980BL as replacement. It can remain a calibrated used/rental option, but should not be treated as the default new-current model. E4980A is also shown as transitioning to E4980B. This updates earlier references to those legacy reference instruments. [1](https://www.keysight.com/us/en/product/E4980AL/precision-lcr-meter-20-hz-300-khz-500-khz-1-mhz.html) [4](https://www.keysight.com/us/en/product/E4980A/precision-lcr-meter-20-hz-2-mhz.html)

Choose based on low-current accuracy, fixture compensation, phase behavior, API/export access and workflow—not maximum MHz alone. The current hardened application remains **nominal 50 kHz only**; an 8 MHz reference instrument does not qualify an 8 MHz AFE or enable sweeps in our firmware.

### A5 — Automation, not expensive ornamentation

This tier becomes worthwhile when you need many devices, conditions and regression runs. It may add automated passive load selection, environmental logging/chambers, long-duration acquisitions, calibrated stimulus/timing checks, unit-to-unit characterization and independently characterized references. Independent references are useful when they address common-mode errors, not just because two instruments are on the bench.

Outsource specialist EMC/electrical-safety work unless utilization and staffing justify bringing it in-house. Buying a safety analyzer does not make its operator an accredited lab.

## Recurring costs and professional time

| Level | Annual cash upkeep/access allowance after the initial year | Estimated professional work, if hired | Labor allowance at $150–$250/h |
|---|---:|---:|---:|
| A1 | $200–$800 | 40–120 h | $6,000–$30,000 |
| A2 | $1,000–$4,000 | 80–200 h | $12,000–$50,000 |
| A3 | $1,500–$4,500 | 150–400 h | $22,500–$100,000 |
| A4 | $3,000–$10,000 | 400–1,000 h | $60,000–$250,000 |
| A5 | $8,000–$30,000+ | 1,500–4,000 h | $225,000–$1,000,000+ |

All allowances above are models. Calibration intervals should follow the quality plan, risk, stability and usage—not an invented universal annual rule. Unpaid DIY hours are not economically free. These hours are for the indicated bench effort, not future clinical/device development.

### An illustrative A3 cart

| Item | Allowance |
|---|---:|
| Primary kit plus optional spare allowance | $1,100 |
| Hioki IM3536 base instrument — listed anchor, quote needed | $5,186 |
| Correct probe/interface/fixture allowance | $1,000 |
| Initial standards and applicable AC calibration | $2,000 |
| DMM | $750 |
| Oscilloscope | $1,800 |
| Bench supply | $500 |
| Additional passive fixture work | $1,500 |
| ESD, cables and local logging/storage | $500 |
| **Subtotal** | **$14,336** |
| 20% hardware uncertainty reserve | $2,867.20 |
| **Illustrative equipment/setup allocation** | **$17,203.20** |

Only the LCR line is a current listed price here. The rest are allowances, not chosen SKUs or guaranteed contents. Do not buy an optional spare until compatibility and support are established. New computer, sales tax, freight and professional labor are not silently included.

The kit's detailed Mouser page shows **$497.15**, 14 immediately shippable units, a possible 8% US tariff and a warning that Mouser will stop carrying it after stock is depleted. The cheaper search snippet is not the detailed-page observation. That is a distributor warning, not proof of manufacturer discontinuation. [1](https://www.mouser.com/ProductDetail/Analog-Devices/EVAL-AD5940BIOZ?qs=w%2Fv1CP2dgqozY%2F%2FPHNLAZQ%3D%3D)

The approved measurement connector/fixture matters: do not use a generic USB-looking cable as a custom electrode/phantom adapter. The existing procurement review documents the manufacturer's connector restrictions and the need to confirm a complete Z-Test interface.

### A professionally run first phase: approximately $80,000, not an unlimited purchase order

Example arithmetic, all estimated except the embedded LCR price anchor:

- Equipment/initial-fixture subtotal: **$14,336**.
- Engineering review, target bring-up, diagnostic development and passive characterization: **200 h × $200/h = $40,000**.
- Independent DUT/fixture verification campaign: **$8,000**, distinct from the initial standards/instrument calibration line.
- Subtotal: **$62,336**.
- 25% program reserve: **$15,584**.
- **Illustrative total: $77,920** before tax/freight or additional scope.

This example uses the equipment subtotal **without** its separate 20% reserve, then applies one program reserve. It does not double-count both reserves. A **$75,000–$100,000 stage cap**, subject to actual quotations, is reasonable for planning—not a promise that every unknown will fit.

# Track B — Custom device engineering

**Do not modify the evaluation kit into a human instrument by adding a battery or a USB isolator.** Human connection is a separate complete-system design and review problem. The manufacturer's evaluation-board prohibition still applies. [23](https://www.analog.com/en/resources/app-notes/an-1557.html)

These are **cumulative engineering/compliance program estimates** through each milestone. They include an approximately $20,000 baseline bench allowance and appropriate development labor, but exclude the large physiological data-collection programs in Track C, mass-production inventory and long-term commercial operations. Credit already-owned equipment/work; do not add every row or add the entire A3 budget again.

| Level | Cumulative engineering allowance | Planning window | Deliverable / complexity |
|---|---:|---|---|
| **B1 — Custom passive-only instrument** | **$100,000–$300,000** | 3–6 months | Custom AFE/MCU board, power/clock architecture, protected inputs, local raw export, PCB iterations, passive calibration/verification; no human connection |
| **B2 — Research instrument eligible for safety/ethics review** | **$300,000–$1 million** | 6–12 months | Complete patient-connected architecture, independent limits/fault analysis, enclosure/electrodes, verification, external specialist testing and study-ready documentation; human work only after required approvals |
| **B3 — Segmental multifrequency research platform** | **$750,000–$2.5 million** | 12–24 months | Characterized switching/channel paths, load cells/geometry, contact QC, timing, drift/settling control, repeatable clinical/research workflow and local data tools |
| **B4 — Productized body-composition platform** | **$2–$8 million+** | 18–36+ months | Manufacturing design/test, supplier control, quality system, software lifecycle, usability/cybersecurity, regulatory work for selected claims, service/update strategy; validation studies still separately budgeted |

These are not construction instructions or an offer to certify a device. A lab report is one input; it is not automatic ethics approval, regulatory authorization or clearance for sale. A simpler wellness product may cost less; a novel diagnostic claim can cost much more.

## Where the engineering money goes

- **Analog/metrology:** stable excitation and independent fault limits; current/voltage acquisition; phase/gain/crosstalk; calibration transfer; electrode/contact and common-mode behavior; noise and drift.
- **Complete-system electrical safety:** intended applied parts, insulation/charging/interface states, normal/single-fault conditions, power-on behavior and independent mitigations. Wireless or battery operation alone is not a safety case.
- **Mechanical/electrode system:** contact geometry, repeatable positioning/pressure, skin-contact materials, cleaning, durability, usability and manufacturing variation.
- **Embedded/software:** meaningful acquisition timestamps, transport-loss handling, diagnostics, testability, versioned configuration/calibration, immutable raw archives, safe firmware updates and cybersecurity as applicable.
- **Scale subsystem:** calibrated load cells, corner loads, creep, temperature and geometry—not simply a “24-bit” ADC label.
- **Quality/regulatory:** qualified specialists determine applicable standards, intended use, product classification, submission strategy, human-research obligations and required evidence.

Potentially relevant standard families include IEC/ANSI-AAMI 60601-1 and 60601-1-2 for electrical safety/EMC, ISO 14971 risk management, IEC 62304 software, IEC 62366-1 usability, ISO 10993 biological evaluation and ISO 13485 quality management. Home use, radio and particular claimed functions can introduce additional requirements. Applicability and current recognized editions must be determined for the actual design/jurisdiction; this is not a statement that every wellness scale must obtain every certificate. FDA maintains recognized consensus-standard information for electrical safety/EMC. [6](https://www.fda.gov/media/142385/download) [2](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/detail.cfm?standard__identification_no=46761)

**Current US context:** FDA's general-wellness guidance was updated January 6, 2026; it is a low-risk/intended-use framework, not permission to make unvalidated disease claims. FDA's QMSR became effective February 2, 2026 and incorporates ISO 13485:2016 by reference. Specific obligations depend on the product and exemptions. Calling a product “research” or “wellness” is not a universal exemption. [1](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-wellness-policy-low-risk-devices) [10](https://www.fda.gov/medical-devices/postmarket-requirements-devices/quality-management-system-regulation-qmsr)

## Staffing matters more than the board price

As an illustration, **4 full-time people × 1 year × $240,000 loaded/person-year = $960,000**, before substantial study costs or manufacturing inventory. That assumption, not the price of a $6–$15 AFE, explains the order of magnitude.

The team may need analog/embedded engineering, metrology, mechanical/electrode design, quality/safety/regulatory input, biostatistics/data engineering and clinical collaborators. Not every role needs to be full-time initially. Outsource specialist work early rather than hiring an entire certification lab.

# Track C — Physiological/body-composition validation

**The core distinction:** accurate R/X measurements do not uniquely measure fat, muscle, fluid compartments, visceral fat or bone mineral density. Those outputs need explicitly defined models and appropriate reference measurements. More frequencies can add information, but not eliminate population, hydration, geometry or identifiability problems.

These are **alternative overall validation-program estimates through the stated milestone**, including appropriate pilot/preparation costs. They exclude Track B device development and purchase of an MRI/DXA facility. The participant counts are illustrative planning scenarios, **not powered sample-size recommendations**.

| Level | Validation-program allowance | Illustrative scope | What conclusions become plausible |
|---|---:|---|---|
| **C1 — Repeatability / feasibility pilot** | **$50,000–$200,000** | Roughly 20–50 participants with repeated visits and selected comparators, after required approvals | Workflow, repeatability, failure rates and preliminary associations; not broad accuracy claims |
| **C2 — Focused body-composition study** | **$500,000–$2 million** | Roughly 300–600 participants, repeated measurements, DXA/reference work, participant-level development/holdout separation | Defined-population performance with honest errors/limits and a locked model; not universal generalization |
| **C3 — Multi-site / broader-claims validation** | **$2–$8 million+** | Roughly 1,000–3,000 participants, diverse sites/groups, independent validation, selected MRI/4-compartment/fluid references and longitudinal work | Stronger subgroup/generalization/change evidence for the outcomes actually studied; not automatic superiority to every commercial device |

Planning windows after appropriate preparation are roughly 3–6 months for C1, 9–18 months for C2, and 18–36+ months for C3; actual protocols and recruitment can extend these substantially. Track C can use suitable finished instruments rather than obligating you to develop custom hardware.

A clinically meaningful change-detection study can require a different design from a cross-sectional body-fat prediction study. Bone-density, edema/disease-management, cardiac-output, rhythm diagnosis and neuropathy claims require their own appropriate reference methods and study designs.

## What must be measured and analyzed

- Freeze intended use, outcomes and acceptable error **before** fitting models.
- Use traceable electrical measurements plus appropriate physiological references. DXA is useful but is not a perfect universal gold standard; water-compartment or visceral-fat claims may need other methods or a justified nested subset.
- Include positioning, repeated electrode placement, operator/day/device effects, temperature and routine hydration variation. Do not invent risky interventions merely to generate “extreme” data.
- Separate training, tuning and independent validation **by participant**, not randomly by visit. Use site/time separation where relevant; avoid reusing test data after model selection.
- Compare with a credible age/height/weight-only baseline as well as existing devices. Added impedance channels should demonstrate incremental value, not merely recreate information already in demographics.
- Report bias, limits of agreement, MAE/RMSE, calibration, repeatability, subgroup failures, missingness and change sensitivity—not just correlation or an attractive R².
- Prespecify handling of contact failure, clipping/compliance flags, invalid spectra and excluded records. Unknown diagnostics must not silently become “normal.”
- Obtain consent, data governance and applicable institutional/regulatory approvals. De-identification and publication rights must be designed into agreements; raw human data cannot simply be dumped into an open repository.

The earlier NHANES analyses are useful model-development evidence, not validation of the unbuilt custom hardware. A generic model also must not be trained to reproduce another commercial scale's proprietary estimates and then described as independently measuring physiology.

## Why study cost escalates: one arithmetic example

A hypothetical study with **300 participants × 2 visits × $800 fully burdened per visit = $480,000**. Add a modeled **$200,000** for protocol, recruitment, sites, data management and analysis, then **25% reserve**: **$850,000**.

The $800 is an assumption, not an actual Boston provider quote. Define whether it includes operator time, participant payments, scan/reference cost, scheduling and data processing, and do not charge those twice. MRI/4-compartment work, difficult recruitment or more visits can push the total far higher. A biostatistician must calculate the actual sample size from endpoints, error margins, subgroup requirements and expected missingness.

Partner with qualified facilities first. Buying an MRI or DXA scanner is a separate facility/operations decision, not the next accessory for an impedance bench.

## Combined envelopes, without double-counting

| Alternative program | Engineering + validation | Modeled envelope |
|---|---|---:|
| Reviewed custom instrument plus feasibility evidence | B2 + C1 | **$350,000–$1.2 million** |
| Segmental research platform plus focused composition study | B3 + C2 | **$1.25–$4.5 million** |
| Productized composition platform plus broader validation | B4 + C3 | **$4–$16 million+** |

These totals already include the baseline bench allowance inside B. They are scenario arithmetic, not quotations or guarantees that the cheapest assumptions can all be achieved simultaneously. They do not include unlimited operating runway, manufacturing inventory or unrelated clinical claims. Do not sum these three alternative rows.

# Broader platform: every major sensor/claim family kept separate

If by “all of it” you mean the breadth discussed earlier, budget for **multiple interacting development and validation projects**, not one larger BIA circuit.

| Capability | Physical signal/system needed | Main added complexity | Important non-equivalence |
|---|---|---|---|
| Weight, balance, posture context | Calibrated load cells; geometry/position information | Mechanical metrology, corner-load effects, reproducible stance | Display resolution ≠ weight accuracy |
| Whole-body and regional BIA/BIS | Known excitation, complex I/V measurements, reviewed electrode switching/contact paths | Path-specific calibration, settling, crosstalk, contact QC and physiological models | Eight contacts ≠ independently validated regional composition |
| ECG | Defined lead vectors, calibrated voltage waveform, appropriate timing/bandwidth | Patient protection, motion/artifact handling, rhythm/diagnostic evidence if claimed | Heart-rate output ≠ multilead ECG or diagnosis |
| Cardiac impedance/ICG | Small pulsatile thoracic impedance with synchronized timing, often ECG | Dynamic bandwidth, motion suppression and reference validation | Slow 50 kHz composition readings or respiration BioZ ≠ validated cardiac output |
| PWV / vascular measurements | Method-specific synchronized wave timing and path-length information | Sensor synchronization, path definition and comparator protocol | ECG-to-finger timing includes pre-ejection time; not automatically PWV |
| ESC / sudomotor | Defined electrochemical excitation/electrodes and response protocol | Independent patient safety, electrode chemistry, norms, IP and clinical validation | Ordinary EDA/GSR ≠ validated ESC or neuropathy assessment |
| EDA / skin conductance | Skin-current/voltage response under a defined method | Contact/site/context and motion effects | A stress/skin-conductance signal is not a nerve-conduction measurement |
| PPG / SpO₂ | Appropriate optical wavelengths, detector/front end and a validated algorithm | Optical mechanics, skin/perfusion effects; specialist validation for medical SpO₂ claims | A PPG breakout or green-only pulse signal ≠ validated oxygen saturation |
| Respiration | Defined thoracic impedance, strain or other respiratory signal | Timing, position, motion and comparator data | Respiration BioZ ≠ ICG cardiac-output validation |
| Temperature / IMU / contact context | Defined-site temperature, inertial and contact sensors | Site calibration, drift, fusion and artifact logic | Skin temperature ≠ core temperature; context sensors do not validate fat estimates |
| Fat, lean tissue, water compartments, visceral-fat estimates | Models tied to the measured signal and specific references | Cohort design, uncertainty, external validation and change detection | More displayed “biomarkers” ≠ more independent sensors |
| Bone mineral density / DXA-type imaging outcomes | Appropriate clinical imaging/reference workflow | Separate physical modality, clinical workflow and validation | BIA “bone mass,” a proxy or regression is not DXA BMD/T-score measurement |

Do not assume every listed capability exists in every target commercial product. This table preserves the scope of the earlier investigation and distinguishes possible complementary instruments from direct replacements.

**Full-platform planning envelope:** approximately **$10–$30 million+ over 3–5+ years** for a serious integrated multi-modality engineering/data/validation effort with selected claims. That is an order-of-magnitude program scenario, not a price for “a scale” or a guarantee of clearance, diagnostic performance or a DEXA replacement. Novel clinical outcomes can exceed it. This is a broader alternative overall program envelope, not a surcharge to add mechanically to the preceding totals. Shared electronics and participants reduce some costs; integration, interference and multiple claims add others. Do not obtain the total by multiplying inexpensive sensor-module prices.

# Buying finished products is a fourth decision, not a failure

If the near-term objective is simply to get human body-composition data rather than invent a device, a suitable finished commercial system can be dramatically cheaper and more mature than Track B.

- **Tanita MC-780U PLUS S:** current manufacturer page shows **$6,999.99**, segmental body-composition outputs, R/reactance/phase data labels and SD/USB/RS-232 outputs. Those labels do not prove that every raw segment/frequency field is available in the purchased export. Request a real sample file and exact license/support terms. The vendor's “comparable to DEXA” wording is marketing, not an equivalence result adopted here. [1](https://tanita.com/products/mc-780u-plus-s-multi-frequency-segmental-body-composition-analyzer)
- **seca/InBody and other professional systems:** obtain configuration-specific quotes, raw-export demonstrations, permitted research use, consumables and recurring-fee terms. The earlier market report documents why a connector or a generic CSV promise is insufficient.
- **Consumer connected scales:** convenient finished workflows, but the closed model/export/subscription arrangement may not meet the open raw-data objective.
- **Used/discontinued research instruments:** only after serial-number support, software-license transfer, raw export, calibration/service and cable availability are verified. A cheap unsupported instrument can become the expensive route.

A finished device is still used only within its manufacturer labeling and limitations. Raw-data connectors do not authorize attaching extra electrical instruments to a person or modifying its patient-connected circuit.

# Subscription and ownership costs: what to demand at every level

Your preference should be encoded into the purchasing contract and acceptance test, not assumed from the price tag.

**Required questions:**

1. Does acquisition and local viewing work indefinitely without an active cloud account?
2. Are per-frequency/per-path raw measurements, quality flags and configuration/calibration exported, or only proprietary derived scores?
3. Are local storage, bulk export, APIs, installer access and firmware updates available after support expires?
4. Are software options perpetual, annual, per-seat, per-device or per-test? Is a used-unit license transferable?
5. Are optional warranties, maintenance/calibration and financial leases being confused with compulsory measurement access?
6. What survives cancellation or vendor shutdown? Who owns the raw data, model weights and trained custom algorithms?
7. Can the actual workflow be demonstrated on your intended OS/network with the quoted configuration?

Companies may prefer subscriptions for recurring revenue, support/cloud costs, ongoing analytics/clinical services, retention and switching costs. Those are business reasons, not a physical requirement for local impedance computation. Conversely, calibration, electrodes, qualified staff and postmarket obligations can be genuine recurring costs even in a completely offline product.

The MFIA manufacturer advertises included LabOne/APIs; Keysight's page separately promotes support and financial subscription offerings. Neither observation is a blanket, perpetual “all features free” license guarantee. Confirm the exact contract. [1](https://www.zhinst.com/en/products/mfia-impedance-analyzer/) [Keysight detailed US listing](https://www.keysight.com/us/en/product/E4980BL/precision-lcr-meter-20-hz-1-mhz.html)

You do **not** have a Withings account. No plan here relies on grandfathered free automatic sync or legacy account entitlements.

For a custom platform, insist on local raw archives, documented schemas, explicit firmware/calibration/model versions, reproducible offline inference and export rights. Open code is not the same as unrestricted upstream licensing: the retained ADI firmware has ADI-targeted restrictions and cannot simply be relabeled MIT/BSD. Human data sharing also remains subject to consent/privacy agreements.

# My recommended staged allocation

## Now: authorize scope, not a shopping spree

**Preferred path: A3 plus professional assistance, with a first-phase cap around $75,000–$100,000.** If you want to do the engineering yourself, begin with the approximately $17,000 equipment allocation and separately quoted independent reference work; recognize the time/skill tradeoff.

Release funds in this order:

1. **Scope/quote gate:** define target load/frequency/amplitude ranges, claim boundaries, required raw data and acceptance criteria; verify exact kit/fixture/debug contents and supplier support. Confirm the reference model's applicable uncertainty, fixture and offline interface.
2. **Target/diagnostic gate:** independent review of our experimental source, reset/clock/UART behavior and memory map; implement a reviewed noise-characterization procedure rather than inserting a guessed current threshold. Existing ARM link success is a useful start, not a completed hardware test.
3. **Passive measurement gate:** run the prescribed known-load/reference tests, quantify uncertainty, fault behavior, drift and transport/timing. Keep the evaluation setup passive-only.
4. **Go/no-go:** if the bench evidence is weak, fix that before buying premium gear or collecting human data. If good, choose between buying a finished human-use device, commissioning B1 custom electronics, or funding a broader program.
5. **Only later:** a complete custom design and appropriate specialist/ethics/regulatory review before any proposed human-connected work.

**What I would not buy now:** three reference analyzers, a used instrument without support/software proof, a DXA/MRI facility, a pile of physiology sensor breakouts, or a custom human electrode rig for the evaluation kit.

With effectively unlimited funds, the best first upgrade is **a qualified analog/metrology engineer and independent reference evidence**, not the most expensive catalog item.

## Price-evidence audit trail

The current observations and retrieval caveats are saved in [JSON](budget-levels/price-observations.json) and [CSV](budget-levels/price-observations.csv). The workbook builder and its arithmetic checks are included under `budget-levels/`; no prices are silently refreshed by the spreadsheet.
