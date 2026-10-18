"""Extract exact upstream function bodies for host-only development tests."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
def extract(path,signature):
    text=path.read_text();start=text.index('\n'+signature)+1;brace=text.index('{',start);depth=0
    # Selected functions contain no brace characters in strings/comments that affect balance.
    for pos in range(brace,len(text)):
        depth += (text[pos]=='{')-(text[pos]=='}')
        if depth==0:return text[start:pos+1]+'\n'
    raise ValueError(signature)
lib=root/'source/examples/ad5940lib/ad5940.c';main=root/'source/examples/AD5940_BIA/AD5940Main.c'
items={name:extract(path,signature) for name,path,signature in [
 ('sweep',lib,'void AD5940_SweepNext('),('wg',lib,'uint32_t AD5940_WGFreqWordCal('),
 ('formatter',main,'int32_t BIAShowResult(')]}
for name,text in items.items():
 (root/'tests'/f'upstream_{name}.inc').write_text('/* VERBATIM EXTRACT: ADI copyright/license apply. See source/LICENSE and source/examples/ad5940lib/LICENSE. */\n'+text)
(root/'tests/extraction-manifest.json').write_text(json.dumps({n:hashlib.sha256(v.encode()).hexdigest() for n,v in items.items()},indent=2)+'\n')
