/* NEW audit/development wrapper. ALL peripherals mocked, no hardware. */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "../source/examples/AD5940_BIA/BodyImpedance.c"
#include "../source/examples/AD5940_BIA/AD5940Main.c"
volatile int32_t AD5940_BenchIoFault;
AD5940BenchCalTrace AD5940_BenchCalTrace;
static BoolFlag bIsS2silicon=bTRUE;
static unsigned mock_count=4,mock_read,mock_wakeup,mock_flags,mock_calls,mock_ready=1,mock_stop,mock_reset,mock_lock;
static unsigned mock_fcw=3355443;
static int mock_cal_error,mock_seq_error;
static unsigned mock_generator,mock_encoded_stop;
static unsigned mock_post_flags,mock_flag_reads;
static float mock_mag=1000,mock_phase;
#include "library_extracts.inc"
#include "peripheral_mocks.inc"
uint32_t AD5940_WakeUp(int32_t n){(void)n;return mock_wakeup;}
void AD5940_SleepKeyCtrlS(uint32_t k){mock_lock=(k==SLPKEY_LOCK);}
void AD5940_SEQGenCtrl(BoolFlag e){mock_generator=e;}
void AD5940_WUPTCtrl(BoolFlag e){if(!e){mock_stop++;if(mock_generator)mock_encoded_stop++;}}
void AD5940_RstClr(void){mock_reset++;}
BoolFlag AD5940_INTCTestFlag(uint32_t a,uint32_t b){(void)a;(void)b;mock_calls++;return mock_ready?bTRUE:bFALSE;}
uint32_t AD5940_INTCGetFlag(uint32_t c){(void)c;return mock_flags|((mock_flag_reads++>0)?mock_post_flags:0);}
uint32_t AD5940_FIFOGetCnt(void){return mock_count;}
void AD5940_FIFORd(uint32_t *p,uint32_t n){mock_read=n;for(uint32_t i=0;i<n;i++)p[i]=(i%4==0)?0xa0002710u:(i%4==2)?5000:0;}
AD5940Err AD5940_HSRtiaCal(HSRTIACal_Type *c,void *p){(void)c;((float*)p)[0]=mock_mag;((float*)p)[1]=mock_phase;AD5940_BenchCalTrace.available=bTRUE;for(unsigned i=0;i<4;i++)AD5940_BenchCalTrace.raw[i]=i+100;return mock_cal_error;}
uint32_t AD5940_ReadReg(uint16_t r){if(r==REG_AFECON_CHIPID)return 0x5501;if(r==REG_AFE_WGFCW)return mock_fcw;return 0;}
AD5940Err AD5940_SEQGenFetchSeq(const uint32_t **p,uint32_t *n){if(mock_seq_error)return mock_seq_error;static uint32_t seq[2]={0,0};*p=seq;*n=2;return 0;}
void AD5940_ClksCalculate(ClksCalInfo_Type *c,uint32_t *n){(void)c;*n=1000;}
uint32_t AD5940_SEQCycleTime(void){return 160000;}
uint32_t AD5940_GetMCUIntFlag(void){return 1;}
uint32_t AD5940_ClrMCUIntFlag(void){return 1;}
static void reset(void){AD5940BIAStructInit();AppBIACfg.ReDoRtiaCal=bFALSE;AppBIACfg.bParaChanged=bFALSE;AppBIACfg.BIAInited=bTRUE;AppBIACfg.StopRequired=bFALSE;AppBIACfg.RtiaCurrValue[0]=1000;AppBIACfg.RtiaCurrValue[1]=0;ExpectedRtia[0]=1000;ExpectedRtia[1]=0;CalSignature=signature();CalValid=bTRUE;CalId=ConfigId=1;}
int main(int argc,char **v){
 reset();if(argc<2)return 2;
 if(!strcmp(v[1],"process")){
  if(argc!=9)return 2;uint32_t raw[4],copy[4];BIABenchFrame f;float rtia[2];
  for(unsigned i=0;i<4;i++)raw[i]=(uint32_t)strtoll(v[i+2],0,0);memcpy(copy,raw,sizeof(raw));
  rtia[0]=strtof(v[6],0);rtia[1]=strtof(v[7],0);float floor=strtof(v[8],0);
  int e=AppBIADecodeFrame(raw,&f,rtia,floor);
  printf("{\"status\":%d,\"r\":%.9g,\"x\":%.9g,\"mag\":%.9g,\"phase\":%.9g,\"raw_unchanged\":%s,\"raw\":[%lu,%lu,%lu,%lu],\"dft\":[%ld,%ld,%ld,%ld]}\n",e,f.r,f.x,f.magnitude,f.phase_rad,memcmp(copy,raw,sizeof(raw))?"false":"true",(unsigned long)f.raw[0],(unsigned long)f.raw[1],(unsigned long)f.raw[2],(unsigned long)f.raw[3],(long)f.dft[0],(long)f.dft[1],(long)f.dft[2],(long)f.dft[3]);
 }else if(!strcmp(v[1],"isr")) {
  if(argc!=8)return 2;mock_count=strtoul(v[2],0,0);uint32_t n=strtoul(v[3],0,0);mock_wakeup=atoi(v[4]);AppBIACfg.BIAInited=atoi(v[5]);mock_flags=strtoul(v[6],0,0);mock_ready=atoi(v[7]);
  uint32_t raw[512];memset(raw,0x55,sizeof(raw));int e=AppBIAISR(raw,&n);
  printf("{\"status\":%d,\"count\":%u,\"read_words\":%u,\"cal_valid\":%d,\"stop_calls\":%u,\"lock\":%u}\n",e,n,mock_read,AppBIABenchCalibrationValid(),mock_stop,mock_lock);
 }else if(!strcmp(v[1],"cal")) {
  if(argc!=5)return 2;mock_cal_error=atoi(v[2]);mock_mag=strtof(v[3],0);mock_phase=strtof(v[4],0);int e=AppBIARtiaCal();
  printf("{\"status\":%d,\"cal_valid\":%d,\"rtia\":%.9g}\n",e,AppBIABenchCalibrationValid(),AppBIACfg.RtiaCurrValue[0]);
 }else if(!strcmp(v[1],"init")) {
  if(argc!=5)return 2;mock_cal_error=atoi(v[2]);mock_ready=atoi(v[3]);AppBIACfg.MinCurrentDftMagnitude=strtof(v[4],0);
  uint32_t raw[512];int e=AppBIAInit(raw,512);
  printf("{\"status\":%d,\"cal_valid\":%d,\"inited\":%d,\"reset_calls\":%u}\n",e,AppBIABenchCalibrationValid(),AppBIACfg.BIAInited,mock_reset);
 }else if(!strcmp(v[1],"stale")) {
  AppBIACfg.RcalVal=11000;uint32_t n=512,raw[512];int e=AppBIAISR(raw,&n);printf("{\"status\":%d,\"count\":%u,\"cal_valid\":%d}\n",e,n,AppBIABenchCalibrationValid());
 }else if(!strcmp(v[1],"stale_rtia")) {
  AppBIACfg.RtiaCurrValue[0]=0;printf("{\"cal_valid\":%d,\"start_status\":%d}\n",AppBIABenchCalibrationValid(),AppBIACtrl(BIACTRL_START,0));
 }else if(!strcmp(v[1],"init_seq_bad")) {
  mock_seq_error=AD5940ERR_BUFF;uint32_t b[512];int e=AppBIAInit(b,512);
  printf("{\"status\":%d,\"stop_calls\":%u,\"cal_valid\":%d,\"inited\":%d,\"generator\":%u,\"encoded_stop\":%u}\n",e,mock_stop,AppBIABenchCalibrationValid(),AppBIACfg.BIAInited,mock_generator,mock_encoded_stop);
 }else if(!strcmp(v[1],"reinit_bad")) {
  AppBIACfg.MinCurrentDftMagnitude=0;uint32_t raw[512];int e=AppBIAInit(raw,512);printf("{\"status\":%d,\"stop_calls\":%u,\"cal_valid\":%d}\n",e,mock_stop,AppBIABenchCalibrationValid());
 }else if(!strcmp(v[1],"sweep")) {
  AppBIACfg.SweepCfg.SweepEn=bTRUE;AppBIACfg.SweepCfg.SweepPoints=atoi(v[2]);printf("{\"status\":%d}\n",AppBIAValidateConfig());
 }else if(!strcmp(v[1],"wait")) {
  mock_ready=0;int e=AD5940_BenchWaitInt(1,2);printf("{\"status\":%d,\"calls\":%u,\"io_fault\":%ld}\n",e,mock_calls,(long)AD5940_BenchIoFault);
 }else if(!strcmp(v[1],"waitreg")) {
  int e=bench_wait_register(0x1234,1);printf("{\"ready\":%d,\"io_fault\":%ld}\n",e,(long)AD5940_BenchIoFault);
 }else if(!strcmp(v[1],"null")) {
  uint32_t n=512;int e=AppBIAISR(NULL,&n);int f=AppBIAISR((void*)1,NULL);printf("{\"status\":%d,\"count\":%u,\"null_count_status\":%d}\n",e,n,f);
 }else if(!strcmp(v[1],"pipeline")) {
  if(BenchLogBegin("synthetic-test"))return 3;uint32_t raw[512];int e=AppBIAInit(raw,512);if(e)return 4;
  if(AppBIABenchExportConfig())return 5;uint32_t n=512;e=AppBIAISR(raw,&n);if(e)return 6;if(AppBIABenchExportFrames())return 7;return AppBIABenchExportEnd()!=0;
 }else if(!strcmp(v[1],"readback_bad")) {
  uint32_t raw[512];if(AppBIAInit(raw,512))return 4;BenchLogBegin("synthetic-test");mock_fcw=0;
  printf("{\"status\":%d}\n",AppBIABenchExportConfig());
 }else if(!strcmp(v[1],"pipeline_bad")) {
  BenchLogBegin("synthetic-test");uint32_t raw[512];if(AppBIAInit(raw,512))return 4;
  if(AppBIABenchExportConfig())return 5;mock_post_flags=16;uint32_t n=512;int e=AppBIAISR(raw,&n);
  if(!e)return 6;if(AppBIABenchExportFrames())return 7;return AppBIABenchExportFault(e)!=0;
 }else if(!strcmp(v[1],"postflag")) {
  mock_post_flags=16;uint32_t raw[512],n=512;int e=AppBIAISR(raw,&n);uint32_t fcount;const BIABenchFrame *f=AppBIABenchFrames(&fcount);
  printf("{\"status\":%d,\"count\":%u,\"captured\":%u,\"frame_status\":%ld}\n",e,n,fcount,(long)f[0].status);
 }else if(!strcmp(v[1],"mainfault")) {
  mock_count=516;AD5940_Main();
 }else if(!strcmp(v[1],"session")) {
  printf("%d\n",BenchLogBegin(v[2]));
 }else if(!strcmp(v[1],"crc")) {
  printf("%08lx\n",(unsigned long)BenchLogCrc32((unsigned char*)"123456789",9));
 }else if(!strcmp(v[1],"wgvalue")) {
  uint32_t word=AD5940_WGFreqWordCal(strtof(v[2],0),16000000);printf("{\"word\":%lu,\"io_fault\":%ld}\n",(unsigned long)word,(long)AD5940_BenchIoFault);
 }else if(!strcmp(v[1],"lib_sweep")) {
  SoftSweepCfg_Type s={.SweepStart=10000,.SweepStop=150000,.SweepPoints=atoi(v[2]),.SweepIndex=0,.SweepLog=bTRUE};float f;
  if(argc>4){s.SweepStart=strtof(v[3],0);s.SweepStop=strtof(v[4],0);}
  AD5940_SweepNext(&s,&f);printf("{\"finite\":%s,\"io_fault\":%ld}\n",isfinite(f)?"true":"false",(long)AD5940_BenchIoFault);
 }else return 2;return 0;
}
