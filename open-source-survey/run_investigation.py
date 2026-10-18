import os,sys,subprocess,time,json,pathlib,tarfile,hashlib,concurrent.futures
ROOT=pathlib.Path('/home/user/open-projects-collection');CACHE=pathlib.Path('/home/user/.cache/open-projects');PY=CACHE/'test-env/bin/python';LOG=ROOT/'verification';LOG.mkdir(exist_ok=True)
index=json.loads((ROOT/'collection-index.json').read_text());by={x['repo']:x for x in index}
def full(repo):
 rec=by[repo];slug=repo.replace('/','__');dest=CACHE/'full'/slug;dest.mkdir(parents=True,exist_ok=True)
 tarpath=CACHE/(slug+'-'+rec['commit']+'.tar.gz')
 with tarfile.open(tarpath) as t:t.extractall(dest,filter='data')
 return next(x for x in dest.iterdir() if x.is_dir())
# Preserve original files: all commands operate on temporary/excluded cache copies.
paths={r:full(r) for r in ['ECSHackWeek/impedance.py','eitcom/pyEIT','eayrenk/bioscale-okok-alternative','melazab/AD5940-BIOZ']}
(ROOT/'verification-source-paths.json').write_text(json.dumps({r:str(p) for r,p in paths.items()},indent=2))
tasks=[]
def task(name,repo,args,subdir='',extra=None,timeout=180):
 tasks.append((name,repo,args,subdir,extra or {},timeout))
task('impedance-py-upstream-tests','ECSHackWeek/impedance.py',[str(PY),'-m','pytest','-q','impedance/tests','--disable-warnings'],timeout=180)
task('pyeit-upstream-tests','eitcom/pyEIT',[str(PY),'-m','pytest','-q','tests','--disable-warnings'],timeout=180)
task('bioscale-upstream-tests','eayrenk/bioscale-okok-alternative',[str(PY),'-m','pytest','-q','tests','--disable-warnings'],timeout=90)
task('ad5940-gui-upstream-tests','melazab/AD5940-BIOZ',[str(PY),'-m','unittest','discover','-s','gui','-p','test_*.py'],timeout=60)
for name in ['blink-led','measure-2wire-bioz','measure-4wire-bioz','time-series-bioz','time-series-bioz-2wire']:
 task('ad5940-build-'+name,'melazab/AD5940-BIOZ',['make','-j2'],subdir=name,timeout=90)
def run(t):
 name,repo,args,subdir,extra,timeout=t;cwd=paths[repo]/subdir;env=os.environ.copy();env.update({'MPLBACKEND':'Agg','PYTHONPATH':str(paths[repo]),'PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1'});env.update(extra);start=time.monotonic();rec={'name':name,'repo':repo,'commit':by[repo]['commit'],'command':args,'cwd':str(cwd),'timeout_seconds':timeout,'environment_overrides':{k:env[k] for k in ['MPLBACKEND','PYTHONPATH','PYTEST_DISABLE_PLUGIN_AUTOLOAD']}}
 try:
  q=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout);text=q.stdout;rec['exit_code']=q.returncode;rec['status']='pass' if q.returncode==0 else 'failed'
 except subprocess.TimeoutExpired as e:text=(e.stdout or b'').decode(errors='replace') if isinstance(e.stdout,bytes) else (e.stdout or '');rec['status']='timeout';rec['exit_code']=None
 except Exception as e:text=repr(e);rec['status']='error';rec['exit_code']=None
 rec['duration_seconds']=round(time.monotonic()-start,3);(LOG/(name+'.log')).write_text(text);rec['log']=name+'.log';rec['log_sha256']=hashlib.sha256(text.encode()).hexdigest();(LOG/(name+'.json')).write_text(json.dumps(rec,indent=2));print(name,rec['status'],'\n',text[-1300:],flush=True);return rec
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(run,tasks))
 (LOG/'results.json').write_text(json.dumps(results,indent=2))
 q=subprocess.run([str(PY),'-m','pip','freeze'],capture_output=True,text=True);(LOG/'environment-freeze.txt').write_text(q.stdout)
 q=subprocess.run(['arm-none-eabi-gcc','--version'],capture_output=True,text=True);(LOG/'arm-gcc-version.txt').write_text(q.stdout)
 (LOG/'python-version.txt').write_text(sys.version+'\n')
