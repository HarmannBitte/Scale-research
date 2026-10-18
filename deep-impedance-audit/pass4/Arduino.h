// Minimal ATmega328P stub for compile-only checks. NOT an Arduino core; nothing runs.
#pragma once
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

typedef bool boolean;
typedef uint8_t byte;
#define HIGH 1
#define LOW 0
#define INPUT 0
#define OUTPUT 1
#define LSBFIRST 0
#define MSBFIRST 1
#define PROGMEM
#define bit(b) (1UL << (b))

void pinMode(uint8_t, uint8_t);
void digitalWrite(uint8_t, uint8_t);
int digitalRead(uint8_t);
unsigned long millis();
unsigned long micros();
void delay(unsigned long);
void delayMicroseconds(unsigned int);
int analogRead(uint8_t);
void analogWrite(uint8_t, int);

class HWSerial {
public:
  void begin(unsigned long) {}
  void print(const char*) {}
  void print(char) {}
  void print(int) {}
  void print(unsigned int) {}
  void print(long) {}
  void print(unsigned long) {}
  void print(double, int = 2) {}
  void println(const char* = "") {}
  void println(char) {}
  void println(int) {}
  void println(unsigned int) {}
  void println(long) {}
  void println(unsigned long) {}
  void println(double, int = 2) {}
  void write(uint8_t) {}
  void write(const char*) {}
  void write(const char*, unsigned int) {}
  int available() { return 0; }
  int read() { return -1; }
  void flush() {}
  operator bool() { return true; }
};
extern HWSerial Serial;

template <class T> inline T min(T a, T b) { return a < b ? a : b; }
template <class T> inline T max(T a, T b) { return a > b ? a : b; }
template <class T> inline T constrain(T x, T a, T b) { return x < a ? a : (x > b ? b : x); }

class String {
public:
  String() {}
  String(const char*) {}
  String(int) {}
  String(long) {}
  String(float, int = 2) {}
  String(double, int = 2) {}
  String operator+(const String&) const { return *this; }
  String& operator+=(const String&) { return *this; }
  const char* c_str() const { return ""; }
  unsigned int length() const { return 0; }
  bool equals(const char*) const { return false; }
  int toInt() const { return 0; }
  float toFloat() const { return 0; }
  void toCharArray(char*, unsigned int) const {}
};
