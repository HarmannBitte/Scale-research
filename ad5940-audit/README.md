# AD5940 BIA source audit materials

**No hardware acquisition, flashing or electrical tests. No human-use authorization.**

Read `../AD5940-Firmware-and-Export-Audit.md` for findings and limits. `Export-and-Remediation-Contract.md` is a proposal, not implemented firmware.

## Scope and licenses

The curated upstream snapshot retains root licenses/documentation, the complete four-wire BIA example directory and ad5940lib worktree. Other examples, docs and .git metadata were removed after recording original file hashes. It is not a full repository or a complete embedded build environment.

Examples pin: `ae917b69b4f71214c7f19ae3eef563b9c547d48f`.
Library pin: `d4c2ba01f0c1f8cb47264905407a4a3f7bf1cd47`.

Upstream code remains unchanged. See `source/LICENSE` and `source/examples/ad5940lib/LICENSE`; ADI-product restrictions and third-party terms apply. Do not treat this package as MIT/BSD-licensed code. Test wrappers/generated extracts are conspicuously identified and supplied for development of the ADI-targeted bench application, not as an unrestricted alternative-device port. This is not legal advice.

## Reproduce host-only probes

Requires Python 3 and GCC on a Linux-like environment; no extra Python packages:

```sh
cd ad5940-audit
sh tests/build_and_test.sh
```

The script regenerates three exact upstream function extracts, builds two native executables and runs 21 unittest tests. Tested here with Python 3.13.16 / GCC 14.2.0. Build outputs are regenerated, not included in the downloadable archive.

- `host_probe.c` includes unchanged `BodyImpedance.c`; unreachable embedded paths are removed by section garbage collection at link time.
- Peripheral calls are **mocks**, including wakeup/FIFO/status/calibration responses. No SPI, ADC, MCU interrupt, real timing, calibration accuracy or transport behavior is emulated.
- `AD5940_SweepNext` and `AD5940_WGFreqWordCal` are exact extracted library function bodies. The harness supplies their silicon-mode state for arithmetic tests; it does not detect an actual device.
- `formatter_probe.c` uses the exact extracted `BIAShowResult` function with a mocked frequency lookup. Its text is a native stdout demonstration, not an observed UART capture.
- The extractor matches selected newline-started function definitions and balances braces. It is deliberately scoped to these pinned functions, not a general C parser.
- `extraction-manifest.json` records hashes of extracted function bodies. Root `source-manifest.json` records the original worktree and retained scope.

**Passing tests do not mean passing firmware qualification.** Tests assert observed stock failure behavior, including ignored capacity, swallowed calibration error, nonfinite result and stale output-count paths. Other tests validate finite arithmetic, sign extension, source preservation and formatter omissions.

The over-capacity tests use physically oversized backing storage while declaring a smaller capacity. They show that the upstream ISR exceeds its input limit without causing an actual native out-of-bounds write. The caller-chain out-of-bounds read risk is a static finding, not executed with an undersized allocation.

No defects were patched. A subsequent development stage must implement fixes and change regression expectations to require safe rejection/recovery. Source-level results do not prove behavior of SensorPal, preflashed vendor firmware or another example/revision.
