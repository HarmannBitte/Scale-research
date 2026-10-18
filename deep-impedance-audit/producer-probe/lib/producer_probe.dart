// Frames built exactly as Example01_BasicECGBioZ.ino sendDataPacket() builds them:
// header 0x0A 0xFA LEN(0x0C,0x00) TYPE 0x02, 12-byte payload, footer 0x00 0x0B.
import 'dart:typed_data';
import 'protocol/packet_framer_v3.dart';
import 'boards/decoders/max30001_decoders.dart';

List<int> le32(int v) => [v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF, (v >> 24) & 0xFF];
List<int> producerFrame(int ecg, int bioz, bool skip) => [
  0x0A, 0xFA, 0x0C, 0x00, 0x02,
  ...le32(ecg), ...le32(bioz), skip ? 0xFF : 0x00, 0x00, 0x00, 0x00,
  0x00, 0x0B,
];

void main() {
  final decoded = <String>[];
  final framer = PacketFramer(
    knownTypes: {2},
    onPacket: (p) {
      final d = decodeMax30001Pkt2(p.payload);
      decoded.add('ecg=${d.channelSamples['ecg']} bioz=${d.channelSamples['bioz']} '
          'heartRate=${d.events['heartRate']} rr=${d.events['rr']}');
    },
    onError: (m) => decoded.add('framer error: $m'),
  );
  // 6 consecutive producer frames, alternating BioZ skip flag as the .ino does.
  for (var i = 0; i < 6; i++) {
    framer.processChunk(Uint8List.fromList(producerFrame(1000 + i, 5000 + i, i.isOdd)));
  }
  for (final line in decoded) print(line);
  print('framer stats: ${framer.stats}');
}
