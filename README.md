# Scale research

Research workspace on DIY body-composition scales and bioimpedance (BIA / BioZ) firmware. It collects open-source scale projects, checks them against the published literature and against the chip datasheets, and records what was verified and what was not.

**Scope.** This is research, not a medical device, and not a replacement for DXA. Nothing here has been validated for clinical use. The hardware checks listed in the findings have not been run.

## Start here

| Question | Read |
|---|---|
| What is the current state of the investigation? | `research-pass-6/RESEARCH-NOTES-2026-10-18.md` (latest sections 8, 12–16) |
| What are the findings (IDs, status, priority)? | `deep-impedance-audit/findings.json`, summary in `deep-impedance-audit/DEEP-FINDINGS.md` |
| How do I reproduce the checks? | `deep-impedance-audit/DEEP-README.md`, `deep-impedance-audit/MANIFEST.json` |
| Which literature was checked and how? | `research-pass-6/fulltext/LITERATURE-FULLTEXT-VERIFICATION.md` |
| What is still open and blocked? | `research-pass-6/OPEN-ITEMS-STATUS-2026-10-18.md`, notes section 16 |

## Repository layout

Folders from earlier passes keep their names. Their contents are not changed.

- **Research notes and reports (root level)**: `BodyScan-2-*`, `DEXA-*`, `NHANES-*`, `Impedance-*`, `Open-Source-*`. Survey, procurement and benchmark reports from the earlier passes.
- **`research-pass-3/`, `research-pass-4/`, `research-pass-5/`**: pass folders. Only the files, not nested git repositories.
- **`research-pass-6/`**: the latest pass. Notes, literature verification, open-items status, and the OKOK test-fix patch.
- **`deep-impedance-audit/`**: the impedance-firmware audit. Findings, probes, build and run logs, the pass 4 and pass 5 analysis (`pass5/`), and the generated probe code.
- **`deep-impedance-audit-pass5/`**: the MAX30001 findings update from pass 6 (`findings-update-6.json`), kept at top level for easy diffing.
- **`uploads/`**: files the user supplied directly (ADI MAX30001 datasheet, block-diagram photo). See the third-party notice below.
- **Firmware and build packages**: `ad5940-*`, `avr-check`, `impedance-bench`, `hardware-search`, `dexa-*`, `budget-levels`. Build outputs and archives from earlier passes.
- **`open-source-survey/`**: collected third-party scale and firmware projects that were investigated, each with their licence files where they were present in the source.
- **`open-projects-collection/`**: the collection packaging for those projects.

Archives (`*.tar.xz`, `*.zip`) have matching `.sha256` files where they were created by this project.

## Status (2026-10-18)

- **Literature**: all main papers are checked against full text, abstract, or table. The verification file lists each claim and any inconsistency found in the papers.
- **MAX30001 datasheet**: the BioZ word, tags, rate bit and conversion equation are checked against the official Rev 3 datasheet.
- **Firmware findings**: F31 and F32 are confirmed at the source level against the datasheet. Hardware tests have not been run. F22, F01, F08, F09, F31, F33, F34 and F35 are waiting for approval to run on hardware.
- **Scale and app candidates**: 9 projects have functional test results. Firmware projects are not built, because toolchains were not available.
- **Open decisions**: licence of the ADI-licensed `ad5940lib` files; F20 maintainer question; hardware approvals.

## Third-party material

Some files here are copied from other people's work, for research use. They keep their own licences and copyright. Including them here does not change those terms.

- **Publisher full texts** (`research-pass-6/fulltext/`, HTML, XML, text, PDF, figures): copyright of the publishers and authors. Shown for verification only.
- **ADI MAX30001 datasheet** and block-diagram photo (`uploads/`): copyright Analog Devices. Shown for reference.
- **`ad5940lib/` (copies in several folders)**: ADI licence. Redistribution limited to use with ADI products; not to be combined with other licences. A decision on this is open.
- **OpenView assets** (`deep-impedance-audit/pass5/openitems/ov_assets/`): from `Protocentral/protocentral_openview`; licence not yet checked.
- **UPRM source** (`deep-impedance-audit/pass5/vendor/uprm_spiFunctions.c` and related): no clear licence (GitHub reports NOASSERTION).
- **no-OS MAX30009 driver** (`deep-impedance-audit/pass5/vendor/max30009.*`): BSD-3-Clause.
- **Protocentral MAX30001 Arduino library** (`deep-impedance-audit/pass5/f21/`): MIT.

If you reuse anything from this repository, check the licence of that file first. The licence of the repository's own notes and analysis is not yet set; add a LICENSE file before reuse.

## Privacy

Some upstream projects publish personal body-composition records. None of that data is copied into this repository.

## Reproducing the checks

Each folder names its own tools and versions in its notes. The audit scripts are under `deep-impedance-audit/` and `deep-impedance-audit/pass5/`. Verify uploads against `UPLOAD-MANIFEST.json` at the root.
