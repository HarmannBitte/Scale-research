# Pass 5d: closing the MAX30001 layout question, and the OpenEBI AD5933 sign bug

No hardware, no maintainer contact, no purchases. Research use only.

## 1. MAX30001 BioZ word layout (closes the open item from 5c)

- The sister part MAX30002 datasheet (Analog Devices, Rev 1, 1/23) describes the BioZ FIFO word: a 20-bit left-justified two's complement voltage, "one bit is set to 0 and the remaining three bits of data hold ... tagging information" (Table 30).
- So D[3] = 0 and BTAG = D[2:0]. The MAX30001 datasheet text (alldatasheet mirror, p. 68) gives the same BTAG = D[2:0] definition for MAX30001.
- BTAG codes (MAX30002 Table 30, same family): 000 valid; 001 over/under range; 010 valid, end of FIFO; 011 over/under range, end of FIFO; 110 empty; 111 overflow.
- Consequence for F31: with D[3] = 0, bits 5:3 of a BioZ word are data bits 5:4 and a fixed 0. The streaming decoder keeps only words with D[5:4] == 0, so about 25% of valid words are kept under uniform data. The reset path (etag == 7) cannot occur. The model in `max30001_bioz_decode_model.py` matches this layout (it reports 25.06% kept, 0% reset).
- Consequence for the correct tag: the streaming decoder accepts only BTAG 000. Under the datasheet it should also accept 001 and 010 as usable data, and treat 110 and 111 as non-data. It treats 111 as a reset only by accident. This is a second reason the path is wrong, separate from the bit positions.
- Caveat: the MAX30001 PDF itself was not reachable (Analog Devices and Maxim URLs failed from the fetch tool). The layout rests on the MAX30002 text plus the MAX30001 BTAG excerpt. A direct read of the MAX30001 register section is still open.

## 2. Evidence for F33 from outside the repo

- Nordic DevZone thread (2024): a developer reading the MAX30001 ECG FIFO got `0x000037`, and the sample value was 0 on every read. A forum reply identified 0x37 as the "FIFO EMPTY" tag.
- This is the failure F33 predicts: the new-API read (`getECGSample`, which sets `sample_valid = true` with no tag check) turns an empty-FIFO word into a zero-valued sample.
- It supports the source-level finding. It is not a test of the Protocentral library itself.

## 3. F34 (new, High): OpenEBI AD5933 reports negative readings as large positive values

- `ad5933_get_real()` and `ad5933_get_imaginary()` in `openebi/software` (`ad5933.c`, lines 239–253) return `(int)(((uint16_t) buf[0] << 8) | buf[1])`. The conversion is unsigned, so any negative two's-complement value becomes 32768–65535.
- The AD5933 datasheet (Rev F, real and imaginary registers) says the values are 16-bit two's complement. So the firmware is wrong for every negative real or imaginary part.
- `take_measurement()` averages these values (`main.c` lines 97–114), so the error passes straight into the sweep output.
- Host probe (`ad5933_sign_probe.c`, output `ad5933_sign_probe.out`, the conversion copied verbatim, I2C stubbed):
  - raw 0xFC18 (−1000 in two's complement): firmware returns 64536.
  - raw 0xFFFE (−2): firmware returns 65534.
  - raw 0x8000 (−32768): firmware returns 32768.
  - Average of four −1000 readings: firmware 64536.0.
- Reachability: any sweep point where the DFT real or imaginary part is negative. That is common across a sweep, because the phase of the measured impedance varies with frequency. The conversion is pure arithmetic, so this does not need hardware to be confirmed. Whether the device returns negative values in a given setup is the only hardware-dependent part, and the datasheet says it does.
- Contrast: `dyarleniber/AD5933-arduino-bioimpedance` declares `short re`, `short img` and gets the sign right on AVR (16-bit `short`). The bug is specific to the OpenEBI code.
- Status: source plus datasheet plus host probe. Not measured on the instrument.

## 4. F35 (new, Medium): I2C read failure returns 0 silently

- Both `ad5933_get_real()` and `ad5933_get_imaginary()` return 0 when the block read fails. Nothing reports the failure.
- `take_measurement()` then adds that 0 into the average. A single bus error yields a point that looks like a valid zero, and it is not flagged in the output.
- Status: source-level and confirmed by the same probe (the last line of the output).
- Severity: Medium. It turns a detectable communication error into silent data corruption.

## 5. Corrections to earlier items

- F13 (BioZ = upper 20 bits, sign-extended) is consistent with the datasheet and with the new-API decoder. It is the correct layout. The streaming decoder (F31/F32) is the one that disagrees.
- F09 (valid-data wait loop has no timeout) is unchanged.
- F08 (`average = 0` gives NaN) is unchanged. It is in the same function (`take_measurement`) and divides by `avg`, so it is the same kind of defect as F34: a missing check on an input.

## 6. Revised status

| ID | Before 5d | After 5d |
|---|---|---|
| MAX30001 BioZ layout (D[3]) | open | confirmed D[3] = 0 and BTAG = D[2:0] (MAX30002 text plus MAX30001 BTAG excerpt) |
| F31 | 25% kept, reset path unclear | 25% kept confirmed; reset path cannot occur; BTAG accept set is also wrong |
| F33 | source-level | Nordic report shows the same empty-FIFO-as-zero pattern |
| F34 | none | OpenEBI AD5933 unsigned conversion; host probe confirms |
| F35 | none | OpenEBI AD5933 silent zero on I2C failure |

## 7. Files

- `ad5933_sign_probe.c` and `ad5933_sign_probe.out`: the probe.
- `max30001_bioz_decode_model.py` and `.json`: updated assumption text (D[3] = 0, now sourced).
- `DEEP-INVESTIGATION-PASS5C.md`, `DEEP-INVESTIGATION-PASS5.md`, `DEEP-INVESTIGATION-PASS5B.md`: earlier passes, unchanged.
