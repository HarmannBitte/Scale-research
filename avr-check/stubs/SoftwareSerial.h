#pragma once
#include "Arduino.h"
class SoftwareSerial : public HWSerial { public: SoftwareSerial(uint8_t,uint8_t){} void listen(){} };
