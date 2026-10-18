/* Exact host-only extracts from modified ADI library; original notice follows. */
/* MODIFIED 2026-10-17: experimental passive-bench hardening fork. NOT qualified firmware. Original ADI licenses apply. */
/**  
 * @file       ad5940.c
 * @brief      AD5940 library. This file contains all AD5940 library functions. 
 * @author     ADI
 * @date       March 2019
 * @par Revision History:
 * 
 * Copyright (c) 2017-2019 Analog Devices, Inc. All Rights Reserved.
 * 
 * This software is proprietary to Analog Devices, Inc. and its licensors.
 * By using this software you agree to the terms of the associated
 * Analog Devices Software License Agreement.
**/
AD5940Err AD5940_BenchWaitInt(uint32_t controller,uint32_t flags) {
 uint32_t n=AD5940_BENCH_POLL_LIMIT;
 while(n--) {
  BoolFlag ready=AD5940_INTCTestFlag(controller,flags);
  if(AD5940_BenchIoFault)return AD5940ERR_TIMEOUT;
  if(ready)return AD5940ERR_OK;
 }
 AD5940_BenchIoFault=AD5940ERR_TIMEOUT;return AD5940ERR_TIMEOUT;
}
static BoolFlag bench_wait_register(uint32_t reg,uint32_t mask) {
 uint32_t n=AD5940_BENCH_POLL_LIMIT;
 while(n--) {
  uint32_t v=AD5940_ReadReg(reg);
  if(AD5940_BenchIoFault)return bFALSE;
  if(v&mask)return bTRUE;
 }
 AD5940_BenchIoFault=AD5940ERR_TIMEOUT;return bFALSE;
}
void AD5940_SweepNext(SoftSweepCfg_Type *pSweepCfg, float *pNextFreq)
{
   if(!pNextFreq){AD5940_BenchIoFault=AD5940ERR_NULLP;return;}
   *pNextFreq=NAN;
   if(!pSweepCfg||pSweepCfg->SweepPoints<2||pSweepCfg->SweepIndex>=pSweepCfg->SweepPoints||
      !isfinite(pSweepCfg->SweepStart)||!isfinite(pSweepCfg->SweepStop)||
      pSweepCfg->SweepStart<=0||pSweepCfg->SweepStop<=0||pSweepCfg->SweepStart==pSweepCfg->SweepStop) {
     AD5940_BenchIoFault=AD5940ERR_PARA;return;
   }

   float frequency;

   if(pSweepCfg->SweepLog)/* Log step */
   {
      if(pSweepCfg->SweepStart<pSweepCfg->SweepStop) /* Normal */
      {
         if(++pSweepCfg->SweepIndex == pSweepCfg->SweepPoints)
            pSweepCfg->SweepIndex = 0;
         frequency = pSweepCfg->SweepStart*pow(10,pSweepCfg->SweepIndex*log10((double)pSweepCfg->SweepStop/pSweepCfg->SweepStart)/(pSweepCfg->SweepPoints-1));
      }
      else
      {
         pSweepCfg->SweepIndex --;
         if(pSweepCfg->SweepIndex >= pSweepCfg->SweepPoints)
            pSweepCfg->SweepIndex = pSweepCfg->SweepPoints-1;
         frequency = pSweepCfg->SweepStop*pow(10,pSweepCfg->SweepIndex*
                                     (log10((double)pSweepCfg->SweepStart/pSweepCfg->SweepStop)/(pSweepCfg->SweepPoints-1)));
      }
   }
   else/* Linear step */
   {
      if(pSweepCfg->SweepStart<pSweepCfg->SweepStop) /* Normal */
      {
         if(++pSweepCfg->SweepIndex == pSweepCfg->SweepPoints)
            pSweepCfg->SweepIndex = 0;
         frequency = pSweepCfg->SweepStart + pSweepCfg->SweepIndex*(double)(pSweepCfg->SweepStop-pSweepCfg->SweepStart)/(pSweepCfg->SweepPoints-1);
      }
      else
      {
         pSweepCfg->SweepIndex --;
         if(pSweepCfg->SweepIndex >= pSweepCfg->SweepPoints)
            pSweepCfg->SweepIndex = pSweepCfg->SweepPoints-1;
         frequency = pSweepCfg->SweepStop + pSweepCfg->SweepIndex*(double)(pSweepCfg->SweepStart - pSweepCfg->SweepStop)/(pSweepCfg->SweepPoints-1);
      }
   }
   
   if(!isfinite(frequency)||frequency<=0){AD5940_BenchIoFault=AD5940ERR_PARA;return;}
   *pNextFreq = frequency;
}
uint32_t AD5940_WGFreqWordCal(float SinFreqHz, float WGClock)
{
  if(!isfinite(SinFreqHz)||SinFreqHz<=0||!isfinite(WGClock)||WGClock<=0) {
    AD5940_BenchIoFault=AD5940ERR_PARA;return 0;
  }

  uint32_t temp;
  uint32_t __BITWIDTH_WGFCW = 26;
  if(bIsS2silicon == bTRUE)
    __BITWIDTH_WGFCW = 30;
  if(WGClock == 0) return 0;
  {
    double scaled=(double)SinFreqHz*(1LL<<__BITWIDTH_WGFCW)/WGClock;
    uint32_t cap=(__BITWIDTH_WGFCW==26)?0xfffffu:0xffffffu;
    if(!isfinite(scaled)||scaled>cap){AD5940_BenchIoFault=AD5940ERR_PARA;return cap;}
    temp=(uint32_t)(scaled+0.5);
  }
  if(temp > ((__BITWIDTH_WGFCW == 26)?0xfffff:0xffffff))
    temp = (__BITWIDTH_WGFCW == 26)?0xfffff:0xffffff;
  
  return temp;
}
