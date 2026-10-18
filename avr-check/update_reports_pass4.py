#!/usr/bin/env python3
"""Append pass-4 results to DEEP-FINDINGS.md, the dossier, and the DEEP-README open items."""
import pathlib, re

H = pathlib.Path('/home/user')
DF = H / 'deep-impedance-audit' / 'DEEP-FINDINGS.md'
DOS = H / 'Open-Source-Projects-Collected-and-Investigated.md'
DR = H / 'deep-impedance-audit' / 'DEEP-README.md'

PASS4_DF = """
## Pass 4 (17 October 2026): outstanding items worked

Done in this pass (no hardware, no maintainer contact, no purchases):

- **F12 resolved from the ADuCM350 manual (UG-587 Rev. E).** `AFE_WG_AMPLITUDE` (0x4008003C): bits [31:11] are RESERVED and read-only; `SINE_AMPLITUDE` is bits [10:0]. The manual's rule for unused bits is that writes have no effect. The 61,323-code bipolar value is therefore most likely masked to 1,931 codes. Still not measured on hardware.
- **F05 narrowed, not resolved.** MAX30009 chunks 0-3 and 6-11 read. The ENOB, accuracy, drive-range, PLL and lead-off tables were read. The `BIOZ_ADC_OSR` bit table was not decoded: the only timing table in the last chunk has no column headers in the fetched text.
- **F26 melazab licence.** No root licence; GitHub's licence API returns 404. The four vendored `ad5940lib/LICENSE` copies are ADI's licence: use only with ADI products, and no combining with terms that differ. This is recorded as a licence difference. The project is not excluded.
- **F25 AVR compile-only.** The MAX30001 Arduino library (`protocentral_max30001.cpp`) compiles for ATmega328P with 0 errors and 13 warnings. The AD5933 sketch compiles with 0 errors and 0 warnings. Both use minimal stub headers, not the Arduino core, and nothing ran on a microcontroller.
- **F28 OpenView tests and build.** 42 tests in 5 files pass (settings 4, update banner 6, update controller 26, widget 2, board decoders 4). `flutter build linux --debug` succeeds. Caveats: the collected snapshot has no `pubspec.lock` and omits the font and branding assets, so the working copy had its asset declarations removed and its dependencies freshly resolved (F24). Two test files first failed because the kernel killed the Dart compiler for lack of memory; after the SDK was moved off the RAM-backed `/tmp`, both passed.

Still open (not doable without hardware or a maintainer): F05 (OSR table), F20 (intended HR/RR contract), F22 (hardware FIFO semantics), F01/F08/F09 (hardware reachability), and the upstream fixes in F24 and F26.

Not run, with reasons: Zephyr (multi-GB SDK on a 2 GB machine), Android (no SDK), MATLAB (no licence), AVR runtime (needs hardware).

Receipts: `deep-impedance-audit/pass4/PASS4-RECEIPT.json` and the logs beside it.
"""

DOS_PASS4 = """

## Pass 4: outstanding items worked (17 October 2026)

Full receipts: `deep-impedance-audit/pass4/PASS4-RECEIPT.json`. Findings: `deep-impedance-audit/findings.json` (29 findings, 5 open items).

- **F12 is now resolved from the chip manual.** On the ADuCM350, the amplitude register's bits above bit 10 are read-only reserved. The 61,323-code bipolar macro is therefore most likely masked to 1,931 codes, about 754 mV equivalent. Still not measured on hardware.
- **F05 is still open.** The MAX30009 OSR bit table was not decoded from the fetched chunks.
- **melazab/AD5940-BIOZ licence (F26).** No root licence; the GitHub licence API returns 404. The vendored ADI library licence limits use to ADI products and forbids combining with differently licensed code. Recorded as a difference; not excluded.
- **AVR compile-only (F25).** `protocentral_max30001.cpp` compiles for ATmega328P (0 errors, 13 warnings). The AD5933 sketch compiles (0 errors, 0 warnings). Stub headers, not the Arduino core; nothing ran on a microcontroller.
- **OpenView (F28, F24).** 42 Flutter tests in 5 files pass, and the Linux debug build succeeds. The collected snapshot has no `pubspec.lock` and omits fonts and branding assets, so the tests ran on a working copy with the asset declarations removed and dependencies freshly resolved.

Not run: Zephyr (multi-GB SDK on a 2 GB machine), Android (no SDK), MATLAB (no licence), AVR runtime and any hardware work (not authorised).
"""

t = DF.read_text()
t = re.sub(r'\n## Pass 4 \(17 October 2026\).*', '', t, flags=re.S) if '## Pass 4 (17 October 2026)' in t else t
t = t.replace('Machine-readable version: `findings.json` (23 findings, 4 open items).', 'Machine-readable version: `findings.json` (29 findings, 5 open items).')
DF.write_text(t.rstrip() + '\n' + PASS4_DF)

d = DOS.read_text()
if '## Pass 4: outstanding items worked' not in d:
    DOS.write_text(d.rstrip() + '\n' + DOS_PASS4)

r = DR.read_text()
r = r.replace('(23 findings, 4 open items)', '(29 findings, 5 open items)')
r = r.replace('- F12: how the AD5940-family register treats bits written above the 11-bit amplitude field. The ADuCM350 register table was not retrieved.\n', '')
r = r.replace('- F05: MAX30009 ADC OSR table (datasheet chunks 1–3 and 6–7 not read).', '- F05: MAX30009 BIOZ_ADC_OSR bit table (not decoded from the fetched chunks).')
r = r.replace('- Hardware reachability of F01, F08 and F09. No device was connected.', '- Hardware reachability of F01, F08 and F09. No device was connected.\n- Upstream fixes in F24 (pubspec.lock and assets missing from the snapshot) and F26 (melazab licence).\n- Not run: Zephyr, Android, MATLAB, AVR runtime (see pass4/PASS4-RECEIPT.json).')
r = r.replace('## Limits', '## Pass 4 receipts\n`pass4/` holds the AVR compile logs, the OpenView test and build logs, and `PASS4-RECEIPT.json`. Rerun the OpenView tests on a stripped working copy: see `openview_strip_assets.py` (copied into `pass4/`).\n\n## Limits')
DR.write_text(r)
print('updated', DF.name, DOS.name, DR.name)
