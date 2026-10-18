"""Generate nominal planning ceilings, not physical reference measurements."""
import cmath,csv,math
from pathlib import Path
FIXTURES={'R100':(100,0,0),'R220':(220,0,0),'R470':(470,0,0),'R1000':(1000,0,0),'RC_A':(470,210,15e-9),'RC_B':(500,500,6.8e-9)}
rows=[]
for name,(rs,rp,c) in FIXTURES.items():
    for f in (5000,10000,20000,50000,100000,200000):
        z=rs+rp/(1+2j*math.pi*f*rp*c)
        rows.append(dict(fixture_id=name,requested_nominal_hz=f,values_kind='ANALYTICAL_PLANNING_ONLY',
            nominal_r_ohm=z.real,nominal_x_ohm=z.imag,nominal_mag_ohm=abs(z),nominal_phase_deg=math.degrees(cmath.phase(z)),
            max_reference_expanded_u_r_ohm=max(.5,.005*abs(z.real))/4,
            max_reference_expanded_u_x_ohm=max(1,.02*abs(z.imag))/4,
            max_reference_expanded_u_mag_ohm=max(.5,.005*abs(z))/4,
            max_reference_expanded_u_phase_deg=.05))
path=Path(__file__).with_name('reference-request-grid.csv')
with path.open('w',newline='') as out:
    w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
assert len(rows)==36
r=next(x for x in rows if x['fixture_id']=='R1000' and x['requested_nominal_hz']==50000)
assert r['max_reference_expanded_u_x_ohm']==.25
print('36 nominal planning cells generated. No physical measurements.')
print('R1000 phase-dominated U(X)=0.25 ohm equivalent:',math.degrees(.25/1000),'degrees')
print('Mouser hypothetical 8% tariff subtotal:',round(497.15*1.08,2))
print('Illustrative reserve subtotal:',487.21+200+1000)
