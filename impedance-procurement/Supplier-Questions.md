# Questions for suppliers, manufacturer and metrology providers

**Drafts only. Nothing has been sent. No order, reservation or technical approval is implied.**

Purpose: passive electrical-phantom bench development only. No connection to people. Please distinguish verified answers for the exact delivered hardware/software from general chip capabilities.

## A. Evaluation-kit supplier / Analog Devices

Subject: Passive-phantom evaluation kit — availability, packing list, revisions and local raw export

Please provide:

1. A written quantity-one US quote for the exact kit, showing USD base price, duties/tariffs, shipping, tax treatment, delivery date/stock allocation, quote validity, return policy, warranty and any nonreturnable conditions. No purchase is authorized by this inquiry.
2. Manufacturer kit status, distributor-specific retirement status, support period, replacement route and approved successor if applicable. Does distribution retirement affect firmware/software availability?
3. Physical MCU/sensor board revisions and silicon revision that would ship, applicable datasheets/errata, and any rework/substitutions. Please identify actual shipment revisions, not only the guide revision.
4. Full packing list:
   - AD5940: confirm EVAL-ADICUP3029, BIOZ shield, Z-Test board, required USB cables, supplied measurement cables and programming/debug capability. Is the separately listed controller already included?
   - MAX30009: confirm MCU and sensor boards, LiPo, programmer, cables, current firmware and required host accessories.
5. Supported near-50 kHz configuration and actual resulting drive frequency; supported settings near nominal 5, 10, 20, 50, 100 and 200 kHz. Please identify clock/PLL/dividers, compatible ADC rates/filters/gain and current/voltage drive settings, constraints, calibration and guaranteed versus typical performance.
6. MAX30009 specifically: explain the product-page 806 kHz feature claim versus retrieved uppercase/lowercase datasheet first pages and transmitter description listing 500 kHz. Which revision/mode supports which limit? We will not assume 806 kHz support without an applicable written specification.
7. Manufacturer-approved passive phantom connection method. For AD5940, the P6 connector guide restricts connections to the supplied Z-Test board or cables: please provide an approved way to evaluate independently characterized custom passive loads. We will not use a generic USB cable/adapter in that measurement port.
8. Exact GUI, firmware, parser and installer versions, current OS requirements and download links. Is an account, activation, paid IDE, internet access, recurring fee or support agreement required at any stage? Is offline acquisition/export supported after installation? Please supply license and redistribution terms separately for firmware, GUI, example source and design files.
9. Example unmodified passive-load raw logs and calibration/configuration exports from those versions. Please document I/Q or voltage/current DFT units, signed scaling, phase convention, timestamps/sample numbers, status bits, register changes, clipping/compliance/lead-off flags, FIFO/transport losses and end-of-run totals.
10. Does the standard GUI export raw channel values, or only magnitude/phase? Are raw voltage/current DFT data available in AD5940 firmware without substantial modification? Can we archive every configuration and per-frequency calibration coefficient/offset and reproduce calibrated R/X offline?
11. Calibration procedure for the exact routing, drive/gain/filter/ADC settings and cable reference plane; standard values/uncertainty required; settling/warm-up; recalibration criteria. Which parasitic effects are and are not included in CAL-port versus external-path calibration?
12. Confirm simulator/passive-load-only handling restrictions and manufacturer-approved fault tests. We are not requesting permission to connect an evaluation board to humans.

Please identify unsupported items explicitly rather than substituting a physiological/body-composition score for raw electrical data.

## B. Independent fixture-characterization laboratory

Subject: Quote request — assembled passive R/RC fixtures, complex impedance and uncertainty at 50 kHz and 5–200 kHz

We plan six assembled held-out fixtures: 100, 220, 470 and 1,000 Ω resistors; RC_A = 470 Ω + (210 Ω || 15 nF); RC_B = 500 Ω + (500 Ω || 6.8 nF). Values are nominal, not standards. A separate calibration standard will be selected according to the final AFE configuration and must also be independently characterized; please price it separately.

Please quote two scopes:
- **Initial:** the six assembled fixtures at the actual supported frequency near 50 kHz, plus the separate calibration standard when specified.
- **Expanded:** the same six fixtures near 5, 10, 20, 50, 100 and 200 kHz, plus the calibration standard as applicable.

The attached `reference-request-grid.csv` provides 36 preliminary nominal-load cells and uncertainty ceilings. Actual frequencies and ceilings must be finalized with the acquisition configuration and measured fixture values.

Please confirm:

1. Will you accept these custom assembled passive artifacts, not just calibrate an LCR instrument? Can a Boston/Wilmington intake route them to the appropriate reference laboratory if needed?
2. Can you report R, signed X, magnitude and phase at each actual frequency, with expanded uncertainty, coverage factor, traceability, date, environmental conditions and applicable accreditation scope? Identify any out-of-scope measurements.
3. Can you meet all per-cell ceilings—not only a headline best magnitude uncertainty? At 1,000 Ω near zero phase, reference U(X) ≤0.25 Ω is required; if phase dominates this implies approximately 0.0143°, stricter than the general 0.05° phase ceiling. Report covariance or sufficient information for consistent R/X-to-magnitude/phase uncertainty propagation.
4. Can measurement signal levels approximate our intended low-excitation operation, and what level dependence must be assessed? The actual AFE configuration will be supplied before work; do not assume the MAX30009 current setpoint applies to an AD5940 voltage-drive setup.
5. Required terminal geometry, fixture interface, reference plane and open/short/load compensation; cable effects and loading; mounting or connector changes you would require. Will the returned assembly match the characterized assembly?
6. Calibration standard/instrument identities and current certificates, frequency accuracy, uncertainty budget, repeat measurements and treatment of loss/parasitics. Is the advertised best capability applicable to these complex loads at the actual frequencies?
7. Itemized cost for six single-frequency checks versus the full sweep, extra calibration artifact, setup, uncertainty reporting, adapters, remeasurement and shipping; turnaround, minimum order and quote validity.
8. Can you provide machine-readable CSV plus a signed report and identify rejected/unstable artifacts? Can we retain all results locally without a mandatory subscription?

Please do not proceed with paid work or modify artifacts without separate authorization.

## C. Precision LCR rental provider

Subject: Quote only — E4980A-class LCR meter and complete passive-fixture setup

Please provide a weekly and monthly all-in quote for an instrument supporting 5–200 kHz, including near-50 kHz actual settings, suitable four-terminal-pair fixture/cables, current calibration certificate with uncertainties and supported export interfaces.

Please confirm actual serial/configuration, availability, low-level signal settings, magnitude/phase and R/X accuracy at 100–1,000 Ω and the stated RC loads, uncertainty calculation support, terminal/reference-plane compensation and included software/driver licenses.

Include shipping both ways, insurance/damage terms, minimum term, deposits, tax, extension/late charges, lead time, training/support, and whether a replacement model changes the fixture/interface or uncertainty. A basic-accuracy headline alone is not enough to establish the required X/phase uncertainty. No rental is authorized by this request.
