# F20 maintainer message (draft, not sent)

Target: Protocentral/protocentral_openview, issue tracker (public). Confirm the right repo before sending: the finding names protocentral/max30001_openview, but that name returned Not Found earlier; the collected repo is Protocentral/protocentral_openview.

Title: Packet type 2 decoder reports heart rate 0/255 and RR 0 for frames with no HR/RR data

Body:

Hi,

I found a mismatch between the MAX30001 Arduino example producer and the packet type 2 decoder in the OpenView app. I reproduced it without hardware, using the decoder and framer as they are in the repository.

What I did:
- Built six frames in the format the Arduino library's Example01 sends (ECG and BioZ samples, no heart rate or RR fields).
- Passed them through the framer and the packet type 2 decoder (lib/boards/decoders/max30001_decoders.dart).

Result for all six frames:
- heartRate = 0, 255, 0, 255, 0, 255
- rr = 0
- framer stats: ok=6, unknown=0, noEof=0, oversize=0, timeout=0

It looks like the decoder reads the skip flag (0x00 / 0xFF) as heart rate, because the producer sends no HR or RR.

Question: is the intended behaviour that frames without HR/RR carry the skip flag and should be treated as "no value", or should the producer send HR/RR? I can share the probe script and the log.

Test details: no hardware used. Decoder source as collected from the repository on 2026-10-18 (exact commit to be added).

Thanks.
