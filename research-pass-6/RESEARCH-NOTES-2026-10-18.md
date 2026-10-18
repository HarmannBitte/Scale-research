# Research pass 6 — 2026-10-18

Scope authorised by the user: research items 1 (technical gaps) and 2 (validation evidence). Not done: maintainer contact, hardware checks, presentation. No purchases, no flashing, no human experiments. DIY BIA is research, not a DXA replacement.

## 1. MAX30009 BioZ OSR table (finding F05) — resolved

Source: `analogdevicesinc/no-OS`, `drivers/afe/max30009/max30009.h` (chunks 1–2) and `max30009.c` (chunks 3–4).

- `BIOZ_CONFIGURATION1` (0x20): `DAC_OSR` bits [7:6], `ADC_OSR` bits [5:3].
- `enum max30009_dac_osr`: `_32, _64, _128, _256` → register values 0–3.
- `enum max30009_adc_osr`: `_8, _16, _32, _64, _128, _256, _512, _1024` → register values 0–7.
- `max30009_set_adc_osr()` writes the enum value directly into the masked field, so the enum value **is** the register value. Register value 4 = OSR 128, value 5 = OSR 256, value 7 = OSR 1024.
- `max30009_set_dac_osr()` note: F_BIOZ = PLL_CLK / (KDIV × DAC_OSR).

Consequence for the UPRM code: the register byte 0xA0 gives ADC field = (0xA0 >> 3) & 7 = 4, which is OSR 128. The code's behaviour matches the driver. The stale part is the comment that says "ADC_OSR = 5 (256)". The finding is closed as a comment/documentation error, not a register-decoding error. Confirm against the datasheet OSR table before relying on the absolute sample rate.

Also confirmed from the same driver: FIFO sample format is TAG[23:20] (0x1 = BioZ I, 0x2 = BioZ Q, 0xE = marker, 0xF = invalid), DATA[19:0] signed two's complement. 0xFFFFFF = invalid, 0xFFFFFE = marker. FIFO depth 256 × 3 bytes. PLL range check 14–28 MHz. Reference clock 32.768 kHz or 32.0 kHz.

Not read: chunks 5–8 of `max30009.c` (the rest of the BioZ/lead-off/calibration code). Not needed for the OSR question.

## 2. BIA vs DXA validation evidence (search excerpts, not full-text reviewed)

Identifiers are as returned by the search. Full text has not been checked, so treat the numbers as provisional until verified.

| Population / device | Outcome | Bias (BIA − DXA) | Agreement | Source id |
|---|---|---|---|---|
| Adults, whole body, multi-frequency | %BF | −4.0 ± 2.8% | SEE 2.6%, r 0.932, CCC 0.819 | PMC11649400 |
| Women, IB770 | FM | −0.22 kg | CCC 0.99 | MDPI 25/16/5037 |
| Women, IB770 | FFM | +3.15 kg | CCC 0.91 | MDPI 25/16/5037 |
| Children, single-frequency | — | — | CCC 0.747–0.881 | Nature 41598-023-44217-0 |
| Children, multi-frequency | — | — | CCC 0.912–0.926 | Nature 41598-023-44217-0 |
| Adults, MF-BIA | R² | proportional bias noted | R² 0.72–0.97 | Frontiers 10.3389/frans.2026.1767078 |
| InBody (adults) | FM | −1.2 kg | LOA −5.7 to +3.8 kg | ScienceDirect S2667268526000409 |
| InBody, arms/legs | segmental | — | ICC 0.69–0.76 | ScienceDirect S2667268526000409 |
| Brazilian cohort | FFM / FM | +3.1 kg / −2.9 kg | CCC ≥ 0.93 | PubMed 41567330 |
| COPD patients | FM | 2.7 kg (sign not recorded) | ρc 0.95 | Nature s41598-022-05887-4 |
| Severe obesity | FM | 1.1 kg (sign not recorded) | LOA −6.9 to +9.0 kg | PubMed 42437547 |
| Frail women | whole-body LM / appendicular FM | 2.1 kg / −0.3 kg (sign of LM not recorded) | — | PubMed 23388666 |
| Older adults | ASMM | ~+2.8 kg overestimate | — | Springer s40520-021-02000-z |
| Consistent with 2008 study | %BF | −4.0 ± 2.8% | — | Frontiers 10.3389/fnut.2024.1491931 |
| Leg lean mass | — | no difference | trunk LOA −4.8 to +2.2 kg | Nature s41387-022-00223-1 |
| Commercial scales, children (InBody 520) | %BF | — | rc 0.926 / 0.912; LOA ~±11% | PMC4475745 |
| Six BIA devices | %BF | most favourable −2.21% | LOA −9.88 to +5.46% | JEN article 206 |

Summary for the evidence review:

- Whole-body multi-frequency BIA correlates strongly with DXA at group level (r ≈ 0.93–0.97, CCC ≈ 0.8–0.95).
- It has a systematic bias: body fat percentage about −4%, fat-free mass over by about 2–3 kg, fat mass under by about 2–3 kg. Bias varies with adiposity (proportional bias).
- Individual limits of agreement are wide, roughly ±6–11 kg for fat mass and about ±11% for %BF. A single reading is not a DXA-equivalent measurement.
- Consumer and commercial scales show similar or wider bias than research devices.
- Within-person trends can be more useful than absolute values, but this has not been tested for the UPRM setup.

## 3. Scale / app repositories (collection status)

Not collected this turn. Licence and file counts only, from earlier work:

- `research-pass-3/fitdays-lefu-scale` — MIT, 10 files. **Tests rerun this turn:** 11 passed, 1 skipped (pytest, editable install in a separate venv). The install artefacts (egg-info, `__pycache__`) were removed. Repo is clean.
- `research-pass-5/hume_pod_ha` — BLUE2SCALE licence (source-available), 43 files. Not tested.
- `research-pass-4/ble-scale-sync` — GPL-3.0, 631 files. Not tested (requires Node dependencies, not installed).

Not done: searching for further scale or app repos. Not done: remaining builds beyond the pytest rerun.

## 4. Open items

- Verify the literature numbers against full text before any figure goes into a deliverable.
- Datasheet OSR table: confirm the absolute sample rate per OSR setting.
- Pushing these notes to GitHub needs the user's go-ahead (not pushed).
- The GitHub token pasted in chat should be revoked.

## 5. Expanded search (candidates found, NOT cloned or tested)

Search only: no licence, activity, or protocol review yet. Listed so they can be triaged. Licence exclusion does not apply to research scope.

Scale protocols / apps:
- oliexdev/openScale (wiki documents Xiaomi Mi Scale reverse engineering); YoannDev90/openScale is a fork.
- KristianP26/ble-scale-sync and JohnTheNerd/ble-scale-sync (the second is apparently a fork of the first; the first is already in the collection as ble-scale-sync).
- faraga1/xiaomi-scale-s200-ble — Xiaomi S200, protocol reference, claims no body-composition values exist in its protocol (weight-only).
- Shah-Dom/SmartScale — IF_B2 Web Bluetooth client, includes its own estimates of body composition.
- PavelDemyanov/qn-scale — QN-Scale protocol (Libra, Renpho, FitIndex, Kamtron).
- eayrenk/bioscale-okok-alternative — Chipsea/OKOK BIA formulas (Janssen 2000, Kyle 2004 cited).
- etlami/opentara — Xiaomi/Huami body-metric formulas (claims to match Zepp Life).
- uniextra/Yunmai-dashboard — Yunmai BLE protocol.
- ronnnnnnnnnnnnn/renpho-escs20m (and iios-co fork) — Renpho ES-CS20M, body-fat algorithm 0x03/0x04 described.
- robzarry/healthtrack — RENPHO Elis 1 logger on ESP32, protocol notes in docs/protocol.md.
- ipanalytics/Xiaomi-Scale-Unlocked-Reverse-Engineering — BLE advertisement layouts, offline decoder.
- lswiderski/MiScaleBodyComposition (C#), lolouk44/xiaomi_mi_scale (Python, MQTT), zibous/ha-miscale2, zibous/hc_scale, dkuku/bodymiscale, dkuku/bodymeasurements (tape-measure model, no impedance).
- jpfranca-br/miscale-dashboard; LookHin/xiaomi-mi-body-composition-scale-2.
- Pasynkov "BodyScan" write-up (GARLYN IF_B8B protocol, DEV Community article).

Open BIA hardware / firmware:
- dyarleniber/AD5933-arduino-bioimpedance — AD5933 BIA, FM/FFM/TBW equations on Arduino, 50 kHz & 100 kHz; has a paper PDF.
- openebi/hardware and openebi/software — four-electrode AD5933 EBI spectrometer, few kHz to 100 kHz.
- syoo15/AD5933_ARDUINO_Biomass — MATLAB + Arduino AD5933 calibration and sweep.
- mjmeli/arduino-ad5933, justiceamoh/autoimpedance, ashtonchase/ad5933_analyzer — AD5933 libraries / instruments.
- analogdevicesinc/MAX32655_MAX30009 — official MAX30009 example on MAX32655. Its register writes match the no-OS driver (see section 1). Its comment gives ADC 222 Sps and DAC 14.208 kHz at ADC field 4, DAC field 3, consistent with the decoding in section 1.
- oscaroflores/UPRM-Multi_Frq-BioZ-Research — UPRM project. Already in the collection; the upstream MAX32655_MAX30009 repo is the reference.

Datasheet note: an application-note table lists BIOZ_DAC_OSR as [2:0] (values 32–256), but the no-OS driver uses a 2-bit field. Check the datasheet before using the table.

## 6. Still open
- Clone and triage the top candidates (openScale, xiaomi-scale-s200-ble, renpho-escs20m, AD5933-arduino-bioimpedance, openebi).
- Build or test any candidate that is actually relevant.
- Verify the literature numbers in section 2 against full text.

## 7. Triage of top candidates (2026-10-18)

Shallow clones (depth 1) in a scratch area, not in the research tree. Test runs used throwaway venvs with each repo's pinned requirements. Nothing was changed in the cloned repos (git status clean).

| Repo | Licence | Last commit | Tracked files | Tests run | Result |
|---|---|---|---|---|---|
| oliexdev/openScale | GPL-3.0 | 2026-10-17 | 632 | not run (Android/Gradle) | candidate for protocol reference |
| faraga1/xiaomi-scale-s200-ble | MIT | 2026-10-14 | 10 | `test_scale_reader.py` | 35 passed (after pinned deps) |
| ronnnnnnnnnnnnn/renpho-escs20m | MIT | 2026-10-11 | 35 | full suite | 413 passed (needs `pytest-asyncio`, declared in pyproject) |
| ipanalytics/Xiaomi-Scale-Unlocked-Reverse-Engineering | MIT | 2026-09-23 | 17 | `unittest discover` | 15 passed |
| eayrenk/bioscale-okok-alternative | MIT | 2026-10-11 | 188 | full suite | 4 passed, 1 failed: `test_classifications` calls `get_classifications()` without the required `height_cm` argument (test or API mismatch; not diagnosed further) |
| dyarleniber/AD5933-arduino-bioimpedance | GPL-3.0 | 2020-05-14 | 4 | none (Arduino sketch) | not built; needs Arduino toolchain and hardware |
| openebi/software | licence file present (2013) | 2013-03-22 | 13 | none (AVR firmware) | not built; needs AVR toolchain and hardware |
| openebi/hardware | none found | 2016-07-21 | 11 | none (schematics/layout) | reference only |
| KristianP26/ble-scale-sync | GPL-3.0 | 2026-10-13 | 631 | not run this turn | already in the collection (research-pass-4) |

Notes:
- The Renpho failure seen before the `pytest-asyncio` install was an environment problem (missing plugin), not a code fault.
- The S200 failure seen before the install was a missing dependency (`cryptography`), not a code fault.
- The OKOK failure is in the repo's own test code or API, so it is a finding to record, not an environment issue.
- Not built: the AD5933 and openebi firmware. Building them needs toolchains and hardware. Hardware checks are outside the authorised scope.
- openScale was not built. It is an Android app and would need the Gradle toolchain.

## 8. Still open after triage (updated 2026-10-18)

Status of every item listed in sections 6 and 8 at the end of this pass:

- Literature checks: the main papers in section 10 are now checked against full text, full abstract or table (section 13). Read: JEN article 206 (full PDF, 2026 retry, section 14). Not read: Sillanpää 2014 (abstract confirmed; LoA from snippet; a conflicting snippet is unresolved, see section 13); the Greek 8-point MF-BIA snippet and the Frontiers fnut.2025.1499752 and MDPI nutrients 10/6/738 snippets (unverified). Hjort 2026 text and table disagree on limits of agreement; the table is used.
- Datasheet OSR table: confirm the absolute sample rate per OSR setting.
- Pushing these notes to GitHub needs the user's go-ahead (not pushed).
- The GitHub token pasted in chat should be revoked.

## 5. Expanded search (candidates found, NOT cloned or tested)

Search only: no licence, activity, or protocol review yet. Listed so they can be triaged. Licence exclusion does not apply to research scope.

Scale protocols / apps:
- oliexdev/openScale (wiki documents Xiaomi Mi Scale reverse engineering); YoannDev90/openScale is a fork.
- KristianP26/ble-scale-sync and JohnTheNerd/ble-scale-sync (the second is apparently a fork of the first; the first is already in the collection as ble-scale-sync).
- faraga1/xiaomi-scale-s200-ble — Xiaomi S200, protocol reference, claims no body-composition values exist in its protocol (weight-only).
- Shah-Dom/SmartScale — IF_B2 Web Bluetooth client, includes its own estimates of body composition.
- PavelDemyanov/qn-scale — QN-Scale protocol (Libra, Renpho, FitIndex, Kamtron).
- eayrenk/bioscale-okok-alternative — Chipsea/OKOK BIA formulas (Janssen 2000, Kyle 2004 cited).
- etlami/opentara — Xiaomi/Huami body-metric formulas (claims to match Zepp Life).
- uniextra/Yunmai-dashboard — Yunmai BLE protocol.
- ronnnnnnnnnnnnn/renpho-escs20m (and iios-co fork) — Renpho ES-CS20M, body-fat algorithm 0x03/0x04 described.
- robzarry/healthtrack — RENPHO Elis 1 logger on ESP32, protocol notes in docs/protocol.md.
- ipanalytics/Xiaomi-Scale-Unlocked-Reverse-Engineering — BLE advertisement layouts, offline decoder.
- lswiderski/MiScaleBodyComposition (C#), lolouk44/xiaomi_mi_scale (Python, MQTT), zibous/ha-miscale2, zibous/hc_scale, dkuku/bodymiscale, dkuku/bodymeasurements (tape-measure model, no impedance).
- jpfranca-br/miscale-dashboard; LookHin/xiaomi-mi-body-composition-scale-2.
- Pasynkov "BodyScan" write-up (GARLYN IF_B8B protocol, DEV Community article).

Open BIA hardware / firmware:
- dyarleniber/AD5933-arduino-bioimpedance — AD5933 BIA, FM/FFM/TBW equations on Arduino, 50 kHz & 100 kHz; has a paper PDF.
- openebi/hardware and openebi/software — four-electrode AD5933 EBI spectrometer, few kHz to 100 kHz.
- syoo15/AD5933_ARDUINO_Biomass — MATLAB + Arduino AD5933 calibration and sweep.
- mjmeli/arduino-ad5933, justiceamoh/autoimpedance, ashtonchase/ad5933_analyzer — AD5933 libraries / instruments.
- analogdevicesinc/MAX32655_MAX30009 — official MAX30009 example on MAX32655. Its register writes match the no-OS driver (see section 1). Its comment gives ADC 222 Sps and DAC 14.208 kHz at ADC field 4, DAC field 3, consistent with the decoding in section 1.
- oscaroflores/UPRM-Multi_Frq-BioZ-Research — UPRM project. Already in the collection; the upstream MAX32655_MAX30009 repo is the reference.

Datasheet note: an application-note table lists BIOZ_DAC_OSR as [2:0] (values 32–256), but the no-OS driver uses a 2-bit field. Check the datasheet before using the table.

## 6. Still open
- Clone and triage the top candidates (openScale, xiaomi-scale-s200-ble, renpho-escs20m, AD5933-arduino-bioimpedance, openebi).
- Build or test any candidate that is actually relevant.
- Verify the literature numbers in section 2 against full text.

## 7. Triage of top candidates (2026-10-18)

Shallow clones (depth 1) in a scratch area, not in the research tree. Test runs used throwaway venvs with each repo's pinned requirements. Nothing was changed in the cloned repos (git status clean).

| Repo | Licence | Last commit | Tracked files | Tests run | Result |
|---|---|---|---|---|---|
| oliexdev/openScale | GPL-3.0 | 2026-10-17 | 632 | not run (Android/Gradle) | candidate for protocol reference |
| faraga1/xiaomi-scale-s200-ble | MIT | 2026-10-14 | 10 | `test_scale_reader.py` | 35 passed (after pinned deps) |
| ronnnnnnnnnnnnn/renpho-escs20m | MIT | 2026-10-11 | 35 | full suite | 413 passed (needs `pytest-asyncio`, declared in pyproject) |
| ipanalytics/Xiaomi-Scale-Unlocked-Reverse-Engineering | MIT | 2026-09-23 | 17 | `unittest discover` | 15 passed |
| eayrenk/bioscale-okok-alternative | MIT | 2026-10-11 | 188 | full suite | 4 passed, 1 failed: `test_classifications` calls `get_classifications()` without the required `height_cm` argument (test or API mismatch; not diagnosed further) |
| dyarleniber/AD5933-arduino-bioimpedance | GPL-3.0 | 2020-05-14 | 4 | none (Arduino sketch) | not built; needs Arduino toolchain and hardware |
| openebi/software | licence file present (2013) | 2013-03-22 | 13 | none (AVR firmware) | not built; needs AVR toolchain and hardware |
| openebi/hardware | none found | 2016-07-21 | 11 | none (schematics/layout) | reference only |
| KristianP26/ble-scale-sync | GPL-3.0 | 2026-10-13 | 631 | not run this turn | already in the collection (research-pass-4) |

Notes:
- The Renpho failure seen before the `pytest-asyncio` install was an environment problem (missing plugin), not a code fault.
- The S200 failure seen before the install was a missing dependency (`cryptography`), not a code fault.
- The OKOK failure is in the repo's own test code or API, so it is a finding to record, not an environment issue.
- Not built: the AD5933 and openebi firmware. Building them needs toolchains and hardware. Hardware checks are outside the authorised scope.
- openScale was not built. It is an Android app and would need the Gradle toolchain.

## 8. Still open after triage (updated 2026-10-18)

Status of every item listed in sections 6 and 8 at the end of this pass:

- Literature full-text checks: 11 of 18 papers verified in full text (see `fulltext/LITERATURE-FULLTEXT-VERIFICATION.md`). Still abstract-level: Campos 2026, Springer s40520, MDPI Sensors 5037, ScienceDirect S2667268526000409 (not fetched), Eur J Clin Nutr 2013, JEN article 206.
- Datasheet OSR table (section 1): resolved from vendor header; the MAX30009 datasheet PDF itself was not retrieved.
- Expanded candidate triage: metadata for 18 repos (`deep-impedance-audit/pass5/openitems/meta_*.json`) and functional runs for the repos in section 12. Not built: all Arduino, STM32 and MAX32655 firmware, and the lswiderski C# suite (no dotnet).
- OKOK test bug: diagnosed; patch in `okok-test-fix.patch`, verified in a scratch copy only. Not applied upstream (no maintainer contact without authorisation).
- Yunmai demo/app formula mismatch (section 12): recorded as a finding; not reported upstream.
- Upload: local commits `2686199`, `e1b7c16`, `eabde99`, `df7d776` are not pushed. Pushing needs a fresh token from the user.
- Licence decision on the ADI-licensed `ad5940lib` files in the public repo: pending user decision.
- Hardware checks (F22, F01, F08, F09, F31, F33, F34, F35) and the F20 maintainer question: need explicit approval. Not started.
- OpenView `assets/` re-collection and the official MAX30001 PDF retry: not done.

## 9. Further investigation (2026-10-18)

### 9a. OKOK test failure: diagnosed, test bug
- `tests/test_calculations.py::test_classifications` calls `get_classifications(metrics, 'M', 35)`, which omits `height_cm`.
- `calculations/body_composition.py:401` requires `height_cm`. Every app caller passes it (`dashboard/layouts/composition_view.py:78`, `comparison_view.py:119,127`, and `body_composition.py:628`).
- With `height_cm=175` supplied, the result is correct: BMI 26.1 → "Sobrepeso", which is what the test asserts.
- Classification: test defect, not a calculation defect. Fix: pass `175` as the fourth argument in the test. Repo not modified (scratch clone).

### 9b. MAX30009 OSR table: confirmed against the datasheet (Analog Devices MAX30009 datasheet, Electrical Characteristics examples)
The datasheet gives the example settings below. All relations are reproduced exactly with the values in the table:

| Relation | Formula | Check |
|---|---|---|
| F_BIOZ | PLL_CLK / (KDIV × BIOZ_DAC_OSR) | 16.384 MHz/(64×256) = 1000 Hz (1 kHz example); 25.591808 MHz/(2×256) = 49.984 kHz (50 kHz example); 25.591808 MHz/(2×128) = 99.968 kHz (100 kHz example) |
| SR_BIOZ | PLL_CLK / (NDIV × BIOZ_ADC_OSR) | 16.384 MHz/(512×512) = 62.5 sps; 25.591808 MHz/(1024×512) = 48.8125 sps; 25.591808 MHz/(1024×256) = 97.625 sps (ICG example); 15.990784 MHz/(512×512) = 61 sps (250 kHz example) |

- The datasheet examples write OSRs as decimal values (DAC 256, ADC 512 and so on). The driver's enum values map to these via the register field (section 1). The OSR values used in the examples are consistent with the driver's enum mapping.
- So the sample-rate formula is now confirmed from two independent sources: the datasheet examples and the no-OS driver's register layout.
- Remaining small discrepancy: the application-note table lists DAC_OSR as 3 bits, but the driver uses a 2-bit field. Note this in the design doc.

### 9c. Literature spot check: PMC11649400 (= Front Nutr 2024, 10.3389/fnut.2024.1491931)
- Verified from the abstract: Looney et al., InBody 770 MF-BIA vs DXA, **n = 14 healthy military-age adults**, duplicate tests across 5 visits over 3 weeks.
- Verified bias: %BF −4.0 ± 2.8% (SEE 2.6%); fat-free mass +2.8 ± 2.1 kg (SEE 2.2 kg); fat mass −2.9 ± 2.0 kg (SEE 1.9 kg).
- Not in the abstract, so unverified: "r 0.932" and "CCC 0.819" (from the earlier search excerpt).
- **Correction to section 2:** the two rows "PMC11649400" and "Frontiers 10.3389/fnut.2024.1491931" are the same paper. The duplicate row has been treated as one source, and the numbers in section 2 are unchanged.
- Caveat for the evidence summary: this is a very small sample of one device. The authors cite a previously reported ~3% body-fat offset, and Potter et al. (US Marine Corps) used a +3% correction. Neither should be generalised to home scales without a validation.

### 9d. Still open
- Verify the remaining literature rows (Nature 41598-023-44217-0, MDPI 25/16/5037, ScienceDirect S2667268526000409, PubMed 41567330, others) against full text.
- Decide whether to add the OKOK test fix. This is a change to someone else's repo, so it's a note only, not a push, unless the user says otherwise.

## 10. Literature verification status (2026-10-18)

Method: abstracts fetched from the publisher or PubMed/PMC pages, or search snippets where the page would not load. "Verified" means the figure appears in the abstract. Full texts were not read.

| # | Source (as cited) | Status | What the source actually says | Changes to section 2 |
|---|---|---|---|---|
| 1 | PMC11649400 = Front Nutr 2024, 10.3389/fnut.2024.1491931 (Looney et al.; InBody 770, n = 14 adults) | Verified bias. r and CCC not in abstract | %BF bias −4.0 ± 2.8% (SEE 2.6%); FFM bias +2.8 ± 2.1 kg (SEE 2.2); FM bias −2.9 ± 2.0 kg (SEE 1.9). Very small sample | Rows "PMC11649400" and "Frontiers …1491931" are the same paper. r/CCC are unverified |
| 2 | Nature s41598-023-44217-0 (children 10–14 y, n = 443, single-frequency BIA) | Verified | r 0.853–1.000. ICC and CCC 0.902–0.972 for FM, FFM and LBM. BIA underestimates %BF (−8.9 to −0.8%), LBM (−3.5 to −1.8%) and body mass; overestimates BMC (62.7–66.5%). Fixed and proportional bias in all indicators. Poor agreement for FM and %BF in the lowest BMI quartile. Authors say BIA is sufficient for within-person longitudinal use | **Correction:** the earlier CCC values (0.747–0.881 single-frequency; 0.912–0.926 multi-frequency) are not supported by this abstract. Removed. Use 0.902–0.972 |
| 3 | MDPI 25/16/5037 is actually Sensors 2025, 25(16), 5037 (women, InBody 770, DXA reference) | Verified (search snippet) | FM MD −0.22 kg (CCC 0.99); FFM MD +3.15 kg (CCC 0.91). Authors caution about higher FM error in women with higher body fat. Study is a 4C-model validation with n ≈ 55 | **Correction:** journal is *Sensors*, not *Nutrients* |
| 4 | Frontiers 10.3389/frans.2026.1767078 (Front Anal Sci 2026; InBody 970S, n = 148 adults 20–45, Malaysia) | Verified R² range. "Proportional bias" not in abstract | R² 0.72–0.97; BFM R² 0.96; FFM R² 0.97. Sensitivity for sarcopenia 95.1%, obesity 75.2%. "Acceptable limits of agreement" | Device is InBody 970S (not generic). Proportional-bias claim unverified |
| 5 | ScienceDirect S2667268526000409 (Hjort et al., Clin Nutr Open Sci 2026; InBody BIA vs DXA, n = 316, Trøndelag) | Partly verified | ICC ≥ 0.97 for total FM and FFM. ICC 0.69 for arm FM and 0.76 for leg FM. Lower agreement for FM with rising BMI | FM bias −1.2 kg and LOA −5.7 to +3.8 kg are **not** in the abstract; treat as unverified |
| 6 | PubMed 41567330 (Brazilian cohort, FFM +3.1 kg, FM −2.9 kg, CCC ≥ 0.93) | **Not verified** | Page returned HTTP 500 | Keep as unverified |
| 7 | Nature s41598-022-05887-4 (Veterans with COPD, n = 50, 96% male, handheld Omron HBF-306C) | Verified | FM ρ 0.94, ρc 0.95 (95% CI 0.93–0.98); mean difference BIA vs DXA 2.7 ± 3.2 kg (direction not stated). %fat ρc 0.67 and FFM ρc 0.74 (moderate). Stronger correlations in obese participants | Device is a handheld, not a multi-frequency scale. Direction of the 2.7 kg bias is not stated |
| 8 | PubMed 42437547 (Campos et al. 2026; severe obesity, n = 49, MF-BIA vs DXA) | Verified | FM bias 1.1 kg (LoA −6.9 to +9.0); FFM bias −0.22 kg (LoA −6.6 to +6.2). Verdich equation underestimates FFM by 2.9 kg. Raw impedance predicts FFM well (R² > 0.70) but FM poorly (R² < 0.25) without body mass | Direction of FM bias is not explicitly stated in the abstract |
| 9 | PubMed 23388666 (frail Japanese women, n = 129, SMF-BIA vs DXA) | Verified | Bias = DXA minus BIA. Whole-body FM bias −1.2 kg (BIA overestimates FM). Whole-body LM bias +2.1 kg (BIA underestimates LM). Appendicular FM bias −0.3 kg. Appendicular LM bias +1.5 kg. R² 0.94 (FM) and 0.85 (LM) | Sign convention: DXA minus BIA |
| 10 | Springer s40520-021-02000-z (Aging Clin Exp Res 2022; n = 73, 55–85 y; ASMM via BIA equation) | Verified | ASMM 21.61 vs 18.82 kg (BIA over by ~2.8 kg); FFM 49.57 vs 46.22 kg (over by ~3.3 kg); FM 24.59 vs 27.13 kg (under by ~2.5 kg). All p < 0.001. Wide limits of agreement | Matches section 2 |
| 11 | Nature s41387-022-00223-1 (Nutr Diabetes 2022; older adults with T2DM, n = 84, InBody 770) | Partly verified | Leg lean mass 14.76 vs 15.19 kg, no difference (p = 0.353). ASMI 7.43 vs 7.47 kg/m², ICC 0.965, no difference | Trunk LOA −4.8 to +2.2 kg is **not** in the abstract; treat as unverified |
| 12 | PMC4475745 = Biomed Res Int 2015 (Wang & Hui; 255 children 9–19 y; four BIA scales vs DXA) | Verified, and **conflicts with earlier notes** | Biodynamics-310, Tanita 543 and Tanita 545: poor CCC agreement for %BF. InBody 520: moderate agreement. Biodynamics-310 showed no significant %BF difference from DXA in boys. | **Correction:** the earlier figures (InBody 520 rc 0.926/0.912; LOA ±11%) are **not** in this paper. Remove them or find their source |
| 13 | JEN article 206 (six BIA devices, most favourable bias −2.21%) | Not checked | — | Keep as unverified |
| 14 | Frontiers fnut.2024.1491931 | Duplicate of row 1 | — | — |

New sources found during verification (not yet read):
- Nature s41430-025-01664-4 (2025): InBody 770 vs DXA in 1,000 healthy adults (667 men, 333 women), including FM, %BF, FFM and VAT. Large sample. Search snippet only.
- PMC9813632 (2022): standing BIA (InBody 770) vs DXA, with a systematic offset in %BF. Search table shows %BF bias −3.4 (all), FFM bias −2.7 kg. A correction equation is also reported. Search snippet only.

### Net effect on the evidence summary (section 2)
- Still robust: consumer and research multi-frequency BIA shows a systematic bias against DXA, typically %BF about −3 to −4%, FFM over by 2–3 kg, and FM under by about 2–3 kg. This pattern appears across verified sources (rows 1, 3, 8, 9, 10).
- Wide individual limits of agreement are confirmed (rows 8, 10).
- Agreement is worse in obesity, in leaner people, in women with higher body fat, and in children (rows 2, 3, 5).
- Within-person tracking is supported by the children's study (row 2), but only as a claim from the authors.
- Several sample sizes are small (n = 14, 49, 50, 73, 84, 129). No single study is strong enough to set a threshold or to support clinical decisions.

### Still open
- Read the full texts of the two new large-sample sources (rows in "New sources") before using them.
- Resolve the PMC4475745 conflict: find the source of the InBody 520 numbers, or drop them.
- Retry PubMed 41567330 and check JEN article 206.

## 11. Final verification pass (2026-10-18)

Every row in section 10 was re-checked. The status below replaces section 10 where they differ.

### Confirmed by the source text
- **PubMed 41567330** (Wahrlich et al., 2026; Brazilian adults and older adults, n = 945, Tanita BC-418 vs DXA): r = 0.97 for FFM and FM; CCC ≥ 0.93; BIA overestimated FFM by 3.1 kg (+7.2%) and underestimated FM by 2.9 kg (−13.0%). Calibration equation published. Previously unverified; now verified.
- **Nature s41430-025-01664-4** (Eur J Clin Nutr; 1,000 adults, InBody 770 vs DXA in uncontrolled conditions): FM bias men −3.7 ± 2.6 kg (r = 0.93), women −1.9 ± 1.8 kg (r = 0.96); %BF bias men −4.2 ± 3.0%, women −2.8 ± 2.6%; FFM bias men +3.4 ± 2.8 kg, women +2.0 ± 2.2 kg. Trunk FM CCC 0.86 (men) and 0.93 (women); VAT poor (CCC 0.68 and 0.34). Reliability ICC 0.987–0.998. This is the largest study in the set.
- **PMC9813632** (Potter et al., BMJ Nutr Prev Health 2022; standing BIA, InBody 770 and a second device, vs DXA): FFM MAE 2.8 and 3.1 kg; %BF MAE 3.4% and 3.9%. The InBody 770 %BF bias is −3.4% overall. The authors also give a correction equation (%BF = 0.8502 × InBody %BF + 6.951). Source is the search snippet of the paper's tables.
- **Hjort et al. 2026** (ScienceDirect S2667268526000409; n = 316): full results table. Mean difference DXA − BIA: FM 1.21 kg (LoA −3.35 to +5.76), FFM −1.28 kg (LoA −6.04 to +3.48), FM arms −1.23 kg (BIA overestimates arm FM by 1.2 kg, LoA −3.77 to +1.31). ICCs: FM 0.97, FFM 0.97, arms FM 0.69, legs FM 0.76.
- **JEN article 206** (Agreement between six BIA devices and DXA; n = 42 men, 35 women): most favourable device (Omron) had %BF mean bias −2.21% with LoA −9.88% to +5.46%. Tanita +3.18% and Renpho +2.38% (moderate positive biases). Reliability ICC 0.66–0.73 for four devices and 0.25–0.43 for two.
- **PMC4475745** (Wang & Hui 2015; children, n = 255): InBody 520 %BF rc = 0.926 (boys) and 0.912 (girls). The earlier rc numbers were correct; they are in the Results text, not the abstract. The "LoA ±11%" figure in my notes was wrong: the range −10.96 to +12.12% in the paper's table belongs to Biodynamics-310 (Model A), not InBody 520. InBody 520 LoA for %BF was not seen.
- **Sillanpää et al. 2014** (Obesity; 18–88 y, multi-frequency BIA vs DXA; new source, from search snippet): BIA FM 3.1 kg lower in women and 2.6 kg lower in men; LM 2.9 kg higher (women) and 1.6 kg higher (men), i.e. BIA overestimates lean mass (corrected in section 13). Authors conclude BIA is not reliable at the individual level (LoA wide; men −17% to +21% FM).
- **Springer s40520-021-02000-z**, **PubMed 42437547**, **PubMed 23388666**, **Nature s41598-022-05887-4**, **Nature s41598-023-44217-0**, **MDPI 25/16/5037 (Sensors)**, **PMC11649400**: confirmed as in section 10.

### Corrections made in this pass
1. **Hjort 2026 limits of agreement.** My notes said FM LoA −5.7 to +3.8 kg. The paper gives −3.35 to +5.76 kg. Also, the difference is DXA − BIA, so the 1.2 kg is BIA underestimating FM.
2. **InBody 520 LoA.** My notes said ±11% for InBody 520. The ±11% belongs to a different device (Biodynamics-310). Removed.
3. **Frontiers 2026 (Malaysian adults, InBody 970S).** The "proportional bias noted" claim is **not in the source**. Removed.
4. **Nature s41387-022-00223-1 (T2DM).** The trunk limits of agreement (−4.8 to +2.2 kg) are **not confirmed** from the abstract, and I did not read the full text. Removed. The leg lean-mass result (no difference, p = 0.353) and ASMI (ICC 0.965) are verified.

### Still unverified (kept as "not stated" rather than guessed)
- Direction of the COPD study's 2.7 kg difference (not stated in the abstract).
- Direction of the severe-obesity study's FM bias of 1.1 kg (not stated in the abstract).

### Final evidence summary (verified only)
- Multi-frequency BIA shows a systematic bias against DXA in adults that is consistent across devices and studies:
  - %BF about −2 to −4%, most consistently −3 to −4% (rows: Looney 2024, Potter 2022, Brazil 2026, uncontrolled InBody 770 study, Sensors 2025 for women).
  - FFM over by about 2–3.5 kg.
  - FM under by about 1–3 kg, but some studies find near-zero bias (Hjort 2026, FM +1.2 kg in DXA − BIA sign convention).
- Individual limits of agreement are wide (about ±6 to ±11 kg for fat mass; about ±10 percentage points for %BF). Sillanpää 2014 concludes BIA is not reliable for individuals.
- Agreement is worse in obesity (fat mass), in children and in women with higher body fat.
- Within-person tracking is supported by the children's study only, and that is the authors' view.
- Sample sizes range from 14 to 1,000. Only the large uncontrolled study (n = 1,000) and the Brazilian study (n = 945) are big enough to be stable.

### Limits
- Abstracts and table snippets only. Full texts were not read in this pass.
- Search snippets are not the same as the paper. Where a figure came from a snippet, the source is named above.
- None of these studies tests a home scale against DXA. The evidence supports a systematic bias, not a usable correction for a home device.

## 12. Functional triage of expanded candidates (2026-10-18)

Shallow clones (depth 1) in `/home/user/.cache/open-projects/triage2/`. Each suite ran in its own venv. Nothing in the clones was changed. Licence restrictions were not used to exclude any candidate (research scope only).

| Repo | Licence (GitHub) | Last push | Runnable test suite | Result |
|---|---|---|---|---|
| dckiller51/bodymiscale | Apache-2.0 | 2026-10-15 | pytest, Home Assistant custom component, Python 3.14 | 372 passed |
| dkuku/bodymiscale | Apache-2.0 | 2026-10-04 | pytest, same harness | 355 passed |
| dkuku/bodymeasurements | Apache-2.0 | 2026-10-07 | pytest, Home Assistant 2026.3+ | 18 passed |
| uniextra/Yunmai-dashboard | MIT | 2026-10-13 | pytest, FastAPI | 27 passed, 6 failed (see below) |
| zibous/hc_scale | NOASSERTION | 2026-10-05 | `testcases/test_calcdata.py` (a script) | Cannot run: the `lib/` package it imports is not in the repo |
| zibous/ha-miscale2 | MIT | 2023-09-25 | `tests/` contains scripts, not a pytest suite | `tests/calc_body_Metrics.py` runs (exit 0). 47 Python files compile |
| lolouk44/xiaomi_mi_scale | MIT | 2024-05-18 | none | Smoke run of `bodyMetrics` (see below) |
| PavelDemyanov/qn-scale | MIT | 2026-09-05 | none | 6 Python files compile |
| Shah-Dom/SmartScale | MIT | 2026-09-27 | none | 4 files, no Python; not run |
| lswiderski/MiScaleBodyComposition | Apache-2.0 | 2025-07-16 | C# xUnit suite | Not run (no dotnet in sandbox) |
| etlami/opentara | GPL-3.0 | 2026-09-29 | none found | Not run |
| analogdevicesinc/MAX32655_MAX30009 | NOASSERTION | 2023-09-20 | none | Not built (needs ARM toolchain) |
| oscaroflores/UPRM-Multi_Frq-BioZ-Research | NOASSERTION | 2026-09-28 | none | Not built (MCU Makefile). Its `selected/` copy is already in the collection |
| kasonhaimen/AD5933_STM32_Platform | none | 2023-06-24 | none | Not built (needs ARM toolchain) |
| justiceamoh/autoimpedance | none | 2013-09-10 | none | Not built (Arduino sketch) |
| mjmeli/arduino-ad5933 | MIT | 2023-01-29 | example sketch only | Not built (needs arduino-cli) |
| ashtonchase/ad5933_analyzer | MIT | 2017-09-06 | none | Not run |
| syoo15/AD5933_ARDUINO_Biomass | none | 2017-04-08 | none | Not built (Arduino sketch) |
| robzarry/healthtrack | — | — | — | Not found on GitHub |

### 12a. Yunmai dashboard (uniextra): details
- Run with `YUNMAI_DB` pointing to a temp file. The default `/data/yunmai.db` is not writable in the sandbox.
- 6 failures, with three causes:
  1. `test_analysis.py`, 4 tests: `'TestClient' object is not callable`. Looks like a test-side API mismatch against the pinned FastAPI 0.115.12 / Starlette 0.46.2. Not diagnosed further.
  2. `test_demo.py::test_build_demo`: the build script expects `<title>Mi Scale Dashboard</title>` in `index.html`, and the title has changed. Build-script drift.
  3. `test_demo.py::test_body_js_matches_body_py`: **real divergence.** The app (`app/body.py`, visceral fat from body fat %) and the demo (`demo/body.js`, visceral fat from height and weight) use different formulas. Example: a 45.2 kg input gives 7.7 in one and 14.6 in the other. The demo does not match the app's visceral-fat output.

### 12b. Xiaomi formula smoke test (lolouk44)
- `bodyMetrics(72.0, 175, 30, 'male', 500)`: fat 20.6%, BMR 1555, visceral 10.7, BMI 23.5, muscle 54.3 kg.
- `bodyMetrics(60.0, 165, 45, 'female', 600)`: fat 32.8%, BMR 1133, visceral 1, BMI 22.0, muscle 37.9 kg.
- `bodyMetrics(72.0, 175, 30, 'male', 0)`: **no error.** Returns fat 15.9% and muscle 57.5 kg, both looking valid. The impedance-0 case is not guarded. This is a silent-failure risk for any user whose scale reports no impedance.
- No reference values were available to compare against, so these are plausibility checks only.

### 12c. Privacy note (zibous/hc_scale)
- The upstream repo commits `data/miscale-Peter.json`, `data/miscale-Reni.json` and per-person monthly CSV histories (`data/history/peter/`, `data/history/reni/`). These are named personal body-composition records. Nothing from them was copied into the research repo, and they must not be uploaded anywhere public.

### 12d. What this triage does not show
- Test passes show the upstream suites are internally consistent. They do not show that any formula matches DXA or that any firmware reads a real scale correctly.
- Not built: all firmware. Hardware-level checks remain blocked pending approval.

## 13. Round 2 continuation (2026-10-18)

- Abstract-only papers re-read from publisher and PubMed pages: Springer s40520, Sensors 25/16/5037, PubMed 42437547 (Campos), PubMed 23388666 (2013), ScienceDirect S2667268526000409 (table). All confirmed. Details and the Hjort text/table inconsistency: `fulltext/LITERATURE-FULLTEXT-VERIFICATION.md`.
- Sensors 25/16/5037 is a study of **55 young women (mean age 21.1)**. Earlier notes called it a general sample; that was wrong.
- Official MAX30001 datasheet PDF (analog.com): fetch failed again. Still mirror-only.
- OpenView `assets/`: 13 files re-collected from `Protocentral/protocentral_openview` at HEAD (about 1.9 MB). Manifest with SHA-256: `deep-impedance-audit/pass5/openitems/ov_assets_manifest.json`. Files are in `pass5/openitems/ov_assets/`. The upstream tree gives no size field, so only download success was checked, not sizes.
- JEN article 206: not reachable from the sandbox (DNS failure).
- Sillanpää 2014 (PubMed 23894111): abstract confirmed. **Sign correction:** BIA overestimated lean mass (+2.9 kg women, +1.6 kg men), not underestimated. A second snippet with the opposite FM sign is unresolved. Details in the verification file.

## 14. Retry of the two unreachable sources (2026-10-18)

- **JEN article 206:** reachable through the journal site on retry. Full PDF read. Per-device results in `fulltext/LITERATURE-FULLTEXT-VERIFICATION.md`. The paper's Conclusions ("Omron had the highest LoA") contradict its Results (Triomph widest). Results used.
- **MAX30001 datasheet PDF:** still not retrieved. Product page reached. Direct PDF fetch fails over HTTP/2 (INTERNAL_ERROR) and times out over HTTP/1.1. Mirror remains the source.

### 14b. MAX30001 datasheet: further attempts (2026-10-18)

Still not retrieved in full. Tried and failed:
- `analog.com/media/en/technical-documentation/data-sheets/max30001.pdf` (fetch tool, curl HTTP/2 and HTTP/1.1): fetch error; curl HTTP/2 INTERNAL_ERROR; HTTP/1.1 timeout.
- `analog.com/.../MAX30001.pdf` (capitalised), `analog.com/en/_/media/...`: no response.
- `datasheets.maximintegrated.com/en/ds/MAX30001.pdf` and lowercase variant: 301 redirect loop or timeout; fetch tool error.
- `maximintegrated.com/.../max30001.html`: HTTP 500 via fetch tool.
- Mouser `pdfdocs/MAX30001.pdf` and `datasheet/2/256/MAX30001-1154814.pdf`: fetch tool error. The 1154814 link is listed by search as Rev 1 (2017), so it is not the target revision anyway.
- DigiKey: Cloudflare challenge.

What does work: `web_search` indexes the Rev 3 PDF (19-100133, Rev 3, 1/23). Search returns excerpts for targeted queries. Excerpts checked so far match the alldatasheet mirror: BTAG table (000 valid, 001 over/under range, 010 valid EOF, 011 over/under EOF, 110 empty, 111 overflow). Use search excerpts for targeted checks; do not treat them as a full read.

## 15. Official MAX30001 datasheet read (user upload, 2026-10-18)

Source: `/home/user/uploads/max30001.pdf` (19-100133, Rev 3, 1/23; 88 pages). Text extracted to `fulltext/max30001_official_rev3.txt` (page separators `=====PAGE=====`). Block diagram supplied as `/home/user/uploads/photo_2026-10-18_13-48-55.jpg`.

Checked against the official text:
- **BioZ FIFO** (p67): 8 words x 24 bits. Data is a 20-bit left-justified two's-complement value. One bit is fixed at 0, and the remaining three bits hold the tag. Matches the mirror.
- **BTAG table 50** (p67–68): 000 valid, 001 over/under range, 010 valid EOF, 011 over/under EOF, 110 empty, 111 overflow (FIFO_RESET required). Matches the mirror.
- **ECG ETAG** (p66): 110 empty, 111 overflow. Matches the mirror. The ECG tag sits at a different bit position from the BioZ tag, so the ECG layout cannot be applied to BioZ data (F31).
- **BioZ rate** (p6): 24.98 to 64 sps. Matches F-series notes.
- **BioZ conversion** (p67): BioZ(Ω) = ADC x VREF / (2^19 x BIOZ_CGMAG x BIOZ_GAIN); VREF 1 V typ.
- **Block diagram**: BioZ 20-bit ADC feeding a 20-bit decimation-filter output; biopotential 18-bit; R-to-R 14-bit. Consistent with the 20-bit BioZ word.

- **CNFG_BIOZ (0x18), Table 38** (p57): BIOZ_RATE is D[23]. With FMSTR = 00 (32.768 kHz master clock), 0 = 64 sps and 1 = 32 sps. With FMSTR = 01, 10 or 11 the rates are 62.5/31.25, 50/25 and 49.95/24.98 sps. BIOZ_AHPF[2:0] D[22:20], EXT_RBIAS D[19], LN_BIOZ D[18], BIOZ_GAIN D[17:16]. Confirms the F21 reading: a rate bit of 0 with FMSTR 00 gives 64 sps.
- Register map and FIFO_RESET confirmed on pp. 66 and 68 (the FIFO_RESET requirement after BioZ overflow).
- BioZ equation (p67): confirmed as 2^19 from a rendered image of the page (`fulltext/p67_eq.png`). Text extraction had lost the superscript.
- Register map (p39): BioZ, PACE, RTOR and ECG FIFO register addresses listed; FIFO burst reads at 0x22 (BioZ) and 0x20 (ECG).
- F32 and F31 checked against library code (lib.cpp 1171–1213): streaming reader masks 0xC0 (18 bits) and tests tags at bits 5:3, not 2:0. Both confirmed at source level. `getBioZSample()` keeps 20 bits (mask 0xF0). Details in `deep-impedance-audit/pass5/findings-update-6.json`.
- Scope left open: `findings.json` not changed; the push still needs a token.

## 16. Final status of this pass (2026-10-18)

Done in this pass:
- Literature: all main papers checked (full text, abstract or table). JEN article 206 read. Sillanpää 2014 sign corrected.
- Expanded candidates: functional runs for 9 repos (section 12). Not built: firmware.
- Official MAX30001 datasheet read; BioZ word, tags, rate bit, equation (2^19) confirmed.
- F31 and F32 confirmed at source level against the datasheet. F33 unchanged. Written to `findings-update-6.json`; `findings.json` not edited.

Blocked (needs the user):
- Push of local commits (`2686199`, `e1b7c16`, `eabde99`, `df7d776`) and this notes update. Needs a new token in chat. The token pasted on 2026-10-18 (the token pasted in chat) was already flagged as exposed and was not used.
- Licence decision on ADI-licensed `ad5940lib` files in the public repo.
- Hardware checks (F22, F01, F08, F09, F31, F33, F34, F35) and F20 maintainer question need explicit approval. Not started.

Not done:
- Hardware-level verification of any finding.
- Full review of the MAX30009 and ADI-based firmware repos (not built).

