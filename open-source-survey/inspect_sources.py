import requests,pathlib,json,concurrent.futures
r=pathlib.Path('/home/user/open-source-survey')
items={
'melazab/AD5940-BIOZ':['gui/main.py','gui/test_flash_targets.py','measure-4wire-bioz/main.c','measure-4wire-bioz/Makefile','measure-4wire-bioz/ad5940lib/LICENSE'],
'oscaroflores/UPRM-Multi_Frq-BioZ-Research':['src/main.c','src/bioZ.c','BLE_GUI.py'],
'dyarleniber/AD5933-arduino-bioimpedance':[],
'analogdevicesinc/no-OS':['drivers/afe/max30009/max30009.c','drivers/afe/max30009/max30009.h','projects/max30009/src/examples/basic/basic_example.c','projects/max30009/README.rst','doc/sphinx/source/projects/afe/max30009.rst','LICENSE'],
'eayrenk/bioscale-okok-alternative':[],
'oliexdev/openScale':['arduino_mcu/README.md']}
for repo in ['dyarleniber/AD5933-arduino-bioimpedance','eayrenk/bioscale-okok-alternative']:
 p=r/repo.replace('/','__');tree=json.loads((p/'tree.json').read_text())['tree'];items[repo]=[x['path'] for x in tree if x['type']=='blob' and (x['path'].endswith('.ino') or ('bia' in x['path'].lower() and x['path'].endswith(('.py','.dart'))))][:8]
def fetch(t):
 repo,file=t;p=r/repo.replace('/','__');p.mkdir(exist_ok=True);m=p/'metadata.json';branch=json.loads(m.read_text())['default_branch'] if m.exists() else 'main'
 if repo=='analogdevicesinc/no-OS':branch='main'
 url=f'https://raw.githubusercontent.com/{repo}/{branch}/{file}'
 try:
  q=requests.get(url,timeout=25)
  if q.status_code==404 and repo=='analogdevicesinc/no-OS':url=url.replace('/main/','/master/');q=requests.get(url,timeout=25)
  if q.status_code==200:
   dest=p/'selected'/file;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(q.content)
  return {'repo':repo,'file':file,'url':url,'status':q.status_code}
 except Exception as e:return {'repo':repo,'file':file,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:result=list(ex.map(fetch,[(repo,f) for repo,files in items.items() for f in files]))
(r/'selected-sources.json').write_text(json.dumps(result,indent=2));print('\n'.join(str(x) for x in result))
