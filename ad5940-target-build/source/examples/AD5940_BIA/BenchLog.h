/* NEW 2026-10-17: passive-bench experimental logger; not qualified firmware. */
#ifndef BIA_BENCH_LOG_H
#define BIA_BENCH_LOG_H
#include "ad5940.h"
#include <stddef.h>
#ifndef BIA_BENCH_RUN_ID
#define BIA_BENCH_RUN_ID "UNSET"
#endif
#ifndef BIA_BENCH_SOURCE_KIND
#define BIA_BENCH_SOURCE_KIND "hardware"
#endif
#ifndef BIA_BENCH_MIN_CURRENT_COUNTS
#define BIA_BENCH_MIN_CURRENT_COUNTS 0
#endif
#ifndef BIA_BENCH_RCAL_OHM
#define BIA_BENCH_RCAL_OHM 0
#endif
#define BIA_BENCH_PAYLOAD_MAX 2048u
AD5940Err BenchLogBegin(const char *run_id);
AD5940Err BenchLogEmitJson(const char *json);
uint32_t BenchLogCrc32(const unsigned char *data,size_t length);
#endif
