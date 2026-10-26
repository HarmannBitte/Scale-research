# Pass 5b: going deeper on the MAX30009 FIFO path and the OSR field

Builds on `DEEP-INVESTIGATION-PASS5.md`. No hardware, no maintainer contact, no purchases.
Sources were fetched into `pass5/vendor/` this pass: the no-OS `max30009.c`/`.h`, the upstream UPRM `src/spiFunctions.c` (full file, not an excerpt), and the Analog Devices datasheet text (chunks 9–10).

## 1. DAC_OSR bit width: resolved, not a 3-bit field

- The datasheet's feature summary says `BIOZ_DAC_OSR[7:6](0x20)` and `BIOZ_ADC_OSR[5:3](0x20)`. The DAC field is 2 bits.
- The `[2:0]` label in the datasheet worked examples is a step label for the value, not the field width. The examples only use 32, 64, 128 and 256.
- The no-OS driver agrees: the mask is `GENMASK(7,6)` and the enum is 0=32, 1=64, 2=128, 3=256.
- A vendor worked example (MAX32655_MAX30009 `MAX30009.c` init, REF 32.768 kHz) checks the code 3 = 256 mapping. The register writes give PLL = 444 × 32768 = 14,548,992 Hz. With KDIV = 4 and DAC_OSR = 256 this gives F_BIOZ = 14,208 Hz, the value in the vendor's comment. The same write gives BIOZ_ADC_CLK = 28,416 Hz and SR = 222 sps (ADC code 4 = 128), also as the comment says.
- Status: F05 is closed for the DAC field. The earlier "3 bits vs 2 bits" open item came from misreading the notation.

## 2. F02 and the full-FIFO case

- Vendor (`max30009.c`, `max30009_fifo_get_count`): count = ((cnt1 & 0x80) >> 7) << 8 | cnt2, clamped to 256.
- UPRM `spiFunctions.c` line 245 uses `(gReadBuf[2] & 0x7F) << 1`, then line 247 adds counter 2.
- Two cases differ:
  - After an overflow (overflow counter, bits 6:0, nonzero): UPRM adds 2 × overflow count.
  - Full FIFO (count = 256, bit 7 set): UPRM masks bit 7 away and requests **0 bytes**. This is the worst case, because the FIFO is most full exactly when the firmware reads nothing.
- Model result (`uprm_burst_model.py`, `uprm_burst_model.json`): a 256-word FIFO gives `fifo_count_bytes = 0` in both MISO scenarios.
- Status: F02 is confirmed against the full source at lines 245 and 247. The full-FIFO case is a new sub-finding.

## 3. F22: byte count versus word count

- Vendor `max30009_read_fifo_data(device, data, len)` takes `len` in bytes. The vendor count is in words (FIFO depth 256 words). UPRM passes the word count as the byte count (lines 249–261, 275–291).
- Model result: UPRM recovers 25–31% of I/Q pairs for 4–32 pairs in both MISO scenarios. Full FIFO recovers 0%.
- Status: strengthened. Still hardware-untested.

## 4. Data offset question (new, inferred)

- `regRead()` (lines 154–186) returns `gReadBuf[2]`, so the vendor's read convention puts the data at byte 2 of the response (the first two bytes are the address and dummy phase).
- `spiBurst` does not apply the same offset. It parses from `rx_buf[0]`.
- If the device behaves as `regRead()` assumes, the parser also consumes two junk bytes at the start. The model shows the recovery rate is the same in both cases, so the main loss is the byte count, not the offset.
- Status: inference from the file's own convention. The MISO content during the address phase is not confirmed on hardware.

## 5. F01: out-of-bounds reads (confirmed in the full source)

- Line 249–252: `tx_buf` and `rx_buf` are VLAs sized `fifoCount`. A count of 0 gives zero-length arrays, and `tx_buf[1] = 0x80` (line 255) writes out of bounds. This matches the existing F01 claim.
- Lines 279–281: `rx_buf[i+1]` and `rx_buf[i+2]` are read with no bounds check. The guard at line 287 covers only the second word.
- Model: out-of-bounds reads occur in several cases (`oob_reads` column in the JSON).
- Status: confirmed in source; reachability on hardware still unknown. Needs the register read and an empty-FIFO interrupt on a real device, which is out of scope here.

## 6. F30: tag handling (now confirmed by the vendor decoder)

- Vendor `max30009_fifo_decode_sample` (`max30009.c` around line 620): reads the 4-bit tag from bits 23:20, treats 0xFFFFFF as invalid and 0xFFFFFE as marker, and decodes tag 0x1 as I and 0x2 as Q.
- UPRM `spiBurst` never reads the tag. Its only check is `rx_buf[i] != 0`, and the I/Q pairing is by position.
- Status: F30 is confirmed in the source. The vendor decoder shows the tag check is the expected behaviour. The effect on hardware is not measured.

## 7. Revised status of the open items

| Item | Before pass 5b | After pass 5b |
|---|---|---|
| DAC_OSR bit width | open | closed: 2 bits, bits 7:6 |
| F02 formula | "any count" | narrowed; full FIFO reads 0 bytes |
| F22 byte vs word | inference | strengthened by vendor read_fifo_data(len in bytes) and the datasheet 256-word FIFO; still untested on hardware |
| F01 out-of-bounds | host probe | confirmed in full source (lines 249–252, 279–281) |
| F30 tag handling | proposed | confirmed against the vendor decoder |
| Hardware FIFO behaviour | open | still open; needs a bench (not authorised) |
| F20, F08, F09, F24/F26 | open | unchanged |

## 8. Files

- `pass5/vendor/max30009.c`, `max30009.h`, `uprm_spiFunctions.c`: fetched sources (BSD-3-Clause and the upstream UPRM licence; research use only).
- `pass5/uprm_burst_model.py` and `.json`: line-accurate burst model with both MISO scenarios.
- `pass5/uprm_fifo_yield.py` and `.json`: simpler yield model from pass 5.
- `pass5/DEEP-INVESTIGATION-PASS5.md`: pass 5.
