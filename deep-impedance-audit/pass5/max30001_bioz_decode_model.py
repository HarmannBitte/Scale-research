"""Pass 5c: model the two BioZ FIFO decoders in protocentral_max30001_arduino_library (lib.cpp).

Decoder S (streaming, _max30001ReadBIOZFIFO, lines ~1194-1220):
  etag = (b2 & 0x38) >> 3 ; 0 -> keep, 7 -> FIFO reset, else drop.
  value = signed24(b0<<16 | b1<<8 | (b2 & 0xC0))           (18 bits kept, 24-bit scale)
Decoder N (new API getBioZSample, lib.cpp ~405-430):
  value = signed(b0<<16 | b1<<8 | (b2 & 0xF0)) >> 4          (20-bit value; no tag check)

Datasheet (MAX30001, CNFG_BIOZ/BIOZ FIFO): BioZ data are 20-bit, left-justified two's complement in
D[23:4]; the BioZ tag is BTAG[2:0] = D[2:0]. Bits D[5:3] are data for BioZ, not an ETAG.

Synthetic input: uniform random 20-bit BioZ codes, BTAG = 000 (valid). No hardware.
"""
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(1)


def s24(v):
    v &= 0xFFFFFF
    return v - (1 << 24) if v & 0x800000 else v


def s32(v):
    v &= 0xFFFFFFFF
    return v - (1 << 32) if v & 0x80000000 else v


def word(code20):
    """20-bit signed code -> 3-byte FIFO word, left-justified, BTAG = 000."""
    raw = (code20 & 0xFFFFF) << 4
    return (raw >> 16) & 0xFF, (raw >> 8) & 0xFF, raw & 0xFF


def decode_stream(b0, b1, b2):
    etag = (b2 & 0x38) >> 3
    if etag == 0:
        u = ((b0 << 16) | (b1 << 8) | (b2 & 0xC0)) << 8
        return "keep", s32(u) >> 8
    if etag == 7:
        return "reset", None
    return "drop", None


def decode_new(b0, b1, b2):
    u = ((b0 << 16) | (b1 << 8) | (b2 & 0xF0)) << 8
    return s32(u) >> 12


def main():
    n = 200_000
    counts = {"keep": 0, "drop": 0, "reset": 0}
    ratios = []
    for _ in range(n):
        code = random.randint(-(1 << 19), (1 << 19) - 1)
        b0, b1, b2 = word(code)
        action, s_val = decode_stream(b0, b1, b2)
        counts[action] += 1
        if action == "keep":
            n_val = decode_new(b0, b1, b2)
            if n_val:
                ratios.append(s_val / n_val)
    kept_frac = counts["keep"] / n
    result = {
        "n_words": n,
        "stream_keep_fraction": round(kept_frac, 4),
        "stream_drop_fraction": round(counts["drop"] / n, 4),
        "stream_fifo_reset_fraction": round(counts["reset"] / n, 4),
        "scale_ratio_stream_over_new_median": round(sorted(ratios)[len(ratios) // 2], 3),
        "expected_keep_if_data_bits_5_4_uniform": 0.25,
        "assumption": "D[3] is 0 in the BioZ word (datasheet BTAG occupies D[2:0] and data occupies D[23:4]); with uniform data, keep = P(D[5:4]==0) = 0.25, and reset (etag 7) needs D[5:3]=111, which cannot occur if D[3]=0.",
        "note": "Synthetic uniform data. Real BioZ codes are not uniform; the drop/reset fractions depend on the data-bit distribution in D[5:3]. The structural point (keep only when D[5:3]==0) does not.",
    }
    print(json.dumps(result, indent=1))
    with open(os.path.join(HERE, "max30001_bioz_decode_model.json"), "w") as fh:
        json.dump(result, fh, indent=1)


if __name__ == "__main__":
    main()
