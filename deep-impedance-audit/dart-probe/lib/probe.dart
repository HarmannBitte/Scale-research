import 'dart:typed_data';
import 'protocol/packet_framer_v3.dart';
void run(String label, List<int> bytes){
  final out=<String>[];
  final f=PacketFramer(knownTypes:{2},onPacket:(p)=>out.add('packet type=${p.pktType} len=${p.payload.length} known=${p.known}'),onError:(m)=>out.add('error: $m'));
  f.processChunk(Uint8List.fromList(bytes));
  print('$label -> ${out.isEmpty?"no output":out.join(" | ")} ${f.stats}');
}
void main(){
  final payload=List<int>.filled(12,0x11);
  // Frame as the header describes: SOF, LEN(LE), TYPE, PAYLOAD, EOF (no pad byte)
  run('no-pad frame (12B payload)',[0x0A,0xFA,12,0,2,...payload,0x0B]);
  // Frame with the 0x00 pad the framer comments expect
  run('0x00-pad frame (12B payload)',[0x0A,0xFA,12,0,2,...payload,0x00,0x0B]);
}
