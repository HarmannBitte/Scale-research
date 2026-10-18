#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static int polls,limit;void _delay_ms(int n){(void)n;}
int ad5933_has_valid_impedance(void){if(++polls>limit){puts("stub_poll_budget_exhausted (upstream never returned)");exit(42);}return limit!=50;}
int ad5933_get_real(void){return -1234;}int ad5933_get_imaginary(void){return 2345;}void ad5933_repeat_frequency(void){}

void take_measurement(uint8_t avg, double *rdata, double *idata)
{
    int i;
    int32_t rdata_raw = 0, idata_raw = 0;

    for (i = 0; i < avg; i++) {
        _delay_ms(1); // The conversion process takes approximately 1 ms using a 16.777 MHz clock.
        while (!ad5933_has_valid_impedance());
        rdata_raw += ad5933_get_real();
        idata_raw += ad5933_get_imaginary();

        if (avg > 1) {
            ad5933_repeat_frequency();
        }
    }

    *rdata = (double) rdata_raw / avg;
    *idata = (double) idata_raw / avg;
}
int main(int argc,char **argv){(void)argc;limit=atoi(argv[2]);double r=9,i=9;take_measurement(atoi(argv[1]),&r,&i);printf("real=%g imag=%g finite=%d polls=%d\n",r,i,isfinite(r)&&isfinite(i),polls);return 0;}
