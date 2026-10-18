# Passive impedance bench package

**Bench-only design materials. No hardware was measured. Do not connect evaluation boards to people.**

## Run the offline demonstration

Python 3.10+; standard library only. No installation, network access, account or hardware driver required.

```sh
cd impedance-bench
python -m unittest -v test_phantom_check
python phantom_check.py demo synthetic-demo
python phantom_check.py analyze synthetic-demo --profile primary --output synthetic-demo/primary-results.json
python phantom_check.py analyze synthetic-demo --profile spectral --output synthetic-demo/spectral-results.json
```

`demo` overwrites the three demonstration input files in the specified directory; use a new directory if preserving an earlier run. `analyze` overwrites only its named result file. Exit code 0 means the numerical checks passed, not that hardware is qualified. A numerical failure or invalid input exits 1. File/JSON read errors may raise a Python exception; no pass result is produced in that case.

The included demo has 1,080 theoretical/noisy rows, not ADC counts or physical measurements. Reference values are analytical with zero mathematical reference uncertainty. Do not use these references as physical standards.

## Checker input schema

The checker reads `run.json`, `references.csv` and `samples.csv`. It is **not** a parser for a vendor CSV. Keep full raw provenance in a separate immutable archive as specified in the accompanying report. This schema is only the normalized numerical-check subset, not the acquisition/data-ownership contract.

`run.json` must explicitly set `source_kind` to `synthetic` or `hardware`. The demonstration also documents its scope/seed. The checker does not authenticate this declaration.

`references.csv` columns:

- `fixture_id`: R100, R220, R470, R1000, RC_A or RC_B.
- `nominal_frequency_hz`: one of 5000, 10000, 20000, 50000, 100000, 200000.
- `frequency_hz`: actual frequency, positive, within proposed ±1% nominal window.
- `r_ohm`, `x_ohm`: independent assembled-fixture complex reference, with negative capacitive X.
- `reference_kind`: `analytical_synthetic` for the demo; `independently_measured` only for actual independent measurements with archived evidence.
- `u_mag`, `u_r`, `u_x`: nonnegative reference expanded uncertainties in ohms.
- `u_phase`: nonnegative reference expanded phase uncertainty in degrees.

For physical fixtures derive magnitude/phase uncertainties consistently with R/X covariance or obtain them directly from the reference instrument/metrology analysis. Archive coverage factors and correlation information; this reduced CSV does not encode them. Do not enter arbitrary zero uncertainties.

`samples.csv` columns:

- `fixture_id`, `frequency_hz`: match an actual-frequency reference key exactly after numeric parsing.
- `repeat_index`: unique nonnegative integer within fixture/frequency.
- `r_ohm`, `x_ohm`: calibrated window-mean complex measurement in ohms, not I/Q ADC counts.
- `clipping`, `compliance_fault`, `lead_off`, `transport_loss`: each 0 or 1. All four are mandatory. Unknown/unavailable hardware status must not be relabeled zero.

At least 30 nonoverlapping measurement windows are required per cell; exactly one reference per fixture/nominal frequency. Do not round actual frequencies differently in the two tables. The primary profile requires the six 50 kHz cells. The spectral profile requires all 36 cells. Additional supported actual-frequency keys within one nominal cell make that cell ambiguous and are rejected. This is a fixed-profile checker, not a general impedance laboratory data manager.

All input numbers are checked for finite values, including outside the selected profile. Duplicate reference/sample keys and missing reference matches are rejected. Status flags assert run invalidity rather than silently dropping rows. There is no interpolation or automatic recalibration.

The tool evaluates error of mean complex Z, reference-uncertainty guard bands, and within-cell SD. It does not perform raw calibration, validate packet counters/timestamps, prove reference independence, implement the physical stress matrix, estimate total system uncertainty, or authorize release. Even a hardware-tagged numerical pass returns `device_qualified: false` and `human_connection_authorized: false`.

## Files

- `phantom_check.py`: offline model/demo/numerical analysis.
- `test_phantom_check.py`, `software-tests.txt`: executed integrity/rejection tests.
- `synthetic-demo/`: clearly labeled theoretical inputs and results.
- `parts-shortlist.csv`: generic evaluation specifications, no purchase/price claims.
- `evidence/`: capture manifest and successful Keysight text capture. ADI direct-download timeouts are recorded, not hidden.
- `../Impedance-Bench-Acquisition-Specification.md`: full plan, source links, safety gates and caveats.

Generated using Python 3.13.16 in the current workspace. Unit tests use temporary directories and do not modify the included demo.
