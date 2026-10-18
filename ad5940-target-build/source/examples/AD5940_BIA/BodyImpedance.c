/* MODIFIED again 2026-10-17: fail-stop sequence-generation errors; experimental passive-bench hardening fork. NOT qualified firmware. Original ADI licenses apply. */
/*!
 *****************************************************************************
 @file:    BodyComposition.c
 @author:  Neo Xu
 @brief:   BIA measurement sequences.
 -----------------------------------------------------------------------------
Copyright (c) 2017-2019 Analog Devices, Inc. All Rights Reserved.
This software is proprietary to Analog Devices, Inc. and its licensors.
By using this software you agree to the terms of the associated
Analog Devices Software License Agreement.
 
*****************************************************************************/
#include "BodyImpedance.h"
#include "BenchLog.h"
#include <float.h>
#include <limits.h>

/* 
  Application configuration structure. Specified by user from template.
  The variables are usable in this whole application.
  It includes basic configuration for sequencer generator and application related parameters
*/
AppBIACfg_Type AppBIACfg = 
{
  .bParaChanged = bFALSE,
  .SeqStartAddr = 0,
  .MaxSeqLen = 0,
  
  .SeqStartAddrCal = 0,
  .MaxSeqLenCal = 0,

  .ReDoRtiaCal = bFALSE,
  .SysClkFreq = 16000000.0,
  .WuptClkFreq = 32000.0,
  .AdcClkFreq = 16000000.0,
  .BiaODR = 20.0, /* 20.0 Hz*/
  .NumOfData = -1,
  .RcalVal = 10000.0, /* 10kOhm */

  .PwrMod = AFEPWR_LP,
  .HstiaRtiaSel = HSTIARTIA_1K,
  .CtiaSel = 16,
  .ExcitBufGain = EXCITBUFGAIN_2,
  .HsDacGain = HSDACGAIN_1,
  .HsDacUpdateRate = 7,
  .DacVoltPP = 800.0,

  .SinFreq = 50000.0, /* 50kHz */

  .ADCPgaGain = ADCPGA_1,
  .ADCSinc3Osr = ADCSINC3OSR_2,
  .ADCSinc2Osr = ADCSINC2OSR_22,

  .DftNum = DFTNUM_8192,
  .DftSrc = DFTSRC_SINC3,
  .HanWinEn = bTRUE,

  .SweepCfg.SweepEn = bFALSE,
  .SweepCfg.SweepStart = 10000,
  .SweepCfg.SweepStop = 150000.0,
  .SweepCfg.SweepPoints = 100,
  .SweepCfg.SweepLog = bTRUE,
  .SweepCfg.SweepIndex = 0,

  .FifoThresh = 4,
  .BIAInited = bFALSE,
  .StopRequired = bFALSE,
  .MeasSeqCycleCount = 0,
};

/* Private zero-initialized snapshot excludes runtime state, pointers and padding. */
typedef struct { float sys, adc, wake, odr, freq, rcal, amplitude, floor;
 uint32_t pwr, rtia, ctia, egain, dgain, update, pga, osr3, osr2, dft, src, window, threshold;
} BenchSignature;
static BenchSignature CalSignature;
static BoolFlag CalValid = bFALSE;
static float ExpectedRtia[2];
static uint32_t CalId, ConfigId, FrameSequence, FrameCount;
static uint32_t LastInterruptFlags,LastFifoWords,LastCapacity;
static BIABenchFrame Frames[BIA_BENCH_MAX_FRAMES];
static BenchSignature signature(void) {
 BenchSignature s; memset(&s,0,sizeof(s));
 s.sys=AppBIACfg.SysClkFreq;s.adc=AppBIACfg.AdcClkFreq;s.wake=AppBIACfg.WuptClkFreq;
 s.odr=AppBIACfg.BiaODR;s.freq=AppBIACfg.SinFreq;s.rcal=AppBIACfg.RcalVal;
 s.amplitude=AppBIACfg.DacVoltPP;s.floor=AppBIACfg.MinCurrentDftMagnitude;
 s.pwr=AppBIACfg.PwrMod;s.rtia=AppBIACfg.HstiaRtiaSel;s.ctia=AppBIACfg.CtiaSel;
 s.egain=AppBIACfg.ExcitBufGain;s.dgain=AppBIACfg.HsDacGain;s.update=AppBIACfg.HsDacUpdateRate;
 s.pga=AppBIACfg.ADCPgaGain;s.osr3=AppBIACfg.ADCSinc3Osr;s.osr2=AppBIACfg.ADCSinc2Osr;
 s.dft=AppBIACfg.DftNum;s.src=AppBIACfg.DftSrc;s.window=AppBIACfg.HanWinEn;s.threshold=AppBIACfg.FifoThresh;
 return s;
}
BoolFlag AppBIABenchCalibrationValid(void) {
 BenchSignature s=signature();
 return CalValid && isfinite(AppBIACfg.RtiaCurrValue[0]) && AppBIACfg.RtiaCurrValue[0]>0 &&
        isfinite(AppBIACfg.RtiaCurrValue[1]) && AppBIACfg.RtiaCurrValue[0]==ExpectedRtia[0] &&
        AppBIACfg.RtiaCurrValue[1]==ExpectedRtia[1] && !AppBIACfg.SweepCfg.SweepEn && !AppBIACfg.ReDoRtiaCal &&
        !AppBIACfg.bParaChanged && memcmp(&s,&CalSignature,sizeof(s))==0;
}
void AppBIABenchInvalidate(void) {
 CalValid=bFALSE;AppBIACfg.RtiaCurrValue[0]=0;AppBIACfg.RtiaCurrValue[1]=0;
}
const BIABenchFrame *AppBIABenchFrames(uint32_t *count) {
 if(count)*count=FrameCount;return Frames;
}
AD5940Err AppBIAValidateConfig(void) {
 /* First hardened integration deliberately refuses sweeps and clock variants.
    Range checks are software bounds, NOT verified analog performance. */
 if(!BIA_BENCH_ARMED || AppBIACfg.SweepCfg.SweepEn) return AD5940ERR_PARA;
 if(!isfinite(AppBIACfg.SinFreq)||AppBIACfg.SinFreq!=50000.0f ||
    !isfinite(AppBIACfg.RcalVal)||AppBIACfg.RcalVal<=0 ||
    !isfinite(AppBIACfg.MinCurrentDftMagnitude)||AppBIACfg.MinCurrentDftMagnitude<=0 ||
    !isfinite(AppBIACfg.BiaODR)||AppBIACfg.BiaODR<=0||AppBIACfg.BiaODR>20 ||
    !isfinite(AppBIACfg.DacVoltPP)||AppBIACfg.DacVoltPP<=0||AppBIACfg.DacVoltPP>800 ||
    AppBIACfg.SysClkFreq!=16000000.0f||AppBIACfg.AdcClkFreq!=16000000.0f||
    !isfinite(AppBIACfg.WuptClkFreq)||AppBIACfg.WuptClkFreq<=0||
    AppBIACfg.WuptClkFreq/AppBIACfg.BiaODR<4 ||
    AppBIACfg.WuptClkFreq/AppBIACfg.BiaODR>1073741824.0f ||
    AppBIACfg.FifoThresh<4||AppBIACfg.FifoThresh>4*BIA_BENCH_MAX_FRAMES ||
    AppBIACfg.FifoThresh%4||AppBIACfg.DftNum>DFTNUM_16384 ||
    AppBIACfg.DftSrc!=DFTSRC_SINC3 ||AppBIACfg.ADCSinc3Osr!=ADCSINC3OSR_2 ||
    AppBIACfg.ADCSinc2Osr!=ADCSINC2OSR_22 ||AppBIACfg.ADCPgaGain!=ADCPGA_1 ||
    AppBIACfg.HstiaRtiaSel!=HSTIARTIA_1K||AppBIACfg.CtiaSel!=16 ||
    AppBIACfg.ExcitBufGain!=EXCITBUFGAIN_2||AppBIACfg.HsDacGain!=HSDACGAIN_1 ||
    AppBIACfg.HsDacUpdateRate!=7||AppBIACfg.PwrMod!=AFEPWR_LP ||
    AppBIACfg.HanWinEn!=bTRUE||AppBIACfg.SeqStartAddr!=0||AppBIACfg.MaxSeqLen!=512) return AD5940ERR_PARA;
 return AD5940ERR_OK;
}
static AD5940Err bench_stop(AD5940Err error) {
 AppBIABenchInvalidate();AppBIACfg.BIAInited=bFALSE;
 /* Disable software recording first: shutdown writes must reach hardware. */
 AD5940_SEQGenCtrl(bFALSE);
 if(AD5940_BenchIoFault){AD5940_RstClr();return error;}
 AD5940_WUPTCtrl(bFALSE);
 AD5940_AFECtrlS(AFECTRL_ADCCNV|AFECTRL_DFT|AFECTRL_WG|AFECTRL_ADCPWR,bFALSE);
 AD5940_SEQCtrlS(bFALSE);
 AD5940_SleepKeyCtrlS(SLPKEY_UNLOCK);
 return error;
}
AD5940Err AppBIABenchAbort(AD5940Err error){return bench_stop(error);}
AD5940Err AppBIADecodeFrame(const uint32_t raw[4],BIABenchFrame *out,
                          const float rtia[2],float min_current) {
 double cr,ci,vr,vi,cm,mag,ph;
 uint32_t i;
 if(!out)return AD5940ERR_NULLP;
 memset(out,0,sizeof(*out));out->status=AD5940ERR_PARA;
 if(!raw||!rtia){out->status=AD5940ERR_NULLP;return out->status;}
 for(i=0;i<4;i++) {
  uint32_t v=raw[i]&0x3ffffu;out->raw[i]=raw[i];
  out->dft[i]=(v&0x20000u)?(int32_t)v-262144:(int32_t)v;
 }
 if(!isfinite(rtia[0])||rtia[0]<=0||!isfinite(rtia[1])||
    !isfinite(min_current)||min_current<=0)return out->status;
 cr=out->dft[0];ci=-out->dft[1];vr=out->dft[2];vi=-out->dft[3];
 cm=sqrt(cr*cr+ci*ci);
 if(cm<min_current){out->status=AD5940ERR_CALOR;return out->status;}
 mag=sqrt(vr*vr+vi*vi)/cm*rtia[0];
 ph=atan2(vi,vr)-atan2(ci,cr)+rtia[1];
 ph=atan2(sin(ph),cos(ph));
 if(!isfinite(mag)||mag>FLT_MAX||!isfinite(ph))return out->status;
 out->magnitude=(float)mag;out->phase_rad=(float)ph;
 out->r=(float)(mag*cos(ph));out->x=(float)(mag*sin(ph));
 if(!isfinite(out->r)||!isfinite(out->x))return out->status;
 out->status=AD5940ERR_OK;return AD5940ERR_OK;
}

/**
   This function is provided for upper controllers that want to change 
   application parameters specially for user defined parameters.
*/
AD5940Err AppBIAGetCfg(void *pCfg)
{
  if(pCfg){
    *(AppBIACfg_Type**)pCfg = &AppBIACfg;
    return AD5940ERR_OK;
  }
  return AD5940ERR_PARA;
}

AD5940Err AppBIACtrl(int32_t BcmCtrl, void *pPara)
{
  switch (BcmCtrl)
  {
    case BIACTRL_START:
    {
      WUPTCfg_Type wupt_cfg;
      if(AppBIAValidateConfig()!=AD5940ERR_OK||!AppBIABenchCalibrationValid()||AD5940_BenchIoFault) return AD5940ERR_CALOR;
      if(AD5940_WakeUp(10) > 10)  /* Wakeup AFE by read register, read 10 times at most */
        return AD5940ERR_WAKEUP;  /* Wakeup Failed */
      if(AppBIACfg.BIAInited == bFALSE)
        return AD5940ERR_APPERROR;
      /* Start it */
      wupt_cfg.WuptEn = bTRUE;
      wupt_cfg.WuptEndSeq = WUPTENDSEQ_A;
      wupt_cfg.WuptOrder[0] = SEQID_0;
      wupt_cfg.SeqxSleepTime[SEQID_0] = (uint32_t)(AppBIACfg.WuptClkFreq/AppBIACfg.BiaODR)-2-1;
      wupt_cfg.SeqxWakeupTime[SEQID_0] = 1; /* The minimum value is 1. Do not set it to zero. Set it to 1 will spend 2 32kHz clock. */
      AD5940_WUPTCfg(&wupt_cfg);
      
      AppBIACfg.FifoDataCount = 0;  /* restart */
      break;
    }
    case BIACTRL_STOPNOW:
    {
      if(AD5940_WakeUp(10) > 10)  /* Wakeup AFE by read register, read 10 times at most */
        return AD5940ERR_WAKEUP;  /* Wakeup Failed */
      /* Start Wupt right now */
      AD5940_WUPTCtrl(bFALSE);
      /* There is chance this operation will fail because sequencer could put AFE back 
        to hibernate mode just after waking up. Use STOPSYNC is better. */
      AD5940_WUPTCtrl(bFALSE);
      break;
    }
    case BIACTRL_STOPSYNC:
    {
      AppBIACfg.StopRequired = bTRUE;
      break;
    }
    case BIACTRL_GETFREQ:
    if(pPara)
    {
      if(AppBIACfg.SweepCfg.SweepEn == bTRUE)
        *(float*)pPara = AppBIACfg.FreqofData;
      else
        *(float*)pPara = AppBIACfg.SinFreq;
    }
    break;
    case BIACTRL_SHUTDOWN:
    {
      AppBIACtrl(BIACTRL_STOPNOW, 0);  /* Stop the measurement if it's running. */
      /* Turn off LPloop related blocks which are not controlled automatically by sleep operation */
      AFERefCfg_Type aferef_cfg;
      LPLoopCfg_Type lp_loop;
      memset(&aferef_cfg, 0, sizeof(aferef_cfg));
      AD5940_REFCfgS(&aferef_cfg);
      memset(&lp_loop, 0, sizeof(lp_loop));
      AD5940_LPLoopCfgS(&lp_loop);
      AD5940_EnterSleepS();  /* Enter Hibernate */
    }
    break;
    default:
    break;
  }
  return AD5940ERR_OK;
}

/* Generate init sequence */
static AD5940Err AppBIASeqCfgGen(void)
{
  AD5940Err error = AD5940ERR_OK;
  uint32_t const *pSeqCmd;
  uint32_t SeqLen;

  AFERefCfg_Type aferef_cfg;
  HSLoopCfg_Type hs_loop;
  LPLoopCfg_Type lp_loop;
  DSPCfg_Type dsp_cfg;
  float sin_freq;

  /* Start sequence generator here */
  AD5940_SEQGenCtrl(bTRUE);

  //AD5940_AFECtrlS(AFECTRL_ALL, bFALSE);  /* Init all to disable state */

  aferef_cfg.HpBandgapEn = bTRUE;
  aferef_cfg.Hp1V1BuffEn = bTRUE;
  aferef_cfg.Hp1V8BuffEn = bTRUE;
  aferef_cfg.Disc1V1Cap = bFALSE;
  aferef_cfg.Disc1V8Cap = bFALSE;
  aferef_cfg.Hp1V8ThemBuff = bFALSE;
  aferef_cfg.Hp1V8Ilimit = bFALSE;
  aferef_cfg.Lp1V1BuffEn = bFALSE;
  aferef_cfg.Lp1V8BuffEn = bFALSE;
  /* LP reference control - turn off them to save power*/
  aferef_cfg.LpBandgapEn = bTRUE;
  aferef_cfg.LpRefBufEn = bTRUE;
  aferef_cfg.LpRefBoostEn = bFALSE;
  AD5940_REFCfgS(&aferef_cfg);	
  hs_loop.HsDacCfg.ExcitBufGain = AppBIACfg.ExcitBufGain;
  hs_loop.HsDacCfg.HsDacGain = AppBIACfg.HsDacGain;
  hs_loop.HsDacCfg.HsDacUpdateRate = AppBIACfg.HsDacUpdateRate;

  hs_loop.HsTiaCfg.DiodeClose = bFALSE;
  hs_loop.HsTiaCfg.HstiaBias = HSTIABIAS_1P1;
  hs_loop.HsTiaCfg.HstiaCtia = AppBIACfg.CtiaSel; /* 31pF + 2pF */
  hs_loop.HsTiaCfg.HstiaDeRload = HSTIADERLOAD_OPEN;
  hs_loop.HsTiaCfg.HstiaDeRtia = HSTIADERTIA_OPEN;
  hs_loop.HsTiaCfg.HstiaRtiaSel = AppBIACfg.HstiaRtiaSel;

  hs_loop.SWMatCfg.Dswitch = SWD_OPEN;
  hs_loop.SWMatCfg.Pswitch = SWP_PL|SWP_PL2;
  hs_loop.SWMatCfg.Nswitch = SWN_NL|SWN_NL2;
  hs_loop.SWMatCfg.Tswitch = SWT_TRTIA;

  hs_loop.WgCfg.WgType = WGTYPE_SIN;
  hs_loop.WgCfg.GainCalEn = bFALSE;
  hs_loop.WgCfg.OffsetCalEn = bFALSE;
  if(AppBIACfg.SweepCfg.SweepEn == bTRUE)
  {
		AppBIACfg.SweepCfg.SweepIndex = 0;
    AppBIACfg.FreqofData = AppBIACfg.SweepCfg.SweepStart;
    AppBIACfg.SweepCurrFreq = AppBIACfg.SweepCfg.SweepStart;
    AD5940_SweepNext(&AppBIACfg.SweepCfg, &AppBIACfg.SweepNextFreq);
    sin_freq = AppBIACfg.SweepCurrFreq;
  }
  else
  {
    sin_freq = AppBIACfg.SinFreq;
    AppBIACfg.FreqofData = sin_freq;
  }
  hs_loop.WgCfg.SinCfg.SinFreqWord = AD5940_WGFreqWordCal(sin_freq, AppBIACfg.SysClkFreq);
  hs_loop.WgCfg.SinCfg.SinAmplitudeWord = (uint32_t)(AppBIACfg.DacVoltPP/800.0f*2047 + 0.5f);
  hs_loop.WgCfg.SinCfg.SinOffsetWord = 0;
  hs_loop.WgCfg.SinCfg.SinPhaseWord = 0;
  AD5940_HSLoopCfgS(&hs_loop);

  lp_loop.LpDacCfg.LpdacSel = LPDAC0;
  lp_loop.LpDacCfg.LpDacSrc = LPDACSRC_MMR;
  lp_loop.LpDacCfg.LpDacSW = LPDACSW_VBIAS2LPPA|LPDACSW_VBIAS2PIN|LPDACSW_VZERO2LPTIA|LPDACSW_VZERO2PIN;
  lp_loop.LpDacCfg.LpDacVzeroMux = LPDACVZERO_6BIT;
  lp_loop.LpDacCfg.LpDacVbiasMux = LPDACVBIAS_12BIT;
  lp_loop.LpDacCfg.LpDacRef = LPDACREF_2P5;
  lp_loop.LpDacCfg.DataRst = bFALSE;
  lp_loop.LpDacCfg.PowerEn = bTRUE;
  lp_loop.LpDacCfg.DacData12Bit = (uint32_t)((1100-200)/2200.0*4095);
  lp_loop.LpDacCfg.DacData6Bit = 31;

  lp_loop.LpAmpCfg.LpAmpSel = LPAMP0;
  lp_loop.LpAmpCfg.LpAmpPwrMod = LPAMPPWR_NORM;
  lp_loop.LpAmpCfg.LpPaPwrEn = bTRUE;
  lp_loop.LpAmpCfg.LpTiaPwrEn = bTRUE;
  lp_loop.LpAmpCfg.LpTiaRf = LPTIARF_20K;
  lp_loop.LpAmpCfg.LpTiaRload = LPTIARLOAD_SHORT;
  lp_loop.LpAmpCfg.LpTiaRtia = LPTIARTIA_OPEN;
  lp_loop.LpAmpCfg.LpTiaSW = LPTIASW(5)|LPTIASW(6)|LPTIASW(7)|LPTIASW(8)|LPTIASW(9)|LPTIASW(12)|LPTIASW(13); /** @todo Optimization needed for new silicon */
  AD5940_LPLoopCfgS(&lp_loop);

  dsp_cfg.ADCBaseCfg.ADCMuxN = ADCMUXN_HSTIA_N;
  dsp_cfg.ADCBaseCfg.ADCMuxP = ADCMUXP_HSTIA_P;
  dsp_cfg.ADCBaseCfg.ADCPga = AppBIACfg.ADCPgaGain;
  
  memset(&dsp_cfg.ADCDigCompCfg, 0, sizeof(dsp_cfg.ADCDigCompCfg));
  
  dsp_cfg.ADCFilterCfg.ADCAvgNum = ADCAVGNUM_16;  /* Don't care because it's disabled */
  dsp_cfg.ADCFilterCfg.ADCRate = ADCRATE_800KHZ;	/* Tell filter block clock rate of ADC*/
  dsp_cfg.ADCFilterCfg.ADCSinc2Osr = AppBIACfg.ADCSinc2Osr;
  dsp_cfg.ADCFilterCfg.ADCSinc3Osr = AppBIACfg.ADCSinc3Osr;
  dsp_cfg.ADCFilterCfg.BpSinc3 = bFALSE;
  dsp_cfg.ADCFilterCfg.BpNotch = bTRUE;
  dsp_cfg.ADCFilterCfg.Sinc2NotchEnable = bTRUE;
  dsp_cfg.DftCfg.DftNum = AppBIACfg.DftNum;
  dsp_cfg.DftCfg.DftSrc = AppBIACfg.DftSrc;
  dsp_cfg.DftCfg.HanWinEn = AppBIACfg.HanWinEn;
  
  memset(&dsp_cfg.StatCfg, 0, sizeof(dsp_cfg.StatCfg)); /* Don't care about Statistic */
  AD5940_DSPCfgS(&dsp_cfg);
    
  /* Enable all of them. They are automatically turned off during hibernate mode to save power */
  AD5940_AFECtrlS(AFECTRL_HPREFPWR|AFECTRL_HSTIAPWR|AFECTRL_INAMPPWR|AFECTRL_EXTBUFPWR|\
                AFECTRL_WG|AFECTRL_DACREFPWR|AFECTRL_HSDACPWR|\
                AFECTRL_SINC2NOTCH, bTRUE);
  AD5940_SEQGpioCtrlS(0/*AGPIO_Pin6|AGPIO_Pin5|AGPIO_Pin1*/);        //GP6->endSeq, GP5 -> AD8233=OFF, GP1->RLD=OFF .
  
  /* Sequence end. */
  AD5940_SEQGenInsert(SEQ_STOP()); /* Add one extra command to disable sequencer for initialization sequence because we only want it to run one time. */

  /* Stop here */
  error = AD5940_SEQGenFetchSeq(&pSeqCmd, &SeqLen);
  AD5940_SEQGenCtrl(bFALSE); /* Stop sequencer generator */
  if(error == AD5940ERR_OK)
  {
    AppBIACfg.InitSeqInfo.SeqId = SEQID_1;
    AppBIACfg.InitSeqInfo.SeqRamAddr = AppBIACfg.SeqStartAddr;
    AppBIACfg.InitSeqInfo.pSeqCmd = pSeqCmd;
    AppBIACfg.InitSeqInfo.SeqLen = SeqLen;
    /* Write command to SRAM */
    AD5940_SEQCmdWrite(AppBIACfg.InitSeqInfo.SeqRamAddr, pSeqCmd, SeqLen);
  }
  else
    return error; /* Error */
  return AD5940ERR_OK;
}

static AD5940Err AppBIASeqMeasureGen(void)
{
  AD5940Err error = AD5940ERR_OK;
  uint32_t const *pSeqCmd;
  uint32_t SeqLen;

  uint32_t WaitClks;
  SWMatrixCfg_Type sw_cfg;
  ClksCalInfo_Type clks_cal;
  
  clks_cal.DataType = DATATYPE_DFT;
  clks_cal.DftSrc = AppBIACfg.DftSrc;
  clks_cal.DataCount = 1L<<(AppBIACfg.DftNum+2); /* 2^(DFTNUMBER+2) */
  clks_cal.ADCSinc2Osr = AppBIACfg.ADCSinc2Osr;
  clks_cal.ADCSinc3Osr = AppBIACfg.ADCSinc3Osr;
  clks_cal.ADCAvgNum = 0;
  clks_cal.RatioSys2AdcClk = AppBIACfg.SysClkFreq/AppBIACfg.AdcClkFreq;
  AD5940_ClksCalculate(&clks_cal, &WaitClks);

  /* Start sequence generator here */
  AD5940_SEQGenCtrl(bTRUE);
  
  AD5940_SEQGpioCtrlS(AGPIO_Pin6/*|AGPIO_Pin5|AGPIO_Pin1*/);//GP6->endSeq, GP5 -> AD8233=OFF, GP1->RLD=OFF .
  
  AD5940_SEQGenInsert(SEQ_WAIT(16*250));  /* @todo wait 250us?? */
  sw_cfg.Dswitch = SWD_CE0;
  sw_cfg.Pswitch = SWP_CE0;
  sw_cfg.Nswitch = SWN_AIN1;
  sw_cfg.Tswitch = SWT_AIN1|SWT_TRTIA;
  AD5940_SWMatrixCfgS(&sw_cfg);
  
  AD5940_ADCMuxCfgS(ADCMUXP_HSTIA_P, ADCMUXN_HSTIA_N);
  AD5940_AFECtrlS(AFECTRL_WG|AFECTRL_ADCPWR, bTRUE);  /* Enable Waveform generator, ADC power */
  AD5940_SEQGenInsert(SEQ_WAIT(16*50));
  AD5940_AFECtrlS(AFECTRL_ADCCNV|AFECTRL_DFT, bTRUE);  /* Start ADC convert and DFT */
  AD5940_SEQGenInsert(SEQ_WAIT(WaitClks));  /* wait for first data ready */  
  AD5940_AFECtrlS(AFECTRL_ADCCNV|AFECTRL_DFT|AFECTRL_WG|AFECTRL_ADCPWR, bFALSE);  /* Stop ADC convert and DFT */

  AD5940_ADCMuxCfgS(ADCMUXP_AIN3, ADCMUXN_AIN2);
  AD5940_AFECtrlS(AFECTRL_WG|AFECTRL_ADCPWR, bTRUE);  /* Enable Waveform generator, ADC power */
  AD5940_SEQGenInsert(SEQ_WAIT(16*50));  //delay for signal settling DFT_WAIT
  AD5940_AFECtrlS(AFECTRL_ADCCNV|AFECTRL_DFT, bTRUE);  /* Start ADC convert and DFT */
  AD5940_SEQGenInsert(SEQ_WAIT(WaitClks));  /* wait for first data ready */
  AD5940_AFECtrlS(AFECTRL_ADCCNV|AFECTRL_DFT|AFECTRL_WG|AFECTRL_ADCPWR, bFALSE);  /* Stop ADC convert and DFT */
  
  sw_cfg.Dswitch = SWD_OPEN;
  sw_cfg.Pswitch = SWP_PL|SWP_PL2;
  sw_cfg.Nswitch = SWN_NL|SWN_NL2;
  sw_cfg.Tswitch = SWT_TRTIA;
  AD5940_SWMatrixCfgS(&sw_cfg); /* Float switches */

  AD5940_SEQGpioCtrlS(0/*AGPIO_Pin6|AGPIO_Pin5|AGPIO_Pin1*/);        //GP6->endSeq, GP5 -> AD8233=OFF, GP1->RLD=OFF .
  AD5940_EnterSleepS();/* Goto hibernate */
  /* Sequence end. */
  error = AD5940_SEQGenFetchSeq(&pSeqCmd, &SeqLen);
  AD5940_SEQGenCtrl(bFALSE); /* Stop sequencer generator */

  AppBIACfg.MeasSeqCycleCount = AD5940_SEQCycleTime();
  AppBIACfg.MaxODR = 1/(((AppBIACfg.MeasSeqCycleCount + 10) / 16.0)* 1E-6)  ;
  if(AppBIACfg.BiaODR > AppBIACfg.MaxODR)
  {
    /* We have requested a sampling rate that cannot be achieved with the time it
       takes to acquire a sample.
    */
    AppBIACfg.BiaODR = AppBIACfg.MaxODR;
    if(!isfinite(AppBIACfg.BiaODR)||AppBIACfg.BiaODR<=0)return AD5940ERR_PARA;
  }

  if(error == AD5940ERR_OK)
  {
    AppBIACfg.MeasureSeqInfo.SeqId = SEQID_0;
    AppBIACfg.MeasureSeqInfo.SeqRamAddr = AppBIACfg.InitSeqInfo.SeqRamAddr + AppBIACfg.InitSeqInfo.SeqLen ;
    AppBIACfg.MeasureSeqInfo.pSeqCmd = pSeqCmd;
    AppBIACfg.MeasureSeqInfo.SeqLen = SeqLen;
    /* Write command to SRAM */
    AD5940_SEQCmdWrite(AppBIACfg.MeasureSeqInfo.SeqRamAddr, pSeqCmd, SeqLen);
  }
  else
    return error; /* Error */
  return AD5940ERR_OK;
}

static AD5940Err AppBIARtiaCal(void)
{
 HSRTIACal_Type c;AD5940Err e;float result[2]={0,0};
 AppBIABenchInvalidate();memset(&AD5940_BenchCalTrace,0,sizeof(AD5940_BenchCalTrace));
 if(AppBIAValidateConfig()!=AD5940ERR_OK)return AD5940ERR_PARA;
 if(CalId==UINT32_MAX)return AD5940ERR_APPERROR;
 ++CalId;memset(&c,0,sizeof(c));
 c.AdcClkFreq=AppBIACfg.AdcClkFreq;c.SysClkFreq=AppBIACfg.SysClkFreq;
 c.ADCSinc2Osr=AppBIACfg.ADCSinc2Osr;c.ADCSinc3Osr=AppBIACfg.ADCSinc3Osr;
 c.bPolarResult=bTRUE;c.DftCfg.DftNum=AppBIACfg.DftNum;c.DftCfg.DftSrc=AppBIACfg.DftSrc;
 c.DftCfg.HanWinEn=AppBIACfg.HanWinEn;c.fRcal=AppBIACfg.RcalVal;c.fFreq=AppBIACfg.SinFreq;
 c.HsTiaCfg.HstiaBias=HSTIABIAS_1P1;c.HsTiaCfg.HstiaCtia=AppBIACfg.CtiaSel;
 c.HsTiaCfg.HstiaDeRload=HSTIADERLOAD_OPEN;c.HsTiaCfg.HstiaDeRtia=HSTIADERTIA_TODE;
 c.HsTiaCfg.HstiaRtiaSel=AppBIACfg.HstiaRtiaSel;
 e=AD5940_HSRtiaCal(&c,result);
 if(e!=AD5940ERR_OK)return e;
 if(AD5940_BenchIoFault)return AD5940ERR_TIMEOUT;
 if(!isfinite(result[0])||result[0]<=0||!isfinite(result[1]))return AD5940ERR_CALOR;
 AppBIACfg.RtiaCurrValue[0]=result[0];AppBIACfg.RtiaCurrValue[1]=result[1];
 ExpectedRtia[0]=result[0];ExpectedRtia[1]=result[1];
 CalSignature=signature();CalValid=bTRUE;
 return AD5940ERR_OK;
}


/* This function provide application initialize.   */
AD5940Err AppBIAInit(uint32_t *pBuffer, uint32_t BufferSize)
{
  AD5940Err error = AD5940ERR_OK;
  SEQCfg_Type seq_cfg;
  FIFOCfg_Type fifo_cfg;

  if(AppBIACfg.BIAInited)bench_stop(AD5940ERR_APPERROR);
  FrameCount=0;AppBIABenchInvalidate();AppBIACfg.BIAInited=bFALSE;
  if(AppBIAValidateConfig()!=AD5940ERR_OK)return AD5940ERR_PARA;
  if(!pBuffer||BufferSize==0||BufferSize<512||AppBIACfg.MaxSeqLen>BufferSize)
    return AD5940ERR_BUFF;
  if(AD5940_BenchIoFault)return AD5940ERR_TIMEOUT;
  if(AD5940_WakeUp(10) > 10)  /* Wakeup AFE by read register, read 10 times at most */
    return AD5940ERR_WAKEUP;  /* Wakeup Failed */

  /* Configure sequencer and stop it */
  seq_cfg.SeqMemSize = SEQMEMSIZE_2KB;  /* 2kB SRAM is used for sequencer, others for data FIFO */
  seq_cfg.SeqBreakEn = bFALSE;
  seq_cfg.SeqIgnoreEn = bFALSE;
  seq_cfg.SeqCntCRCClr = bTRUE;
  seq_cfg.SeqEnable = bFALSE;
  seq_cfg.SeqWrTimer = 0;
  AD5940_SEQCfg(&seq_cfg);

  /* Do RTIA calibration */
  
  if((AppBIACfg.ReDoRtiaCal == bTRUE) || \
      AppBIACfg.BIAInited == bFALSE)  /* Do calibration on the first initializaion */
  {
    error=AppBIARtiaCal();
    if(error!=AD5940ERR_OK)return bench_stop(error);
    AppBIACfg.ReDoRtiaCal = bFALSE;
  }
  /* Reconfigure FIFO */
  AD5940_FIFOCtrlS(FIFOSRC_DFT, bFALSE);									/* Disable FIFO firstly */
  fifo_cfg.FIFOEn = bTRUE;
  fifo_cfg.FIFOMode = FIFOMODE_FIFO;
  fifo_cfg.FIFOSize = FIFOSIZE_4KB;                       /* 4kB for FIFO, The reset 2kB for sequencer */
  fifo_cfg.FIFOSrc = FIFOSRC_DFT;
  fifo_cfg.FIFOThresh = AppBIACfg.FifoThresh;              /* DFT result. One pair for RCAL, another for Rz. One DFT result have real part and imaginary part */
  AD5940_FIFOCfg(&fifo_cfg);

  AD5940_INTCClrFlag(AFEINTSRC_ALLINT);
  
  /* Start sequence generator */
  /* Initialize sequencer generator */
  if((AppBIACfg.BIAInited == bFALSE)||\
       (AppBIACfg.bParaChanged == bTRUE))
  {
    if(pBuffer == 0)  return AD5940ERR_PARA;
    if(BufferSize == 0) return AD5940ERR_PARA;   
    AD5940_SEQGenInit(pBuffer, BufferSize);

    /* Generate initialize sequence */
    error = AppBIASeqCfgGen(); /* Application initialization sequence using either MCU or sequencer */
    if(error != AD5940ERR_OK) return bench_stop(error);

    /* Generate measurement sequence */
    error = AppBIASeqMeasureGen();
    if(error != AD5940ERR_OK) return bench_stop(error);

    AppBIACfg.bParaChanged = bFALSE; /* Clear this flag as we already implemented the new configuration */
  }

  /* Initialization sequencer  */
  AppBIACfg.InitSeqInfo.WriteSRAM = bFALSE;
  AD5940_SEQInfoCfg(&AppBIACfg.InitSeqInfo);
  seq_cfg.SeqEnable = bTRUE;
  AD5940_SEQCfg(&seq_cfg);  /* Enable sequencer */
  AD5940_SEQMmrTrig(AppBIACfg.InitSeqInfo.SeqId);
  if(AD5940_BenchWaitInt(AFEINTC_1,AFEINTSRC_ENDSEQ)!=AD5940ERR_OK)return bench_stop(AD5940ERR_TIMEOUT);
  
  /* Measurement sequence  */
  AppBIACfg.MeasureSeqInfo.WriteSRAM = bFALSE;
  AD5940_SEQInfoCfg(&AppBIACfg.MeasureSeqInfo);

  seq_cfg.SeqEnable = bTRUE;
  AD5940_SEQCfg(&seq_cfg);  /* Enable sequencer, and wait for trigger */
  AD5940_ClrMCUIntFlag();   /* Clear interrupt flag generated before */

  AD5940_AFEPwrBW(AppBIACfg.PwrMod, AFEBW_250KHZ);
  AD5940_WriteReg(REG_AFE_SWMUX, 1<<3);
  if(AD5940_BenchIoFault)return bench_stop(AD5940ERR_TIMEOUT);
  /* ODR may have been limited during sequence generation; bind final state. */
  CalSignature=signature();
  if(ConfigId==UINT32_MAX)return bench_stop(AD5940ERR_APPERROR);
  ++ConfigId;
  AppBIACfg.BIAInited = bTRUE;  /* BIA application has been initialized. */
  return AD5940ERR_OK;
}

/* Modify registers when AFE wakeup */
static AD5940Err AppBIARegModify(int32_t * const pData, uint32_t *pDataCount)
{
  if(AppBIACfg.NumOfData > 0)
  {
    AppBIACfg.FifoDataCount += *pDataCount/4;
    if(AppBIACfg.FifoDataCount >= AppBIACfg.NumOfData)
    {
      AD5940_WUPTCtrl(bFALSE);
      AppBIACfg.StopRequired=bTRUE;
      return AD5940ERR_OK;
    }
  }
  if(AppBIACfg.StopRequired == bTRUE)
  {
    AD5940_WUPTCtrl(bFALSE);
    return AD5940ERR_OK;
  }
  if(AppBIACfg.SweepCfg.SweepEn) /* Need to set new frequency and set power mode */
  {
    AD5940_WGFreqCtrlS(AppBIACfg.SweepNextFreq, AppBIACfg.SysClkFreq);
  }
  return AD5940ERR_OK;
}

/* Depending on the data type, do appropriate data pre-process before return back to controller */
static AD5940Err AppBIADataProcess(const uint32_t *data,uint32_t words,uint32_t flags)
{
 AD5940Err error=AD5940ERR_OK;uint32_t i;
 FrameCount=0;
 if(!data||!words||words%4||words/4>BIA_BENCH_MAX_FRAMES)return AD5940ERR_BUFF;
 if(!AppBIABenchCalibrationValid())return AD5940ERR_CALOR;
 for(i=0;i<words/4;i++) {
  BIABenchFrame *f=&Frames[i];AD5940Err e;
  e=AppBIADecodeFrame(&data[4*i],f,AppBIACfg.RtiaCurrValue,AppBIACfg.MinCurrentDftMagnitude);
  f->sequence=FrameSequence++;f->config_id=ConfigId;f->calibration_id=CalId;
  f->frequency_requested_hz=AppBIACfg.SinFreq;f->interrupt_flags=flags;
  if(e!=AD5940ERR_OK)error=e;
 }
 FrameCount=words/4;
 if(error!=AD5940ERR_OK)for(i=0;i<FrameCount;i++)Frames[i].status=error;
 return error;
}


/**
*/
AD5940Err AppBIAISR(void *pBuff,uint32_t *pCount)
{
 uint32_t capacity,words,flags;AD5940Err error;
 FrameCount=0;LastInterruptFlags=LastFifoWords=LastCapacity=0;
 if(!pCount)return bench_stop(AD5940ERR_NULLP);
 capacity=*pCount;LastCapacity=capacity;*pCount=0;
 if(!pBuff||capacity<4)return bench_stop(AD5940ERR_BUFF);
 if(!AppBIACfg.BIAInited)return AD5940ERR_APPERROR;
 if(AppBIAValidateConfig()!=AD5940ERR_OK||!AppBIABenchCalibrationValid())return bench_stop(AD5940ERR_CALOR);
 if(AD5940_BenchIoFault)return bench_stop(AD5940ERR_TIMEOUT);
 if(AD5940_WakeUp(10)>10)return bench_stop(AD5940ERR_WAKEUP);
 AD5940_SleepKeyCtrlS(SLPKEY_LOCK);
 flags=AD5940_INTCGetFlag(AFEINTC_1);LastInterruptFlags=flags;
 if(AD5940_BenchIoFault)return bench_stop(AD5940ERR_TIMEOUT);
 if(flags&(AFEINTSRC_DATAFIFOOF|AFEINTSRC_DATAFIFOUF|AFEINTSRC_ADCMINERR|AFEINTSRC_ADCMAXERR|
           AFEINTSRC_SEQTIMEOUTERR|AFEINTSRC_CMDFIFOOF|AFEINTSRC_CMDFIFOUF))
   return bench_stop(AD5940ERR_APPERROR);
 if(!AD5940_INTCTestFlag(AFEINTC_0,AFEINTSRC_DATAFIFOTHRESH)) {
  AD5940_SleepKeyCtrlS(SLPKEY_UNLOCK);return AD5940ERR_OK;
 }
 words=AD5940_FIFOGetCnt();LastFifoWords=words;
 if(AD5940_BenchIoFault)return bench_stop(AD5940ERR_TIMEOUT);
 /* Reject rather than truncate: active-sequence partial frames require target timing validation. */
 if(!words||words%4||words>capacity||words>4*BIA_BENCH_MAX_FRAMES)return bench_stop(AD5940ERR_BUFF);
 if(FrameSequence>UINT32_MAX-words/4)return bench_stop(AD5940ERR_APPERROR);
 AD5940_FIFORd((uint32_t*)pBuff,words);
 if(AD5940_BenchIoFault)return bench_stop(AD5940ERR_TIMEOUT);
 AD5940_INTCClrFlag(AFEINTSRC_DATAFIFOTHRESH);
 flags|=AD5940_INTCGetFlag(AFEINTC_1);LastInterruptFlags=flags;
 if(AD5940_BenchIoFault)return bench_stop(AD5940ERR_TIMEOUT);
 error=AppBIADataProcess((const uint32_t*)pBuff,words,flags);*pCount=FrameCount;
 /* Post-read faults still preserve captured raw frames, explicitly invalid. */
 if(flags&(AFEINTSRC_DATAFIFOOF|AFEINTSRC_DATAFIFOUF|AFEINTSRC_ADCMINERR|AFEINTSRC_ADCMAXERR|
           AFEINTSRC_SEQTIMEOUTERR|AFEINTSRC_CMDFIFOOF|AFEINTSRC_CMDFIFOUF))error=AD5940ERR_APPERROR;
 if(error!=AD5940ERR_OK) {
   uint32_t i;for(i=0;i<FrameCount;i++)Frames[i].status=error;
   return bench_stop(error);
 }
 AppBIARegModify((int32_t*)pBuff,&words);
 AD5940_SleepKeyCtrlS(SLPKEY_UNLOCK);
 if(AD5940_BenchIoFault){*pCount=0;FrameCount=0;return bench_stop(AD5940ERR_TIMEOUT);}
 return AD5940ERR_OK;
}
 

/**
  * @}
  */

#include "BenchLog.inc"
