#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static uint8_t regs[256];static double bioz_ohm_coeff=1.0;double ndiv,bioz_adc_osr,sr_bioz;
int regRead(int a){return regs[a];}void regWrite(int a,int b){regs[a]=b;}

void changeReg(uint8_t regAddr, uint8_t val, uint8_t bit1, uint8_t numBits)
{
  /*
  This is a function to change specific bits of the byte
  */

  int i = 0;
  uint8_t x1 = 0;
  for (i = 7; i > bit1; i--)
  {
    x1 = x1 + pow(2, i);
  }

  uint8_t x2 = 0;
  for (i = 0; i < (bit1 - numBits + 1); i++)
  {

    x2 = x2 + (pow(2, i));
  }

  uint8_t newBits = x1 + x2;
  uint8_t reg1 = regRead(regAddr);
  newBits = reg1 & newBits;
  val = val << (bit1 - numBits + 1);
  newBits = newBits + val;
  regWrite(regAddr, newBits);
}/**
 * @brief Change M divider value.
 *
 * @param val The value to set for the M divider.
 *
 * This function changes the M divider value, which spans over two separate registers.
 */
void setMdiv(int val)
{
  /*
  This function is specifically to change the M divider value
  as it spans over two seperate registers


  */
  uint32_t V = val;

  uint8_t a = V >> 8;

  uint8_t b = V & 0xFF;

  changeReg(0x17, a, 7, 2); // step 3:
  changeReg(0x18, b, 7, 8); // MDIV
}

/**
 * @brief Configure the BioZ BIA settings for the MAX30009.
 *
 * This function initializes the BioZ BIA settings by configuring various registers
 * to set up the device for BioZ measurements. It includes PLL, clock, gain setup,
 * basic sensor/AFE configuration, interrupt setup, and DAC/ADC OSR configuration.
 * It also clears the status register and brings the device out of shutdown.
 * It must be called before starting any BioZ measurements.
 */
void BIAsettings()
{
  // --- Reset and bring device out of shutdown ---
  regWrite(0x20, 1 << 2); // BIOZ_BG_EN
  regWrite(0x11, 0);      // clear SHDN
  regWrite(0x17, 0);      // clear PLL_EN
  regWrite(0x1A, 0);      // clear REF_CLK_SEL
  regWrite(0x11, 1);      // issue RESET

  // --- Clear status ---
  regRead(0x00); // read status to clear

  // --- PLL, Clock and Gain Setup ---
  regWrite(0x18, 0xBB);
  regWrite(0x19, 0x01);
  regWrite(0x1A, (0 << 6) | (1 << 5));
  regWrite(0x17, (1 << 6) | (0 << 5) | (2 << 1) | 1);

  // --- Basic Sensor/AFE Configuration ---
  regWrite(0x10, 0x00); // BIOZ_CONFIG
  regWrite(0x12, 0x04); // CMDET_EN
  regWrite(0x13, 0x00); // No Lead-Off Comparator
  regWrite(0x14, 0x00); // Reserved
  regWrite(0x21, 0x20); // HIZ after reset
  regWrite(0x22, 0x28); // BIOZ_VDRV_MAG = 2 (2.5x), BIOZ_IDRV_RGE = 2 (32uA)
  regWrite(0x23, 0x00); // default
  regWrite(0x24, 0x33); // Amp Biasing
  regWrite(0x25, 0xCA); // AMP_RGE and bandwidth
  regWrite(0x26, 0x00);
  regWrite(0x27, 0xFF);
  regWrite(0x28, 0x12); // Drive Freq Trim
  regWrite(0x41, 0x06); // BIOZ_MUX Config, MUX_EN
  regWrite(0x42, 0x01); // MUX2
  regWrite(0x43, 0xA0); // BIOZ_RBIAS and Bias Driver
  regWrite(0x44, 0xD1); // Refbuf trim
  regWrite(0x50, 0x00);
  regWrite(0x51, 0x00);
  regWrite(0x58, 0x07); // All clock gates on

  // --- Interrupt Setup ---
  regWrite(0x80, 0xA0); // Enable A_FULL_EN and FIFO_DATA_RDY_EN
  regWrite(0x81, 0x00); // Optional: disable error interrupts for now

  // --- DAC/ADC OSR Config ---
  regWrite(0x20, 0xA0); // DAC_OSR = 2 (128), ADC_OSR = 5 (256), BG_EN, Q_EN, I_EN = 0

  // --- Note: Must call setFreq() after this to finalize DAC/ADC and KDIV settings
  changeReg(0x17, 0, 5, 1); // NDIV = 0 (512)
  setMdiv(512);
}

/**
 * @brief Get the reference clock frequency in Hz.
 *
 * This function determines the reference clock frequency based on the
 * settings in the MAX30009 registers. It checks the reference clock selection
 * and clock frequency selection bits to return the appropriate frequency.
 *
 * @return The reference clock frequency in Hz.
 */
uint32_t getRefClkHz()
{

  uint8_t ref_clk_sel = regRead(0x1A) & 0b01000000;  // Bit 6
  uint8_t clk_freq_sel = regRead(0x1A) & 0b00100000; // Bit 5
  // printf("ref_clk_sel: %d\t", ref_clk_sel);
  // printf("clk_freq_sel: %d\n", clk_freq_sel);
  if (ref_clk_sel == 0)
  {
    // Internal oscillator
    return (clk_freq_sel == 0) ? 32000 : 32768;
  }
  else
  {
    // External oscillator
    return (clk_freq_sel == 0) ? 32000 : 32768;
  }
}

/**
 * @brief Get the sample interval in seconds.
 *
 * This function calculates the sample interval based on the reference clock frequency,
 * M divider, N divider, and ADC oversampling rate.
 *
 * @return The sample interval in seconds.
 */
double getSampleInterval()
{
  uint32_t ref_clk = getRefClkHz();

  int mdiv_high = (regRead(0x17) >> 6) & 0x03;
  int mdiv_low = regRead(0x18);
  int mdiv = (mdiv_high << 8) | mdiv_low;
  // printf("M Divider: %d\n", mdiv);

  double pll_clk = (double)ref_clk * (mdiv + 1);
  // printf("PLL Clock: %.2f Hz\n", pll_clk);
  uint8_t ndiv_raw = (regRead(0x17) >> 5) & 0x01;
  ndiv = (ndiv_raw == 0) ? 512.0 : 1024.0;
  // printf("N Divider: %.0f\n", ndiv);

  uint8_t adc_osr_raw = (regRead(0x20) >> 3) & 0x07;
  uint16_t adc_osr_table[] = {8, 16, 32, 64, 128, 256, 512, 1024};
  bioz_adc_osr = adc_osr_table[adc_osr_raw];
  // printf("BioZ ADC OSR: %.0f\n", bioz_adc_osr);

  sr_bioz = pll_clk / (ndiv * bioz_adc_osr);
  // printf("SR: %.4f\n", sr_bioz); // Prints with more decimal places

  if (sr_bioz == 0.0)
    return 0.0;
  return 1 / sr_bioz;
}

/**
 * @brief Get the DAC oversampling rate.
 *
 * This function reads the DAC oversampling rate from the MAX30009 registers.
 * It returns the oversampling rate in terms of samples per second.
 * The possible values are 32, 64, 128, or 256.
 * @return The DAC oversampling rate in samples per second.
 */
int getDACOSR()
{
  uint8_t val = (regRead(0x20) & 0b11000000) >> 6;
  switch (val)
  {
  case 0:
    return 32;
  case 1:
    return 64;
  case 2:
    return 128;
  case 3:
    return 256;
  default:
    return 32; // fallback
  }
}

/**
 * @brief Get the K divider value.
 *
 * This function reads the K divider value from the MAX30009 registers.
 * The K divider is used to set the frequency of the BioZ signal.
 *
 * @return The K divider value.
 */
int getKDiv()
{

  uint8_t k_div = (regRead(0x17) & 0b00011110) >> 1; // Bits 4:1
  uint16_t k_div_table[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 8192, 8192};

  if (k_div < 14)
  {
    return k_div_table[k_div];
  }
  else
  {
    return 8192;
  }
}

/**
 * @brief Get the BioZ gain value.
 *
 * This function reads the BioZ gain setting from the MAX30009 registers.
 * It returns the gain factor based on the bits set in the register.
 *
 * @return The BioZ gain factor.
 */
double getBiozGain()
{
  uint8_t reg_val = regRead(0x24);    // If your doc says 0x24, change this
  uint8_t gain_bits = reg_val & 0x03; // Bits [1:0]

  switch (gain_bits)
  {
  case 0x00:
    return 1.0;
  case 0x01:
    return 2.0;
  case 0x02:
    return 5.0;
  case 0x03:
    return 10.0;
  default:
    printf("Invalid GAIN bits: %u\n", gain_bits);
    return -1.0;
  }
}

/**
 * @brief Get the BioZ current in microamperes.
 *
 * This function reads the BioZ current settings from the MAX30009 registers
 * and calculates the current in microamperes based on the VDRV_MAG and IDRV_RGE settings.
 * It uses predefined values for VDRV_MAG and IDRV_RGE to compute the current.
 *
 * @return The BioZ current in microamperes (µA).
 */
double getBiozCurrent_uA()
{
  uint8_t reg_val = regRead(0x22);

  uint8_t vdrv_mag_bits = (reg_val >> 4) & 0x03; // bits 5:4
  uint8_t idrv_rge_bits = (reg_val >> 2) & 0x03; // bits 3:2

  // VDRV_MAG mV values
  const double vdrv_mag_mv[] = {50.0, 100.0, 250.0, 500.0}; // in mV
  // IDRV_RGE resistor values (in Ohms)
  const double r_idrv[] = {552500.0, 110500.0, 5525.0, 276250.0}; // in Ohms

  double vdrv_volts = vdrv_mag_mv[vdrv_mag_bits] / 1000.0;
  double r = r_idrv[idrv_rge_bits];

  double i_amperes = vdrv_volts / r; // I = V / R
  return (i_amperes * 1e6);          // return µA
}

/**
 * @brief Set the frequency for BioZ signal generation.
 *
 * This function configures the frequency-specific settings for BioZ signal generation.
 * It supports two frequencies: 4 kHz and 131 kHz.
 *
 * @param freq The frequency to set:
 *             0 for 4 kHz, 1 for 131 kHz.
 *
 * @note Only supports 4kHz and 131 kHz. Refactoring necessary for other frequencies.
 */
void setFreq(int freq)
{

  switch (freq)
  {
  case 0:
    changeReg(0x17, 5, 4, 4); // k_div = 32, 4kHz

    break;

  case 1:
    changeReg(0x17, 0, 4, 4); // k_div = 1, 131kHz

    break;

  default:
    printf("Invalid frequency: %d kHz\n", freq);
    break;
  }
}
/**
 * @brief Get the M divider value.
 *
 * This function reads the M divider value from the MAX30009 registers.
 * The M divider is used to set the frequency of the BioZ signal.
 *
 * @return The M divider value.
 */
int getMdiv(void)
{
  int mdiv_high = (regRead(0x17) >> 6) & 0x03;
  int mdiv_low = regRead(0x18);
  return (mdiv_high << 8) | mdiv_low;
}

/**
 * @brief Get the PLL clock frequency.
 *
 * This function calculates the PLL clock frequency based on the reference clock
 * and the M divider value. It uses the formula:
 * PLL_CLK = Ref_Clk_Hz * (M + 1)
 *
 * @return The PLL clock frequency in Hz.
 */
double getPllClk(void)
{
  int M = getMdiv(); // Uses your getMdiv() function
  return getRefClkHz() * (M + 1);
}

/**
 * @brief Get the BioZ frequency.
 *
 * This function calculates the BioZ frequency based on the PLL clock,
 * K divider, and DAC oversampling rate. It uses the formula:
 * F_BIOZ = PLL_CLK / (K_DIV * DAC_OSR)
 *
 * @return The BioZ frequency in Hz.
 */
double getBiozFreq(void)
{
  int M = getMdiv();
  double PLL_CLK = getRefClkHz() * (M + 1);
  return PLL_CLK / (getKDiv() * getDACOSR());
}

/**
 * @brief Convert ADC counts to resistance in Ohms.
 *
 * @param count The ADC count value to convert.
 *
 * This function converts the ADC counts from the BioZ measurement
 * to resistance in Ohms using the formula:
 *
 * R = (count * V_REF) / (ADC_FS * gain * (2/π) * I)
 *
 * @return The calculated resistance in Ohms.
 */
double convertCountsToOhms(double count)
{
  const double V_REF = 1.0;
  const double TWO_OVER_PI = 2.0 / M_PI;
  const double ADC_FS = pow(2, 19);

  double gain = getBiozGain();
  double i_mag = getBiozCurrent_uA() / 1e6;

  if (gain <= 0 || i_mag <= 0)
  {
    printf("Invalid gain or current. Gain=%.2f, I=%.6f A\n", gain, i_mag);
    return 0.0;
  }

  return (count * V_REF) / (ADC_FS * gain * TWO_OVER_PI * i_mag);
}

double getBiozOhmCoeff(void)
{
  const double V_REF = 1.0;
  const double TWO_OVER_PI = 2.0 / M_PI;
  const double ADC_FS = pow(2, 19);

  double gain = getBiozGain();
  double i_mag = getBiozCurrent_uA() / 1e6;
  if (gain <= 0 || i_mag <= 0)
  {
    return 0.0;
  }
  return V_REF / (ADC_FS * gain * TWO_OVER_PI * i_mag);
}

void setBiozOhmCoeff(double c)
{
  if (c > 0.0)
  {
    bioz_ohm_coeff = c;
  }
}

double getBiozOhmCoeffCached(void)
{
  return bioz_ohm_coeff;
}
int main(void){BIAsettings();printf("reg17=%u reg20=%u raw_mdiv=%d gain=%.12g current_uA=%.12g coeff_ohm_per_count=%.12g\n",regs[0x17],regs[0x20],getMdiv(),getBiozGain(),getBiozCurrent_uA(),getBiozOhmCoeff());double sec=getSampleInterval();printf("interval_seconds=%.12g sample_interval_us_assigned_as_upstream=%u samples_per_second=%.12g\n",sec,(uint32_t)sec,sr_bioz);setFreq(0);printf("low_frequency_Hz=%.12g\n",getBiozFreq());setFreq(1);printf("high_frequency_Hz=%.12g\n",getBiozFreq());return 0;}
