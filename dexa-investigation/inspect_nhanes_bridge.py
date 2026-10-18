"""Inspect public CDC files for an impedance/DXA research bridge; no model fitting.
The first imputation is used ONLY to count unique subjects, never for inference.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests, hashlib, io, gzip, json
import pandas as pd
ROOT=Path(__file__).resolve().parent
URLS={
 'BIX':'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/BIX.xpt',
 'DXX':'https://wwwn.cdc.gov/nchs/data/nhanes/public/1999/datafiles/dxx.xpt',
}
def get(item):
 name,url=item
 r=requests.get(url,timeout=60);r.raise_for_status(); raw=r.content
 if not raw.startswith(b'HEADER RECORD'):raise ValueError(f'{name}: not SAS transport: {raw[:80]!r}')
 (ROOT/'data').mkdir(exist_ok=True)
 (ROOT/'data'/f'{name}.xpt.gz').write_bytes(gzip.compress(raw))
 df=pd.read_sas(io.BytesIO(raw),format='xport')
 return name,df,{'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'rows':len(df),'unique_seqn':int(df.SEQN.nunique()),'columns':list(df.columns)}
a=list(ThreadPoolExecutor(max_workers=2).map(get,URLS.items()))
dfs={n:d for n,d,m in a}; meta={n:m for n,d,m in a}
b=dfs['BIX'];d=dfs['DXX'];multi=[c for c in d if 'MULT' in c.upper()]
meta['join']={'imputation_column':multi,'shared_unique_seqn':len(set(b.SEQN)&set(d.SEQN)), 'resistance_columns':len([c for c in b if c.startswith('BIXS')]),'reactance_columns':len([c for c in b if c.startswith('BIXC')]),'both_50khz_present':int(b[['BIXS050K','BIXC050K']].notna().all(axis=1).sum()),'note':'Overlap and nonmissing counts only. No validity/adult/survey-weight/model analysis; imputed records are not independent participants.'}
(ROOT/'nhanes-bridge-inspection.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({k:({x:y for x,y in v.items() if x!='columns'} if isinstance(v,dict) else v) for k,v in meta.items()},indent=2))
