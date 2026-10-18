# Reproducing software checks

The receipts preserve exact commands, working directories, timeouts and logs. Original absolute paths identify the sandbox working copies; substitute your extracted **full upstream** working directories. Some test fixtures are intentionally omitted from the compact collection, so restore the corresponding pinned full source first using `fetch_upstream.py` if necessary. Do not interpret missing compact-snapshot data as an upstream defect.

Use disposable environments and passive/software-only work. Do not run flash scripts or connect a person. No tool here authorizes purchases or firmware deployment.

## Environments

- `verification/python-version.txt` and `arm-gcc-version.txt`: executed interpreter/toolchain.
- `environment-freeze.txt`: initial scientific test environment.
- `analysis-environment-freeze.txt`: separate environment used for actual DearEIS/pyimpspec installation and tests.

These are observed package versions, **not a hash-locked, offline dependency distribution**. Some freeze entries point to the original local source path: replace that with the corresponding pinned full source before installing. Network wheel availability, native packages and platform differences may affect reproduction. Keep legacy OpenEIT separate from modern analysis packages.

For scientific Python tests, the harness disabled pytest plugin autoload and selected a noninteractive Matplotlib backend. Bounded follow-ups also set `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`.

## Executed test selections

From each appropriate repository root, with its dependencies installed:

- pyEIT: `python -m pytest -q tests --disable-warnings` — 62 passed.
- BioScale: `python -m pytest -q tests --disable-warnings` — 4 passed, 1 failed because the test omits `height_cm`.
- melazab: `python -m unittest discover -s gui -p 'test_*.py'` — 5 passed; subprocesses mocked, no actual flashing.
- melazab firmware: `make -j2` in each of `blink-led`, `measure-2wire-bioz`, `measure-4wire-bioz`, `time-series-bioz`, `time-series-bioz-2wire` — all linked; inspect linker warnings. Do **not** run `make flash`.
- impedance.py: `python -m pytest -q impedance/tests -k 'not test_circuit_fit' --disable-warnings` — 34 passed, 1 deselected. Its test fixtures expect a directory named `impedance.py` relative to the test working directory; preserve the expected layout rather than editing source. A subsequent isolated `impedance/tests/test_fitting.py::test_circuit_fit` attempt timed out at 90 seconds even with thread caps. The original full-suite attempt timed out at 180 seconds.
- Synthetic RC: inspect/run `verification/synthetic-rc-check.py` in the environment with the pinned impedance.py importable. It generates its own six-point spectrum; there is no measured input dataset.
- OpenEIT parser: `tools/research-history/run_followups.py` documents the exact AST isolation and seven probes. It does not exercise the dashboard, hardware, BLE or serial transport. The portable receipt includes inputs/results.

## Analysis stack

Both pinned full pyimpspec and DearEIS sources were pip-installed together in a separate Python 3.13 virtual environment with pytest. Selected tests were then executed from their upstream `tests/` directories:

```
# pyimpspec, from its tests directory; upstream runner style:
python -m unittest -v test_circuit test_connection test_element test_data
# 139 passed

# DearEIS, from its tests directory:
python -m pytest -q test_project.py test_utility.py --disable-warnings
# 43 passed
```

An earlier pyimpspec pytest run of the same four modules yielded 138 passes and one redirected-stderr assertion failure. Upstream-style unittest resolved it without source changes; preserve that distinction when comparing results. No interactive DearEIS window was launched, and the complete fitting/DRT suites were not run.

## Historical helpers

`tools/research-history/` preserves how the collection was obtained and augmented, how omissions/notices were repaired, and how software checks were orchestrated. It is a methods record with hard-coded sandbox paths, not a supported turnkey build tool. Initial `results.json`/`followup-results.json` are chronological receipts, **not the final combined status**. Consult the dossier and later per-job receipts for corrections.
