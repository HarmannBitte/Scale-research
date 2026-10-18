from pathlib import Path
import re,subprocess
root=Path(__file__).resolve().parents[1];lib=root/'source/examples/ad5940lib/ad5940.c'
def extract(sig):
 t=lib.read_text();a=t.index('\n'+sig)+1;o=t.index('{',a);d=0
 for i in range(o,len(t)):
  d+=(t[i]=='{')-(t[i]=='}')
  if d==0:return t[a:i+1]+'\n'
 raise ValueError(sig)
(root/'tests/library_extracts.inc').write_text('/* Exact host-only extracts from modified ADI library; original notice follows. */\n'+lib.read_text().split('#include',1)[0]+''.join(extract(x) for x in ['AD5940Err AD5940_BenchWaitInt(', 'static BoolFlag bench_wait_register(', 'void AD5940_SweepNext(', 'uint32_t AD5940_WGFreqWordCal(']))
# Generate only no-op peripheral mocks. Significant output/error behaviors are custom below.
custom={'AD5940_SEQGenCtrl','AD5940_BenchWaitInt','AD5940_SweepNext','AD5940_WGFreqWordCal','AD5940_HSRtiaCal','AD5940_ReadReg','AD5940_FIFOGetCnt','AD5940_FIFORd','AD5940_INTCTestFlag','AD5940_INTCGetFlag','AD5940_WakeUp','AD5940_SEQGenFetchSeq','AD5940_ClksCalculate','AD5940_SEQCycleTime','AD5940_SleepKeyCtrlS','AD5940_WUPTCtrl','AD5940_RstClr','AD5940_GetMCUIntFlag','AD5940_ClrMCUIntFlag'}
needed=set()
for name in ('body.o','main.o'):
 out=subprocess.check_output(['nm','-u',str(root/'tests'/name)],text=True)
 needed.update(re.findall(r'\b(AD5940_\w+)$',out,re.M))
header=(root/'source/examples/ad5940lib/ad5940.h').read_text()
out=['/* GENERATED NO-OP PERIPHERAL MOCKS, NOT hardware emulation. */\n']
for name in sorted(needed-custom-{'AD5940_BenchIoFault','AD5940_BenchCalTrace'}):
 m=re.search(r'^([^\n;{}]*\b'+name+r'\([^;]*?\));',header,re.M)
 if not m:raise ValueError('Missing prototype '+name)
 decl=m.group(1).strip();rtype=decl.split(name)[0].strip()
 out.append(decl+' {'+('' if rtype=='void' else 'return 0;')+'}\n')
(root/'tests/peripheral_mocks.inc').write_text(''.join(out))
