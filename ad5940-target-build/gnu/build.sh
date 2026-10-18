#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
CC=${CC:-arm-none-eabi-gcc}
DFP=vendor/ADuCM302x_DFP-3.2.1
CORE=vendor/CMSIS-5.2.0/Include
COMMON="-std=c99 -mcpu=cortex-m3 -mthumb -mfloat-abi=soft -Os -g3 -ffile-prefix-map=$(pwd)=. -ffunction-sections -fdata-sections -fstack-usage -fno-common -Wall -Wextra -Werror=implicit-function-declaration -Werror=incompatible-pointer-types -Werror=return-type -D_DEFAULT_SOURCE -DCHIPSEL_594X -D__ADUCM3029__ -D__STACK_SIZE=8192 -D__HEAP_SIZE=4096 -D__STARTUP_CLEAR_BSS -I$DFP/Include -I$DFP/Include/config -I$CORE -Isource/examples/ad5940lib -Isource/examples/AD5940_BIA"
for PROFILE in unarmed fullpath-linkcheck; do
  DEST="build/$PROFILE"
  mkdir -p "$DEST"
  rm -f "$DEST"/*.o "$DEST"/*.d "$DEST"/*.su "$DEST/firmware.elf"
  if [ "$PROFILE" = unarmed ]; then ARM=0; else ARM=1; fi
  FLAGS="$COMMON -DBIA_BENCH_ARMED=$ARM"
  printf '#include "BenchLog.h"\n' | $CC $FLAGS -dM -E -x c - > "$DEST/compiled-macros.txt"
  # RUN_ID stays UNSET and both characterization inputs stay zero in BOTH profiles.
  for SOURCE in \
    source/examples/ad5940lib/ad5940.c \
    source/examples/AD5940_BIA/BodyImpedance.c \
    source/examples/AD5940_BIA/AD5940Main.c \
    source/examples/AD5940_BIA/ADICUP3029/main.c \
    source/examples/AD5940_BIA/ADICUP3029/ADICUP3029Port.c \
    "$DFP/Source/GCC/startup_ADuCM3029.c" \
    "$DFP/Source/system_ADuCM3029.c" \
    gnu/newlib_io.c; do
    NAME=$(basename "$SOURCE" .c)
    echo "$CC [$PROFILE] $SOURCE"
    $CC $FLAGS -MMD -MP -c "$SOURCE" -o "$DEST/$NAME.o"
  done
  $CC -mcpu=cortex-m3 -mthumb -mfloat-abi=soft \
    -T"$DFP/Source/GCC/ADuCM3029.ld" \
    -Wl,--gc-sections,-Map="$DEST/firmware.map",--cref,--print-memory-usage \
    "$DEST"/*.o -lm -o "$DEST/firmware.elf"
  arm-none-eabi-size "$DEST/firmware.elf"
  arm-none-eabi-readelf -h -A "$DEST/firmware.elf" > "$DEST/elf-header.txt"
  arm-none-eabi-nm -n -S "$DEST/firmware.elf" > "$DEST/symbols.txt"
  arm-none-eabi-objdump -d "$DEST/firmware.elf" > "$DEST/disassembly.txt"
done
