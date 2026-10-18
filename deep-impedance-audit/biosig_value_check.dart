import 'dart:io';
import 'biosignal_file_reader.dart';
Future<void> main() async {
  final r = BiosignalFileReader(File('/tmp/probe_rec.hpd'));
  await r.open();
  final s = await r.readSamples().toList();
  await r.close();
  for (final x in s) {
    if (x.sequenceNumber >= 19 && x.sequenceNumber <= 21) print('seq ${x.sequenceNumber} values ${x.values}');
  }
  print('total ${s.length}');
}
