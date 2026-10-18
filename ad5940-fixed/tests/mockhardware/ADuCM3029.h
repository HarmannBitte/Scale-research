/* FAKE HOST-ONLY REGISTER STORAGE. NOT an MCU device pack; NEVER use for a target build. */
#ifndef FAKE_ADUCM_H
#define FAKE_ADUCM_H
#include <stdint.h>
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
static struct {volatile uint32_t CFG;volatile uint32_t IEN;volatile uint32_t PE;} storage_pADI_GPIO0;
#define pADI_GPIO0 (&storage_pADI_GPIO0)
#define BITM_SPI_CTL_CON 1u
#define BITM_SPI_CTL_CSRST 1u
#define BITM_SPI_CTL_MASEN 1u
#define BITM_SPI_CTL_OEN 1u
#define BITM_SPI_CTL_RXOF 1u
#define BITM_SPI_CTL_SPIEN 1u
#define BITM_SPI_CTL_TIM 1u
#define BITM_SPI_CTL_ZEN 1u
#define BITM_SPI_STAT_XFRDONE 1u
#define BITM_XINT_CLR_IRQ0 1u
#define XINT_EVT0_IRQn 1u
static inline void NVIC_EnableIRQ(unsigned int n){(void)n;}
#endif
