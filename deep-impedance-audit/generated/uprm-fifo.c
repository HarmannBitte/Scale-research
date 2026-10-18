#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
uint8_t gReadBuf[100],gHold[100];
static int hi,lo,decoded;
#define SPI ((void*)1)
#define E_NO_ERROR 0
struct request {void *spi;uint8_t *txData,*rxData;int txLen,rxLen,ssIdx,ssDeassert,txCnt,rxCnt;void *completeCB;} req;
int regRead(int addr){gReadBuf[2]=addr==0x0A?hi:lo;return gReadBuf[2];}
int MXC_SPI_MasterTransaction(struct request *r){
 fprintf(stdout,"transaction_bytes=%d (upstream fifoCount=(counter1&0x7F)*2+counter2)\n",r->rxLen);fflush(stdout);
 const uint8_t samples[]={0,0,0x10,0,100,0x2F,0xFF,0xCE};
 for(int i=0;i<r->rxLen;i++)r->rxData[i]=samples[i%8];return 0;}
int calcBioZ(uint8_t *b,bool f){(void)b;(void)f;decoded++;return 0;}

int spiBurst(bool freqLogged)
{
  uint8_t regAddr = 0x0C;
  int err = 0;

  regRead(0x0A);
  uint16_t fifoCount = (gReadBuf[2] & 0x7F) << 1;
  regRead(0x0B);
  fifoCount += gReadBuf[2];

  uint8_t tx_buf[fifoCount];
  uint8_t rx_buf[fifoCount];
  memset(tx_buf, 0, fifoCount);
  memset(rx_buf, 0, fifoCount);

  tx_buf[0] = regAddr;
  tx_buf[1] = 0x80;

  req.spi = SPI;
  req.txData = tx_buf;
  req.rxData = rx_buf;
  req.txLen = fifoCount;
  req.rxLen = fifoCount;
  req.ssIdx = 0;
  req.ssDeassert = 1;
  req.txCnt = 0;
  req.rxCnt = 0;
  req.completeCB = NULL;

  err = MXC_SPI_MasterTransaction(&req);
  if (err != E_NO_ERROR)
  {
    printf("\nSPI TRANSACTION FAIL: %d\n", err);
    return err;
  }

  for (int i = 0; i < fifoCount; i++)
  {
    if (rx_buf[i] != 0)
    {
      gHold[0] = rx_buf[i];
      gHold[1] = rx_buf[i + 1];
      gHold[2] = rx_buf[i + 2];
      i += 3;

      while (i < fifoCount && rx_buf[i] == 0)
        i++;

      if (i + 2 < fifoCount)
      {
        gHold[3] = rx_buf[i];
        gHold[4] = rx_buf[i + 1];
        gHold[5] = rx_buf[i + 2];
        i += 2;

        calcBioZ(gHold, freqLogged);
      }
    }
  }

  return err;
}
int main(int argc,char **argv){(void)argc;hi=atoi(argv[1]);lo=atoi(argv[2]);int ret=spiBurst(false);printf("return=%d decoded_pairs=%d\n",ret,decoded);return 0;}
