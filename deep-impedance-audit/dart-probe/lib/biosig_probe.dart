import 'dart:io';
import 'biosignal_file_writer.dart';
import 'biosignal_file_reader.dart';
import 'recording_models.dart';

Future<void> main() async {
  final f = File('/tmp/probe_rec.hpd');
  if (f.existsSync()) f.deleteSync();
  final meta = RecordingMetadata(
    deviceId: 'probe', channels: [
      ChannelInfo(id: 'ecg', name: 'ECG', unit: 'adc', samplingRate: 128),
      ChannelInfo(id: 'bioz', name: 'BioZ', unit: 'adc', samplingRate: 128),
    ], totalSamples: 30);
  final w = BiosignalFileWriter(f);
  await w.writeHeader(meta);
  for (var b = 0; b < 3; b++) {
    await w.writeSamples(List.generate(10, (i) => MultiChannelSample(
        sequenceNumber: b * 10 + i, timestampMicros: (b * 10 + i) * 7812,
        values: {'ecg': 100.0 + i, 'bioz': 1000.0 + b * 10 + i})));
  }
  await w.finalize();

  Future<int> count(String label) async {
    final r = BiosignalFileReader(f);
    await r.open();
    var n = 0;
    try { await for (final x in r.readSamples()) { n++; if (x.sequenceNumber == 10) print('  seq10 bioz=${x.values['bioz']}'); } }
    catch (e) { print('$label exception: $e'); }
    await r.close();
    print('$label -> samples read: $n');
    return n;
  }

  await count('intact file');
  // Corrupt one BioZ float byte inside block 2 (keeps the file length, changes content).
  final bytes = f.readAsBytesSync();
  final marker = [0x41, 0x54, 0x41, 0x44]; // 'DATA' little-endian bytes of 0x44415441
  var found = 0; var pos = -1;
  for (var i = 0; i < bytes.length - 4; i++) {
    if (bytes[i] == marker[0] && bytes[i+1] == marker[1] && bytes[i+2] == marker[2] && bytes[i+3] == marker[3]) {
      found++; if (found == 2) { pos = i; break; }
    }
  }
  // skip marker(4)+seq(4)+count(4)+ts(8) = 20 bytes, then first sample: seq4 ts8 ecg8 bioz8 -> flip a byte in sample 0 bioz
  bytes[pos + 20 + 22] ^= 0xFF; // sample 0 of block 2 (seq 10): block hdr 20, seq4+ts8+ecg8 = 20, bioz byte 2
  f.writeAsBytesSync(bytes);
  await count('one corrupted byte in block 2 (CRC not checked)');

  // Truncate the file in the middle of block 3.
  final cut = f.readAsBytesSync();
  f.writeAsBytesSync(cut.sublist(0, cut.length - 200));
  await count('truncated by 200 bytes');
}
