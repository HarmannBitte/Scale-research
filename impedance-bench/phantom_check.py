"""Offline passive-phantom numerical check; no hardware driver or human-use release."""
import argparse
import cmath
import csv
import hashlib
import json
import math
from pathlib import Path
import random
import statistics

FIXTURES = {'R100': (100., 0., 0.), 'R220': (220., 0., 0.),
            'R470': (470., 0., 0.), 'R1000': (1000., 0., 0.),
            'RC_A': (470., 210., 15e-9), 'RC_B': (500., 500., 6.8e-9)}
FREQUENCIES = (5000, 10000, 20000, 50000, 100000, 200000)
FLAGS = ('clipping', 'compliance_fault', 'lead_off', 'transport_loss')
LIMITS = {'mag': (.5, .005), 'r': (.5, .005), 'x': (1., .02), 'phase': (.2, 0.)}

def impedance(f, rs, rp=0., c=0.):
    if not all(math.isfinite(v) for v in (f, rs, rp, c)) or f <= 0 or min(rs, rp, c) < 0:
        raise ValueError('Invalid passive-model parameters')
    return complex(rs) + rp / (1 + 2j * math.pi * f * rp * c)

def phase(z):
    return math.degrees(cmath.phase(z))

def phase_delta(a, b):
    return (a - b + 180) % 360 - 180

def finite(value):
    v = float(value)
    if not math.isfinite(v):
        raise ValueError('Nonfinite number')
    return v

def save_csv(path, rows):
    with Path(path).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def demo(folder):
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261017)
    refs, samples = [], []
    for name, parts in FIXTURES.items():
        for f in FREQUENCIES:
            z = impedance(f, *parts)
            refs.append(dict(fixture_id=name, nominal_frequency_hz=f, frequency_hz=f,
                             r_ohm=z.real, x_ohm=z.imag, reference_kind='analytical_synthetic',
                             u_mag=0., u_r=0., u_x=0., u_phase=0.))
            for i in range(30):
                # Noise added to calibrated ohms, NOT a simulation of AFE I/Q counts.
                samples.append(dict(fixture_id=name, frequency_hz=f, repeat_index=i,
                                    r_ohm=z.real+rng.gauss(0,.03), x_ohm=z.imag+rng.gauss(0,.03),
                                    **{flag:0 for flag in FLAGS}))
    save_csv(folder/'references.csv', refs); save_csv(folder/'samples.csv', samples)
    (folder/'run.json').write_text(json.dumps(dict(source_kind='synthetic',
        scope='Numerical demonstration only. No board, cables or components measured.',
        seed=20261017, repetitions=30, profiles=['primary','spectral']), indent=2)+'\n')

def analyze(folder, profile='primary'):
    folder = Path(folder)
    meta = json.loads((folder/'run.json').read_text())
    if meta.get('source_kind') not in ('synthetic', 'hardware'):
        raise ValueError('source_kind must be explicit')
    frequencies = (50000,) if profile == 'primary' else FREQUENCIES
    if profile not in ('primary','spectral'): raise ValueError('Unknown profile')
    with (folder/'references.csv').open(newline='') as f: refs = list(csv.DictReader(f))
    with (folder/'samples.csv').open(newline='') as f: samples = list(csv.DictReader(f))
    refmap = {}; grouped = {}; seen = set()
    # Parse the ENTIRE input, not just the chosen frequency, to reject NaN and duplicate IDs.
    for ref in refs:
        key = (ref['fixture_id'], finite(ref['frequency_hz']))
        if key in refmap: raise ValueError('Duplicate reference key')
        if key[0] not in FIXTURES or key[1] <= 0: raise ValueError('Unknown fixture/frequency')
        for field in ('r_ohm','x_ohm','nominal_frequency_hz','u_mag','u_r','u_x','u_phase'):
            ref[field] = finite(ref[field])
        if any(ref['u_'+q] < 0 for q in LIMITS): raise ValueError('Negative uncertainty')
        if ref['nominal_frequency_hz'] not in FREQUENCIES: raise ValueError('Unknown nominal frequency')
        if abs(key[1]/ref['nominal_frequency_hz'] - 1) > .01:
            raise ValueError('Actual frequency outside proposed 1% target window')
        refmap[key] = ref
    for sample in samples:
        key = (sample['fixture_id'], finite(sample['frequency_hz']))
        if key not in refmap: raise ValueError('Sample lacks same-frequency reference')
        idx = int(sample['repeat_index'])
        if idx < 0 or (key,idx) in seen: raise ValueError('Negative or duplicate repeat index')
        seen.add((key,idx))
        z = complex(finite(sample['r_ohm']), finite(sample['x_ohm']))
        flags = [int(sample[x]) for x in FLAGS]
        if any(v not in (0,1) for v in flags): raise ValueError('Flags must be 0 or 1')
        grouped.setdefault(key,[]).append((z, any(flags)))
    outputs = []; selection = set()
    for name in FIXTURES:
        for nominal in frequencies:
            keys = [k for k,r in refmap.items() if k[0] == name and r['nominal_frequency_hz'] == nominal]
            if len(keys) != 1: raise ValueError('Missing or ambiguous required reference cell')
            key = keys[0]; selection.add(key); ref = refmap[key]; rows = grouped.get(key,[])
            zs = [z for z,_ in rows]; n = len(zs)
            if n < 30: raise ValueError('At least 30 rows required per fixture/frequency')
            target = complex(ref['r_ohm'],ref['x_ohm']); mean = sum(zs)/n
            if abs(target) == 0: raise ValueError('Zero load is not an in-range verification load')
            expected = {'mag':abs(target),'r':target.real,'x':target.imag,'phase':phase(target)}
            observed = {'mag':abs(mean),'r':mean.real,'x':mean.imag,'phase':phase(mean)}
            errors = {q:abs(phase_delta(observed[q],expected[q])) if q == 'phase'
                      else abs(observed[q]-expected[q]) for q in LIMITS}
            limits = {q:max(floor,relative*abs(expected[q])) for q,(floor,relative) in LIMITS.items()}
            qualified_ref = ref['reference_kind'] == 'independently_measured'
            reference_uncertainty_ok = all(ref['u_'+q] <= limits[q]/4 for q in LIMITS)
            # Guard band for supplied reference expanded uncertainty only; not a full system budget.
            accuracy_ok = all(errors[q]+ref['u_'+q] <= limits[q] for q in LIMITS)
            sd_r = statistics.stdev(z.real for z in zs); sd_x = statistics.stdev(z.imag for z in zs)
            no_faults = not any(flag for _,flag in rows)
            outputs.append(dict(fixture_id=name, frequency_hz=key[1], n=n,
                expected_r_ohm=target.real, expected_x_ohm=target.imag,
                mean_r_ohm=mean.real,mean_x_ohm=mean.imag,absolute_errors=errors,limits=limits,
                sd_r_ohm=sd_r,sd_x_ohm=sd_x,accuracy_ok=accuracy_ok,
                reference_uncertainty_ok=reference_uncertainty_ok,independent_reference=qualified_ref,
                no_faults=no_faults,
                numeric_pass=accuracy_ok and reference_uncertainty_ok and sd_r<=.2 and sd_x<=.2 and no_faults))
    passed = all(x['numeric_pass'] for x in outputs)
    hardware_evidence_eligible = meta['source_kind']=='hardware' and all(x['independent_reference'] for x in outputs)
    return dict(profile=profile,source_kind=meta['source_kind'], numerical_acceptance=passed,
        reference_eligibility_for_hardware_review=hardware_evidence_eligible,
        status=('SIMULATED_NUMERIC_PASS' if passed else 'SIMULATED_NUMERIC_FAIL')
               if meta['source_kind']=='synthetic' else 'HARDWARE_DATA_REQUIRES_REVIEW',
        device_qualified=False,human_connection_authorized=False,
        limitations=['No metadata authentication or hardware driver','No drift/contact/fault-injection verification',
                     'No proof of calibration traceability or electrical safety'],
        input_sha256={n:hashlib.sha256((folder/n).read_bytes()).hexdigest()
                      for n in ('run.json','references.csv','samples.csv')},cells=outputs)

def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='command',required=True)
    d=sub.add_parser('demo');d.add_argument('folder')
    a=sub.add_parser('analyze');a.add_argument('folder');a.add_argument('--profile',choices=['primary','spectral'],default='primary')
    a.add_argument('--output',required=True)
    args=p.parse_args()
    if args.command=='demo': demo(args.folder)
    else:
        try: result=analyze(args.folder,args.profile)
        except (ValueError,KeyError,TypeError,ZeroDivisionError) as e:
            result={'status':'INVALID_INPUT','error':str(e),'device_qualified':False,'human_connection_authorized':False}
        Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        print(result.get('status'))
        if not result.get('numerical_acceptance',False):raise SystemExit(1)
if __name__=='__main__':main()
