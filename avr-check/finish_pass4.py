#!/usr/bin/env python3
"""Pass 4 receipts: copy the build and test evidence into deep-impedance-audit/pass4/, add findings F28-F29,
regenerate MANIFEST.json. Nothing here touches hardware or the archived collection."""
import hashlib, json, pathlib, shutil, re

H = pathlib.Path('/home/user')
DA = H / 'deep-impedance-audit'
P4 = DA / 'pass4'
P4.mkdir(exist_ok=True)
AV = H / 'avr-check'
TEST_LOGS = {
    'settings_updates_test.dart': ('final-settings_updates_test.log', 4),
    'update_banner_test.dart': ('final-update_banner_test.log', 6),
    'update_controller_test.dart': ('final-update_controller_test.log', 26),
    'widget_test.dart': ('final-widget_test.log', 2),
    'test/boards/st1vafe3bx_decoders_test.dart': ('final-st1vafe3bx_decoders_test.log', 4),
}

def count_pass(text):
    t = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text).replace('\r', '')
    m = re.findall(r'\+(\d+): All tests passed!', t)
    return int(m[-1]) if m else None

tests = []
for name, (log, expected) in TEST_LOGS.items():
    text = (AV / log).read_text(errors='replace')
    n = count_pass(text)
    tests.append({'file': name, 'log': log, 'passed': n, 'all_passed_line': n is not None and n == expected, 'rc': 0 if n is not None else None})

for src in list(AV.glob('*.log')) + [AV / 'build_avr.sh', AV / 'make_and_build_ad5933.py', AV / 'openview_strip_assets.py',
                                       AV / 'stubs' / 'Arduino.h', AV / 'stubs' / 'SPI.h', AV / 'stubs' / 'Wire.h',
                                       AV / 'stubs' / 'SoftwareSerial.h', AV / 'ad5933_sketch.cpp', H / 'open-projects-collection' / 'WHERE-ARE-THE-SOURCES.txt']:
    if src.is_file() and not src.name.startswith('ov-'):
        shutil.copy2(src, P4 / src.name)
for log in AV.glob('ov-*.log'):
    shutil.copy2(log, P4 / log.name)
shutil.copy2(H / 'Open-Source-Projects-Collection.tar.xz.sha256', P4 / 'collection-archive.sha256')
(P4 / 'PASS4-RECEIPT.json').write_text(json.dumps({
    'date': '2026-10-17',
    'toolchains': {'avr-gcc': '14.2 (Debian trixie)', 'arm-none-eabi-gcc': 'installed, not used this pass', 'flutter': '3.47.7 stable', 'dart': '3.13.5 (Flutter-bundled)'},
    'avr_compile_only_against_stub_headers': [
        {'source': 'Protocentral MAX30001 Arduino library src/protocentral_max30001.cpp', 'flags': '-std=gnu++17 -Os -mmcu=atmega328p -Wall', 'rc': 0, 'errors': 0, 'warnings': 13, 'text_bytes': 4886},
        {'source': 'dyarleniber AD5933.ino (IDE-style prototypes added)', 'flags': '-std=gnu++17 -Os -mmcu=atmega328p -Wall', 'rc': 0, 'errors': 0, 'warnings': 0, 'text_bytes': 540},
    ],
    'openview_flutter_tests_stripped_working_copy': tests,
    'openview_linux_debug_build': {'command': 'flutter build linux --debug', 'rc': 0, 'output': 'build/linux/x64/debug/bundle/OpenView'},
    'caveats': [
        'AVR results are compile-only against minimal stub headers; they are not Arduino core builds and nothing ran on a microcontroller.',
        'OpenView tests ran on a working copy with the asset and font declarations removed (the collected snapshot omits those files) and with freshly resolved dependencies (the snapshot has no pubspec.lock).',
        'settings_updates_test and update_banner_test first failed with the Dart compiler killed by the kernel OOM killer (the sandbox has 2 GB RAM and /tmp is RAM-backed). Re-run after moving the Dart SDK off tmpfs; both pass.',
        'The Linux bundle was built but not launched (no display).',
    ],
}, indent=1))

fp = DA / 'findings.json'
d = json.load(open(fp))
d['findings'] = [f for f in d['findings'] if f['id'] not in ('F28', 'F29')]
d['findings'].append(dict(
    id='F28', repo='protocentral/max30001_openview',
    claim=('OpenView Flutter test suite: 42 tests in 5 files pass (settings 4, update banner 6, update controller 26, widget 2, '
           'board decoders 4), on the working copy with asset declarations removed and freshly resolved dependencies. '
           'The Linux debug build (flutter build linux --debug) also succeeds.'),
    levels=['T'],
    evidence=['deep-impedance-audit/pass4/final-*.log', 'deep-impedance-audit/pass4/PASS4-RECEIPT.json'],
    status='Verified in this session. Not a release build, not a GUI run, not a hardware run.',
    severity='Positive result, with the reproducibility caveat in F24.'))
d['findings'].append(dict(
    id='F29', repo='Protocentral/MAX30001 Arduino library; dyarleniber AD5933',
    claim='AVR compile-only checks (F25) and OpenView tests and build (F28) are the only executed builds in pass 4. Zephyr, Android, MATLAB, and AVR runtime were not run.',
    levels=['T'],
    evidence=['deep-impedance-audit/pass4/PASS4-RECEIPT.json'],
    status=('Zephyr: not attempted (multi-GB SDK on a 2 GB machine). Android: not built (SDK not installed). MATLAB: no licence in this sandbox. '
            'AVR runtime and hardware: not authorised.'),
    severity='Coverage gap, not a defect.'))
json.dump(d, open(fp, 'w'), indent=1)

# Regenerate the manifest for the whole folder (excluding itself).
files = []
for p in sorted(DA.rglob('*')):
    if p.is_file() and p.name != 'MANIFEST.json' and '.dart_tool' not in p.parts and 'build' not in p.parts:
        files.append({'path': str(p.relative_to(DA)), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
(DA / 'MANIFEST.json').write_text(json.dumps({'files': files}, indent=1))
print('findings', len(d['findings']), 'open', len(d['open_items']), 'manifest files', len(files))
print('tests', [(t['file'], t['passed']) for t in tests])
