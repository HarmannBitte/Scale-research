#!/usr/bin/env python3
# Emulate the Arduino IDE for one .ino: put prototypes just before setup(), then compile for ATmega328P (stub headers).
import re, pathlib, subprocess
here = pathlib.Path(__file__).resolve().parent
src_path = pathlib.Path('/home/user/.cache/open-projects/src/Open-Source-Projects-Collection/sources/dyarleniber__AD5933-arduino-bioimpedance/AD5933.ino')
src = src_path.read_text(errors='replace').splitlines()
protos = []
for line in src:
    m = re.match(r'^([A-Za-z_][\w \*]*?)\s+(\w+)\s*\(([^)]*)\)\s*\{?\s*$', line)
    if m and m.group(2) not in ('if', 'for', 'while', 'switch', 'return', 'setup', 'loop'):
        protos.append(line.rstrip().rstrip('{').rstrip() + ';')
body = [l for l in src if not l.strip().startswith('#include')]
i = next(k for k, l in enumerate(body) if l.startswith('void setup()'))
out = ['#include "Arduino.h"', '#include "Wire.h"', '#include <SoftwareSerial.h>'] + body[:i] + protos + body[i:]
(here / 'ad5933_sketch.cpp').write_text('\n'.join(out) + '\n')
print('prototypes', len(protos), 'inserted before line', i + 1)
r = subprocess.run(['avr-g++', '-std=gnu++17', '-Os', '-mmcu=atmega328p', '-DF_CPU=16000000UL', '-I', 'stubs', '-Wall', '-c',
                    '-o', 'ad5933.o', 'ad5933_sketch.cpp'], cwd=here, capture_output=True, text=True)
(here / 'ad5933-build.log').write_text(r.stdout + r.stderr)
errs = [l for l in (r.stderr).splitlines() if ' error' in l]
print('ad5933 rc', r.returncode, 'errors', len(errs), 'warnings', r.stderr.count('warning:'))
print('\n'.join(errs[:5]))
if r.returncode == 0:
    print(subprocess.run(['avr-size', 'ad5933.o'], cwd=here, capture_output=True, text=True).stdout)
