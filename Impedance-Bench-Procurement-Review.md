# Passive impedance bench: kit availability, costs and supplier checks

**Research date: 17 October 2026 · US-facing listings, Boston-area service options**

## Bottom line

**Do not order the MAX30009 kit based on the earlier technical preference alone.** Its distributor listings now present substantial availability restrictions. Keep it as a conditional technical choice, but make the **EVAL-AD5940BIOZ bundle the first practical quote request for a passive 50 kHz–200 kHz bench evaluation**. This is a procurement recommendation, not a claim of superior accuracy or an instruction to buy.

The strongest displayed kit prices in this review are **$487.21 at Newark** and **$497.15 at Mouser**, with important caveats below. These are web observations, **not confirmed quotations, reservations, or checkout totals**. Neither vendor nor the manufacturer has been contacted. [1](https://www.newark.com/analog-devices/eval-ad5940bioz/eval-board-electrochemical-front/dp/50AK1328) [2](https://www.mouser.com/ProductDetail/Analog-Devices/EVAL-AD5940BIOZ?qs=w%2Fv1CP2dgqozY%2F%2FPHNLAZQ%3D%3D)

**No purchase, account creation, supplier message, hardware download/install, wiring or measurement occurred.** Everything remains passive-bench-only. Manufacturer AN-1557 explicitly says never to connect the AD5940 evaluation board to a human body; nothing in this review relaxes that restriction. [AN-1557](https://www.analog.com/en/resources/app-notes/an-1557.html)

Companion deliverables: [observations CSV](impedance-procurement/vendor-observations.csv), [supplier questions](impedance-procurement/Supplier-Questions.md), and [evidence notes](impedance-procurement/evidence-notes.json). The [preceding bench specification](Impedance-Bench-Acquisition-Specification.md) remains the measurement/test plan; this review updates its procurement assumptions.

## 1. What the ordering pages actually showed

### MAX30009EVKIT# — do not treat as readily available

| Source | Observation | Procurement interpretation |
|---|---|---|
| Mouser, US-facing detailed page | “Restricted Availability”; not currently available; region restriction; product comment says Mouser will no longer carry the item | **Not an actionable normal-stock purchase route.** No current usable price established |
| DigiKey, US search extraction | “Discontinued at Digi-Key” alongside “Available To Order” and “Factory Stock: 75” | Internally conflicting listing; **availability unconfirmed**. Detailed page fetch failed |
| Newark, search extraction | Historical-looking $237.71 display alongside pricing-unavailable/no-longer-stocked/no-longer-manufactured text | **Not a current buyable quote**; distributor language is not sufficient proof of manufacturer discontinuation |
| Manufacturer kit page | Still describes two-board kit, links Rev 2 kit guide, design files and GUI 1.0.2 | Documentation exists; this does **not** prove orderability, current support life or shipped revision |

Sources: [3](https://eu.mouser.com/ProductDetail/Analog-Devices-Maxim-Integrated/MAX30009EVKIT?qs=doiCPypUmgHaoxp50UdVug%3D%3D), plus the directly retrieved [US-facing Mouser page](https://www.mouser.com/ProductDetail/Analog-Devices-Maxim-Integrated/MAX30009EVKIT?qs=doiCPypUmgHaoxp50UdVug%3D%3D); [1](https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX30009EVKIT/16889691); [8](https://www.newark.com/analog-devices/max30009evkit/evaluation-kit-bioimpedance-measurement/dp/62AK1776); [9](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/max30009evkit.html).

**Decision:** request a written direct-manufacturer availability/support answer or an approved successor. Do not substitute an unknown-marketplace kit or bare chip merely to keep the project moving. Distributor-specific retirement does not establish that MAX30009 silicon is discontinued.

### EVAL-AD5940BIOZ — more actionable, but with lifecycle warnings

| Supplier | Observed unit price, USD | Observed availability | Evidence quality and caveat |
|---|---:|---|---|
| Newark, part 50AK1328 | **$487.21** | 48 in stock; 33 incoming; 4–6 business days from UK stock; standard manufacturer lead time 25 weeks | Detailed page retrieved. Also contains a network/403 error banner. Says displayed price includes applicable duties/tariffs. Confirm final price, stock and delivery in a written quote |
| Mouser, part 584-EVAL-AD5940BIOZ | **$497.15** | 14 can ship immediately | Detailed US-facing page retrieved. Says it will no longer be available from Mouser when stock is depleted; warns an **8% tariff may apply** to US shipments |
| DigiKey, part 505-EVAL-AD5940BIOZ-ND | **$499.46** | Search extraction says 54 in stock | **Search-only backup lead**: detailed page fetch failed, and associated-product snippets showed other prices. Not independently confirmed |

Sources: [1](https://www.newark.com/analog-devices/eval-ad5940bioz/eval-board-electrochemical-front/dp/50AK1328), [2](https://www.mouser.com/ProductDetail/Analog-Devices/EVAL-AD5940BIOZ?qs=w%2Fv1CP2dgqozY%2F%2FPHNLAZQ%3D%3D), [5](https://www.digikey.com/en/products/detail/analog-devices-inc/EVAL-AD5940BIOZ/10124784).

**Why these differ from search results:** earlier search snippets returned $453.25 at Mouser and roughly $419.57–$430.29 at Newark; the subsequently retrieved detailed pages displayed the higher figures above. Use the detailed-page observations for planning, not the cheapest snippet. Even those pages can be cached, region-dependent or change before checkout. [1](https://www.newark.com/analog-devices/eval-ad5940bioz/eval-board-electrochemical-front/dp/50AK1328) [2](https://www.mouser.com/ProductDetail/Analog-Devices/EVAL-AD5940BIOZ?qs=w%2Fv1CP2dgqozY%2F%2FPHNLAZQ%3D%3D) [3](https://www.newark.com/analog-devices/eval-ad5940bioz/evaluation-board-front-end-16/dp/50AK1328)

Mouser's lifecycle statement applies to its distribution of the kit. It does not, by itself, establish manufacturer end-of-life. Nevertheless, it is a real maintainability concern: get a replacement/support path before committing software development to this exact kit.

## 2. Bundle contents: avoid buying the controller twice

The manufacturer's EVAL-AD5940BIOZ landing page says the evaluation kit **includes EVAL-ADICUP3029**, the BIOZ board with AD5940 and AD8233, and custom micro-USB/ECG snap connectors. Newark's overview repeats the bundled-controller description. Thus **do not automatically add a separate ADICUP3029 to the budget**. The short “kit contents” product attribute is less detailed than the overview; ask the seller for the packing list. [4](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/eval-ad5940bioz.html) [1](https://www.newark.com/analog-devices/eval-ad5940bioz/eval-board-electrochemical-front/dp/50AK1328)

The manufacturer BIA example requires the controller, BIOZ shield and **Z-Test board**, and says the impedance-test board is provided with the hardware. However, the short landing-page packing list does not explicitly enumerate the Z-Test board. **Get explicit confirmation that it is included in the actual order**, rather than assuming a generic listing guarantees it. [BIA example](https://wiki.analog.com/resources/eval/user-guides/eval-ad5940/software_examples/ad5940_bia)

For MAX30009, the manufacturer describes MAXSENSORBLE_EVKIT_B plus MAX30009_EVKIT_B, battery/BLE and a MAXDAP-TYPE-C programmer. The kit guide is Rev 2; that is a **document revision**, not proof of the boards physically shipped. [9](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/max30009evkit.html) [13](https://www.analog.com/media/en/technical-documentation/data-sheets/max30009evkit-evk-rev2.pdf)

## 3. Revision, frequency and connector checks

### Frequency conflict remains unresolved—not a filename problem

I checked the manufacturer-linked **uppercase `MAX30009.pdf`** as well as the previously consulted lowercase URL. The retrieved uppercase first-page text also says **500 kHz**, including its BIA/BIS feature list. This means simply switching filename capitalization did **not** substantiate 806 kHz support. The earlier bench specification records the product-page discrepancy; ask ADI for the applicable frequency/clock/register combinations and silicon revision. Do not represent 806 kHz, 1 MHz or Hydra-equivalent coverage as verified. [Uppercase datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX30009.pdf)

Keep the proposed initial scope at **near-50 kHz complex impedance**, followed by a characterized 5–200 kHz profile. Near-50 kHz settings, actual frequencies and calibration support still require confirmation for the delivered hardware.

### AD5940 documentation is accessible, but not completely consistent

The correct main guide is [`.../user-guides/ad5940`](https://wiki.analog.com/resources/eval/user-guides/ad5940). The guessed `.../user-guides/eval-ad5940` root returns a page-not-found message, though its deeper pages exist. The BIOZ shield guide lists four-wire BIA with Z-board and two-wire BIOZ, and links Rev B design files. This is evidence of documented configurations/design resources, **not verification that a supplier will ship Rev B**. [Shield guide](https://wiki.analog.com/resources/eval/user-guides/eval-ad5940/hardware/eval-ad5940bioz)

**Connector warning:** the shield's P6 micro-USB-shaped measurement connector is not a normal interchangeable USB port. Its guide says it must only be used with the supplied Z-Test board or provided ECG cables; no other cable should be connected. Do not buy a generic USB adapter to attach the custom phantom. Request a manufacturer-approved fixture interface or written instructions for passive-load characterization. [Shield guide](https://wiki.analog.com/resources/eval/user-guides/eval-ad5940/hardware/eval-ad5940bioz)

There is also conflicting human-use wording across the BIA example, shield guide and AN-1557. The plan adopts the **stronger simulator/bench-only restriction**: no human connection, regardless of battery power or PC disconnection. A permissive sentence in one guide is not complete-system safety clearance. [BIA example](https://wiki.analog.com/resources/eval/user-guides/eval-ad5940/software_examples/ad5940_bia) [Shield guide](https://wiki.analog.com/resources/eval/user-guides/eval-ad5940/hardware/eval-ad5940bioz) [AN-1557](https://www.analog.com/en/resources/app-notes/an-1557.html)

## 4. Export support: what is documented versus proven

| Platform | Documented evidence | Still required before acceptance |
|---|---|---|
| MAX30009 | Kit guide documents raw flash logging, binary-to-CSV conversion, I/Q fields, register preamble, status fields and missed-packet footer; landing page links software 1.0.2 | Actual sample logs from the supplied software; units/count scaling; calibration coefficients and configuration export; supported OS; installer/license/offline behavior |
| AD5940 | Manufacturer links SensorPal installer; wiki documents firmware loading and GUI workflow; BIA example provides a serial-output development route | Actual raw voltage/current DFT or I/Q access, file/protocol schema, calibration/configuration export, data-loss handling, sign/units and exact firmware branch/version |

Sources: [13](https://www.analog.com/media/en/technical-documentation/data-sheets/max30009evkit-evk-rev2.pdf), [9](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/max30009evkit.html), [4](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/eval-ad5940bioz.html), [SensorPal guide](https://wiki.analog.com/resources/eval/user-guides/eval-ad5940/tools/sensorpal_setup_guide), [BIA example](https://wiki.analog.com/resources/eval/user-guides/eval-ad5940/software_examples/ad5940_bia).

**Neither export path was executed.** The presence of a GUI, source link or plotted impedance is not proof that the available output meets the full acquisition contract. No software license, activation requirement or current Windows compatibility was certified. The included offline checker from the previous phase does not parse either vendor format directly.

## 5. Independent reference-measurement options

### First inquiry: Transcat reference electrical calibration service

Transcat advertises impedance capability covering **1 Ω–100 kΩ, 10 Hz–1 MHz, best uncertainty 0.06%**, traceable through an E4980A calibrated by the Keysight standards laboratory. This is the best explicit range match found here for the proposed 100–1,000 Ω-class, 5–200 kHz fixtures. **“Best uncertainty” is not a guarantee at our loads, phase angles, signal levels or fixture geometry.** [3](https://www.transcat.com/reference-electrical-calibration-labs)

Its Boston-area page identifies a Wilmington location and electrical calibration services. Ask whether the custom-fixture work can be accepted locally or must be routed to a reference lab. Do not assume that the local lab's full accreditation scope includes the requested complex-impedance characterization. [1](https://www.transcat.com/calibration-lab-boston)

**Critical unresolved issue:** the proposed bench plan asks for reference expanded phase uncertainty **≤0.05°** and sufficiently small R/X uncertainty. A magnitude best-uncertainty statement does not demonstrate this. In fact, the X-uncertainty requirement can be stricter: at a nominally resistive **1,000 Ω**, the required reference expanded X uncertainty is **≤0.25 Ω**, corresponding to approximately **0.0143°** if phase dominates. A 0.05° phase uncertainty alone would contribute about **0.873 Ω** to X uncertainty there. Obtain a load-/frequency-specific uncertainty statement, covariance information and scope confirmation before selecting the service. These are derived planning calculations, not measured performance. The [36-cell reference request table](impedance-procurement/reference-request-grid.csv) supplies nominal-load uncertainty ceilings; final ceilings must use the actual measured values.

### Second inquiry: IET Labs / GenRad metrology services

IET advertises calibration/repair of LCR meters, impedance bridges and electrical standards, with accredited capabilities subject to its published scope. This is a credible **technical inquiry lead**, but this review did not establish a price, location-specific service, or an offer to characterize our custom RC networks at 50–200 kHz and the required phase uncertainty. [1](https://www.ietlabs.com/directory-of-services/calibration-and-repair)

A service that calibrates an LCR meter is not automatically a service that will accept an assembled custom fixture. Specify the actual artifact and deliverables.

### Rental alternative: E4980A-class precision LCR meter

Transcat advertises E4980A rental with weekly/monthly terms; Electro Rent also lists rental availability. The listed 20 Hz–2 MHz range covers the proposed frequency profile. **US rental rates were not established; request a quote.** [1](https://www.transcat.com/keysight-technologies-e4980a-for-rent) [6](https://www.electrorent.com/us/products/lcr--impedance-analyzers/lcr-meters/keysight-technologies/e4980a/01t1O000004TnjeQAC)

Ask for calibration with uncertainty, correct four-terminal-pair fixture/cabling, actual load/phase accuracy, signal-level capability, export support, insurance, shipping, minimum term and damage charges. A basic 0.05% accuracy headline does not establish expanded phase uncertainty for the complete setup. Reference-plane/fixture compensation and competent operation remain necessary. [17](https://www.keysight.com/us/en/assets/7018-01349/brochures/5989-4235.pdf)

**Recommendation:** seek outsourced fixture-characterization and rental quotes in parallel. Prefer characterization for a one-time feasibility run if it meets the requirements at lower total cost; prefer rental/access if repeated fixture changes and drift testing dominate. No provider has accepted this work yet.

## 6. Costs: known observations, unknown costs and an explicit planning example

### Kit-only arithmetic

- **Newark observation:** $487.21, with the page saying applicable duties/tariffs are included. Do not add Mouser's tariff warning to Newark's displayed price. Tax/shipping and actual invoice terms remain unconfirmed. [1](https://www.newark.com/analog-devices/eval-ad5940bioz/eval-board-electrochemical-front/dp/50AK1328)
- **Mouser observation:** $497.15. If the warned 8% tariff applies to that entire base price, the arithmetic is **$39.77 additional, or $536.92 before tax/shipping**. Applicability and basis must be confirmed; this is not a quoted landed price. [2](https://www.mouser.com/ProductDetail/Analog-Devices/EVAL-AD5940BIOZ?qs=w%2Fv1CP2dgqozY%2F%2FPHNLAZQ%3D%3D)
- No defensible buyable MAX30009 kit price was established.

### Total bench cost is not just the kit

`Total = confirmed bundle + approved fixture interface + six check fixtures + calibration standard + reference characterization/rental + other needed instrumentation/access + shipping/tax + engineering effort`.

Do not double-count an included controller or Z-Test board. Do not omit independent metrology merely because the chip has an internal calibration resistor. The supplier/lab questionnaires identify the missing costs.

**Illustrative reserve calculation—not a supplier estimate or recommended budget:** choose Newark's displayed $487.21 as the kit base, an arbitrary $200 reserve for passive fixtures/interface, and an arbitrary $1,000 reserve for reference work. That produces **$1,687.21 before tax/shipping, labor and any additional instrumentation**. The $200 and $1,000 are user-adjustable placeholders, not researched market prices, and might be inadequate. A complete ready-to-operate total is currently **unknown**.

No human-connected design, clinical/reference DXA work or safety certification is included in that example.

## 7. Subscription and lock-in implications

The purchase decision should require local access to raw measurements, configuration, calibration and historical files. Do not accept a cloud-only physiological score as a substitute. The existing offline checker has no account or recurring service requirement, but that does not prove either vendor's installer/license/support is unrestricted.

Distinguish:
- **Necessary recurring quality costs:** reference recalibration, standards maintenance and replacement components as appropriate.
- **Optional commercial services:** cloud storage, synchronization, dashboards, interpretation, coaching and support contracts.
- **Development access risks:** installer removal, old firmware tools, restrictive licensing, discontinued distribution or dependence on a particular host OS.

A one-time kit purchase can still create software lock-in. An optional service subscription can fund useful support, but should not be required to recover raw bench measurements. Obtain these terms in writing; do not infer them from a free download button.

## 8. Concrete shortlist and decision rules

1. **Quote lead: Newark EVAL-AD5940BIOZ, 50AK1328.** Require a binding itemized quote, actual stock, controller/Z-Test packing list, shipped revisions, return terms and approved passive-fixture interface. Page errors prevent treating it as a confirmed order route.
2. **Backup: Mouser EVAL-AD5940BIOZ, 584-EVAL-AD5940BIOZ.** Resolve tariff and finite-stock/distribution-retirement risk before relying on it for continuing support.
3. **Conditional technical preference: ADI direct MAX30009 kit or manufacturer-approved successor.** Proceed only after written orderability, frequency, revision and export confirmation; otherwise do not spend time implementing its parser first.
4. **Metrology inquiry: Transcat reference electrical service**, with Boston/Wilmington intake/routing question; **IET Labs** as a second technical lead.
5. **Rental fallback: Transcat/Electro Rent E4980A-class instrument**, conditional on complete fixture/uncertainty quote and access to a competent operator.

The listing facts supporting these leads are cited in sections 1 and 5. **My decision rule:** no kit order until packing list, interface, export path and independent reference-measurement feasibility are all resolved. A cheap kit with inaccessible logs or unachievable phase reference is not the cheaper project.

The [supplier/lab questions](impedance-procurement/Supplier-Questions.md) are ready to copy into inquiries. They are **drafts only and have not been sent**.

## Evidence limits

This is a dated web check, not real-time inventory verification. Search extractions and detailed page retrievals disagreed on price/availability; the report gives priority to detailed pages and marks search-only leads explicitly. Some detailed pages failed to fetch, and a displayed page can itself contain network errors. No checkout, telephone confirmation, supplier response, installer execution, current accreditation-scope audit or hardware validation was performed. The evidence file stores concise observations and retrieval outcomes—not full-page captures or manufacturer-document byte hashes.
