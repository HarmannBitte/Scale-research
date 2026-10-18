#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
COMMON='-std=c99 -DCHIPSEL_594X -Isource/examples/ad5940lib -Isource/examples/AD5940_BIA'
gcc $COMMON -c source/examples/AD5940_BIA/BodyImpedance.c -o tests/body.o
gcc $COMMON -c source/examples/AD5940_BIA/AD5940Main.c -o tests/main.o
gcc $COMMON -c source/examples/ad5940lib/ad5940.c -o tests/library.o
python tests/prepare_probes.py
# Whole app included, actual processing/control/init; mocked hardware, exact library helper extracts.
FLAGS='-O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-pie -no-pie'
gcc $COMMON $FLAGS -DBIA_BENCH_ARMED=1 -DBIA_BENCH_MIN_CURRENT_COUNTS=1 -DBIA_BENCH_RCAL_OHM=10000 -DAD5940_BENCH_POLL_LIMIT=8 '-DBIA_BENCH_RUN_ID="synthetic-test"' '-DBIA_BENCH_SOURCE_KIND="synthetic"' tests/host_probe.c -lm -o tests/host_probe
gcc $COMMON $FLAGS -DBIA_BENCH_MIN_CURRENT_COUNTS=1 -DBIA_BENCH_RCAL_OHM=10000 -DAD5940_BENCH_POLL_LIMIT=8 '-DBIA_BENCH_SOURCE_KIND="synthetic"' tests/host_probe.c -lm -o tests/host_probe_unarmed
gcc $COMMON $FLAGS -DAD5940_BENCH_POLL_LIMIT=8 -Itests/mockhardware tests/port_probe.c -o tests/port_probe
