/* Tests actual GNU adapter and MCU source using fake registers. No MCU emulator. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define main bench_mcu_main
#define fputc bench_uart_putchar
#define _exit bench_exit
#include "../source/examples/AD5940_BIA/ADICUP3029/main.c"
#undef main
#include "../source/examples/AD5940_BIA/ADICUP3029/ADICUP3029Port.c"
#include "../gnu/newlib_io.c"
#undef fputc
#undef _exit
volatile int32_t AD5940_BenchIoFault;
unsigned char __HeapBase[4096];
__asm__(".global __HeapLimit\n.set __HeapLimit, __HeapBase+4096");
void AD5940_Main(void){}
int main(int argc,char **argv)
{
 if(argc!=2)return 2;
 if(!strcmp(argv[1],"write")) {
  pADI_UART0->COMLSR=0x20;int n=_write(1,"abc",3);
  printf("{\"n\":%d,\"tx\":%u,\"fault\":%ld}\n",n,(unsigned)pADI_UART0->COMTX,(long)AD5940_BenchIoFault);
 }else if(!strcmp(argv[1],"stalled")) {
  int n=_write(1,"abc",3);printf("{\"n\":%d,\"tx\":%u,\"fault\":%ld,\"errno\":%d}\n",n,(unsigned)pADI_UART0->COMTX,(long)AD5940_BenchIoFault,errno);
 }else if(!strcmp(argv[1],"heap")) {
  int a=_sbrk(4096)==__HeapBase,b=_sbrk(1)==(void*)-1,c=_sbrk(-4096)==__HeapBase+4096,d=_sbrk(-1)==(void*)-1;
  int e=_sbrk(PTRDIFF_MIN)==(void*)-1,f=_sbrk(PTRDIFF_MAX)==(void*)-1,g=_sbrk(0)==__HeapBase;
  printf("{\"checks\":%d}\n",a+b+c+d+e+f+g);
 }else if(!strcmp(argv[1],"invalid_write")) {
  int a=_write(9,"x",1)==-1,b=_write(1,NULL,1)==-1,c=_write(1,NULL,(size_t)INT_MAX+1)==-1,d=_write(1,NULL,0)==0;
  printf("{\"checks\":%d,\"tx\":%u}\n",a+b+c+d,(unsigned)pADI_UART0->COMTX);
 }else if(!strcmp(argv[1],"stat")) {
  struct stat st;memset(&st,0xff,sizeof(st));int n=_fstat(1,&st);
  printf("{\"n\":%d,\"char\":%s,\"size\":%ld,\"blocksize\":%ld,\"invalid\":%d}\n",n,S_ISCHR(st.st_mode)?"true":"false",(long)st.st_size,(long)st.st_blksize,_fstat(9,&st));
 }else if(!strcmp(argv[1],"reset")) {
  int n=AD5940_MCUResourceInit(NULL);
  printf("{\"status\":%d,\"output\":%u,\"clear\":%u,\"set\":%u}\n",n,(unsigned)(pADI_GPIO2->OEN&64),(unsigned)(pADI_GPIO2->CLR&64),(unsigned)(pADI_GPIO2->SET&64));
 }else if(!strcmp(argv[1],"irq")) {
  pADI_CLKG0_CLK->CTL0=0x201;uart_irq_enabled=1;int n=UrtCfg(230400);
  printf("{\"status\":%d,\"ien\":%u,\"enabled\":%u,\"enable_calls\":%u}\n",n,(unsigned)pADI_UART0->COMIEN,uart_irq_enabled,uart_enable_calls);
 }else if(!strcmp(argv[1],"clock")) {
  printf("{\"status\":%lu,",(unsigned long)MCUPlatformInit(NULL));
  printf("\"fault\":%ld}\n",(long)AD5940_BenchIoFault);
 }else if(!strcmp(argv[1],"badbaud")) {
  int a=UrtCfg(0),b=UrtCfg(115200);printf("{\"first\":%d,\"second\":%d,\"fault\":%ld}\n",a,b,(long)AD5940_BenchIoFault);
 }else if(!strcmp(argv[1],"baddivider")) {
  pADI_CLKG0_CLK->CTL0=2; /* PLL selected with multiplier zero -> invalid divisor. */
  int n=UrtCfg(230400);printf("{\"status\":%d,\"fault\":%ld}\n",n,(long)AD5940_BenchIoFault);
 }else return 2;
 return 0;
}
