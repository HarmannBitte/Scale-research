"""Pass 5: simulate UPRM spiBurst() byte-count behaviour against a vendor-layout FIFO.
Synthetic only (no hardware). Mirrors the parse loop in generated/uprm-fifo.c:
burst length = fifoCount BYTES, parse by nonzero first byte, no tag check.
Vendor semantics: FIFO count = number of 24-bit WORDS (datasheet: 256-word FIFO).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def upr_count(c1, c2):
    """UPRM: (counter1 & 0x7F)*2 + counter2"""
    return (c1 & 0x7F) * 2 + c2


def vendor_count(c1, c2):
    """Vendor: (counter1 bit7 << 8) | counter2, clamped to 256"""
    return min((((c1 & 0x80) >> 7) << 8) | c2, 256)


def uprm_parse(buf):
    """Mirror of the UPRM loop: returns the (I, Q) 3-byte pairs it would accept."""
    out, i, n = [], 0, len(buf)
    while i < n:
        if buf[i] != 0:
            hold1 = buf[i:i + 3]
            i += 3
            while i < n and buf[i] == 0:
                i += 1
            if i + 2 < n:
                hold2 = buf[i:i + 3]
                i += 2
                out.append((hold1, hold2))
        i += 1
    return out


def fifo_bytes(n_pairs):
    """Vendor layout: I word (tag 0x1), Q word (tag 0x2), 24-bit data, nonzero."""
    b = bytearray()
    for k in range(n_pairs):
        b += bytes([0x10 | (k & 0x0F), 0x12, 0x34])
        b += bytes([0x20 | (k & 0x0F), 0x56, 0x78])
    return bytes(b)


def main():
    res = {}
    # Sanity: the two formulas agree in the normal state (overflow = 0, count < 256)
    normal_ok = all(upr_count(0, c2) == vendor_count(0, c2) for c2 in range(256))
    res["normal_state_formulas_agree"] = normal_ok
    for n_pairs in (4, 8, 16, 32):
        words = 2 * n_pairs
        fifo = fifo_bytes(n_pairs)
        ucount = upr_count(0, words & 0xFF)     # UPRM reads this many BYTES
        read_bytes = min(ucount, len(fifo))
        got = uprm_parse(fifo[:read_bytes])
        res[f"{n_pairs}_pairs"] = {
            "vendor_words": words,
            "uprm_count_requested_bytes": ucount,
            "bytes_available": len(fifo),
            "bytes_read": read_bytes,
            "pairs_recovered": len(got),
            "pairs_actual": n_pairs,
            "fraction_recovered": round(len(got) / n_pairs, 3),
        }
    print(json.dumps(res, indent=1))
    with open(os.path.join(HERE, "uprm_fifo_yield.json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
