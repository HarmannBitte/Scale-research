# Impedance acquisition: bench-only specification and phantom qualification plan

**17 October 2026 · Design proposal, not a tested instrument**

## Decision in brief

Evaluate the **MAX30009EVKIT# first**, with an independently characterized passive impedance fixture. Start with **complex impedance near 50 kHz**, then qualify a modest frequency sweep for quality-control research. Use the **AD5940BIOZ evaluation stack as the alternative**, particularly if its firmware ecosystem is preferable and a roughly 200 kHz upper limit is sufficient.

Do **not** start by building a scale, connecting electrodes to a person, or deploying the NHANES body-composition models on these measurements. Electrical accuracy is a necessary intermediate step, not proof of biological validity or safety.

Delivered with this plan:
- [Offline Python analysis tool](impedance-bench/phantom_check.py), using only Python's standard library.
- [Fourteen software tests and execution receipt](impedance-bench/software-tests.txt).
- [Synthetic demonstration inputs and results](impedance-bench/synthetic-demo/primary-results.json), with a separate [spectral result](impedance-bench/synthetic-demo/spectral-results.json).
- [Bench parts shortlist](impedance-bench/parts-shortlist.csv), [operating instructions](impedance-bench/README.md), and a downloadable [complete package](Impedance-Bench-Package.zip).

**Actual status:** no board purchased, no wiring assembled, no electrical measurements performed, no human connection, and no clinical validation. The software tests validate calculations and rejection behavior only.

## 1. Why this follows the NHANES work

The [fresh-cycle analysis](NHANES-Impedance-DXA-Fresh-Cycle-Validation.md) found that adding 50 kHz resistance/reactance to anthropometry improved held-out fat-percentage MAE by about **0.40–0.47 percentage points**, depending on model. Adding the complete available spectrum produced a smaller further improvement of roughly **0.03–0.05 points** for that comparison.

That supports prioritizing good complex-impedance acquisition over collecting more derived marketing metrics. It does **not** establish that a single-frequency instrument is sufficient: the NHANES 50 kHz groups were screened using full-spectrum fit/quality information. Its Hydra instrument sampled 50 frequencies from 5 kHz to 1 MHz. A reduced sweep cannot automatically reproduce that screening, and neither candidate below is established here as a full Hydra replacement. [S6]

This phase measures **R, signed X, magnitude, phase, and acquisition quality**, not fat, muscle, hydration, visceral fat, bone mineral, vascular age, ECG, EDA, PWV, or other physiological outcomes. A chip's application list does not validate those outcomes in a finished device.

## 2. Platform choice and procurement caveats

| Issue | MAX30009EVKIT# — preferred first evaluation | AD5940BIOZ stack — alternative |
|---|---|---|
| Measurement approach | Simultaneous I/Q acquisition; configurable two-/four-electrode operation; precision calibration port | Voltage/current DFT measurements, switch matrix, TIA calibration; verify the specific two-/four-wire application configuration |
| Documented kit | Rev 2 guide identifies MAX30009_EVKIT_B sensor board and MAXSENSORBLE_EVKIT_B MCU board, LiPo, BLE, programmer, and Windows GUI | AN-1557 identifies EVAL-ADICUP3029, EVAL-AD5940BIOZ, and AD5940 Z test board |
| Initial frequency scope | 50 kHz first; proposed 5–200 kHz sweep subject to actual register/clock settings | 50 kHz first; high-speed loop documented up to/about 200 kHz; characterize endpoint performance |
| Calibration | GUI supports per-frequency coefficients/offsets, settling/averaging counts, CSV calibration setup, and sweep mode | Use application-specific RCAL/RTIA and voltage/current calibration; MAX30009 coefficients are not transferable |
| Export | Guide documents direct CSV and flash-binary-to-CSV workflow; register preamble and footer require a real parser | Preserve raw DFT voltage/current results, configuration, calibration, and derived complex Z; prove the chosen firmware export |
| Human use | This plan permits passive electrical fixtures only | Manufacturer explicitly says: **“Never connect the AD5940 evaluation board to the human body.”** |

Sources: manufacturer kit guide, product/datasheet, and AN-1557. [S1–S4]

### Frequency discrepancy: do not paper over it

The current MAX30009 product page advertises **1–806 kHz** BIA/BIS in its feature list, while the same page's transmitter description says **16 Hz–500 kHz**. The lowercase datasheet URL retrieved for this investigation also lists a 500 kHz drive limit. The product page links a Rev. 2 datasheet using an uppercase filename. These are not sufficient evidence for one consistent, guaranteed frequency envelope across revisions and configurations. [S2–S3]

Before ordering, ask the manufacturer for the exact silicon revision, supported clock/PLL/drive combinations, applicable datasheet revision and errata, and measured kit support at the intended frequencies. Archive the actual documents and firmware supplied. **The proposed baseline stops at 200 kHz; 500 kHz or 806 kHz is not a promised deliverable.** Even 806 kHz is below Hydra's 1 MHz upper endpoint.

### What to verify before spending money

1. Exact orderable kit number, both board revisions, included battery/programmer/cables, current stock, lead time, return policy and replacement path. A distributor's discontinued listing for a kit does not prove the chip itself is discontinued.
2. GUI/firmware versions, download availability, host OS support and offline operation. The Rev 2 guide specifies Windows 10/.NET 4.7.2 or later; Windows 11 compatibility was not tested here. [S1]
3. Ability to export raw samples and registers, calibration coefficients, sample numbering, status and packet-loss metadata—not just a plotted magnitude or proprietary body-composition score.
4. Design-file and software licenses. Published schematic/BOM/layout files do not by themselves establish a completely open-source, redistributable product.
5. Reference-instrument rental or laboratory access. A cheap DMM can check DC resistors but cannot establish AC phase accuracy of the completed fixture.

**No current price or stock is certified here.** Historical kit prices and volume chip prices are not quotes for a complete bench setup. The parts shortlist is a specification for evaluation, not a shopping cart or authorization to purchase.

## 3. Acquisition contract

### Canonical electrical quantities

Use the engineering convention

`Z(f) = R(f) + j X(f)`

`|Z| = hypot(R, X)` and `phase_deg = degrees(atan2(X, R))`.

A passive capacitive phantom has **negative X** and negative phase. Keep original manufacturer I/Q signs and counts unchanged in the raw archive; document the calibrated transformation into this convention. If a downstream dataset represents capacitive reactance as a positive magnitude, create an explicitly named transformed feature. Do not silently flip signs or equate raw Q counts with ohms.

Compute phase with **atan2**, including correct quadrant handling. Use wrapped angular differences for errors. A nominal resistor should have approximately zero phase; independently measured fixture parasitics may make its reference phase nonzero.

### Proposed acquisition settings

- Primary target: **50,000 Hz nominal**, with actual frequency derived from the clock/dividers and independently checked where feasible. Proposed initial window: ±1% of target, explicitly not proof of equivalence to NHANES.
- Spectral development profile: nominal **5, 10, 20, 50, 100 and 200 kHz**. Record actual supported frequencies. Compare against references at those actual frequencies, not values calculated at a different nominal frequency.
- Tetrapolar/Kelvin-style force and sense connections at the passive load reference plane. This is a fixture topology, not authorization to use four skin electrodes.
- For the MAX30009 bench evaluation, **32 µA RMS is a candidate initial setpoint**, supported in the retrieved current-options table; verify SNR, gain, compliance and actual current on the passive fixture. It is not a human-safety limit. Do not copy this setting into an AD5940 voltage-drive configuration. [S3]
- Choose gain, ADC rate, filters, drive mode and averaging from the applicable manufacturer procedure. Freeze them in a configuration file; do not propose one sample rate as universally compatible with every drive frequency.
- Determine settling empirically after every frequency/path/gain change. Start with the kit's documented settling/averaging controls, then lengthen settling until results stop depending on the discarded interval. “32 points” in a GUI example is not universal evidence of settling. [S1]
- Save **at least 30 nonoverlapping measurement windows per verification cell**, retaining the raw samples underlying each window and its averaging duration. Within-run SD is descriptive repeatability, not an independent-sample confidence interval.

A valid measurement must include the applicable calibration/configuration IDs and quality status. Missing or unknown clipping, compliance, lead-off or packet-loss information must not be converted to a clean zero flag.

## 4. Passive phantom set

### Model and reference plane

For RC_A and RC_B, build the passive topology:

```text
force+ ----o---- Rseries ----+---- Rparallel ----+----o---- force−
          |                 |                  |    |
        sense+              +------- C --------+  sense−
```

Force/sense pairs join at the two marked load terminals. Thus sense+ is **before** Rseries and measures the entire network. For a resistor-only fixture, replace the network with that resistor. Fixture cable/contact impedances outside these terminals are not part of the ideal model.

`Z(f) = Rseries + Rparallel / (1 + j·2πf·Rparallel·C)`

This is a one-time-constant passive model, **not** a validated human-tissue phantom or a general fractional-order Cole model.

| Verification fixture | Nominal parts | Nominal R at 50 kHz (Ω) | Nominal X (Ω) | Nominal phase (°) |
|---|---|---:|---:|---:|
| R100 | 100 Ω | 100.0000 | 0 | 0 |
| R220 | 220 Ω | 220.0000 | 0 | 0 |
| R470 | 470 Ω | 470.0000 | 0 | 0 |
| R1000 | 1,000 Ω | 1,000.0000 | 0 | 0 |
| RC_A | Rseries 470 Ω; Rparallel 210 Ω; C 15 nF | 576.0975 | −104.9943 | −10.3288 |
| RC_B | Rseries 500 Ω; Rparallel 500 Ω; C 6.8 nF | 733.5438 | −249.4578 | −18.7817 |

These numbers are **analytical nominal values**, not measured standards. Real capacitors have tolerance, loss and parasitics; resistors, connectors, wiring and mounting introduce additional errors. Component tolerances cannot be ignored because the equation is exact.

Use low-temperature-coefficient precision resistors and low-loss capacitors—C0G/NP0 or suitable film where available. Start with resistor tolerance ≤0.1% and capacitor tolerance ≤1%, but independently characterize the **assembled fixture** at each test frequency. Tolerance alone is not its AC uncertainty. Avoid solderless breadboards for final qualification; keep lead geometry fixed, label fixtures, and document a photograph/drawing and terminal reference plane.

Keep a separate precision calibration resistor—**680 Ω is a candidate**, subject to the board procedure and range. It must not double as an independent check load. For AD5940, AN-1557 selects RCAL near RTIA for its particular configuration; do not substitute this candidate indiscriminately. [S4]

## 5. Calibration and independent verification

1. **Freeze the setup:** record board serial/revision, supply/charger state, firmware/GUI versions, register dump, lead geometry, ambient temperature, gain/filter/drive settings and clock source. Warm up for at least 10 minutes as a proposed starting procedure; characterize whether more is needed.
2. **Characterize reference loads independently:** use an appropriate calibrated impedance analyzer/LCR instrument with stated magnitude and phase uncertainty over the required range. Save complex values and expanded uncertainty, coverage factor, date, instrument/certificate IDs, settings and reference plane. Measure assembled fixtures, not only loose parts.
3. **Compensate the reference instrument/fixture:** use that instrument's documented open/short/load or fixture compensation procedure at its reference plane. Keysight's documentation illustrates why fixture compensation matters, but its algorithm is not automatically applicable to a BioZ AFE. [S5]
4. **Calibrate the AFE by its own procedure:** for MAX30009 the kit guide documents external CALx or electrode-path calibration, per-frequency coefficients/offsets and optional inclusion of electrode-pin parasitic effects. Record which route is used. Calibration at CALx does not automatically remove the complete external cable fixture error. [S1]
5. **Repeat calibration when configuration changes** unless a documented, verified calibration mapping covers the new state. At minimum track frequency, clock, drive, gain/filter/ADC settings, routing and temperature validity.
6. **Verify on held-out loads:** measure the six verification fixtures, not the calibration resistor. Start at 50 kHz; qualify the spectral profile only after this passes. Retain every flagged measurement and rejected run with a reason.
7. **Separate adjustment from acceptance:** do not fit a correction to a verification fixture and then report its corrected agreement as independent validation. If a correction is necessary, declare a new calibration version and reserve additional unseen check fixtures.

The datasheet's small error figures apply to specified loads, settings, temperature and calibration conditions. They are not a blanket system guarantee. The proposed thresholds below are **our engineering targets**, not manufacturer specifications or clinically derived tolerances. [S3]

## 6. Proposed numerical acceptance targets

Apply these initially to the six fixtures at 50 kHz. The offline spectral profile applies the same ambitious targets at all six frequencies; failure would identify an unqualified frequency/configuration, not prove the chip defective.

| Metric | Proposed bound |
|---|---|
| Error in magnitude of the mean complex measurement | ≤ max(0.5 Ω, 0.5% of reference magnitude) |
| Error in mean R | ≤ max(0.5 Ω, 0.5% of absolute reference R) |
| Error in mean signed X | ≤ max(1 Ω, 2% of absolute reference X) |
| Wrapped phase error of mean complex measurement | ≤0.20° |
| Within-cell SD of window-mean R and X | Each ≤0.20 Ω, at least 30 windows |
| Reference expanded uncertainty for each metric | ≤one-quarter of that metric's bound |
| Guard band | Absolute mean error **plus supplied reference expanded uncertainty** must remain within the bound |
| Valid-run clipping/compliance/lead-off/transport-loss flags | None asserted; unknown status is invalid, not “clear” |

Magnitude and phase here are calculated from the mean complex Z, not the mean of individual magnitudes/angles. The guard band covers the supplied **reference uncertainty only**; it is not a complete system uncertainty budget. A metrology review must include correlation, clock/current, fixture, calibration, drift, quantization, repeatability and environmental contributions.

### Additional physical tests — not implemented by the offline checker

| Test | Procedure and proposed decision |
|---|---|
| Drift | Repeat fixed RC_A and R470 checks after 10, 30 and 60 minutes without recalibrating. Target changes ≤0.2% magnitude and ≤0.1° phase, while remaining within absolute acceptance bounds. |
| Reconnection | Ten complete disconnect/reconnect cycles, measuring RC_A after settling each time. Target SD of cycle means ≤0.5 Ω in R/X and every cycle within accuracy bounds. |
| Force/contact asymmetry | On a passive fixture, add removable 0, 1 kΩ and 10 kΩ series impedances in each force/sense lead separately, then asymmetric pairs. Stay within rated operating conditions. In-range readings must meet the original bounds; if limits are exceeded, the system must reliably report invalid/compliance/contact quality rather than publish a plausible clean number. |
| Reactive contact perturbation | Characterize added passive lead networks, initially 10 kΩ in parallel with 10 nF, one lead at a time. This is a stress network, not a universal skin model. Distinguish intentional sense-path loading from changes inside the defined load reference plane. |
| Cable sensitivity | Compare fixed short leads with a documented longer cable and altered routing; check parasitic effects at all intended frequencies. Recalibration must be explicit. No claim of universal cable-length immunity. |
| Controlled faults | Use manufacturer-approved passive open/load-switching tests and only permitted short tests, at low bench excitation. Log the raw/status behavior, invalidation time and recovery. Proposed application-level flagging target: ≤1 second; no stale valid value after the fault is known. Open/short states are not ordinary in-range accuracy loads. |
| Data integrity | Run at least 30 minutes; verify sample ordering, timestamps, counters, BLE/FIFO losses and file footer totals. Force a transport interruption; it must be visible, not interpolated away. |
| Configuration/temperature | Repeat after power cycle, firmware/configuration reload and across the intended bench temperature envelope. Characterize validity intervals before promising operation outside the initial room-temperature setup. |

Some contact perturbations may be indistinguishable from a genuine load without additional diagnostics. If they cannot be detected or bounded, record that limitation and do not claim robust contact screening. A six-frequency sweep is an investigational QC input, not a proven substitute for the original full-spectrum Cole-fit screen.

## 7. Data ownership, export and subscription design

The MAX30009 Rev 2 guide provides more concrete export information than a generic “CSV supported” claim: rows 1–4 hold register information, row 5 start time, row 6 the header, then data and footer metadata. Listed fields include timestamp, sample number, BIOZI, BIOZQ, temperature, RTC, status caches and register-related fields. Flash logging stores raw binary and the GUI can parse it into CSV. [S1]

**Do not feed this vendor CSV directly into the included checker.** An acquisition adapter remains to be written and tested against actual files from the chosen GUI/firmware. Preserve preamble/footer, counters and original binary; verify whether each exported column is counts or calibrated units. A plot checkbox is not proof that the file contains calibrated ohms.

### Archive structure required for a real run

- Immutable original binary/CSV files plus hashes and parser version.
- Run manifest: board/firmware/software IDs, UTC time plus monotonic acquisition time/counters, power state, temperature, operator/setup, path IDs, source kind and purpose.
- Configuration snapshots: complete register/PLL/filter/gain/drive/ADC values, requested and actual frequencies, excitation setpoint and independent current-check record.
- Calibration archive: measured calibration-standard values/uncertainty, route/reference plane, coefficients/offsets by configuration/frequency, dates and expiry/recalibration rules.
- Sample archive: original I/Q or voltage/current DFT values, sample counters, timestamps, raw status bits and documented decoded flags. Preserve unknown states as unknown.
- Derived table: calibrated R/X in ohms, calculated magnitude/phase, fixture ID, actual frequency, window membership/averaging duration, quality flags, and links to immutable raw/config/calibration records.
- Independent reference measurements and certificates, environmental records, all failed runs and software analysis outputs.

This enables a **local-first, subscription-independent architecture**: raw measurements and calibration history stay accessible without a vendor body-composition service. The offline checker has no network calls or account requirement. The vendor GUI's installation, licensing and offline behavior still require practical verification.

Companies can monetize cloud synchronization, coaching, historical dashboards, interpretation and recurring support because these generate continuing revenue and retention; subscriptions can also fund ongoing services. Those business incentives do **not** mean complex impedance acquisition intrinsically needs a subscription. Conversely, open export does not make measurement validation, maintenance or safe hardware free. Do not build a new dependence on a proprietary score when the goal is reproducible local measurements.

## 8. What the supplied software does—and does not do

The Python tool computes passive-model expectations and checks already-calibrated measurement tables. It checks completeness, duplicate sample/reference keys, finite numbers, frequency matching, phase sign/wrapping, uncertainty bounds, quality flags, mean error and repeatability.

The synthetic demonstration contains **1,080 generated rows: six fixtures × six frequencies × 30 repeats**. Seeded noise is added to theoretical calibrated ohms. It does **not** simulate a calibrated analog front end, ADC counts, lead parasitics, packet transport or physiological signals. Its zero reference uncertainty reflects exact arithmetic model references, not physical standards.

**Executed results:** the primary six-cell and spectral 36-cell numerical demonstrations both pass their numerical checks. **Fourteen software tests pass**, including deliberate sign reversal, 2% R bias, fault flags, missing cells, duplicate records, nonfinite numbers, mismatched frequency and invalid uncertainty. See the saved receipt.

Every result explicitly keeps `device_qualified: false` and `human_connection_authorized: false`. Hardware-tagged data still require review; metadata are not authenticated and a user-entered “independently measured” label cannot establish traceability. The checker does not implement a vendor-file adapter, acquire data, calibrate I/Q, measure current, verify safety or conduct the additional physical test matrix.

Do not change `source_kind` on the demonstration and call it a hardware run. Real references must come from independent assembled-fixture measurements, with their uncertainties and documentation.

## 9. Release gates and next action

| Gate | Evidence required | Current state |
|---|---|---|
| 0: documented bench design | Board/configuration/revision choice, passive fixtures, data schema, test plan | Proposed here; exact board availability/frequency support still to confirm |
| 1: software arithmetic | Reproducible synthetic calculations and rejection tests | **14 tests passed**; no hardware implication |
| 2: physical 50 kHz bench accuracy | Independent reference characterization, verified calibration/export adapter, six held-out fixtures, uncertainty review | **Not performed** |
| 3: expanded bench robustness | Spectral/contact/fault/drift/reconnection/data-integrity tests | **Not performed** |
| 4: separate human-connected design | Qualified electrical/biomedical engineering review of the complete system, intended use and applicable standards; isolation/leakage and normal/single-fault analysis and testing, power/charger/USB paths, current limits across frequency, protection, materials and ethics/regulatory plan | **Not designed or authorized**; no evaluation-board connection to people |
| 5: physiological validation | Appropriately approved paired study with reference measurements; repeatability/longitudinal and subgroup evaluation; independent held-out validation | **Not performed** |

Neither battery power nor BLE alone establishes electrical safety. Passing every passive-phantom test still does not authorize human use. Manufacturer application-note current examples are not complete-system certification or universal limits for every applied part and fault condition.

**Recommended next action:** obtain a written manufacturer/supplier confirmation of the MAX30009 kit revision, applicable datasheet, actual near-50 kHz settings and local raw export. Then obtain a quote for independent fixture characterization and decide whether to fund a strictly passive bench evaluation. Do not buy electrodes or add body-composition predictions at this stage.

## Sources and evidence limits

Manufacturer sources were consulted on 17 October 2026. The kit PDF identifies itself as **319-100859; Rev 2; 3/24**; a web publication date is not the document revision date.

- **[S1]** Analog Devices, [MAX30009EVKIT# Rev 2 guide](https://www.analog.com/media/en/technical-documentation/data-sheets/max30009evkit-evk-rev2.pdf): kit contents, host requirements, calibration controls, logging and output-file format. Relevant tool-extracted portions: chunks 0, 4 and 5. [Kit landing page](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/max30009evkit.html).
- **[S2]** Analog Devices, [MAX30009 product page](https://www.analog.com/en/products/max30009.html): simultaneous I/Q, configurations, calibration port and conflicting frequency statements; links Rev. 2 datasheet. Do not convert its volume chip price into a kit price.
- **[S3]** Analog Devices, [MAX30009 lowercase datasheet URL](https://www.analog.com/media/en/technical-documentation/data-sheets/max30009.pdf): retrieved electrical-characteristic tables include current options, drive-frequency limits and load-/temperature-/calibration-specific accuracy conditions. Exact delivered revision/configuration must be reconciled before design freeze.
- **[S4]** Analog Devices, [AN-1557](https://www.analog.com/en/resources/app-notes/an-1557.html): evaluation stack, simulator-only warning, high-speed measurement loop, voltage/current DFT and application-specific calibration component selection.
- **[S5]** Keysight, [Open/short/load fixture compensation](https://helpfiles.keysight.com/csg/e5061b/measurement_with_options/option_005_impedance_analysis/setting_up_measurement/eliminating_error_factor_of_fixture/open_short_load_compensation.htm): instrument-specific compensation context. [Saved extracted text](impedance-bench/evidence/fixture-compensation.txt) and [retrieval manifest](impedance-bench/evidence/manifest.json).
- **[S6]** CDC, [NHANES 2003–2004 BIX documentation](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2003/DataFiles/BIX_C.htm), also saved in the preceding benchmark project: Hydra spectrum and fit-quality definitions.

**Archival limitation:** direct sandbox downloads of the three ADI documents timed out, although the page-fetch tool returned the relevant source text. The evidence manifest records these failed direct-download attempts; it does not falsely claim complete archived ADI PDFs or hashes. The saved Keysight capture has source/text hashes. This package does not freeze all external manufacturer documentation; that remains a design-freeze requirement.
