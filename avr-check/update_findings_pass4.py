#!/usr/bin/env python3
"""Pass 4: record the results of the doable-now items in deep-impedance-audit/findings.json."""
import json, pathlib
p = pathlib.Path('/home/user/deep-impedance-audit/findings.json')
d = json.load(open(p))
F = {x['id']: x for x in d['findings']}

F['F12'].update(
    levels=['S', 'H', 'DS'],
    status=("Source and arithmetic confirmed. The ADuCM350 Hardware Reference Manual (UG-587 Rev. E, AFE_WG_AMPLITUDE at 0x4008003C) "
            "lists bits [31:11] as RESERVED, read-only, and SINE_AMPLITUDE as bits [10:0], unsigned. The manual's general rule for unused bits "
            "is that writes have no effect (stated for another register; the exact sentence was seen in a manual excerpt, not the full table). "
            "So the 61,323 written value is most likely masked to 1,931 codes. Not measured on hardware."),
    severity="HIGH review priority for any future hardware work. No hazard claim is made; no electrode-level output was measured.")

F['F05'].update(
    levels=['S', 'H', 'DS'],
    status=("MAX30009: chunks 0-3 and 6-11 read in pass 4 (chunk 10 holds a timing-example table with no column headers in the fetched text, "
            "so the BIOZ_ADC_OSR bit table was not decoded). The ADC OSR register table is still not confirmed. Open."))

F['F22'].update(status="Inference from the vendor driver. Hardware not tested. Datasheet chunks 2-3 read in pass 4 (no FIFO count layout in them).")

d['findings'].append(dict(
    id='F24', repo='protocentral/max30001_openview',
    claim=("The collected OpenView snapshot has no pubspec.lock and no assets/ fonts or branding files, even though pubspec.yaml declares them. "
           "A plain 'flutter pub get' therefore resolves fresh versions (150 dependencies changed in the working copy), and 'flutter test' fails with "
           "'Failed to build asset bundle' until the asset declarations are removed."),
    levels=['T', 'S'],
    evidence=['Collection listing: no pubspec.lock; flutter test output in avr-check/openview-flutter-test.log',
              'avr-check/openview_strip_assets.py and STRIPPED-FOR-TEST.json (working copy only)'],
    status='Verified in this session. The test result below applies only to the stripped, freshly resolved working copy.',
    severity='Reproducibility: the collected snapshot cannot be built or tested as-is.'))

d['findings'].append(dict(
    id='F25', repo='Protocentral/MAX30001 Arduino library; dyarleniber/AD5933-arduino-bioimpedance',
    claim=("Both Arduino sources compile for ATmega328P (avr-g++ 14.2, -Os, -Wall) against minimal stub headers: "
           "protocentral_max30001.cpp with 0 errors and 13 warnings (4,886 bytes of text), and the AD5933.ino sketch with 0 errors and 0 warnings (540 bytes). "
           "The sketch needed Arduino-IDE-style prototypes, added by a script."),
    levels=['T'],
    evidence=['avr-check/build_avr.sh, avr-check/make_and_build_ad5933.py, avr-check/max30001-build.log, avr-check/ad5933-build.log'],
    status=('Compile-only evidence. The stub headers are not the Arduino core, so the build is not an Arduino IDE build and nothing ran on an AVR. '
            'Does not show the code works on hardware.'),
    severity='Low: confirms the sources compile; does not confirm behaviour.'))

d['findings'].append(dict(
    id='F26', repo='melazab/AD5940-BIOZ',
    claim=("No licence file exists at the repository root, and the GitHub licence API returns 404 (no detected licence). "
           "The four vendored ad5940lib/LICENSE copies are the ADI licence: redistribution is permitted only for use with ADI products, "
           "and the code may not be combined 'in any manner that would cause the software to become subject to terms... which differ'. "
           "The melazab-authored code therefore has no stated licence, while its vendored ADI library carries restrictive terms."),
    levels=['S', 'T'],
    evidence=['sources/melazab__AD5940-BIOZ/*/ad5940lib/LICENSE (4 copies, identical licence text)',
              'GitHub API licence endpoint: 404 (fetch 2026-10-18)'],
    status='Verified. Recorded as a licence difference only; the project is not excluded.',
    severity='Licence: the root project has no grant of rights; the vendored ADI licence limits redistribution and combination.'))

d['findings'].append(dict(
    id='F27', repo='ADI MAX30009 datasheet',
    claim=("MAX30009 facts read in pass 4: ADC resolution 20 bits; ENOB 16.3 bits at BIOZ_ADC_OSR=128 and 9.6 bits at OSR=8; "
           "phase accuracy +/-0.15 deg at 50 kHz for a Cole load after calibration; magnitude accuracy +/-0.1 % at 50 kHz for the same load; "
           "current-drive ranges 16 nARMS to 1.28 mARMS; 16 Hz to 500 kHz drive; ADC sample rate 16 to 4546 sps; "
           "full-scale lead-off current options 5.5 to 110 nA; PLL 14-28 MHz; FCLK accuracy requirement 347 ppm for IEC 60601-2-47."),
    levels=['DS'],
    evidence=['analog.com MAX30009.pdf, fetch chunks 1, 2, 3, 6, 7 (pass 4)'],
    status="Vendor-stated characteristics under the datasheet's test conditions (manufacturer test load). Not independent validation.",
    severity='Context for the F03 and F04 unit checks. Not a device claim.'))

d['open_items'] = [
    "F05 MAX30009 BIOZ_ADC_OSR bit table: the register map and the table were not in the fetched chunks (chunk 10 has no headers). Needs the full PDF register section.",
    "F20 intended HR/RR contract for OpenView packet type 2 (maintainer question; no contact authorised).",
    "F22 hardware FIFO semantics (count in samples or bytes) on a real MAX30009; needs a bench (not authorised).",
    "F01, F08, F09 hardware reachability (not authorised).",
    "F24/F26 upstream-level fixes: pubspec.lock and assets missing from the collection; melazab licence unstated (maintainer or repo owner question).",
]
d['generated'] = d.get('generated', '') + ' pass4 2026-10-17'
json.dump(d, open(p, 'w'), indent=1)
print('findings', len(d['findings']), 'open', len(d['open_items']))
