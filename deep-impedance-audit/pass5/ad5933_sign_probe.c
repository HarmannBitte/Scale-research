/* Pass 5d: host probe of OpenEBI ad5933_get_real()/get_imaginary() (triage/software/ad5933.c, lines 239-253).
 * The I2C layer is stubbed: rblock() fills two bytes with a chosen 16-bit register value,
 * or fails. The conversion expression is copied verbatim from the source.
 * AD5933 datasheet Rev. F: real/imaginary registers are 16-bit two's complement.
 */
#include <stdint.h>
#include <stdio.h>

static uint8_t stub_hi, stub_lo;
static int stub_fail;

static int ad5933_rblock(uint8_t reg, uint8_t *buf, int n)
{
    (void)reg; (void)n;
    if (stub_fail) return 0;
    buf[0] = stub_hi; buf[1] = stub_lo;
    return 2;
}

/* verbatim from ad5933.c */
int ad5933_get_real(void)
{
    uint8_t buf[2];
    if (ad5933_rblock(0x94, buf, 2) == 2)
        return (int) (((uint16_t) buf[0] << 8) | buf[1]);
    return 0;
}

static void show(const char *label, uint16_t raw, int fail)
{
    stub_hi = raw >> 8; stub_lo = raw & 0xFF; stub_fail = fail;
    int got = ad5933_get_real();
    int32_t want = (int16_t)raw;               /* datasheet: 16-bit two's complement */
    printf("%-28s raw=0x%04X  firmware=%6d  datasheet=%6d  %s\n",
           label, raw, got, want, (got == want) ? "ok" : "WRONG");
}

int main(void)
{
    show("positive +1000", 0x03E8, 0);
    show("negative -1000", 0xFC18, 0);
    show("negative -2", 0xFFFE, 0);
    show("most negative -32768", 0x8000, 0);

    /* averaging as in take_measurement(): mean of the readings over 4 repeats */
    uint16_t raws[4] = {0xFC18, 0xFC18, 0xFC18, 0xFC18};  /* -1000 each */
    int32_t sum = 0;
    for (int i = 0; i < 4; i++) {
        stub_hi = raws[i] >> 8; stub_lo = raws[i] & 0xFF; stub_fail = 0;
        sum += ad5933_get_real();
    }
    printf("average of four -1000 readings: firmware=%.1f  datasheet=-1000.0\n", sum / 4.0);

    /* I2C failure path: returns 0 silently */
    show("I2C read failure", 0x1234, 1);
    return 0;
}
