import pathlib,json,zipfile,hashlib,shutil,tarfile,subprocess,sys,os
H=pathlib.Path('/home/user');R=H/'open-projects-collection';C=H/'.cache/open-projects';P=C/'release';D=P/'Open-Source-Projects-Collection';OUT=H/'Open-Source-Projects-Collection.tar.xz'
if D.exists():shutil.rmtree(D)
D.mkdir(parents=True);(D/'sources').mkdir();(D/'manifests').mkdir();(D/'tools/research-history').mkdir(parents=True)
idx=[];old=[]
for p in sorted(R.glob('*.json')):
 d=json.loads(p.read_text())
 if not isinstance(d,dict) or not d.get('compact_archive'):continue
 old.append((p,R/d['compact_archive']));slug=d['compact_archive'][:-4];sd=D/'sources'/slug;sd.mkdir()
 zf=R/d['compact_archive'];assert hashlib.sha256(zf.read_bytes()).hexdigest()==d['compact_archive_sha256']
 with zipfile.ZipFile(zf) as z:
  assert set(z.namelist())=={x['path'] for x in d['source_files']}
  assert len(z.namelist())==len(set(z.namelist()))
  for item in d['source_files']:
   q=(sd/item['path']).resolve();assert q.is_relative_to(sd.resolve());b=z.read(item['path']);assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 for key in ['compact_archive','compact_archive_bytes','compact_archive_sha256']:
  d[key.replace('compact_archive','staging_archive')]=d.pop(key)
 d['source_directory']='sources/'+slug;d['manifest']='manifests/'+p.name;d['distribution_note']='Files laid out directly under source_directory; staging ZIP recorded for provenance but not duplicated.';(D/'manifests'/p.name).write_text(json.dumps(d,indent=2));idx.append({k:v for k,v in d.items() if k not in {'source_files','omitted_files'}})
idx.sort(key=lambda d:(d['repo'],d['commit']));(D/'collection-index.json').write_text(json.dumps(idx,indent=2));assert len(idx)==26 and len({d['repo'] for d in idx})==25
shutil.copy2(H/'Open-Source-Projects-Collected-and-Investigated.md',D/'INVESTIGATION.md');shutil.copy2(H/'open-source-survey/COLLECTION-README.md',D/'README.md');shutil.copy2(H/'open-source-survey/REPRODUCING.md',D/'tools/REPRODUCING.md');shutil.copytree(R/'verification',D/'verification');shutil.copytree(R/'research',D/'research');shutil.copy2(R/'project-catalog.csv',D/'project-catalog.csv');shutil.copy2(R/'submodule-pins.json',D/'submodule-pins.json')
for name in ['verify_collection.py','fetch_upstream.py']:shutil.copy2(H/'open-source-survey'/name,D/'tools'/name)
for name in ['collect_full.py','run_investigation.py','run_followups.py','check_analysis_packages.py','make_research_catalog.py','pack_release.py']:shutil.copy2(H/'open-source-survey'/name,D/'tools/research-history'/name)
for name in ['augment_collection.py','hardware_inventory.py','fix_notices.py','packaging_check.py','add_required_snapshot.py']:
 p=C/name
 if p.exists():shutil.copy2(p,D/'tools/research-history'/name)
files=[]
for p in sorted(D.rglob('*')):
 if p.is_file():files.append({'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'BUNDLE-FILE-HASHES.json').write_text(json.dumps({'algorithm':'SHA-256','excludes':['BUNDLE-FILE-HASHES.json'],'files':files},indent=2))
q=subprocess.run([sys.executable,str(D/'tools/verify_collection.py')],text=True,capture_output=True);print(q.stdout);assert q.returncode==0,q.stderr
# Verify the negative path on the original prepared tree; restore before packaging.
target=next((D/'sources').rglob('README.md'));b=target.read_bytes();target.write_bytes(b+b'\nQA corruption probe\n');bad=subprocess.run([sys.executable,str(D/'tools/verify_collection.py')],capture_output=True,text=True);target.write_bytes(b);assert bad.returncode==1,'Verifier missed corruption'
# Produce one solid archive (better deduplication than nested compressed ZIPs).
with tarfile.open(OUT,'w:xz',preset=6) as t:t.add(D,arcname=D.name)
sha=hashlib.sha256(OUT.read_bytes()).hexdigest();(H/(OUT.name+'.sha256')).write_text(sha+'  '+OUT.name+'\n')
E=C/'release-extracted'
if E.exists():shutil.rmtree(E)
E.mkdir()
with tarfile.open(OUT) as t:t.extractall(E,filter='data')
q=subprocess.run([sys.executable,str(E/D.name/'tools/verify_collection.py')],text=True,capture_output=True);print(q.stdout);assert q.returncode==0,q.stderr
shutil.copy2(D/'project-catalog.csv',H/'Open-Source-Project-Catalog.csv')
qa={'date':'2026-10-18','distinct_repositories':25,'snapshots':26,'source_files':sum(len(json.loads(p.read_text())['source_files']) for p in (D/'manifests').glob('*.json')),'bundle_file_count_including_hash_inventory':len(files)+1,'archive':OUT.name,'archive_bytes':OUT.stat().st_size,'archive_sha256':sha,'prepared_tree_verification':True,'deliberate_corruption_detected':True,'extracted_archive_verification':True,'verification_output':q.stdout};(H/'Open-Source-Collection-Packaging-QA.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
# Avoid duplicating the compressed sources in the persisted workspace.
for meta,z in old:meta.unlink();z.unlink()
(R/'collection-index.json').write_text(json.dumps(idx,indent=2));shutil.copy2(D/'README.md',R/'README.md');(R/'WHERE-ARE-THE-SOURCES.txt').write_text('Sources and per-file manifests are in ../Open-Source-Projects-Collection.tar.xz. Extract it; run tools/verify_collection.py. The intermediate ZIPs were removed only after the extracted final archive passed verification, to avoid duplicate storage.\n')
print('Intermediate ZIPs removed only after archive round-trip and negative-control verification.')
