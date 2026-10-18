#pragma once
#include "Arduino.h"
class TwoWire { public: void begin(){} void beginTransmission(uint8_t){} uint8_t endTransmission(bool=true){return 0;} size_t write(uint8_t){return 1;} size_t write(const uint8_t*,size_t){return 0;} int available(){return 0;} int read(){return -1;} uint8_t requestFrom(uint8_t,uint8_t){return 0;} void setClock(uint32_t){} };
extern TwoWire Wire;
