import cmath,copy,json,math,random,subprocess,sys,unittest,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from parse_bia_stream import parse,encode_for_test,InvalidStream

def native(*args,unarmed=False):
    binary=ROOT/'tests'/('host_probe_unarmed' if unarmed else 'host_probe')
    return subprocess.check_output([str(binary),*map(str,args)],text=True)
def obj(*a,**k):return json.loads(native(*a,**k))
def decode(cr=10000,ci=0,vr=5000,vi=0,mag=1000,phase=0,floor=1):return obj('process',cr,ci,vr,vi,mag,phase,floor)
def isr(n=4,capacity=512,wake=0,inited=1,flags=0,ready=1):return obj('isr',n,capacity,wake,inited,flags,ready)
class NativeFixes(unittest.TestCase):
 def test_nominal_r(self):self.assertEqual(decode()['r'],500)
 def test_capacitive_sign(self):self.assertEqual(decode(vi=1000)['x'],-100)
 def test_raw_preserved_including_high_bits(self):
  r=decode(cr=0xa0002710);self.assertTrue(r['raw_unchanged']);self.assertEqual(r['raw'][0],0xa0002710);self.assertEqual(r['dft'][0],10000)
 def test_negative_boundary(self):self.assertEqual(decode(-131072,0,-65536)['r'],500)
 def test_positive_boundary(self):self.assertEqual(decode(131071,0,131071)['r'],1000)
 def test_zero_current_rejected(self):self.assertLess(decode(0,0)['status'],0)
 def test_both_zero_rejected(self):self.assertLess(decode(0,0,0,0)['status'],0)
 def test_noise_floor_rejected(self):self.assertLess(decode(cr=5,floor=10)['status'],0)
 def test_invalid_floors_rejected(self):
  for floor in [0,-1,'nan','inf']:
   with self.subTest(floor=floor):self.assertLess(decode(floor=floor)['status'],0)
 def test_invalid_calibration_rejected(self):
  for mag,ph in [(0,0),(-1,0),('nan',0),('inf',0),(1000,'nan'),(1000,'inf')]:
   with self.subTest(mag=mag,phase=ph):self.assertLess(decode(mag=mag,phase=ph)['status'],0)
 def test_wrapped_phase(self):self.assertLessEqual(abs(decode(phase=4)['phase']),math.pi)
 def test_complex_parity_100_cases(self):
  rng=random.Random(20261017)
  for i in range(100):
   vals=[rng.randint(-120000,120000) for _ in range(4)];mag=rng.uniform(200,10000);ph=rng.uniform(-6,6)
   with self.subTest(case=i):
    r=decode(*vals,mag=mag,phase=ph);cr,ci,vr,vi=vals;expected=complex(vr,-vi)/complex(cr,-ci)*cmath.rect(mag,ph)
    self.assertEqual(r['status'],0);self.assertLess(abs(complex(r['r'],r['x'])-expected),max(.002,abs(expected)*2e-6))
 def test_ordinary_fifo(self):
  r=isr();self.assertEqual((r['status'],r['count'],r['read_words']),(0,1,4));self.assertEqual(r['lock'],0)
 def test_oversized_fifo_no_read(self):
  for words in [132,516,1024]:
   with self.subTest(words=words):
    r=isr(words);self.assertEqual(r['status'],-4);self.assertEqual(r['count'],0);self.assertEqual(r['read_words'],0);self.assertFalse(r['cal_valid']);self.assertEqual(r['lock'],0)
 def test_zero_capacity_no_read(self):
  r=isr(capacity=0);self.assertEqual(r['count'],0);self.assertEqual(r['read_words'],0)
 def test_small_capacity_no_read(self):self.assertEqual(isr(capacity=3)['read_words'],0)
 def test_partial_frame_no_read(self):self.assertEqual(isr(n=6)['read_words'],0)
 def test_wakeup_error_zero_count(self):
  r=isr(wake=11);self.assertEqual(r['status'],-9);self.assertEqual(r['count'],0)
 def test_uninitialized_zero_count(self):
  r=isr(inited=0);self.assertEqual(r['status'],-100);self.assertEqual(r['count'],0)
 def test_no_threshold_unlocks(self):
  r=isr(ready=0);self.assertEqual(r['status'],0);self.assertEqual(r['count'],0);self.assertEqual(r['lock'],0)
 def test_hardware_status_flags_stop(self):
  for flags in [16,32,0x04000000,0x08000000,0x20000]:
   with self.subTest(flags=flags):
    r=isr(flags=flags);self.assertLess(r['status'],0);self.assertEqual(r['read_words'],0);self.assertFalse(r['cal_valid'])
 def test_null_inputs(self):
  r=obj('null');self.assertEqual(r['count'],0);self.assertLess(r['status'],0);self.assertEqual(r['null_count_status'],-3)
 def test_cal_error_propagates_and_invalidates(self):
  r=obj('cal',-2,1000,0);self.assertEqual(r['status'],-2);self.assertFalse(r['cal_valid']);self.assertEqual(r['rtia'],0)
 def test_cal_success(self):self.assertEqual(obj('cal',0,1000,0)['cal_valid'],1)
 def test_cal_invalid_output(self):
  for mag,ph in [(0,0),('nan',0),('inf',0),(1000,'nan')]:
   with self.subTest(mag=mag,ph=ph):self.assertFalse(obj('cal',0,mag,ph)['cal_valid'])
 def test_config_change_invalidates(self):
  r=obj('stale');self.assertLess(r['status'],0);self.assertEqual(r['count'],0);self.assertFalse(r['cal_valid'])
 def test_cal_coefficient_tamper_prevents_start(self):
  r=obj('stale_rtia');self.assertFalse(r['cal_valid']);self.assertLess(r['start_status'],0)
 def test_sequence_generation_failure_stops_and_invalidates(self):
  r=obj('init_seq_bad');self.assertLess(r['status'],0);self.assertGreater(r['stop_calls'],0);self.assertFalse(r['cal_valid']);self.assertFalse(r['inited']);self.assertEqual(r['generator'],0);self.assertEqual(r['encoded_stop'],0)
 def test_bad_reinit_stops_old_run(self):
  r=obj('reinit_bad');self.assertLess(r['status'],0);self.assertGreater(r['stop_calls'],0);self.assertFalse(r['cal_valid'])
 def test_app_sweeps_fail_closed(self):
  for points in [0,1,2,100,101]:self.assertLess(obj('sweep',points)['status'],0)
 def test_library_log_ratio_does_not_overflow_float(self):
  r=obj('lib_sweep',2,'1e-30','1e30');self.assertTrue(r['finite']);self.assertEqual(r['io_fault'],0)
 def test_library_bad_sweep_latches_error(self):
  for n in [0,1]:
   r=obj('lib_sweep',n);self.assertFalse(r['finite']);self.assertEqual(r['io_fault'],-2)
 def test_poll_timeout(self):
  r=obj('wait');self.assertEqual(r,dict(status=-10,calls=8,io_fault=-10))
 def test_register_poll_timeout(self):self.assertEqual(obj('waitreg'),dict(ready=0,io_fault=-10))
 def test_init_ok(self):
  r=obj('init',0,1,1);self.assertEqual(r['status'],0);self.assertTrue(r['cal_valid']);self.assertTrue(r['inited'])
 def test_init_failed_cal_stays_uninitialized(self):
  r=obj('init',-2,1,1);self.assertEqual(r['status'],-2);self.assertFalse(r['inited']);self.assertFalse(r['cal_valid'])
 def test_init_missing_threshold(self):self.assertLess(obj('init',0,1,0)['status'],0)
 def test_init_timeout_asserts_reset(self):
  r=obj('init',0,0,1);self.assertEqual(r['status'],-10);self.assertFalse(r['inited']);self.assertGreater(r['reset_calls'],0)
 def test_unarmed_refuses_init(self):self.assertLess(obj('init',0,1,1,unarmed=True)['status'],0)
 def test_crc_standard_vector(self):self.assertEqual(native('crc').strip(),'cbf43926')
 def test_bad_session_ids(self):
  for run in ['UNSET','bad"id','bad id','x'*49]:self.assertLess(int(native('session',run)),0)
 def test_main_fault_does_not_format_stale_count(self):
  r=parse(native('mainfault').encode());self.assertEqual(r['measurement_count'],0);self.assertEqual(r['terminal_event'],'fault')

 def test_invalid_frequency_word_inputs(self):
  for f in ['nan','inf',-1,0,'1e30']:
   with self.subTest(f=f):self.assertEqual(obj('wgvalue',f)['io_fault'],-2)
 def test_frequency_word_normal(self):
  r=obj('wgvalue',50000);self.assertEqual(r['io_fault'],0);self.assertEqual(r['word'],3355443)
 def test_logger_rejects_wrong_frequency_readback(self):
  r=json.loads(native('readback_bad').splitlines()[-1]);self.assertLess(r['status'],0)
 def test_maximum_batch(self):
  r=isr(n=128);self.assertEqual((r['status'],r['count'],r['read_words']),(0,32,128))
 def test_postread_fault_preserves_invalid_raw(self):
  r=obj('postflag');self.assertLess(r['status'],0);self.assertEqual(r['captured'],1);self.assertEqual(r['count'],1);self.assertLess(r['frame_status'],0)
 def test_actual_port_stalled_spi(self):
  r=subprocess.check_output([str(ROOT/'tests/port_probe'),'spi'],text=True).strip();self.assertEqual(r,'-10 0')
 def test_actual_port_stalled_delay(self):
  r=subprocess.check_output([str(ROOT/'tests/port_probe'),'delay'],text=True).strip();self.assertEqual(r,'-10 0')
 def test_actual_port_zero_length(self):
  r=subprocess.check_output([str(ROOT/'tests/port_probe'),'zero'],text=True).strip();self.assertEqual(r,'0')
 def test_actual_port_null_buffers(self):
  r=subprocess.check_output([str(ROOT/'tests/port_probe'),'null'],text=True).strip();self.assertEqual(r,'-2')

class StreamTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=native('pipeline').encode();cls.records=parse(cls.data)['records']
 def changed(self,fn):
  rows=copy.deepcopy(self.records);fn(rows);return b''.join(encode_for_test(x) for x in rows)
 def test_full_pipeline(self):
  r=parse(self.data);self.assertEqual(r['measurement_count'],1);self.assertTrue(r['clean_terminal']);self.assertEqual(r['source_kind'],'synthetic');self.assertFalse(r['device_qualified']);self.assertFalse(r['human_connection_authorized'])
 def test_raw_config_cal_linkage(self):
  rows=parse(self.data)['records'];self.assertEqual(rows[3]['raw'][0],0xa0002710);self.assertEqual(rows[2]['raw_rcal_rtia_dft'],[100,101,102,103]);self.assertEqual(rows[3]['config_id'],rows[1]['config_id'])
 def test_diagnostics_unknown_not_clear(self):
  r=self.records[3];self.assertTrue(r['numerical_valid']);self.assertFalse(r['qualification_eligible']);self.assertIsNone(r['clipping'])
 def test_invalid_raw_record_survives_fault(self):
  r=parse(native('pipeline_bad').encode());self.assertEqual(r['terminal_event'],'fault');self.assertEqual(r['measurement_count'],1)
  f=next(x for x in r['records'] if x['type']=='measurement');self.assertFalse(f['numerical_valid']);self.assertIsNone(f['derived_r_x_mag_ohm_phase_rad']);self.assertEqual(f['raw'][0],0xa0002710)
 def test_wrong_readback_rejected_even_consistent_estimate(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[1].update(frequency_word=1,frequency_estimate_hz=16000000/1073741824)))
 def test_declared_current_floor_enforced(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[1].update(min_current_dft_counts=100000)))
 def test_huge_calibration_rejected(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[2].update(rtia_magnitude_ohm=1e308)))
 def test_unwrapped_phase_rejected(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[3]['derived_r_x_mag_ohm_phase_rad'].__setitem__(3,2*math.pi)))
 def test_config_claims_and_bounds(self):
  for values in [dict(frequency_measured_hz=50000),dict(full_register_dump_available=True),dict(min_current_dft_counts=0),dict(frequency_estimate_hz=1234),dict(effective_odr_hz=21),dict(sweep_enabled=True),dict(clock_assumed_hz=32000000),dict(settings={})]:
   with self.subTest(values=values),self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[1].update(values)))
 def test_crc_corruption(self):
  data=self.data.replace(b'"synthetic"',b'"synthEtic"',1)
  with self.assertRaises(InvalidStream):parse(data)
 def test_truncated(self):
  with self.assertRaises(InvalidStream):parse(self.data[:-1])
 def test_length_mismatch(self):
  with self.assertRaises(InvalidStream):parse(self.data.replace(b'BIA1 141',b'BIA1 140',1))
 def test_reordered_provenance(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r.__setitem__(slice(1,3),list(reversed(r[1:3])))))
 def test_sequence_gap(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[3].update(sequence=2)))
 def test_duplicate_sequence(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r.insert(4,copy.deepcopy(r[3]))))
 def test_session_mismatch(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[3].update(run_id='other')))
 def test_null_config_id_rejected(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[3].update(config_id=[])))
 def test_raw_decode_mismatch(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[3]['dft_counts'].__setitem__(0,999)))
 def test_derived_mismatch(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[3]['derived_r_x_mag_ohm_phase_rad'].__setitem__(0,123)))
 def test_fake_clean_diagnostic(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[3].update(clipping=False)))
 def test_qualification_claim_rejected(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[3].update(qualification_eligible=True)))
 def test_end_count_mismatch(self):
  with self.assertRaises(InvalidStream):parse(self.changed(lambda r:r[4].update(frames_decoded=2)))
 def test_no_end_marked_incomplete(self):
  r=parse(b''.join(encode_for_test(x) for x in self.records[:-1]));self.assertFalse(r['clean_terminal'])
 def test_extra_after_end(self):
  with self.assertRaises(InvalidStream):parse(self.data+encode_for_test(self.records[3]))
 def test_boot_noise_rejected(self):
  with self.assertRaises(InvalidStream):parse(b'Hello AD5940\n'+self.data)
 def test_nonfinite_json(self):
  p=b'{"type":"session","schema":1,"bad":NaN}'
  d=b'BIA1 '+str(len(p)).encode()+b' '+f'{zlib.crc32(p):08x}'.encode()+b' '+p+b'\n'
  with self.assertRaises(InvalidStream):parse(d)
 def test_duplicate_json_keys(self):
  p=b'{"type":"session","type":"session"}'
  d=b'BIA1 '+str(len(p)).encode()+b' '+f'{zlib.crc32(p):08x}'.encode()+b' '+p+b'\n'
  with self.assertRaises(InvalidStream):parse(d)

if __name__=='__main__':unittest.main(verbosity=2)
