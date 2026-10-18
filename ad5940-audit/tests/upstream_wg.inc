/* VERBATIM EXTRACT: ADI copyright/license apply. See source/LICENSE and source/examples/ad5940lib/LICENSE. */
uint32_t AD5940_WGFreqWordCal(float SinFreqHz, float WGClock)
{
  uint32_t temp;
  uint32_t __BITWIDTH_WGFCW = 26;
  if(bIsS2silicon == bTRUE)
    __BITWIDTH_WGFCW = 30;
  if(WGClock == 0) return 0;
  temp = (uint32_t)(SinFreqHz*(1LL<<__BITWIDTH_WGFCW)/WGClock + 0.5f);
  if(temp > ((__BITWIDTH_WGFCW == 26)?0xfffff:0xffffff))
    temp = (__BITWIDTH_WGFCW == 26)?0xfffff:0xffffff;
  
  return temp;
}
