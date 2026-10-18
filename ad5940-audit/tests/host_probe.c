/* Audit-only wrapper, not firmware. ADI source included unchanged for development tests.
   Peripheral functions below are mocks; this does not emulate hardware/timing. */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "../source/examples/AD5940_BIA/BodyImpedance.c"
static BoolFlag bIsS2silicon=bFALSE;
#include "upstream_sweep.inc"
#include "upstream_wg.inc"
static uint32_t mock_count, mock_read, mock_wakeup;
static unsigned cal_calls;
uint32_t AD5940_WakeUp(int32_t n){(void)n;return mock_wakeup;}
void AD5940_SleepKeyCtrlS(uint32_t k){(void)k;}
BoolFlag AD5940_INTCTestFlag(uint32_t a,uint32_t b){(void)a;(void)b;return bTRUE;}
uint32_t AD5940_FIFOGetCnt(void){return mock_count;}
void AD5940_FIFORd(uint32_t *buf,uint32_t n){mock_read=n;for(uint32_t i=0;i<n;i++)buf[i]=(i%4==0)?10000:(i%4==2)?5000:0;}
void AD5940_INTCClrFlag(uint32_t f){(void)f;}
void AD5940_WUPTCtrl(BoolFlag e){(void)e;}
void AD5940_WGFreqCtrlS(float a,float b){(void)a;(void)b;}
AD5940Err AD5940_HSRtiaCal(HSRTIACal_Type *c,void *p){(void)c;(void)p;cal_calls++;return AD5940ERR_PARA;}
static void reset(void){AppBIACfg.SweepCfg.SweepEn=bFALSE;AppBIACfg.BIAInited=bTRUE;AppBIACfg.NumOfData=-1;AppBIACfg.StopRequired=bFALSE;AppBIACfg.RtiaCurrValue[0]=1000;AppBIACfg.RtiaCurrValue[1]=0;}
int main(int argc,char **argv){
 reset();
 if(argc>1&&!strcmp(argv[1],"process")){
  if(argc!=8)return 2;
  int32_t raw[8]={0};
  for(int i=0;i<4;i++)raw[i]=(uint32_t)strtoll(argv[2+i],0,0)&0x3ffff;
  AppBIACfg.RtiaCurrValue[0]=strtof(argv[6],0);AppBIACfg.RtiaCurrValue[1]=strtof(argv[7],0);
  uint32_t n=4;int err=AppBIADataProcess(raw,&n);fImpPol_Type *out=(fImpPol_Type*)raw;
  printf("%d %u %.9g %.9g %d\n",err,n,out[0].Magnitude,out[0].Phase,isfinite(out[0].Magnitude)&&isfinite(out[0].Phase));
 }else if(argc>1&&!strcmp(argv[1],"isr")){
  if(argc!=6)return 2;
  mock_count=strtoul(argv[2],0,0);uint32_t n=strtoul(argv[3],0,0);mock_wakeup=strtoul(argv[4],0,0);AppBIACfg.BIAInited=atoi(argv[5]);
  // Larger physical storage intentionally prevents an actual overflow, while testing a smaller declared capacity.
  uint32_t raw[2048]={0};if(mock_count>2048)return 2;
  int err=AppBIAISR(raw,&n);printf("%d %u %u\n",err,n,mock_read);
 }else if(argc>1&&!strcmp(argv[1],"calfail")){
  AppBIACfg.RcalVal=0;int err=AppBIARtiaCal();printf("%d %u %.9g\n",err,cal_calls,AppBIACfg.RtiaCurrValue[0]);
 }else if(argc>1&&!strcmp(argv[1],"sweep")){
  if(argc!=3)return 2;
  SoftSweepCfg_Type s={.SweepStart=10000,.SweepStop=150000,.SweepPoints=atoi(argv[2]),.SweepLog=bTRUE,.SweepIndex=0};
  float f;AD5940_SweepNext(&s,&f);printf("%.9g %u %d\n",f,s.SweepIndex,isfinite(f));
 }else if(argc>1&&!strcmp(argv[1],"wg")){
  if(argc!=4)return 2;bIsS2silicon=atoi(argv[3]);float target=strtof(argv[2],0);
  uint32_t word=AD5940_WGFreqWordCal(target,16000000);printf("%u %.9g\n",word,(double)word*16000000/(bIsS2silicon?(1LL<<30):(1LL<<26)));
 }else return 2;
 return 0;
}
