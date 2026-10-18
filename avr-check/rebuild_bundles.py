#!/usr/bin/env python3
"""Final pass-4 packaging: fix the F12 wording in DEEP-FINDINGS.md, regenerate the deep-audit manifest,
rebuild Deep-Impedance-Audit.tar.xz, and rebuild the collection archive with the current dossier and deep audit.
Work happens under ~/.cache (not the RAM-backed /tmp). Only the two archives and their .sha256 files are replaced."""
import hashlib, json, pathlib, re, shutil, subprocess, tarfile

H = pathlib.Path('/home/user')
DA = H / 'deep-impedance-audit'
DF = DA / 'DEEP-FINDINGS.md'

t = DF.read_text()
t = t.replace('Whether bits above bit 10 are ignored by the register write is also unverified. No hazard claim is made, and no electrode-level output was measured.',
              'The ADuCM350 manual lists bits above bit 10 of the amplitude register as read-only reserved (pass 4), so the value is most likely masked. Not measured on hardware. No hazard claim is made, and no electrode-level output was measured.')
t = t.replace('| F12 | Spectra | Bipolar amplitude wraps 61,323 → 1,931 codes | S, H | Confirmed in source and arithmetic; HIGH review |',
              '| F12 | Spectra | Bipolar amplitude wraps 61,323 → 1,931 codes | S, H, DS | Confirmed; ADuCM350 manual says upper bits are read-only reserved (pass 4); HIGH review |')
DF.write_text(t)

# 1) Deep-audit manifest (excluding itself and any build directories)
files = []
for p in sorted(DA.rglob('*')):
    if p.is_file() and p.name != 'MANIFEST.json':
        files.append({'path': str(p.relative_to(DA)), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
(DA / 'MANIFEST.json').write_text(json.dumps({'files': files}, indent=1))
print('deep manifest', len(files))

# 2) Deep-audit bundle
out = H / 'Deep-Impedance-Audit.tar.xz'
with tarfile.open(out, 'w:xz', preset=6) as tf:
    tf.add(DA, arcname='deep-impedance-audit', filter=lambda ti: None if '.dart_tool' in ti.name or '/build/' in ti.name else ti)
sha = hashlib.sha256(out.read_bytes()).hexdigest()
(H / 'Deep-Impedance-Audit.tar.xz.sha256').write_text(f'{sha}  Deep-Impedance-Audit.tar.xz\n')
print('deep bundle', out.stat().st_size, sha[:16])

# 3) Collection archive: extract to ~/.cache, swap in the current dossier and deep audit, rebuild the bundle hash list, repack.
W = H / '.cache' / 'open-projects' / 'repack'
shutil.rmtree(W, ignore_errors=True)
W.mkdir(parents=True)
with tarfile.open(H / 'Open-Source-Projects-Collection.tar.xz') as tf:
    tf.extractall(W, filter='data')
C = W / 'Open-Source-Projects-Collection'
shutil.copy2(H / 'Open-Source-Projects-Collected-and-Investigated.md', C / 'INVESTIGATION.md')
shutil.rmtree(C / 'deep-impedance-audit', ignore_errors=True)
shutil.copytree(DA, C / 'deep-impedance-audit', ignore=shutil.ignore_patterns('.dart_tool', 'build'))
# The collection-level bundle hash list, excluding itself.
bl = []
for p in sorted(C.rglob('*')):
    if p.is_file() and p.name != 'BUNDLE-FILE-HASHES.json':
        bl.append({'path': str(p.relative_to(C)), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
(C / 'BUNDLE-FILE-HASHES.json').write_text(json.dumps({'algorithm': 'SHA-256', 'excludes': ['BUNDLE-FILE-HASHES.json'], 'files': bl}, indent=2))
q = subprocess.run(['python3', str(C / 'tools' / 'verify_collection.py')], capture_output=True, text=True)
print('verify (prepared tree):', q.stdout.strip().splitlines()[-1] if q.stdout.strip() else q.stderr[-300:], 'rc', q.returncode)
assert q.returncode == 0
archive = H / 'Open-Source-Projects-Collection.tar.xz'
with tarfile.open(archive, 'w:xz', preset=6) as tf:
    tf.add(C, arcname=C.name)
csha = hashlib.sha256(archive.read_bytes()).hexdigest()
(H / 'Open-Source-Projects-Collection.tar.xz.sha256').write_text(f'{csha}  Open-Source-Projects-Collection.tar.xz\n')
print('collection archive', archive.stat().st_size, csha[:16])

# 4) Round-trip check: fresh extraction, verify, compare hashes
R = H / '.cache' / 'open-projects' / 'roundtrip'
shutil.rmtree(R, ignore_errors=True)
R.mkdir(parents=True)
with tarfile.open(archive) as tf:
    tf.extractall(R, filter='data')
q2 = subprocess.run(['python3', str(R / C.name / 'tools' / 'verify_collection.py')], capture_output=True, text=True)
print('verify (extracted archive):', q2.stdout.strip().splitlines()[0], 'rc', q2.returncode)
assert q2.returncode == 0
ok = all(hashlib.sha256((R / C.name / f['path']).read_bytes()).hexdigest() == f['sha256'] for f in bl)
print('bundle hash list matches extracted archive:', ok, 'entries', len(bl))
shutil.rmtree(W, ignore_errors=True)
shutil.rmtree(R, ignore_errors=True)
