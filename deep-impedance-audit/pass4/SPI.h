#pragma once
#include "Arduino.h"
class SPIClass { public: void begin(){} void end(){} void beginTransaction(...){} void endTransaction(){} uint8_t transfer(uint8_t){return 0;} void setBitOrder(uint8_t){} void setDataMode(uint8_t){} void setClockDivider(uint8_t){} };
extern SPIClass SPI;
#define SPI_MODE0 0
#define SPI_MODE1 1
#define SPI_MODE2 2
#define SPI_MODE3 3
class SPISettings { public: SPISettings(uint32_t=0, uint8_t=0, uint8_t=0){} };
