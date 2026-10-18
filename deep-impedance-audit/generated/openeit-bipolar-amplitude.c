#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define VPEAK (599)
#define VPEAK_BIPOLAR (12.73)
#define DAC_LSB_SIZE (0.39072)
#define SINE_AMPLITUDE ((uint16_t)((VPEAK) / DAC_LSB_SIZE + 0.5))
#define SINE_AMPLITUDE_BIPOLAR ((uint16_t)((VPEAK * 40) / DAC_LSB_SIZE + 0.5))
#define SEQ_MMR_WRITE(addr, data)   (0x80000000 | ((addr & 0xFC) << 23) | data)
#define REG_AFE_AFE_WG_AMPLITUDE 0x4008003C
#define BITM_SINE_AMPLITUDE 0x000007FF  /* ADuCM350 afe header: 11-bit field */
int main(void){
 printf("unipolar_word=%u\n",(unsigned)SINE_AMPLITUDE);
 printf("bipolar_word=%u\n",(unsigned)SINE_AMPLITUDE_BIPOLAR);
 printf("bipolar_word_hex=0x%X\n",(unsigned)SINE_AMPLITUDE_BIPOLAR);
 uint32_t seq=SEQ_MMR_WRITE(REG_AFE_AFE_WG_AMPLITUDE,SINE_AMPLITUDE_BIPOLAR);
 printf("sequence_word=0x%08X address_field_ok=%d\n",seq,((seq>>23)&0xFC)==(REG_AFE_AFE_WG_AMPLITUDE&0xFC));
 printf("field_after_11bit_mask=%u\n",(unsigned)(SINE_AMPLITUDE_BIPOLAR & BITM_SINE_AMPLITUDE));
 printf("field_mV_equiv_at_0.39072mV_per_code=%.2f\n",(SINE_AMPLITUDE_BIPOLAR & BITM_SINE_AMPLITUDE)*DAC_LSB_SIZE);
 printf("intended_mV_equiv=%.2f\n",VPEAK*40.0);
 printf("full_scale_11bit_mV=%.2f\n",2047*DAC_LSB_SIZE);
 printf("unipolar_mV_equiv=%.2f\n",SINE_AMPLITUDE*DAC_LSB_SIZE);
 return 0;}
