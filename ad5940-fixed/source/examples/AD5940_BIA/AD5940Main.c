/* MODIFIED 2026-10-17: experimental passive-bench hardening fork. NOT qualified firmware. Original ADI licenses apply. */
/*!
 *****************************************************************************
 @file:    AD5940Main.c
 @author:  Neo Xu
 @brief:   Used to control specific application and process data.
 -----------------------------------------------------------------------------

Copyright (c) 2017-2019 Analog Devices, Inc. All Rights Reserved.

This software is proprietary to Analog Devices, Inc. and its licensors.
By using this software you agree to the terms of the associated
Analog Devices Software License Agreement.
 
*****************************************************************************/
/** 
 * @addtogroup AD5940_System_Examples
 * @{
 *  @defgroup BioElec_Example
 *  @{
  */
#include "ad5940.h"
#include "BenchLog.h"
#include <stdio.h>
#include "string.h"
#include "math.h"
#include "BodyImpedance.h"

#define APPBUFF_SIZE 512
uint32_t AppBuff[APPBUFF_SIZE];

/* It's your choice here how to do with the data. Here is just an example to print them to UART */
int32_t BIAShowResult(uint32_t *pData,uint32_t DataCount)
{
 uint32_t count; (void)pData;AppBIABenchFrames(&count);
 if(count!=DataCount)return AD5940ERR_PARA;
 return AppBIABenchExportFrames();
}


/* Initialize AD5940 basic blocks like clock */
static int32_t AD5940PlatformCfg(void)
{
  CLKCfg_Type clk_cfg;
  FIFOCfg_Type fifo_cfg;
  AGPIOCfg_Type gpio_cfg;

  /* Use hardware reset */
  AD5940_HWReset();
  /* Platform configuration */
  AD5940_Initialize();
  if(AD5940_BenchIoFault)return AD5940ERR_TIMEOUT;
  /* Step1. Configure clock */
  clk_cfg.ADCClkDiv = ADCCLKDIV_1;
  clk_cfg.ADCCLkSrc = ADCCLKSRC_HFOSC;
  clk_cfg.SysClkDiv = SYSCLKDIV_1;
  clk_cfg.SysClkSrc = SYSCLKSRC_HFOSC;
  clk_cfg.HfOSC32MHzMode = bFALSE;
  clk_cfg.HFOSCEn = bTRUE;
  clk_cfg.HFXTALEn = bFALSE;
  clk_cfg.LFOSCEn = bTRUE;
  AD5940_CLKCfg(&clk_cfg);
  if(AD5940_BenchIoFault)return AD5940ERR_TIMEOUT;
  /* Step2. Configure FIFO and Sequencer*/
  fifo_cfg.FIFOEn = bFALSE;
  fifo_cfg.FIFOMode = FIFOMODE_FIFO;
  fifo_cfg.FIFOSize = FIFOSIZE_4KB;                       /* 4kB for FIFO, The reset 2kB for sequencer */
  fifo_cfg.FIFOSrc = FIFOSRC_DFT;
  fifo_cfg.FIFOThresh = 4;//AppBIACfg.FifoThresh;        /* DFT result. One pair for RCAL, another for Rz. One DFT result have real part and imaginary part */
  AD5940_FIFOCfg(&fifo_cfg);                             /* Disable to reset FIFO. */
  fifo_cfg.FIFOEn = bTRUE;  
  AD5940_FIFOCfg(&fifo_cfg);                             /* Enable FIFO here */
  
  /* Step3. Interrupt controller */
  
  AD5940_INTCCfg(AFEINTC_1, AFEINTSRC_ALLINT, bTRUE);           /* Enable all interrupt in Interrupt Controller 1, so we can check INTC flags */
  AD5940_INTCCfg(AFEINTC_0, AFEINTSRC_DATAFIFOTHRESH, bTRUE);   /* Interrupt Controller 0 will control GP0 to generate interrupt to MCU */
  AD5940_INTCClrFlag(AFEINTSRC_ALLINT);
  /* Step4: Reconfigure GPIO */
  gpio_cfg.FuncSet = GP6_SYNC|GP5_SYNC|GP4_SYNC|GP2_TRIG|GP1_SYNC|GP0_INT;
  gpio_cfg.InputEnSet = AGPIO_Pin2;
  gpio_cfg.OutputEnSet = AGPIO_Pin0|AGPIO_Pin1|AGPIO_Pin4|AGPIO_Pin5|AGPIO_Pin6;
  gpio_cfg.OutVal = 0;
  gpio_cfg.PullEnSet = 0;

  AD5940_AGPIOCfg(&gpio_cfg);
  AD5940_SleepKeyCtrlS(SLPKEY_UNLOCK);  /* Allow AFE to enter sleep mode. */
  return 0;
}

/* !!Change the application parameters here if you want to change it to none-default value */
void AD5940BIAStructInit(void)
{
  AppBIACfg_Type *pBIACfg;
  
  AppBIAGetCfg(&pBIACfg);
  
  pBIACfg->MinCurrentDftMagnitude = BIA_BENCH_MIN_CURRENT_COUNTS; /* REQUIRED: replace only with characterized bench threshold. */
  pBIACfg->SeqStartAddr = 0;
  pBIACfg->MaxSeqLen = 512; /** @todo add checker in function */
  
  pBIACfg->RcalVal = BIA_BENCH_RCAL_OHM; /* Independently characterized standard, not an assumed nominal. */
  pBIACfg->DftNum = DFTNUM_8192;
  pBIACfg->NumOfData = -1;      /* Never stop until you stop it manually by AppBIACtrl() function */
  pBIACfg->BiaODR = 20;         /* ODR(Sample Rate) 20Hz */
  pBIACfg->FifoThresh = 4;      /* 4 */
  pBIACfg->ADCSinc3Osr = ADCSINC3OSR_2;
}

void AD5940_Main(void)
{
 AD5940Err error;uint32_t count;
 if(BenchLogBegin(BIA_BENCH_RUN_ID)!=AD5940ERR_OK)return;
 /* Unarmed default must never start platform/AFE excitation. */
 AD5940BIAStructInit();
 if(AppBIAValidateConfig()!=AD5940ERR_OK) {AppBIABenchExportFault(AD5940ERR_PARA);return;}
 error=AD5940PlatformCfg();
 if(error!=AD5940ERR_OK){AppBIABenchAbort(error);AppBIABenchExportFault(error);return;}
 error=AppBIAInit(AppBuff,APPBUFF_SIZE);
 if(error!=AD5940ERR_OK){AppBIABenchAbort(error);AppBIABenchExportFault(error);return;}
 if(AppBIABenchExportConfig()!=AD5940ERR_OK){AppBIABenchAbort(AD5940ERR_ERROR);return;}
 error=AppBIACtrl(BIACTRL_START,0);
 if(error!=AD5940ERR_OK){AppBIABenchAbort(error);AppBIABenchExportFault(error);return;}
 while(1) {
  if(AD5940_BenchIoFault){AppBIABenchAbort(AD5940ERR_ERROR);AppBIABenchExportFault(AD5940ERR_TIMEOUT);return;}
  if(AD5940_GetMCUIntFlag()) {
   AD5940_ClrMCUIntFlag();count=APPBUFF_SIZE;
   error=AppBIAISR(AppBuff,&count);
   if(error!=AD5940ERR_OK) {
    /* Raw invalid frames, if captured, remain available; never format a stale count. */
    AppBIABenchExportFrames();AppBIABenchExportFault(error);return;
   }
   if(BIAShowResult(AppBuff,count)!=AD5940ERR_OK){AppBIABenchAbort(AD5940ERR_ERROR);return;}
   { AppBIACfg_Type *cfg;
     if(AppBIAGetCfg(&cfg)!=AD5940ERR_OK){AppBIABenchAbort(AD5940ERR_APPERROR);return;}
     if(cfg->StopRequired){AppBIABenchAbort(AD5940ERR_OK);AppBIABenchExportEnd();return;}
   }
  }
 }
}


/**
 * @}
 * @}
 * */
 
