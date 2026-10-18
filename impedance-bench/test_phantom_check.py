import csv
import math
import tempfile
import unittest
from pathlib import Path
import phantom_check as p

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name);p.demo(self.path)
    def tearDown(self):self.tmp.cleanup()
    def rows(self,name='samples.csv'):
        with (self.path/name).open(newline='') as f:return list(csv.DictReader(f))
    def test_dc_limit_and_high_frequency(self):
        self.assertAlmostEqual(p.impedance(1e-9,470,210,15e-9).real,680)
        self.assertAlmostEqual(p.impedance(1e15,470,210,15e-9).real,470)
    def test_rc_sign_and_corner(self):
        z=p.impedance(1/(2*math.pi*210*15e-9),470,210,15e-9)
        self.assertAlmostEqual(z.real,575);self.assertAlmostEqual(z.imag,-105)
    def test_phase_wrap(self):self.assertAlmostEqual(p.phase_delta(-179,179),2)
    def test_demo_not_hardware(self):
        a=p.analyze(self.path,'spectral');self.assertTrue(a['numerical_acceptance'])
        self.assertEqual(len(a['cells']),36);self.assertFalse(a['device_qualified'])
        self.assertFalse(a['reference_eligibility_for_hardware_review'])
        self.assertFalse(a['human_connection_authorized'])
    def test_primary_only(self):self.assertEqual(len(p.analyze(self.path)['cells']),6)
    def test_sign_inversion_fails(self):
        rows=self.rows()
        for r in rows:r['x_ohm']=-float(r['x_ohm'])
        p.save_csv(self.path/'samples.csv',rows)
        self.assertFalse(p.analyze(self.path)['numerical_acceptance'])
    def test_flag_fails(self):
        rows=self.rows();next(r for r in rows if int(r['frequency_hz'])==50000)['clipping']=1
        p.save_csv(self.path/'samples.csv',rows);self.assertFalse(p.analyze(self.path)['numerical_acceptance'])
    def test_missing_cell_rejected(self):
        rows=[r for r in self.rows() if r['fixture_id']!='RC_A']
        p.save_csv(self.path/'samples.csv',rows)
        with self.assertRaises(ValueError):p.analyze(self.path)
    def test_duplicate_rejected(self):
        rows=self.rows();rows.append(rows[0]);p.save_csv(self.path/'samples.csv',rows)
        with self.assertRaises(ValueError):p.analyze(self.path)
    def test_nonfinite_rejected(self):
        rows=self.rows();rows[0]['r_ohm']='NaN';p.save_csv(self.path/'samples.csv',rows)
        with self.assertRaises(ValueError):p.analyze(self.path)
    def test_reference_uncertainty_fails(self):
        rows=self.rows('references.csv')
        for r in rows:r['u_phase']=.3
        p.save_csv(self.path/'references.csv',rows);self.assertFalse(p.analyze(self.path)['numerical_acceptance'])
    def test_actual_frequency_mismatch_rejected(self):
        rows=self.rows();rows[0]['frequency_hz']=49999;p.save_csv(self.path/'samples.csv',rows)
        with self.assertRaises(ValueError):p.analyze(self.path)
    def test_large_gain_bias_fails(self):
        rows=self.rows()
        for r in rows:r['r_ohm']=float(r['r_ohm'])*1.02
        p.save_csv(self.path/'samples.csv',rows);self.assertFalse(p.analyze(self.path)['numerical_acceptance'])
    def test_negative_uncertainty_rejected(self):
        rows=self.rows('references.csv');rows[0]['u_x']=-1;p.save_csv(self.path/'references.csv',rows)
        with self.assertRaises(ValueError):p.analyze(self.path)

if __name__=='__main__':unittest.main(verbosity=2)
