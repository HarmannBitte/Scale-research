#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p build/host
python tests/prepare_mock_header.py
gcc -std=c99 -D_DEFAULT_SOURCE -DCHIPSEL_594X -DAD5940_BENCH_POLL_LIMIT=8 -O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-pie -no-pie -Itests/mockhardware -Isource/examples/ad5940lib tests/target_io_probe.c -o build/host/target_io_probe
