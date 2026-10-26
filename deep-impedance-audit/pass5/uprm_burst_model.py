"""Pass 5b: line-accurate model of UPRM spiBurst() (src/spiFunctions.c lines 239-300).

Two MISO scenarios, because the device's response during the two address/dummy bytes
is not confirmed on hardware:
  A) data start at rx_buf[0] (the literal reading of the burst code)
  B) data start at rx_buf[2] (the convention regRead() uses: gReadBuf[2] holds the data)
Also reports every access at index >= fifoCount (out-of-bounds read, F01 family).
No hardware. Synthetic vendor-layout words: I (tag 0x1) then Q (tag 0x2), nonzero.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def upr_count(c1, c2):
    return (c1 & 0x7F) * 2 + c2          # spiFunctions.c line 245 and 247


def fifo_words(n_pairs):
    out = []
    for k in range(n_pairs):
        out.append((0x10 | (k & 0x0F), 0x12, 0x34))   # I
        out.append((0x20 | (k & 0x0F), 0x56, 0x78))   # Q
    return out


def simulate(n_pairs, data_offset):
    words = fifo_words(n_pairs)
    payload = bytearray(b for w in words for b in w)
    # what MISO shows: junk (0) for the first data_offset bytes, then FIFO payload
    device_stream = bytearray(data_offset) + payload
    words = 2 * n_pairs
    # vendor: count = (counter1 bit7 << 8) | counter2 ; full FIFO = 256 words -> bit7 set, counter2 = 0
    c1 = 0x80 if words >= 256 else 0
    fifo_count = upr_count(c1, words & 0xFF)          # UPRM byte count (masks bit 7)
    rx = device_stream[:fifo_count]                   # MISO captured for fifo_count bytes
    rx += bytes(max(0, fifo_count - len(rx)))         # pad
    oob_reads = 0
    pairs = []
    i = 0
    n = fifo_count

    def at(idx):
        nonlocal oob_reads
        if idx >= n:
            oob_reads += 1
            return 0                                  # value is outside the VLA; treated as 0 here
        return rx[idx]

    while i < n:
        if at(i) != 0:
            hold1 = (at(i), at(i + 1), at(i + 2))     # lines 279-281: unchecked i+1, i+2
            i += 3
            while i < n and at(i) == 0:               # line 284
                i += 1
            if i + 2 < n:                             # line 287 guard
                hold2 = (at(i), at(i + 1), at(i + 2))
                i += 2
                pairs.append((hold1, hold2))
        i += 1
    return {
        "pairs_actual": n_pairs,
        "fifo_count_bytes": fifo_count,
        "pairs_recovered": len(pairs),
        "fraction_recovered": round(len(pairs) / n_pairs, 3),
        "oob_reads": oob_reads,
    }


def main():
    res = {"model": "UPRM spiBurst, lines 239-300",
           "note": "scenario A = data at index 0; B = data at index 2 (regRead convention)"}
    for n_pairs in (4, 8, 16, 32, 128):
        res[f"{n_pairs}_pairs"] = {
            "A_data_at_0": simulate(n_pairs, 0),
            "B_data_at_2": simulate(n_pairs, 2),
        }
    print(json.dumps(res, indent=1))
    with open(os.path.join(HERE, "uprm_burst_model.json"), "w") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
