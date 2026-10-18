# Emulates the Arduino IDE: copy the .ino to .cpp and add prototypes for top-level functions defined in the sketch.
import re,sys,pathlib
src=pathlib.Path(sys.argv[1]).read_text(errors='replace').splitlines()
protos=[]
for line in src:
    m=re.match(r'^([A-Za-z_][\w \*]*?)\s+(\w+)\s*\(([^)]*)\)\s*\{?\s*$',line)
    if m and m.group(2) not in ('if','for','while','switch','return') and not line.startswith(' '):
        protos.append(line.rstrip().rstrip('{').rstrip()+';')
out=['#include "Arduino.h"','#include "Wire.h"','#include <SoftwareSerial.h>','#include <stdint.h>']
# The IDE puts prototypes after the includes and before the body.
body=[l for l in src if not l.strip().startswith('#include')]
pathlib.Path(sys.argv[2]).write_text('\n'.join(out+protos+body)+'\n')
print('prototypes',len(protos))
