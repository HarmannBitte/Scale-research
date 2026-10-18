"""Read-only public upstream collection. Downloads stay in excluded cache; compact source archives persist."""
import concurrent.futures,hashlib,io,json,pathlib,subprocess,tarfile,time,requests,zipfile
ROOT=pathlib.Path('/home/user/open-projects-collection');ROOT.mkdir(exist_ok=True)
CACHE=pathlib.Path('/home/user/.cache/open-projects');CACHE.mkdir(parents=True,exist_ok=True)
REPOS=['openebi/hardware','openebi/software','melazab/AD5940-BIOZ','oscaroflores/UPRM-Multi_Frq-BioZ-Research','analogdevicesinc/MAX32655_MAX30009','OpenEIT/EIT_Firmware','OpenEIT/EIT_EE','OpenEIT/OpenEIT','eitcom/pyEIT','ECSHackWeek/impedance.py','vyrjana/DearEIS','oliexdev/openScale','dyarleniber/AD5933-arduino-bioimpedance','TAMU-ESP/BioZPulse-Sim-Platform','Protocentral/protocentral_max30001','eayrenk/bioscale-okok-alternative','analogdevicesinc/ad5940-examples','analogdevicesinc/no-OS','vyrjana/pyimpspec','oliexdev/openScale-sync','Protocentral/protocentral_openview','dioptre/EIT_Firmware']
SOURCE_EXT={'.c','.h','.cpp','.hpp','.cc','.cxx','.s','.S','.asm','.ld','.lds','.icf','.sct','.map','.py','.pyi','.m','.ino','.java','.kt','.kts','.dart','.js','.jsx','.ts','.tsx','.html','.css','.scss','.json','.yaml','.yml','.toml','.ini','.cfg','.conf','.txt','.md','.rst','.sh','.bash','.bat','.ps1','.mk','.cmake','.pro','.pri','.qrc','.ui','.xml','.sch','.brd','.lbr','.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_mod','.lib','.dcm','.cam','.gbr','.ger','.drl','.net','.cir','.asc','.mod','.sp','.spice','.csv','.tsv','.sv','.v','.vhd','.vhdl','.ucf','.xdc','.ioc','.uvprojx','.uvoptx','.ewp','.eww','.ewd','.cproject','.project','.launch','.properties','.gradle','.gitmodules','.gitignore'}
GENERATED_DIRS={'node_modules','.git','.venv','venv','__pycache__','.gradle','.idea','build','dist','out','target','obj','objects','listings','bin','.dart_tool','.next','debug','release','__macosx'}
def select(path,size,repo):
 parts=path.lower().split('/');base=parts[-1];ext=pathlib.PurePosixPath(path).suffix
 if repo=='analogdevicesinc/no-OS':
  allowed=(path.startswith(('drivers/afe/max30009/','projects/max30009/','doc/sphinx/source/projects/afe/max30009','include/','util/','tools/scripts/','drivers/platform/maxim/')) or '/' not in path)
  if not allowed:return False,'outside scoped MAX30009 snapshot'
 if any(p in GENERATED_DIRS for p in parts[:-1]):return False,'generated/environment directory'
 if any(p in {'data','datasets','logs','images','screenshots','assets','fastlane','matlab'} for p in parts[:-1]) and size>180000 and ext not in {'.sch','.brd','.lbr','.asc','.cir','.m'}:return False,'large data/media asset'
 if ext.lower()=='.pdf':
  if any(w in base for w in ['schem','spectra','bom','circuit','design','openebi']) and size<5000000:return True,'hardware PDF'
  return False,'paper/manual PDF; upstream path retained'
 if size>2200000:return False,'large file; upstream path retained'
 if ext in SOURCE_EXT or base.lower().startswith(('license','licence','copying','readme','makefile','cmakelists','requirements','notice','authors','contributors','dockerfile','platformio','meson','procfile','gemfile','gradlew','package-lock','pubspec')):return True,'source/design/text'
 if size<100000 and any(w in base for w in ['bom','gerber','license','licence']):return True,'design/licence auxiliary'
 return False,'non-source/binary/media asset'
def work(repo):
 slug=repo.replace('/','__');rec={'repo':repo,'url':'https://github.com/'+repo,'checked_date':'2026-10-18'}
 try:
  q=subprocess.run(['git','ls-remote','--symref','https://github.com/'+repo+'.git','HEAD'],capture_output=True,text=True,timeout=45,check=True)
  ls=q.stdout.splitlines();rec['default_branch']=next((x.split('refs/heads/',1)[1].split()[0] for x in ls if x.startswith('ref:')),'unknown');rec['commit']=next(x.split()[0] for x in ls if not x.startswith('ref:') and x.endswith('\tHEAD'))
  sha=rec['commit'];url=f'https://codeload.github.com/{repo}/tar.gz/{sha}';rec['archive_url']=url;dest=CACHE/(slug+'-'+sha+'.tar.gz')
  # no-OS's entire repository is intentionally not downloaded; use a scoped source set via API tree + raw files.
  if repo=='analogdevicesinc/no-OS':
   tr=requests.get(f'https://api.github.com/repos/{repo}/git/trees/{sha}',params={'recursive':1},timeout=90);tr.raise_for_status();tree=tr.json();rec['tree_truncated']=tree.get('truncated');members=[];saved=[];omitted=[]
   for x in tree.get('tree',[]):
    if x['type']!='blob':continue
    ok,reason=select(x['path'],x.get('size',0),repo)
    if ok:members.append(x)
    else:omitted.append({'path':x['path'],'size':x.get('size'),'reason':reason})
   def raw(x):
    u=f'https://raw.githubusercontent.com/{repo}/{sha}/{x["path"]}';r=requests.get(u,timeout=45);r.raise_for_status();return x['path'],r.content
   out=ROOT/(slug+'.zip')
   with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
     for path,body in ex.map(raw,members):z.writestr(path,body);saved.append({'path':path,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
   rec.update({'scope':'MAX30009 driver/project plus core headers/utilities, Maxim platform and build scripts; not complete no-OS repository','upstream_full_archive_downloaded':False,'source_files':saved,'omitted_files':omitted})
  else:
   if not dest.exists():
    with requests.get(url,stream=True,timeout=(25,180)) as r:
     r.raise_for_status()
     with dest.open('wb') as f:
      for b in r.iter_content(1024*1024):f.write(b)
   rec['upstream_full_archive_downloaded']=True;rec['upstream_archive_bytes']=dest.stat().st_size;rec['upstream_archive_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();saved=[];omitted=[];submodules=[]
   out=ROOT/(slug+'.zip');extract=CACHE/slug;extract.mkdir(exist_ok=True)
   with tarfile.open(dest,'r:gz') as tar,zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for m in tar:
     if not m.isfile():continue
     path=m.name.split('/',1)[1] if '/' in m.name else m.name
     ok,reason=select(path,m.size,repo)
     if ok:
      body=tar.extractfile(m).read();z.writestr(path,body);saved.append({'path':path,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
      # safe cache extraction of selected files only
      pp=pathlib.PurePosixPath(path)
      if not pp.is_absolute() and '..' not in pp.parts:
       f=extract/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(body)
      if path=='.gitmodules':submodules.append(body.decode(errors='replace'))
     else:omitted.append({'path':path,'size':m.size,'reason':reason})
   rec.update({'scope':'compact source/design snapshot; binary/media/generated omissions enumerated','source_files':saved,'omitted_files':omitted,'submodule_definitions':submodules})
  rec['compact_archive']=out.name;rec['compact_archive_bytes']=out.stat().st_size;rec['compact_archive_sha256']=hashlib.sha256(out.read_bytes()).hexdigest();rec['status']='collected'
 except Exception as e:rec['status']='error';rec['error']=repr(e)
 (ROOT/(slug+'.json')).write_text(json.dumps(rec,indent=2));print(repo,rec['status'],rec.get('compact_archive_bytes'),len(rec.get('source_files',[])),rec.get('error',''),flush=True);return rec
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:records=list(ex.map(work,REPOS))
 (ROOT/'collection-index.json').write_text(json.dumps([{k:v for k,v in x.items() if k not in {'source_files','omitted_files'}} for x in records],indent=2))
 print('TOTAL compact bytes',sum(x.get('compact_archive_bytes',0) for x in records),flush=True)
