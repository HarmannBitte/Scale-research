# Hardware check plan (draft, not approved to run)

Status: NOT RUN. Each item needs a yes from the user before any step is taken.

## Constraints that apply
- No purchases. Only hardware the user already owns.
- No flashing of devices unless the user lifts the "no flashing" constraint for that item. Most firmware tests need flashing, so this is the main blocker.
- No human experiments.
- Host-only tests (ASan, stubbed SPI/I2C) are not hardware checks. They can run without approval, but results are reported separately.

## Questions the user must answer first
1. Which boards are owned? (MAX30001 eval board, MAX30009 board, AD5933 module, MAX32655 board, UPRM firmware target.)
2. Is flashing allowed for the owned boards?

## Per-item plan

| ID | Claim (from findings) | Hardware needed | Procedure | Expected if claim holds | Flash needed? |
|---|---|---|---|---|---|
| F22 | UPRM burst-reads `fifoCount` bytes but count is in samples (need count x 3) | MAX30009 board + MAX32655 target | Fill FIFO to a known count; read count register; compare bytes requested vs bytes needed | Under-read by two-thirds on full FIFO | Yes |
| F01 | `spiBurst` writes `tx_buf[1]` and reads past buffer for count 0/1 | MAX32655 target | Host ASan first (stubbed SPI, counts 0,1,2,3). Then bench with empty and 1-sample FIFO | ASan reports overflow; bench may fault or read garbage | Bench part: yes |
| F08 | OpenEBI `take_measurement(0)` gives NaN | None for the core claim (host confirmed). Optional: AD5933 module | Host run already confirmed; bench only if the user wants the serial output seen | "NaN" on serial | Optional |
| F09 | AD5933 valid-data wait loop has no timeout | AD5933 module + MCU | Run with the data-ready pin/bit never set (e.g. unplugged) under a watchdog | Hang with no output | Yes |
| F31 | BioZ streaming reader uses ECG tag bits (5:3) | MAX30001 board + MCU | Read BioZ FIFO words; compare the reader's valid/overflow decisions with BTAG at bits 2:0 | Valid samples dropped; overflow words misread | Yes |
| F33 | Empty ECG/BioZ FIFO read returns a sample with `sample_valid = true` | MAX30001 board | Read FIFO with no data pending; record the tag and returned value | Tag 110 returned; value 0; still marked valid | Yes |
| F34 | AD5933 real/imag cast of uint16 to int: negatives read as 32768–65535 | AD5933 module | Measure a known negative-real load (or inject a known register value); compare with expected sign | Large positive values where negative expected | Yes |
| F35 | I2C read failure returns 0 with no error | AD5933 module | Disconnect SDA or SCL during a read; log returned value | Zero returned as a valid point | Yes |

## Order I would suggest
1. Host-only checks first (F01 ASan, F08 already done). No approval needed for host-only work.
2. Bench checks in this order: F33 and F31 (MAX30001 board, read-only, no flashing if the existing firmware can be used), then F34 and F35 (AD5933), then F09 (AD5933 with watchdog), then F22 and F01 bench parts (MAX32655 target).

## Stop conditions
- Stop at any sign of a hang that cannot be recovered without power-cycling.
- Do not connect any device to mains without the user's approval.
- Record every step in a log under `deep-impedance-audit/bench-logs/`.
