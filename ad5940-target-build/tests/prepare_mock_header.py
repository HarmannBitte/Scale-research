"""Generate FAKE host register storage with real DFP bit-mask values, not an MCU emulator."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
base=ROOT/'source/examples/AD5940_BIA/ADICUP3029'
text=(base/'main.c').read_text()+(base/'ADICUP3029Port.c').read_text()
defs={}
for p in (ROOT/'vendor/ADuCM302x_DFP-3.2.1/Include').rglob('*.h'):
    defs.update(re.findall(r'^#define\s+(\w+)\s+([^\r\n]+)',p.read_text(encoding="latin1"),re.M))
def value(name):
    expr=defs[name].split('/*',1)[0]
    num=re.search(r'0x[0-9a-fA-F]+',expr)
    if num:return int(num[0],16)
    alias=re.search(r'\bBITM_\w+',expr)
    if alias:return value(alias[0])
    raise ValueError((name,expr))
objects={}
for obj,field in re.findall(r'(pADI_\w+|SysTick)->(\w+)',text):objects.setdefault(obj,set()).add(field)
lines=['/* GENERATED FAKE HOST-ONLY registers; real DFP bit masks; not MCU hardware. */','#ifndef FAKE_MCU_H','#define FAKE_MCU_H','#include <stdint.h>']
for name,fields in objects.items():
    lines+=['static struct {'+';'.join('volatile uint32_t '+f for f in sorted(fields))+';} storage_'+name+';', '#define '+name+' (&storage_'+name+')']
for name in sorted(set(re.findall(r'\bBITM_\w+\b',text))):lines.append(f'#define {name} {value(name):#x}u')
lines+=['#define XINT_EVT0_IRQn 1u','#define UART_EVT_IRQn 14u','static unsigned uart_irq_enabled,uart_enable_calls;','static inline void NVIC_EnableIRQ(unsigned n){if(n==14){uart_irq_enabled=1;uart_enable_calls++;}}','static inline void NVIC_DisableIRQ(unsigned n){if(n==14)uart_irq_enabled=0;}','static inline void __disable_irq(void){}','static inline void __WFI(void){}','#endif']
(ROOT/'tests/mockhardware/ADuCM3029.h').write_text('\n'.join(lines)+'\n')
