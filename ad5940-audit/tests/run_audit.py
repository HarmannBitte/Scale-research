"""Host-only source audit for development targeting ADI hardware. No acquisition."""
import cmath,hashlib,json,math,random,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def probe(*args):
 return subprocess.check_output([str(ROOT/'tests/host_probe'),*map(str,args)],text=True).strip().split()
def process(cr,ci,vr,vi,mag=1000,ph=0):
 out=probe('process',cr,ci,vr,vi,mag,ph)
 return dict(status=int(out[0]),count=int(out[1]),mag=float(out[2]),phase=float(out[3]),finite=bool(int(out[4])))
class Audit(unittest.TestCase):
 def test_nominal_resistor(self):
  r=process(10000,0,5000,0);self.assertEqual(r['status'],0);self.assertAlmostEqual(r['mag'],500);self.assertEqual(r['phase'],0)
 def test_capacitive_sign(self):
  r=process(10000,0,5000,1000);z=cmath.rect(r['mag'],r['phase']);self.assertAlmostEqual(z.real,500,places=4);self.assertAlmostEqual(z.imag,-100,places=4)
 def test_18bit_negative_boundary(self):
  r=process(-131072,0,-65536,0);self.assertAlmostEqual(r['mag'],500);self.assertAlmostEqual(r['phase'],0)
 def test_18bit_positive_boundary(self):self.assertAlmostEqual(process(131071,0,131071,0)['mag'],1000)
 def test_random_complex_agreement(self):
  rng=random.Random(20261017)
  for i in range(40):
   cr,ci,vr,vi=[rng.randint(-120000,120000) for _ in range(4)];mag=rng.uniform(200,10000);ph=rng.uniform(-.3,.3)
   with self.subTest(case=i):
    r=process(cr,ci,vr,vi,mag,ph);ref=complex(vr,-vi)/complex(cr,-ci)*cmath.rect(mag,ph);z=cmath.rect(r['mag'],r['phase'])
    self.assertLess(abs(z-ref),max(.002,abs(ref)*1e-6))
 def test_zero_current_nonfinite_success(self):
  r=process(0,0,5000,0);self.assertEqual(r['status'],0);self.assertFalse(r['finite']);self.assertTrue(math.isinf(r['mag']))
 def test_zero_both_nonfinite_success(self):
  r=process(0,0,0,0);self.assertEqual(r['status'],0);self.assertTrue(math.isnan(r['mag']))
 def test_invalid_zero_calibration_accepted(self):
  r=process(10000,0,5000,0,0,0);self.assertEqual(r['status'],0);self.assertEqual(r['mag'],0)
 def test_phase_not_wrapped(self):self.assertGreater(process(10000,0,5000,0,1000,4)['phase'],math.pi)
 def test_normal_fifo(self):self.assertEqual(list(map(int,probe('isr',4,512,0,1))),[0,1,4])
 def test_declared_capacity_exceeded(self):self.assertEqual(list(map(int,probe('isr',516,512,0,1))),[0,129,516])
 def test_zero_capacity_not_enforced(self):self.assertEqual(list(map(int,probe('isr',4,0,0,1))),[0,1,4])
 def test_fifo_full_1024_vs_buffer512(self):self.assertEqual(list(map(int,probe('isr',1024,512,0,1))),[0,256,1024])
 def test_wakeup_error_leaves_capacity_as_count(self):
  r=list(map(int,probe('isr',4,512,11,1)));self.assertLess(r[0],0);self.assertEqual(r[1:], [512,0])
 def test_uninitialized_error_leaves_capacity_as_count(self):
  r=list(map(int,probe('isr',4,512,0,0)));self.assertLess(r[0],0);self.assertEqual(r[1:], [512,0])
 def test_calibration_failure_swallowed(self):self.assertEqual(probe('calfail'),['0','1','1000'])
 def test_invalid_single_point_sweep_nonfinite(self):self.assertEqual(probe('sweep',1)[2],'0')
 def test_valid_log_sweep(self):
  r=probe('sweep',100);self.assertEqual(r[2],'1');self.assertAlmostEqual(float(r[0]),10000*(15**(1/99)),places=2)
 def test_frequency_word_both_silicon_modes(self):
  for silicon in [0,1]:
   for f in [5000,10000,20000,50000,100000,200000]:
    with self.subTest(silicon=silicon,f=f):self.assertLess(abs(float(probe('wg',f,silicon)[1])-f),.13)
 def test_formatter_omits_per_record_metadata(self):
  out=subprocess.check_output([str(ROOT/'tests/formatter_probe')],text=True)
  self.assertEqual(out.count('Freq:'),1);self.assertEqual(out.count('RzMag:'),2)
  for absent in ['timestamp','raw','status','calibration_id','sample_id']:self.assertNotIn(absent,out)
 def test_retained_source_hashes_unchanged(self):
  m=json.loads((ROOT/'source-manifest.json').read_text())
  for f in (ROOT/'source').rglob('*'):
   if f.is_file():self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),m['original_worktree_sha256'][str(f.relative_to(ROOT/'source'))])

if __name__=='__main__':unittest.main(verbosity=2)
