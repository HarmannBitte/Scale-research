#!/usr/bin/env python3
"""Offline integrity check. Does not build, flash, connect, or validate safety."""
import argparse, hashlib, json, pathlib, sys

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('root',nargs='?',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent);a=ap.parse_args();root=a.root.resolve();errors=[]
 def safe(p):
  q=(root/p).resolve()
  if not q.is_relative_to(root):raise ValueError('Unsafe path: '+p)
  return q
 try:
  inventory=json.loads((root/'BUNDLE-FILE-HASHES.json').read_text());idx=json.loads((root/'collection-index.json').read_text())
  for item in inventory['files']:
   p=safe(item['path'])
   if not p.is_file():errors.append('Missing '+item['path'])
   elif p.stat().st_size!=item['bytes'] or digest(p)!=item['sha256']:errors.append('Changed '+item['path'])
  n=0
  for rec in idx:
   m=json.loads(safe(rec['manifest']).read_text());base=safe(rec['source_directory']);expected=set()
   for item in m['source_files']:
    p=(base/item['path']).resolve()
    if not p.is_relative_to(base):raise ValueError('Unsafe source path')
    expected.add(p);n+=1
    if not p.is_file():errors.append('Missing source '+str(p.relative_to(root)))
    elif p.stat().st_size!=item['bytes'] or digest(p)!=item['sha256']:errors.append('Source changed '+str(p.relative_to(root)))
   actual={p.resolve() for p in base.rglob('*') if p.is_file()}
   for p in actual-expected:errors.append('Unmanifested source '+str(p.relative_to(root)))
  print(f"{len(set(d['repo'] for d in idx))} repositories; {len(idx)} snapshots; {n} source/design/notice files checked.")
  if errors:
   print('\n'.join(errors));return 1
  print(f"PASS: source manifests and {len(inventory['files'])} bundled file hashes match.")
  print('Integrity only: not a signature, safety certification or measurement validation.');return 0
 except Exception as e:print('ERROR:',str(e),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
