import requests,concurrent.futures,pathlib,json
root=pathlib.Path('/home/user/open-source-survey')
repos=['openebi/hardware','openebi/software','melazab/AD5940-BIOZ','oscaroflores/UPRM-Multi_Frq-BioZ-Research','analogdevicesinc/MAX32655_MAX30009','OpenEIT/EIT_Firmware','OpenEIT/EIT_EE','OpenEIT/OpenEIT','eitcom/pyEIT','ECSHackWeek/impedance.py','vyrjana/DearEIS','oliexdev/openScale','dyarleniber/AD5933-arduino-bioimpedance','TAMU-ESP/BioZPulse-Sim-Platform','Protocentral/protocentral_max30001','eayrenk/bioscale-okok-alternative']
def get(repo):
 p=root/repo.replace('/','__');p.mkdir(exist_ok=True)
 result={'repo':repo}
 try:
  r=requests.get('https://api.github.com/repos/'+repo,timeout=25);result['metadata_status']=r.status_code
  if r.status_code!=200:return result
  d=r.json();(p/'metadata.json').write_text(json.dumps(d,indent=2));branch=d['default_branch']
  result.update({k:d.get(k) for k in ['default_branch','pushed_at','archived','license','fork','parent']})
  r=requests.get('https://api.github.com/repos/'+repo+'/git/trees/'+branch,params={'recursive':'1'},timeout=25);result['tree_status']=r.status_code
  paths=[]
  if r.status_code==200:
   tree=r.json();(p/'tree.json').write_text(json.dumps(tree,indent=2));paths=[t['path'] for t in tree.get('tree',[]) if t['type']=='blob'];result['tree_sha']=tree['sha'];result['truncated']=tree.get('truncated')
  chosen=[x for x in paths if '/' not in x and (x.lower().startswith('readme') or 'licen' in x.lower() or 'copying' in x.lower())]
  if not chosen:chosen=['README.md']
  result['saved']=[]
  for f in chosen:
   r=requests.get(f'https://raw.githubusercontent.com/{repo}/{branch}/{f}',timeout=25)
   if r.status_code==200:(p/f).write_bytes(r.content);result['saved'].append(f)
  result['interesting_paths']=[x for x in paths if any(w in x.lower() for w in ['test','calib','bioz','bioimp','bodyimp','license','schem','bom','readme','gui','main.c','max30009'])][:100]
 except Exception as e:result['error']=str(e)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 results=list(ex.map(get,repos))
(root/'inventory.json').write_text(json.dumps(results,indent=2))
for d in results:print(d['repo'], d.get('metadata_status'),d.get('pushed_at'),(d.get('license') or {}).get('spdx_id'), 'tree',d.get('tree_status'),'saved',d.get('saved'),d.get('error',''))
