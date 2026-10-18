import subprocess,pathlib,json,os,time,hashlib
C=pathlib.Path('/home/user/.cache/open-projects');L=pathlib.Path('/home/user/open-projects-collection/verification');envdir=C/'analysis-env'
subprocess.run(['python','-m','venv',str(envdir)],check=True)
P=envdir/'bin/python';src={r:next((C/'full'/r).iterdir()) for r in ['vyrjana__pyimpspec','vyrjana__DearEIS']}
def run(name,args,cwd,timeout=150,extra=None):
 env=os.environ.copy();env.update({'MPLBACKEND':'Agg','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1'});env.update(extra or {});t=time.monotonic()
 try:q=subprocess.run(args,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout);s=q.stdout;status='pass' if q.returncode==0 else 'failed';code=q.returncode
 except subprocess.TimeoutExpired as e:s=(e.stdout or b'').decode(errors='replace') if isinstance(e.stdout,bytes) else e.stdout or '';status='timeout';code=None
 rec={'name':name,'status':status,'command':args,'cwd':str(cwd),'timeout_seconds':timeout,'duration_seconds':time.monotonic()-t,'exit_code':code,'log':name+'.log','log_sha256':hashlib.sha256(s.encode()).hexdigest()};(L/(name+'.log')).write_text(s);(L/(name+'.json')).write_text(json.dumps(rec,indent=2));print(name,status,s[-1800:],flush=True);return code
ret=run('analysis-packages-install',[str(P),'-m','pip','install',str(src['vyrjana__pyimpspec']),str(src['vyrjana__DearEIS']),'pytest'],C,180)
if ret==0:
 run('pyimpspec-selected-upstream-tests',[str(P),'-m','pytest','-q','test_circuit.py','test_connection.py','test_element.py','test_data.py','--disable-warnings'],src['vyrjana__pyimpspec']/'tests',180)
 run('deareis-selected-upstream-tests',[str(P),'-m','pytest','-q','test_project.py','test_utility.py','--disable-warnings'],src['vyrjana__DearEIS']/'tests',120)
 q=subprocess.run([str(P),'-m','pip','freeze'],capture_output=True,text=True);(L/'analysis-environment-freeze.txt').write_text(q.stdout)
