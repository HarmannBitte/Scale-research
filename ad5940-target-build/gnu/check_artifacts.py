"""Inspect linked ARM ELFs, real-header dependencies and startup/memory wiring. No execution."""
from pathlib import Path
import csv,json,re,struct,subprocess
ROOT=Path(__file__).resolve().parents[1]
if not __debug__:raise SystemExit('Checks require normal Python mode, not -O/PYTHONOPTIMIZE.')
summary={}
for profile,armed in [('unarmed','0'),('fullpath-linkcheck','1')]:
    folder=ROOT/'build'/profile;elf=folder/'firmware.elf';data=elf.read_bytes()
    assert data[:7]==b'\x7fELF\x01\x01\x01'
    assert struct.unpack_from('<H',data,18)[0]==40 # EM_ARM
    entry=struct.unpack_from('<I',data,24)[0]
    phoff,shoff=struct.unpack_from('<II',data,28)
    phsize,phnum,shsize,shnum,shstr=struct.unpack_from('<HHHHH',data,42)
    sections=[struct.unpack_from('<IIIIIIIIII',data,shoff+i*shsize) for i in range(shnum)]
    names=sections[shstr];strings=data[names[4]:names[4]+names[5]]
    sections={strings[s[0]:].split(b'\0',1)[0].decode():s for s in sections}
    v=sections['.vectors'];sp,reset=struct.unpack_from('<II',data,v[4])
    nm=subprocess.check_output(['arm-none-eabi-nm','-n',str(elf)],text=True)
    symbols={parts[2]:int(parts[0],16) for line in nm.splitlines() if len(parts:=line.split())==3}
    assert sp==symbols['__StackTop']==0x20004000
    assert reset==(symbols['Reset_Handler']|1)==entry
    assert symbols['__StackTop']-symbols['__StackLimit']==8192
    assert symbols['__HeapLimit']-symbols['__HeapBase']==4096
    assert symbols['__HeapLimit']<=symbols['__StackLimit']
    assert sections['.security_options'][3]==0x180
    assert symbols['Ext_Int0_Handler']!=symbols['Default_Handler']
    assert symbols['UART_Int_Handler']==symbols['Default_Handler'] # Deliberately disabled TX-only IRQ.
    undefined=subprocess.check_output(['arm-none-eabi-nm','-u',str(elf)],text=True)
    assert not undefined.strip(),undefined
    for function in ['_write','_sbrk','_exit','fputc','AD5940_ReadWriteNBytes']:
        assert function in symbols,function
    if armed=='1':
        for function in ['AppBIADecodeFrame','AppBIAISR','AD5940_HSRtiaCal']:assert function in symbols,function
    assert 'AD5940_ADCPGACal' not in symbols # Known uninitialized-code warning is outside linked BIA path.
    for dep in folder.glob('*.d'):assert 'mockhardware' not in dep.read_text()
    deps=(folder/'main.d').read_text()+(folder/'ADICUP3029Port.d').read_text()
    assert 'vendor/ADuCM302x_DFP-3.2.1/Include/ADuCM3029.h' in deps
    assert 'vendor/CMSIS-5.2.0/Include/core_cm3.h' in deps
    macros=dict(re.findall(r'^#define (\w+) (.+)$',(folder/'compiled-macros.txt').read_text(),re.M))
    for name,expected in [('BIA_BENCH_ARMED',armed),('BIA_BENCH_RUN_ID','"UNSET"'),('BIA_BENCH_MIN_CURRENT_COUNTS','0'),('BIA_BENCH_RCAL_OHM','0')]:assert macros[name]==expected,(name,macros[name])
    loads=[]
    for i in range(phnum):
        p=struct.unpack_from('<IIIIIIII',data,phoff+i*phsize)
        if p[0]==1:
            _,offset,vaddr,paddr,filesz,memsz,flags,align=p
            assert 0<=paddr<0x40000 and paddr+filesz<=0x40000
            loads.append(dict(vaddr=vaddr,paddr=paddr,flash_load_bytes=filesz,memory_bytes=memsz))
    assert symbols['__data_start__']==0x20040000
    assert symbols['__bss_end__']<=0x20044000
    dis=(folder/'disassembly.txt').read_text()
    assert not re.search(r'\bbkpt\s+(?:0x00ab|0xab|171)\b',dis,re.I)
    assert not any(x in symbols for x in ['initialise_monitor_handles','do_AngelSWI','_swiwrite'])
    frames=[]
    for p in folder.glob('*.su'):
        for line in p.read_text().splitlines():
            where,amount,kind=line.split('\t');frames.append(dict(function=where.rsplit(':',1)[-1],bytes=int(amount),kind=kind,source=where))
    frames.sort(key=lambda r:r['bytes'],reverse=True)
    with (folder/'stack-frames.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['function','bytes','kind','source']);w.writeheader();w.writerows(frames)
    summary[profile]=dict(arm_elf=True,entry=entry,initial_stack_pointer=sp,vector_reset_matches_entry=True,stack_reserved_bytes=8192,heap_reserved_bytes=4096,unallocated_bank_a_gap_bytes=symbols['__StackLimit']-symbols['__HeapLimit'],static_bank_b_bytes=symbols['__bss_end__']-symbols['__data_start__'],static_bank_b_remaining_bytes=0x20044000-symbols['__bss_end__'],flash_load_bytes=sum(p['flash_load_bytes'] for p in loads),flash_address_high_water=max(p['paddr']+p['flash_load_bytes'] for p in loads),largest_compiled_c_frame=frames[0],target_executed=False,semihosting_backend_detected=False,complete_stack_bound_proven=False,acquisition_gates=dict(armed=int(armed),run_id='UNSET',current_floor=0,rcal_ohm=0),loads=loads)
(ROOT/'receipts/artifact-checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS: both ARM ELFs, vectors, reservations, real-header dependencies, gates, symbol resolution and selected backend checks.')
print('Not a target execution, runtime stack proof, flash authorization or electrical test.')
