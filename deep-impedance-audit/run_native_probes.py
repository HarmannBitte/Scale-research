"""Generate and run exact upstream C-function probes with simulated peripherals.
Usage: python run_native_probes.py --sources PATH/TO/COLLECTION/sources
No hardware, SDK calls or firmware flashing. GCC host tests are not target builds.
"""
import argparse,pathlib,re,json,hashlib,subprocess,os
ap=argparse.ArgumentParser();ap.add_argument('--sources',type=pathlib.Path,required=True);a=ap.parse_args();S=a.sources.resolve();O=pathlib.Path(__file__).resolve().parent;G=O/'generated';G.mkdir(exist_ok=True);C=pathlib.Path('/home/user/.cache/open-projects/deep-audit/native');C.mkdir(parents=True,exist_ok=True);provenance=[];results=[]
def extract(repo,path,name):
 p=S/repo/path;t=p.read_text();masked=re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',lambda m:' '*len(m[0]),t,flags=re.S);pat=re.compile(r'(?m)^[\w\s*]+\b'+re.escape(name)+r'\s*\([^;{}]*\)\s*\{');m=pat.search(masked)
 if not m:raise ValueError((path,name))
 start=m.start();pos=m.end();depth=1
 while depth:
  if masked[pos]=='{':depth+=1
  elif masked[pos]=='}':depth-=1
  pos+=1
 piece=t[start:pos];provenance.append({'repo_directory':repo,'path':path,'function':name,'line':t[:start].count('\n')+1,'full_file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'function_sha256':hashlib.sha256(piece.encode()).hexdigest()});return piece

def run(group,src,cases,flags=None):
 file=G/(group+'.c');file.write_text(src);exe=C/group;cmd=['gcc','-std=gnu11','-O1','-g','-Wall','-Wextra']+(flags or [])+[str(file),'-lm','-o',str(exe)];q=subprocess.run(cmd,capture_output=True,text=True);(O/(group+'-compile.log')).write_text(q.stdout+q.stderr)
 if q.returncode:raise RuntimeError(q.stderr)
 for case in cases:
  env=os.environ.copy();env['ASAN_OPTIONS']='detect_leaks=0:halt_on_error=1';q=subprocess.run([str(exe)]+list(map(str,case)),capture_output=True,text=True,timeout=5,env=env);name=group+'-'+'-'.join(map(str,case));(O/(name+'.log')).write_text(q.stdout+q.stderr);results.append({'name':name,'group':group,'arguments':case,'exit_code':q.returncode,'stdout':q.stdout,'diagnostic':q.stderr[:900],'log':name+'.log'})
base='#include <stdint.h>\n#include <stdbool.h>\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n#include <math.h>\n'
# UPRM exact FIFO read function, normal C ABI peripheral stubs.
prefix=base+'''uint8_t gReadBuf[100],gHold[100];
static int hi,lo,decoded;
#define SPI ((void*)1)
#define E_NO_ERROR 0
struct request {void *spi;uint8_t *txData,*rxData;int txLen,rxLen,ssIdx,ssDeassert,txCnt,rxCnt;void *completeCB;} req;
int regRead(int addr){gReadBuf[2]=addr==0x0A?hi:lo;return gReadBuf[2];}
int MXC_SPI_MasterTransaction(struct request *r){
 fprintf(stdout,"transaction_bytes=%d (upstream fifoCount=(counter1&0x7F)*2+counter2)\\n",r->rxLen);fflush(stdout);
 const uint8_t samples[]={0,0,0x10,0,100,0x2F,0xFF,0xCE};
 for(int i=0;i<r->rxLen;i++)r->rxData[i]=samples[i%8];return 0;}
int calcBioZ(uint8_t *b,bool f){(void)b;(void)f;decoded++;return 0;}
'''
body=extract('oscaroflores__UPRM-Multi_Frq-BioZ-Research','src/spiFunctions.c','spiBurst');src=prefix+body+'''\nint main(int argc,char **argv){(void)argc;hi=atoi(argv[1]);lo=atoi(argv[2]);int ret=spiBurst(false);printf("return=%d decoded_pairs=%d\\n",ret,decoded);return 0;}
''';run('uprm-fifo',src,[(0,0),(128,0),(0,1),(0,2),(0,3),(0,8),(1,0)],['-fsanitize=address','-fno-omit-frame-pointer','-no-pie'])
# UPRM init + clock/scaling helpers, exact algorithms and byte-register model.
names=['setMdiv','BIAsettings','getRefClkHz','getSampleInterval','getDACOSR','getKDiv','getBiozGain','getBiozCurrent_uA','setFreq','getMdiv','getPllClk','getBiozFreq','convertCountsToOhms','getBiozOhmCoeff','setBiozOhmCoeff','getBiozOhmCoeffCached']
prefix=base+'''static uint8_t regs[256];static double bioz_ohm_coeff=1.0;double ndiv,bioz_adc_osr,sr_bioz;
int regRead(int a){return regs[a];}void regWrite(int a,int b){regs[a]=b;}
'''+extract('oscaroflores__UPRM-Multi_Frq-BioZ-Research','src/spiFunctions.c','changeReg')
src=prefix+'\n'.join(extract('oscaroflores__UPRM-Multi_Frq-BioZ-Research','src/bioZ.c',n) for n in names)+'''\nint main(void){BIAsettings();printf("reg17=%u reg20=%u raw_mdiv=%d gain=%.12g current_uA=%.12g coeff_ohm_per_count=%.12g\\n",regs[0x17],regs[0x20],getMdiv(),getBiozGain(),getBiozCurrent_uA(),getBiozOhmCoeff());double sec=getSampleInterval();printf("interval_seconds=%.12g sample_interval_us_assigned_as_upstream=%u samples_per_second=%.12g\\n",sec,(uint32_t)sec,sr_bioz);setFreq(0);printf("low_frequency_Hz=%.12g\\n",getBiozFreq());setFreq(1);printf("high_frequency_Hz=%.12g\\n",getBiozFreq());return 0;}
''';run('uprm-clock-scale',src,[()])
# OpenEBI exact averaging: average=0 and bounded peripheral no-data behavior.
prefix=base+'''static int polls,limit;void _delay_ms(int n){(void)n;}
int ad5933_has_valid_impedance(void){if(++polls>limit){puts("stub_poll_budget_exhausted (upstream never returned)");exit(42);}return limit!=50;}
int ad5933_get_real(void){return -1234;}int ad5933_get_imaginary(void){return 2345;}void ad5933_repeat_frequency(void){}
''';src=prefix+extract('openebi__software','main.c','take_measurement')+'''\nint main(int argc,char **argv){(void)argc;limit=atoi(argv[2]);double r=9,i=9;take_measurement(atoi(argv[1]),&r,&i);printf("real=%g imag=%g finite=%d polls=%d\\n",r,i,isfinite(r)&&isfinite(i),polls);return 0;}
''';run('openebi-averaging',src,[(0,1000),(1,1000),(16,1000),(1,50)])
# Spectra exact fixed-point magnitude, host union's full field only (no bitfield ABI assumption).
prefix=base+'''typedef int32_t q31_t;typedef int64_t q63_t;typedef union{int32_t full;}fixed32_t;
''';src=prefix+extract('OpenEIT__EIT_Firmware','OpenEIT.c','calculate_magnitude')+'''\nint main(void){int32_t nums[]={1000,1000,134217728,268435456};int32_t den[]={1000,0,1,1};for(int i=0;i<4;i++){fixed32_t z=calculate_magnitude(nums[i],den[i],1);printf("numerator=%d denominator=%d raw=%d displayed_ohm_equivalent=%.6f\\n",nums[i],den[i],z.full,z.full/16.0);}return 0;}
''';run('spectra-fixed-point',src,[()])

# --- Added in deep audit pass 2: OpenEIT bipolar amplitude word (macros copied from modes.h) ---
mh=(S/'OpenEIT__EIT_Firmware'/'modes.h').read_text(errors='replace')
def macro(name): 
 m=re.search(r'#define\s+'+name+r'\s+(.+)',mh);return m[1].strip()
src=base+'''#define VPEAK (599)
#define VPEAK_BIPOLAR (12.73)
#define DAC_LSB_SIZE (0.39072)
#define SINE_AMPLITUDE ((uint16_t)((VPEAK) / DAC_LSB_SIZE + 0.5))
#define SINE_AMPLITUDE_BIPOLAR ((uint16_t)((VPEAK * 40) / DAC_LSB_SIZE + 0.5))
#define SEQ_MMR_WRITE(addr, data)   (0x80000000 | ((addr & 0xFC) << 23) | data)
#define REG_AFE_AFE_WG_AMPLITUDE 0x4008003C
#define BITM_SINE_AMPLITUDE 0x000007FF  /* ADuCM350 afe header: 11-bit field */
int main(void){
 printf("unipolar_word=%u\\n",(unsigned)SINE_AMPLITUDE);
 printf("bipolar_word=%u\\n",(unsigned)SINE_AMPLITUDE_BIPOLAR);
 printf("bipolar_word_hex=0x%X\\n",(unsigned)SINE_AMPLITUDE_BIPOLAR);
 uint32_t seq=SEQ_MMR_WRITE(REG_AFE_AFE_WG_AMPLITUDE,SINE_AMPLITUDE_BIPOLAR);
 printf("sequence_word=0x%08X address_field_ok=%d\\n",seq,((seq>>23)&0xFC)==(REG_AFE_AFE_WG_AMPLITUDE&0xFC));
 printf("field_after_11bit_mask=%u\\n",(unsigned)(SINE_AMPLITUDE_BIPOLAR & BITM_SINE_AMPLITUDE));
 printf("field_mV_equiv_at_0.39072mV_per_code=%.2f\\n",(SINE_AMPLITUDE_BIPOLAR & BITM_SINE_AMPLITUDE)*DAC_LSB_SIZE);
 printf("intended_mV_equiv=%.2f\\n",VPEAK*40.0);
 printf("full_scale_11bit_mV=%.2f\\n",2047*DAC_LSB_SIZE);
 printf("unipolar_mV_equiv=%.2f\\n",SINE_AMPLITUDE*DAC_LSB_SIZE);
 return 0;}
'''
run('openeit-bipolar-amplitude',src,[()])

(O/'native-source-provenance.json').write_text(json.dumps(provenance,indent=2));(O/'native-probe-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
