"""Strict offline parser for this fork's BIA1 frames, NOT legacy vendor UART."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import zlib
MAX_PAYLOAD=2048
class InvalidStream(ValueError):pass

def unique(pairs):
    result={}
    for k,v in pairs:
        if k in result:raise InvalidStream('Duplicate JSON key')
        result[k]=v
    return result

def encode_for_test(record):
    p=json.dumps(record,separators=(',',':'),allow_nan=False).encode('ascii')
    return b'BIA1 '+str(len(p)).encode()+b' '+f'{zlib.crc32(p):08x}'.encode()+b' '+p+b'\n'

def finite(v):
    try:return type(v) in (float,int) and math.isfinite(v)
    except OverflowError:return False

def reject_nonfinite_tree(v):
    if isinstance(v,float) and not math.isfinite(v):raise InvalidStream('Nonfinite JSON number')
    if isinstance(v,dict):
        for value in v.values():reject_nonfinite_tree(value)
    if isinstance(v,list):
        for value in v:reject_nonfinite_tree(value)
def integer(v):return type(v) is int and 0<=v<=0xffffffff

def parse(data):
    if not isinstance(data,bytes) or not data:raise InvalidStream('Empty/nonbyte input')
    records=[];run=None;config={};cal={};next_sequence=0;terminal=None
    for number,line in enumerate(data.splitlines(keepends=True),1):
        if terminal:raise InvalidStream('Records after terminal event')
        if not line.endswith(b'\n'):raise InvalidStream('Truncated frame')
        # CRLF accepted only as transport line ending, outside CRC payload.
        frame=line[:-2] if line.endswith(b'\r\n') else line[:-1]
        m=re.fullmatch(rb'BIA1 ([0-9]{1,5}) ([0-9a-f]{8}) (.*)',frame)
        if not m:raise InvalidStream(f'Bad framing at line {number}')
        count=int(m[1]);payload=m[3]
        if not 0<count<=MAX_PAYLOAD or count!=len(payload):raise InvalidStream('Payload length mismatch/limit')
        if zlib.crc32(payload)!=int(m[2],16):raise InvalidStream('CRC mismatch')
        try:
            r=json.loads(payload.decode('ascii'),object_pairs_hook=unique,
                         parse_constant=lambda _:(_ for _ in ()).throw(InvalidStream('Nonfinite JSON')))
        except (UnicodeError,json.JSONDecodeError,RecursionError) as e:raise InvalidStream('Invalid JSON') from e
        reject_nonfinite_tree(r)
        if not isinstance(r,dict):raise InvalidStream('Record must be an object')
        typ=r.get('type')
        if not records:
            if typ!='session' or type(r.get('schema')) is not int or r.get('schema')!=1 or r.get('source_kind') not in ('hardware','synthetic'):
                raise InvalidStream('Expected supported session record')
            run=r.get('run_id')
            if not isinstance(run,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,48}',run) or run=='UNSET':raise InvalidStream('Invalid run ID')
            if r.get('device_qualified') is not False:raise InvalidStream('Qualification claim prohibited')
        elif typ=='session' or r.get('run_id')!=run:raise InvalidStream('Session mismatch/restart')
        elif typ=='configuration':
            cid=r.get('config_id');kid=r.get('calibration_id')
            if not integer(cid) or not cid or cid in config or not integer(kid) or not kid:raise InvalidStream('Invalid/duplicate config')
            if not finite(r.get('frequency_requested_hz')) or r['frequency_requested_hz']!=50000:raise InvalidStream('Unsupported frequency')
            if not finite(r.get('frequency_estimate_hz')) or r['frequency_estimate_hz']<=0:raise InvalidStream('Invalid estimate')
            if r.get('frequency_measured_hz','missing') is not None or r.get('full_register_dump_available') is not False or r.get('sweep_enabled') is not False:raise InvalidStream('Unsupported configuration claim')
            for field,upper in [('min_current_dft_counts',3.402823466e38),('effective_odr_hz',20),('dac_parameter_mvpp',800),('wake_clock_assumed_hz',3.402823466e38)]:
                if not finite(r.get(field)) or not 0<r[field]<=upper:raise InvalidStream('Invalid configuration bound')
            if r.get('clock_assumed_hz')!=16000000 or r.get('adc_clock_assumed_hz')!=16000000:raise InvalidStream('Unsupported clocks')
            chip=r.get('chip_id');word=r.get('frequency_word')
            if not integer(chip) or chip not in (0x5500,0x5501,0x5502) or not integer(word):raise InvalidStream('Invalid frequency readback')
            scale=67108864 if chip==0x5500 else 1073741824
            if word!=int(50000*scale/16000000+0.5):raise InvalidStream('Frequency readback mismatch')
            estimate=word*16000000/(67108864 if chip==0x5500 else 1073741824)
            if abs(estimate-r['frequency_estimate_hz'])>1e-6:raise InvalidStream('Inconsistent frequency estimate')
            settings=r.get('settings')
            fixed={'power':0,'rtia':1,'ctia':16,'excitation_gain':0,'dac_gain':0,'dac_update':7,'pga':0,'osr3':2,'osr2':0,'dft_source':1,'hanning':1}
            if not isinstance(settings,dict) or any(type(settings.get(k)) is not int or settings[k]!=v for k,v in fixed.items()):raise InvalidStream('Unsupported settings')
            dft=settings.get('dft');threshold=settings.get('fifo_threshold_words')
            if not integer(dft) or dft>12 or not integer(threshold) or not 4<=threshold<=128 or threshold%4:raise InvalidStream('Invalid DFT/FIFO setting')
            config[cid]=r
        elif typ=='calibration':
            cid=r.get('config_id');kid=r.get('calibration_id')
            if not integer(cid) or not integer(kid) or cid not in config or config[cid]['calibration_id']!=kid or kid in cal:raise InvalidStream('Calibration/config mismatch')
            if r.get('status')!=0 or not finite(r.get('rtia_magnitude_ohm')) or r['rtia_magnitude_ohm']<=0 or not finite(r.get('rtia_phase_rad')):
                raise InvalidStream('Invalid successful calibration')
            if type(r.get('status')) is not int or r['rtia_magnitude_ohm']>3.402823466e38:raise InvalidStream('Invalid calibration representation')
            if not finite(r.get('rcal_configured_ohm')) or not 0<r['rcal_configured_ohm']<=3.402823466e38 or r.get('reference_certificate','missing') is not None:raise InvalidStream('Invalid/unimplemented calibration provenance')
            rawcal=r.get('raw_rcal_rtia_dft')
            if type(r.get('raw_dft_available')) is not bool or not isinstance(rawcal,list) or len(rawcal)!=4 or not all(integer(x) for x in rawcal):raise InvalidStream('Invalid raw calibration')
            cal[kid]=r
        elif typ=='measurement':
            cid=r.get('config_id');kid=r.get('calibration_id');seq=r.get('sequence')
            if not integer(seq) or seq!=next_sequence:raise InvalidStream('Sequence gap/duplicate/reorder')
            if not integer(cid) or not integer(kid) or cid not in config or kid not in cal or cal[kid]['config_id']!=cid:raise InvalidStream('Missing/mismatched provenance')
            if config[cid]['frequency_requested_hz']!=r.get('frequency_requested_hz'):raise InvalidStream('Frequency mismatch')
            raw=r.get('raw');dft=r.get('dft_counts')
            if not isinstance(raw,list) or len(raw)!=4 or not all(integer(x) for x in raw):raise InvalidStream('Bad raw words')
            decoded=[((x&0x3ffff)-262144 if x&0x20000 else x&0x3ffff) for x in raw]
            if dft!=decoded or not isinstance(dft,list) or any(type(x) is not int for x in dft):raise InvalidStream('DFT decode mismatch')
            vals=r.get('derived_r_x_mag_ohm_phase_rad');status=r.get('status')
            if type(status) is not int:raise InvalidStream('Bad status')
            if r.get('numerical_valid') is True:
                if status!=0 or not isinstance(vals,list) or len(vals)!=4 or not all(finite(x) for x in vals):raise InvalidStream('Invalid numerical result')
                cr,ci,vr,vi=dft;current=complex(cr,-ci)
                if abs(current)<config[cid]['min_current_dft_counts']:raise InvalidStream('Current below declared floor')
                rt=cal[kid];z=complex(vr,-vi)/current*complex(rt['rtia_magnitude_ohm']*math.cos(rt['rtia_phase_rad']),rt['rtia_magnitude_ohm']*math.sin(rt['rtia_phase_rad']))
                if not finite(z.real) or not finite(z.imag) or not finite(abs(z)) or abs(vals[3])>math.pi+1e-6:raise InvalidStream('Invalid expected value/wrapped phase')
                if abs(complex(vals[0],vals[1])-z)>max(.002,abs(z)*2e-6):raise InvalidStream('Raw/calibrated mismatch')
                if vals[2]<0 or abs(math.hypot(vals[0],vals[1])-vals[2])>max(.002,abs(z)*2e-6):raise InvalidStream('Magnitude mismatch')
                if abs(math.atan2(math.sin(vals[3]-math.atan2(vals[1],vals[0])),math.cos(vals[3]-math.atan2(vals[1],vals[0]))))>2e-6:raise InvalidStream('Phase mismatch')
            elif r.get('numerical_valid') is not False or vals is not None or status==0:raise InvalidStream('Invalid failure record')
            if r.get('qualification_eligible') is not False:raise InvalidStream('Qualification claim prohibited')
            if any(k not in r or r[k] is not None for k in ('clipping','compliance_fault','lead_off','transport_loss')):raise InvalidStream('Unvalidated diagnostics must remain unknown')
            if r.get('acquisition_time_ns','missing') is not None or not integer(r.get('interrupt_flags')):raise InvalidStream('Unsupported acquisition-time/flag representation')
            next_sequence+=1
        elif typ in ('fault','end'):
            if r.get('qualification_eligible') is not False:raise InvalidStream('Qualification claim prohibited')
            if typ=='end' and (not integer(r.get('frames_decoded')) or r['frames_decoded']!=next_sequence):raise InvalidStream('End count mismatch')
            terminal=typ
        else:raise InvalidStream('Unsupported record type')
        records.append(r)
    return dict(source_sha256=hashlib.sha256(data).hexdigest(),source_kind=records[0]['source_kind'],
                run_id=run,record_count=len(records),measurement_count=next_sequence,
                terminal_event=terminal,clean_terminal=(terminal=='end'),
                device_qualified=False,human_connection_authorized=False,
                upstream_loss_extent='unknown',records=records)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists() or a.output.resolve()==a.input.resolve():p.error('Output must be a new file, not the source')
    try:result=parse(a.input.read_bytes())
    except (InvalidStream,OSError) as e:p.exit(1,f'INVALID STREAM: {e}\n')
    a.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(f"Parsed {result['record_count']} records; terminal={result['terminal_event']}; device_qualified=false")
if __name__=='__main__':main()
