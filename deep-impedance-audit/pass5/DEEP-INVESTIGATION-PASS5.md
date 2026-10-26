# Deep investigation, pass 5 (no hardware, no maintainer contact)

Scope: the two MAX30009 FIFO findings (F02, F22) and the open register-table item (F05).
Original `findings.json` is unchanged. Corrections are in `findings-update.json`.

## 1. F05: BIOZ_ADC_OSR register table (resolved, with a limit)

- Register and field: `MAX30009_REG_BIOZ_CONFIGURATION1` (0x20) holds `DAC_OSR` in bits 7:6 and `ADC_OSR` in bits 5:3 (`max30009.h`, chunk 0 of 4).
- Enum: the no-OS driver's `ADC_OSR` enum value equals the register field value (4 = 128, 5 = 256, 7 = 1024), as recorded in pass 4.
- Datasheet check: the SR formula (`SR = PLL/(NDIV x ADC_OSR)`) reproduces the datasheet's BIA example rates (62.5, 48.8125, 97.625, 61 sps) with the stated OSR values.
- Limit: the datasheet's printed bit-level table was not read directly (chunk 10 has no headers). The bit mapping rests on the driver enum plus datasheet arithmetic. Full confirmation needs the PDF register table.
- The UPRM comment (ADC_OSR = 5 = 256) and the firmware table (0xA0 decodes to 128) still disagree. F05 is a documentation issue, now resolved in favour of the driver mapping.

## 2. F02: FIFO count formula (narrowed)

Vendor layout, confirmed from `max30009.h` (chunk 0):
- Register 0x0A (`FIFO_COUNTER1`): bit 7 = `DATA_COUNT_MSB`; bits 6:0 = `OVF_COUNTER`.
- Register 0x0B (`FIFO_COUNTER2`): bits 7:0 = `DATA_COUNT_LSB`.
- Vendor count = (bit7 << 8) | counter2, clamped to 256.

UPRM: `(counter1 & 0x7F) * 2 + counter2`. It uses the overflow counter as if it were the count, and it ignores the MSB.

Exhaustive check over all 65,536 register pairs (`pass5/` run, this session):
- 65,153 pairs disagree.
- The formulas agree in the normal state: overflow counter = 0 and count < 256 (`normal_state_formulas_agree: true`).

Correction to the original F02 wording. The claim "disagrees for any FIFO count" is too broad. The defect appears when the overflow counter is nonzero (after an overflow) or when the count is 256. In the normal state the numbers match. This makes F02 a wrong-after-overflow defect, not a constant error.

## 3. F22: byte count versus word count (strengthened, still not on hardware)

- The datasheet describes a 256-word FIFO. A word is one 24-bit I or Q value. The vendor count is therefore in words, not bytes.
- UPRM requests `fifoCount` bytes and then parses 3-byte words from them. It reads one third of the words the count describes.
- Synthetic simulation (`uprm_fifo_yield.py`, output `uprm_fifo_yield.json`): with a vendor-layout FIFO of 4, 8, 16 and 32 I/Q pairs, UPRM recovers 1, 2, 5 and 10 pairs. That is 25% to 31% of the pairs.
- The synthetic FIFO is the vendor layout, with nonzero words and tags 0x1 and 0x2. Real behaviour on silicon is not tested.

## 4. Additional source observation (new, not in the original 29)

Proposed as F30 (Medium, source-level). The UPRM parse loop in `spiFunctions.c` (as mirrored in `generated/uprm-fifo.c`) finds samples by the first nonzero byte and never checks the FIFO tag bits (0x1 = I, 0x2 = Q, 0xE = marker, 0xF = invalid). Its I/Q pairing is therefore positional. Any marker, invalid word or a single-channel FIFO would shift the pairing silently. Fixing F22 without fixing F30 would still leave pairing unverified.

## 5. Still open (not done here)

- Hardware FIFO semantics on a real MAX30009 (F22, F02 after overflow). Needs a bench. Not authorised.
- F20 maintainer question. Not authorised.
- F01, F08, F09 reachability. Not authorised.
- DAC_OSR bit width (the datasheet table gives 3 bits, the driver uses 2). Needs the register table.
- Upstream files: `spiFunctions.c` is not in the collected snapshot (only `main.c`, `bioZ.c`). F22 and F30 rely on the audit's excerpt of lines 245–291.
