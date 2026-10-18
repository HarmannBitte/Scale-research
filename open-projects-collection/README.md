# Open-source impedance / biosensing research collection

Collected and investigated through 18 October 2026. **25 repositories, 26 snapshots, 15 project families.** All surveyed candidates are included; licence restrictions were not used to exclude candidates.

## Start here

1. Read `INVESTIGATION.md` for technical findings, actual tests and limitations.
2. Browse `project-catalog.csv` or `collection-index.json` for every snapshot.
3. Run `python tools/verify_collection.py` from an extracted archive (Python 3.9+).
4. Inspect `sources/`, `research/` and `verification/` as needed.

**These are selected source/design snapshots, not full Git mirrors.** Every collected file has a SHA-256 in its manifest. Omitted upstream files are explicitly inventoried, including path/size and the collector's reason. No-OS is an intentionally scoped MAX30009 snapshot, not a complete framework/SDK. Many large datasets/manuals/binaries are not distributed here. Available CAD/fabrication files and important notices were deliberately restored after the initial collection filter. The reviewed 55-page AD5933 thesis is included.

## Contents and provenance

- `sources/<snapshot>/`: original upstream file contents in original relative paths. Build/test operations used separate working copies, not these distributed snapshots.
- `manifests/<snapshot>.json`: commit, source/archive URL, original archive hash where available, per-file hashes, all observed omissions, and scope.
- `collection-index.json`: 26 snapshot records. AD5940 library is deliberately represented twice: observed default-branch revision and exact dependency required by the examples.
- `project-catalog.csv`: human-readable capability/test/licence observations; not a licence-based ranking.
- `research/`: schematic/PDF inventory, 26 source-level findings with pinned links, and recalculated historical electrical-validation errors.
- `verification/`: raw tests/build/install outputs, environment freezes and receipts. Historical failures are retained beside corrected follow-ups, not deleted.
- `tools/verify_collection.py`: portable, offline hash check. Also checks bundled non-source files against `BUNDLE-FILE-HASHES.json`.
- `tools/fetch_upstream.py`: optional network retrieval of complete pinned upstream archives to restore omissions. It does not extract or execute them. Use `--list`; select one repo and, for AD5940 library, one commit. Full no-OS archive was not originally downloaded/hashed; fetching it requires explicit `--allow-unhashed`.
- `tools/research-history/`: historical collection/investigation helpers. They contain original sandbox paths, are not a portable one-command build system, and must not be rerun blindly.

Manifest fields beginning `staging_archive_` describe the intermediate ZIP used during collection. Those ZIPs are **not** duplicated inside this archive: source files are laid out directly under `sources/`. Their per-file hashes are the relevant distributed-content checks. Upstream archive hashes refer to the original downloaded tarballs, not this final research archive. GitHub may regenerate archives; a mismatch should be investigated, not bypassed silently.

`BUNDLE-FILE-HASHES.json` hashes every included file except itself. The separately supplied archive SHA-256 covers the archive as a whole. These are integrity checks, not a cryptographic identity/signature or certification.

## Evidence boundaries

- Successful compilation/linking is not a running firmware test.
- A test-suite pass is not a calibration, phantom study, human study, safety qualification or clinical validation.
- The synthetic RC example is explicitly synthetic; it is not measured impedance accuracy.
- The AD5933 thesis comparisons are historical passive-load results, not new measurements or DXA validation.
- Selected analysis-package tests are not the full test suites.
- No IAR/AVR/Arduino/Android/Flutter/Zephyr build is claimed here. Five melazab GNU ARM builds were executed.
- Full OpenEIT dashboard/transport and interactive DearEIS GUI operation were not demonstrated.
- No devices were purchased, connected, flashed or used on people in this investigation.

The collection is for inspectable research. **The AD5940 evaluation board remains never-human-connected.** No source-code licence, public schematic or successful test result removes that restriction or substitutes for a safety-engineering review.

## Licences and notices

Keep original file-level and root notices with their corresponding material. The catalogue records observed licences, not a legal opinion or permission to remove requirements. Some repositories have mixed/unclear original-code and dependency coverage. User acceptance of research-stage licence constraints does not relicense upstream material. Historical helpers and this report do not change upstream terms.

The previous science, procurement, budget, subscription/account and hardened ARM deliverables are separate and unchanged. Their older test counts must not be attributed to these unmodified upstream snapshots.
