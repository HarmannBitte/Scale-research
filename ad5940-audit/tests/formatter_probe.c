/* Audit wrapper around exact upstream formatter; no UART/hardware used. */
#include <stdlib.h>
#include "BodyImpedance.h"
AD5940Err AppBIACtrl(int32_t cmd,void *ptr){(void)cmd;*(float*)ptr=50000;return AD5940ERR_OK;}
#include "upstream_formatter.inc"
int main(void){fImpPol_Type values[2]={{500.,0.},{600.,-.1}};return BIAShowResult((uint32_t*)values,2);}
