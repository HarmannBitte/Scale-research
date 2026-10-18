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
