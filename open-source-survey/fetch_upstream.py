#!/usr/bin/env python3
"""Retrieve original pinned upstream archives. Never executes their contents."""
import argparse,hashlib,json,pathlib,sys,urllib.request
ROOT=pathlib.Path(__file__).resolve().parent.parent

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--list',action='store_true');p.add_argument('--repo');p.add_argument('--commit',help='Full commit or unambiguous prefix');p.add_argument('--destination',type=pathlib.Path,default=ROOT/'downloads');p.add_argument('--allow-unhashed',action='store_true',help='Allow no-OS full download: original full archive was not downloaded/hashed in this survey');a=p.parse_args();rows=json.loads((ROOT/'collection-index.json').read_text())
 if a.list:
  for r in rows:print(r['repo'],r['commit'],'archive-hash-recorded' if r.get('upstream_archive_sha256') else 'NO original full-archive hash')
  return 0
 if not a.repo:p.error('Use --list or --repo owner/name [--commit prefix]')
 rows=[r for r in rows if r['repo']==a.repo and (not a.commit or r['commit'].startswith(a.commit))]
 if len(rows)!=1:p.error('Select exactly one listed snapshot; AD5940 library has two revisions.')
 r=rows[0];want=r.get('upstream_archive_sha256')
 if not want and not a.allow_unhashed:p.error('No original full-archive hash recorded. Inspect manifest; explicitly use --allow-unhashed if desired.')
 a.destination.mkdir(parents=True,exist_ok=True);dst=a.destination/(r['repo'].replace('/','__')+'-'+r['commit']+'.tar.gz');part=dst.with_suffix(dst.suffix+'.partial')
 if dst.exists():p.error('Destination already exists; not overwriting '+str(dst))
 h=hashlib.sha256();count=0;url=r['archive_url'];print('Downloading',url)
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Pinned-research-collection/1.0'})
  with urllib.request.urlopen(req,timeout=180) as resp,part.open('wb') as f:
   for b in iter(lambda:resp.read(1024*1024),b''):h.update(b);f.write(b);count+=len(b)
  got=h.hexdigest()
  if want and got!=want:part.unlink(missing_ok=True);raise RuntimeError('Archive hash differs from recorded upstream archive. It may have been regenerated. No verified output retained.')
  part.rename(dst);print('Saved',dst,'bytes',count,'sha256',got);print('Archive matches recorded hash.' if want else 'WARNING: no original full-archive hash existed; hash is newly computed only.');return 0
 except Exception as e:part.unlink(missing_ok=True);print('ERROR:',e,file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
