import ast,concurrent.futures,hashlib,json,math,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path('/home/user/open-projects-collection');CACHE=pathlib.Path('/home/user/.cache/open-projects');PY=CACHE/'test-env/bin/python';LOG=ROOT/'verification';paths=json.loads((ROOT/'verification-source-paths.json').read_text());idx={x['repo']:x for x in json.loads((ROOT/'collection-index.json').read_text())}
def run(name,args,cwd,env=None,timeout=90):
 e=os.environ.copy();e.update({'MPLBACKEND':'Agg','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'});e.update(env or {});t=time.monotonic();rec={'name':name,'command':args,'cwd':str(cwd),'environment_overrides':{k:e[k] for k in ['MPLBACKEND','PYTEST_DISABLE_PLUGIN_AUTOLOAD','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']},'timeout_seconds':timeout}
 try:
  p=subprocess.run(args,cwd=cwd,env=e,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout);s=p.stdout;rec.update(status='pass' if p.returncode==0 else 'failed',exit_code=p.returncode)
 except subprocess.TimeoutExpired as ex:s=(ex.stdout or b'').decode(errors='replace') if isinstance(ex.stdout,bytes) else ex.stdout or '';rec.update(status='timeout',exit_code=None)
 rec['duration_seconds']=round(time.monotonic()-t,3);rec['log']=name+'.log';rec['log_sha256']=hashlib.sha256(s.encode()).hexdigest();(LOG/(name+'.log')).write_text(s);(LOG/(name+'.json')).write_text(json.dumps(rec,indent=2));print(name,rec['status'],s[-1100:],flush=True);return rec
code='''import json,numpy as np
from impedance.models.circuits import CustomCircuit
f=np.array([5000.,10000.,20000.,50000.,100000.,200000.])
R0,R1,C1=100.,500.,1e-8
z=R0+R1/(1+1j*2*np.pi*f*R1*C1)
c=CustomCircuit('R0-p(R1,C1)',initial_guess=[90,450,1.2e-8])
c.fit(f,z)
r=c.predict(f)
assert np.allclose(c.parameters_,[R0,R1,C1],rtol=1e-4)
assert np.all(z.imag<0)
assert np.max(np.abs(r-z))<1e-3
print(json.dumps({'label':'SYNTHETIC NOT HARDWARE DATA','frequency_Hz':f.tolist(),'true_parameters':[R0,R1,C1],'fit_parameters':c.parameters_.tolist(),'max_complex_error_ohm':float(np.max(np.abs(r-z)))}))
'''
script=ROOT/'verification/synthetic-rc-check.py';script.write_text(code)
fs=[
 ('impedance-py-bounded-upstream-tests',[str(PY),'-m','pytest','-q','impedance/tests','-k','not test_circuit_fit','--disable-warnings'],pathlib.Path(paths['ECSHackWeek/impedance.py']),{'PYTHONPATH':paths['ECSHackWeek/impedance.py']},90),
 ('impedance-py-synthetic-rc-check',[str(PY),str(script)],pathlib.Path(paths['ECSHackWeek/impedance.py']),{'PYTHONPATH':paths['ECSHackWeek/impedance.py']},60),
 ('pyimpspec-install-dry-run',[str(PY),'-m','pip','install','--dry-run',str(CACHE/'vyrjana__pyimpspec')],CACHE,{},90)]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(lambda t:run(*t),fs))
# Isolate one pure upstream function with AST, avoiding imports, BLE, serial, GUI or device connection.
f=CACHE/'OpenEIT__OpenEIT/OpenEIT/backend/serialhandler.py';tree=ast.parse(f.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='parse_any_line');space={};exec(compile(ast.Module(body=[node],type_ignores=[]),str(f),'exec'),space);fn=space['parse_any_line'];probes=[]
for label,line,mode in [('time_series','1.5,-2.0','a'),('spectroscopy','magnitudes:50000;123.4','b'),('EIT','magnitudes:1,2,3','c'),('bad_token','magnitudes:1,wrong,3','c'),('nonfinite','magnitudes:nan,inf,-inf','c'),('empty_frame','magnitudes:','c'),('empty_fields','magnitudes:1,,3','c')]:
 out=fn(line,mode);probes.append({'label':label,'input':line,'mode':mode,'returned':None if out is None else [str(x) if not math.isfinite(x) else x for x in out]})
record={'repo':'OpenEIT/OpenEIT','commit':idx['OpenEIT/OpenEIT']['commit'],'source_path':str(f),'method':'AST-isolated exact upstream parse_any_line; no transport/GUI executed','probes':probes,'interpretation':'Valid lines parse and nonnumeric text rejects; NaN/infinity, empty frames and dropped empty fields are accepted without a quality flag. No expected frame-length check in this function.'}
(LOG/'openeit-parser-probes.json').write_text(json.dumps(record,indent=2));print(json.dumps(record,indent=2),flush=True)
(LOG/'followup-results.json').write_text(json.dumps(results,indent=2))
