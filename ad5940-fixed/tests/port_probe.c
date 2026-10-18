/* Host-only tests of actual modified port code using FAKE register storage. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../source/examples/AD5940_BIA/ADICUP3029/ADICUP3029Port.c"
volatile int32_t AD5940_BenchIoFault;
int main(int argc,char **argv){
 if(argc!=2)return 2;
 if(!strcmp(argv[1],"spi")){
  unsigned char tx[7]={1,2,3,4,5,6,7},rx[7]={9,9,9,9,9,9,9};
  AD5940_ReadWriteNBytes(tx,rx,7);
  printf("%ld %u\n",(long)AD5940_BenchIoFault,(unsigned)(rx[0]|rx[1]|rx[2]|rx[3]|rx[4]|rx[5]|rx[6]));
 }else if(!strcmp(argv[1],"delay")){
  AD5940_Delay10us(1);printf("%ld %u\n",(long)AD5940_BenchIoFault,(unsigned)SysTick->CTRL);
 }else if(!strcmp(argv[1],"zero")){
  AD5940_ReadWriteNBytes(NULL,NULL,0);printf("%ld\n",(long)AD5940_BenchIoFault);
 }else if(!strcmp(argv[1],"null")){
  AD5940_ReadWriteNBytes(NULL,NULL,1);printf("%ld\n",(long)AD5940_BenchIoFault);
 }else return 2;return 0;
}
