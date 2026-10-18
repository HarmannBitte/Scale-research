/* GENERATED FAKE HOST-ONLY registers; real DFP bit masks; not MCU hardware. */
#ifndef FAKE_MCU_H
#define FAKE_MCU_H
#include <stdint.h>
static struct {volatile uint32_t CTL;} storage_pADI_WDT0;
#define pADI_WDT0 (&storage_pADI_WDT0)
static struct {volatile uint32_t CTL;volatile uint32_t KEY;} storage_pADI_CLKG0_OSC;
#define pADI_CLKG0_OSC (&storage_pADI_CLKG0_OSC)
static struct {volatile uint32_t CTL0;volatile uint32_t CTL1;volatile uint32_t CTL3;volatile uint32_t CTL5;} storage_pADI_CLKG0_CLK;
#define pADI_CLKG0_CLK (&storage_pADI_CLKG0_CLK)
static struct {volatile uint32_t CFG;volatile uint32_t IEN;volatile uint32_t PE;} storage_pADI_GPIO0;
#define pADI_GPIO0 (&storage_pADI_GPIO0)
static struct {volatile uint32_t COMDIV;volatile uint32_t COMFBR;volatile uint32_t COMFCR;volatile uint32_t COMIEN;volatile uint32_t COMLCR;volatile uint32_t COMLCR2;volatile uint32_t COMLSR;volatile uint32_t COMTX;} storage_pADI_UART0;
#define pADI_UART0 (&storage_pADI_UART0)
static struct {volatile uint32_t CNT;volatile uint32_t CTL;volatile uint32_t DIV;volatile uint32_t FIFO_STAT;volatile uint32_t RX;volatile uint32_t STAT;volatile uint32_t TX;} storage_pADI_SPI0;
#define pADI_SPI0 (&storage_pADI_SPI0)
static struct {volatile uint32_t CFG;volatile uint32_t CLR;volatile uint32_t OEN;volatile uint32_t PE;volatile uint32_t SET;} storage_pADI_GPIO1;
#define pADI_GPIO1 (&storage_pADI_GPIO1)
static struct {volatile uint32_t CLR;volatile uint32_t OEN;volatile uint32_t PE;volatile uint32_t SET;} storage_pADI_GPIO2;
#define pADI_GPIO2 (&storage_pADI_GPIO2)
static struct {volatile uint32_t CTRL;volatile uint32_t LOAD;} storage_SysTick;
#define SysTick (&storage_SysTick)
static struct {volatile uint32_t CFG0;volatile uint32_t CLR;} storage_pADI_XINT0;
#define pADI_XINT0 (&storage_pADI_XINT0)
#define BITM_CLKG_CLK_CTL0_CLKMUX 0x3u
#define BITM_CLKG_CLK_CTL1_PCLKDIVCNT 0x3f00u
#define BITM_CLKG_CLK_CTL3_SPLLNSEL 0x1fu
#define BITM_CLKG_OSC_CTL_HFOSCEN 0x2u
#define BITM_CLKG_OSC_CTL_HFXTALEN 0x8u
#define BITM_CLKG_OSC_CTL_HFXTALOK 0x800u
#define BITM_SPI_CTL_CON 0x800u
#define BITM_SPI_CTL_CSRST 0x4000u
#define BITM_SPI_CTL_MASEN 0x2u
#define BITM_SPI_CTL_OEN 0x200u
#define BITM_SPI_CTL_RXOF 0x100u
#define BITM_SPI_CTL_SPIEN 0x1u
#define BITM_SPI_CTL_TIM 0x40u
#define BITM_SPI_CTL_ZEN 0x80u
#define BITM_SPI_STAT_XFRDONE 0x2u
#define BITM_UART_COMFCR_FIFOEN 0x1u
#define BITM_UART_COMFCR_RFCLR 0x2u
#define BITM_UART_COMFCR_RFTRIG 0xc0u
#define BITM_UART_COMFCR_TFCLR 0x4u
#define BITM_XINT_CLR_IRQ0 0x1u
#define XINT_EVT0_IRQn 1u
#define UART_EVT_IRQn 14u
static unsigned uart_irq_enabled,uart_enable_calls;
static inline void NVIC_EnableIRQ(unsigned n){if(n==14){uart_irq_enabled=1;uart_enable_calls++;}}
static inline void NVIC_DisableIRQ(unsigned n){if(n==14)uart_irq_enabled=0;}
static inline void __disable_irq(void){}
static inline void __WFI(void){}
#endif
