import json,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def probe(name):return json.loads(subprocess.check_output([str(ROOT/'build/host/target_io_probe'),name],text=True))
class TargetIO(unittest.TestCase):
 def test_resource_init_keeps_afe_reset_asserted(self):self.assertEqual(probe('reset'),dict(status=0,output=64,clear=64,set=0))
 def test_newlib_write_reaches_uart(self):self.assertEqual(probe('write'),dict(n=3,tx=99,fault=0))
 def test_stalled_uart_reports_error_and_stops(self):
  r=probe('stalled');self.assertEqual(r['n'],-1);self.assertEqual(r['tx'],97);self.assertEqual(r['fault'],-10);self.assertNotEqual(r['errno'],0)
 def test_reserved_heap_boundaries(self):self.assertEqual(probe('heap')['checks'],7)
 def test_invalid_writes_do_not_touch_uart(self):self.assertEqual(probe('invalid_write'),dict(checks=4,tx=0))
 def test_fstat_does_not_return_uninitialized_fields(self):self.assertEqual(probe('stat'),dict(n=0,char=True,size=0,blocksize=0,invalid=-1))
 def test_tx_only_uart_has_no_unhandled_receive_interrupt(self):self.assertEqual(probe('irq'),dict(status=0,ien=0,enabled=0,enable_calls=0))
 def test_mcu_crystal_wait_is_bounded(self):self.assertEqual(probe('clock'),dict(status=0,fault=-10))
 def test_unsupported_baud_rejected(self):self.assertEqual(probe('badbaud'),dict(first=-1,second=-1,fault=-2))
 def test_invalid_divider_rejected_before_divide(self):self.assertEqual(probe('baddivider'),dict(status=-1,fault=-2))
if __name__=='__main__':unittest.main(verbosity=2)
