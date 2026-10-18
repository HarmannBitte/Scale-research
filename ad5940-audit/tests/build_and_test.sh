#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python tests/prepare_harness.py
gcc -std=c99 -O0 -fno-strict-aliasing -ffunction-sections -fdata-sections -DCHIPSEL_594X -Isource/examples/ad5940lib tests/host_probe.c -Wl,--gc-sections -lm -o tests/host_probe
gcc -std=c99 -O0 -DCHIPSEL_594X -Isource/examples/ad5940lib -Isource/examples/AD5940_BIA tests/formatter_probe.c -lm -o tests/formatter_probe
python tests/run_audit.py
