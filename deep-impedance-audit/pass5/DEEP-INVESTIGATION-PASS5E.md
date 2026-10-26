# Pass 5e: direct read of the MAX30001 datasheet (register section and FIFO tables)

No hardware, no maintainer contact, no purchases. Research use only.

## Provenance

- The Analog Devices and Maxim PDF URLs failed from the fetch tool (`fetch_page` error). The text was read from the alldatasheet.com HTML mirror of the MAX30001 datasheet (Maxim/ADI, 86 pages), one page per URL.
- Pages read: 57 (Table 38, CNFG_BIOZ part 1), 58 (Table 38, part 2), 67 (BIOZ FIFO memory, data structure, Table 50), 68 (BTAG text, from pass 5d).
- Mirror text is third-party. Confirm against the official PDF before publishing numbers.

## 1. CNFG_BIOZ (0x18), page 57, Table 38

- D[23] BIOZ_RATE, default 0. With FMSTR = 00 (fMSTR = 32,768 Hz): 0 = 64 sps, 1 = 32 sps.
- D[22:20] BIOZ_AHPF[2:0], default 010. The library writes 010.
- Result: the library's `cnfg_bioz.bit.rate = 0` gives 64 sps. This confirms pass 5c and corrects F21 with a direct citation. The OpenView decoder's 128 sps label is wrong.
- The library's FIFO register addresses also match the register map: ECG_FIFO 0x21, BIOZ_FIFO 0x23 (normal read), and bursts at 0x20 and 0x22 (`lib.h` lines 106–110).

## 2. BIOZ FIFO data structure, page 67

- "The BIOZ FIFO memory is a standard circular FIFO consisting of 8 words, each with 24 bits." So the BioZ FIFO holds **8 words**, not 256. (The 256-word figure in pass 5 applies to the MAX30009, not the MAX30001.)
- Data: "20-bit BIOZ voltage ... left justified two's complement. One bit is set to 0 and the remaining three bits of data hold ... tagging information (Table 50)." So D[3] = 0 and BTAG = D[2:0]. This closes the open layout item.
- Table 50 (BTAG[2:0] = D[2:0]), with the datasheet's recommended action:

| BTAG | Meaning | Data valid | Time valid |
|---|---|---|---|
| 000 | Valid sample | Yes | Yes |
| 001 | Over/under range sample | ? (check lead-off) | Yes |
| 010 | Last valid sample (EOF) | Yes | Yes |
| 011 | Last over/under range sample (EOF) | ? | Yes |
| 10x | Unused | - | - |
| 110 | FIFO empty (exception) | No | No |
| 111 | FIFO overflow (exception) | No | No |

## 3. What this changes

**F31 (streaming BioZ decoder), now precise.**
- The streaming decoder reads the tag from D[5:3] (the ECG position). Under the datasheet, D[5:3] are data bits 5:4 plus a fixed 0 in bit 3.
- The accept rule `etag == 0` also drops BTAG 001, 010 and 011, which are valid time steps. It keeps only 000.
- It treats 111 as a reset only when D[5:3] = 111, which cannot happen when D[3] = 0. Overflow is therefore never detected on this path.
- Model result (`max30001_bioz_decode_model.py`): 25% kept under uniform data, 0% reset. Consistent with the datasheet layout.

**F33 (new-API read path), strengthened by the datasheet.**
- The datasheet says a word tagged 110 is "FIFO empty (exception): discard this sample without incrementing the time base."
- `getBioZSample()` and `getECGSample()` do not read the tag. They return `sample_valid = true` for every word, so an empty-FIFO word (110) is stored as a sample.
- This is the same symptom as the Nordic report (ECG word `0x000037` read as a zero-valued sample). For ECG, `0x37` has ETAG bits 5:3 = 110, which is the empty exception. The explanation now matches the datasheet.
- Status: source plus datasheet. Hardware effect not measured.

**F13 (correct BioZ layout), confirmed.** The new API takes the upper 20 bits of the word, which matches "20-bit left justified". F13 stays correct.

**New risk (not a finding yet): BioZ FIFO depth is 8 words.**
- At 64 sps, 8 words is 125 ms of buffer. `Example01` reads BioZ once per two ECG frames, inside the ECG branch.
- If the loop stalls for more than about 125 ms, the BioZ FIFO overflows and the datasheet says samples are lost. The sketch cannot see this, because it does not check tags (F33).
- Status: a design risk from the datasheet depth plus the sketch's read pattern. Not measured.

## 4. Revised status

| ID | Before 5e | After 5e |
|---|---|---|
| F21 | rate label wrong (5c, from library and bit layout) | confirmed directly on datasheet page 57 |
| BioZ layout (D[3]) | open | closed: D[3] = 0, BTAG = D[2:0] (page 67) |
| F31 | 25% kept; accept set unclear | precise: keeps only BTAG 000; drops 001/010/011 valid samples; overflow never detected |
| F33 | source-level; Nordic symptom | datasheet says 110 must be discarded; library stores it |
| F13 | correct | confirmed |
| BioZ FIFO depth | not stated | 8 words (page 67) |

## 5. Still not read directly

- The ECG FIFO tag table (ETAG) page in full. The 110 = empty meaning for ECG is used here by analogy, supported by the Nordic report and the ECG table excerpt in the search results. Read that page before relying on it.
- The overflow timing (the 125 ms figure) is arithmetic from the depth and rate. It is not a measured timing.
