#!/usr/bin/env bash
# Compile-only AVR check (ATmega328P) of two Arduino sources against MINIMAL STUB headers.
# This is not an Arduino core build and does not run on hardware.
set -u
cd "$(dirname "$0")"
SRC=/home/user/.cache/open-projects/src/Open-Source-Projects-Collection/sources
: <<"SKIP"
import re,pathlib
p=pathlib.Path('stubs/Arduino.h');t=p.read_text()
if 'template<class T> inline T min' not in t:
    t=re.sub(r'#define min\(a,b\).*\n#define max\(a,b\).*\n#define abs\(x\).*\n#define constrain.*\n#define map.*\n',
      'template<class T> inline T min(T a,T b){return a<b?a:b;}\ntemplate<class T> inline T max(T a,T b){return a>b?a:b;}\ntemplate<class T> inline T constrain(T x,T a,T b){return x<a?a:(x>b?b:x);}\n',t)
    t+='\nclass String { public: String(){} String(const char*){} String(int){} String(long){} String(float,int=2){} String(double,int=2){} String operator+(const String&) const {return *this;} String& operator+=(const String&){return *this;} const char* c_str() const {return "";} unsigned int length() const {return 0;} bool equals(const char*) const {return false;} int toInt() const {return 0;} float toFloat() const {return 0;} };\n'
    p.write_text(t)
SKIP
FLAGS="-std=gnu++17 -Os -mmcu=atmega328p -DF_CPU=16000000UL -I stubs -Wall -c"
avr-g++ $FLAGS -o max30001.o "$SRC/Protocentral__protocentral_max30001_arduino_library/src/protocentral_max30001.cpp" > max30001-build.log 2>&1
echo "max30001 rc=$? errors=$(grep -c ' error' max30001-build.log) warnings=$(grep -c 'warning:' max30001-build.log)"
cp "$SRC/dyarleniber__AD5933-arduino-bioimpedance/AD5933.ino" ad5933_sketch.cpp
avr-g++ $FLAGS -include Arduino.h -o ad5933.o ad5933_sketch.cpp > ad5933-build.log 2>&1
echo "ad5933 rc=$? errors=$(grep -c ' error' ad5933-build.log) warnings=$(grep -c 'warning:' ad5933-build.log)"
grep ' error' max30001-build.log ad5933-build.log | head -10
avr-size max30001.o ad5933.o
