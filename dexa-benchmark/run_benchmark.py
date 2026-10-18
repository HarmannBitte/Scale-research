"""Reproducible, fixed-protocol exploratory benchmark. See PROTOCOL.md."""
import os
os.environ.setdefault('OMP_NUM_THREADS','2')
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
from pathlib import Path
import json, hashlib, platform
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import Ridge
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
SEED=20261017
TARGETS={'fat_pct':'percentage points','fat_kg':'kg','lean_kg':'kg','alm_kg':'kg'}
TCOLS=['DXDTOPF','DXDTOFAT','DXDTOLE','DXDLALE','DXDRALE','DXDLLLE','DXDRLLE']
ANTH=['BMXWT','BMXHT','BMXWAIST','BMXARMC','BMXCALF','BMXTHICR','BMXARML','BMXLEG']

def load(path):
 df=pd.read_sas(path,format='xport',compression='gzip')
 # IBM/SAS floating zero may decode as a tiny nonzero in pandas. Log count.
 tiny=(df.abs()<1e-50)&df.notna()&(df!=0)
 count=int(tiny.sum().sum());df=df.mask(tiny,0.0)
 return df,count

def cohort(cycle):
 tiny={};tables={}
 for name in ['DEMO','BMX','BIX','DXX']:
  path=ROOT/(name+('_B' if cycle=='2001' else '')+'.xpt.gz')
  if cycle=='1999' and name in ['BIX','DXX']:path=ROOT.parent/'dexa-investigation/data'/(name+'.xpt.gz')
  tables[name],tiny[name]=load(path)
 d=tables['DXX']; measured=d[(d.DXAEXSTS==1)&(d.DXITOT==0)]
 assert measured.groupby('SEQN').size().eq(5).all()
 assert measured.groupby('SEQN')[TCOLS].nunique(dropna=False).eq(1).all().all()
 d=d[d._MULT_==1].copy();assert d.SEQN.is_unique
 demo=tables['DEMO'][['SEQN','RIDAGEYR','RIAGENDR','RIDEXPRG','RIDRETH1']]
 df=d.merge(tables['BIX'],on='SEQN',validate='one_to_one').merge(demo,on='SEQN',validate='one_to_one').merge(tables['BMX'][['SEQN']+ANTH],on='SEQN',validate='one_to_one')
 flow=[{'stage':'one-to-one merged unique participants','n':len(df)}]
 def keep(mask,label):
  nonlocal df
  before=len(df);df=df.loc[mask].copy();flow.append({'stage':label,'n':len(df),'excluded':before-len(df)})
 keep(df.RIDAGEYR.between(18,49),'adults 18–49')
 keep(df.RIDEXPRG.ne(1),'not known pregnant')
 keep(df.DXAEXSTS.eq(1)&df.DXITOT.eq(0),'DXA complete and no region imputed')
 keep(df[TCOLS].notna().all(axis=1),'all target components present')
 keep(df.BIAEXSTS.eq(1)&df.BIDFIT.isin([0,1]),'BIA complete, excellent/good Cole fit')
 rcols=[c for c in df if c.startswith('BIXS')];xcols=[c for c in df if c.startswith('BIXC')]
 assert len(rcols)==len(xcols)==50
 keep(np.isfinite(df[rcols+xcols]).all(axis=1)&df[rcols].gt(0).all(axis=1),'all 100 raw channels finite, resistance positive')
 keep(np.isfinite(df[ANTH]).all(axis=1)&df[ANTH].gt(0).all(axis=1),'complete positive expanded anthropometry')
 keep(df.RIAGENDR.isin([1,2]),'recorded sex present')
 df['fat_pct']=df.DXDTOPF;df['fat_kg']=df.DXDTOFAT/1000;df['lean_kg']=df.DXDTOLE/1000
 df['alm_kg']=df[['DXDLALE','DXDRALE','DXDLLLE','DXDRLLE']].sum(axis=1)/1000
 df['age']=df.RIDAGEYR;df['sex']=df.RIAGENDR;df['height']=df.BMXHT;df['weight']=df.BMXWT
 df['bmi']=df.weight/(df.height/100)**2;df['waist']=df.BMXWAIST;df['waist_height']=df.waist/df.height
 for f in ['005K','050K','200K','500K','1M']:
  r=df['BIXS'+f];x=df['BIXC'+f]
  df['h2_r_'+f]=df.height**2/r;df['phase_'+f]=np.degrees(np.arctan2(x,r))
 basic=['age','sex','height','weight','bmi'];waist=basic+['waist','waist_height']
 f50=['BIXS050K','BIXC050K','h2_r_050K','phase_050K']
 spectrum=rcols+xcols+['h2_r_'+f for f in ['005K','050K','200K','500K','1M']]+['phase_'+f for f in ['005K','050K','200K','500K','1M']]
 expanded=waist+['BMXARMC','BMXCALF','BMXTHICR','BMXARML','BMXLEG']
 sets={'basic':basic,'waist':waist,'basic_50k':basic+f50,'waist_50k':waist+f50,'waist_spectra':waist+spectrum,'expanded':expanded,'expanded_50k':expanded+f50,'expanded_spectra':expanded+spectrum}
 for cols in sets.values():assert not any(c in TCOLS or c.startswith('BID') or c=='SEQN' for c in cols)
 summary={'cycle':cycle,'flow':flow,'tiny_zero_corrections':tiny,'n':len(df),'recorded_sex':df.sex.value_counts().to_dict(),'age_min':float(df.age.min()),'age_max':float(df.age.max()),'bmi_min':float(df.bmi.min()),'bmi_max':float(df.bmi.max()),'negative_reactance_values':int(df[xcols].lt(0).sum().sum()),'targets':df[list(TARGETS)].describe().to_dict()}
 return df,sets,summary

def metrics(y,p):
 e=np.asarray(p)-np.asarray(y);sd=e.std(ddof=1)
 return {'n':len(e),'mae':float(np.abs(e).mean()),'rmse':float(np.sqrt(np.mean(e**2))),'bias':float(e.mean()),'loa_low':float(e.mean()-1.96*sd),'loa_high':float(e.mean()+1.96*sd),'residual_p025':float(np.quantile(e,.025)),'residual_p975':float(np.quantile(e,.975))}

def main():
 a,sets,sa=cohort('1999');b,sets2,sb=cohort('2001');assert sets==sets2;assert not set(a.SEQN)&set(b.SEQN)
 (OUT/'cohort.json').write_text(json.dumps([sa,sb],indent=2))
 (OUT/'features.json').write_text(json.dumps(sets,indent=2))
 tr,te=train_test_split(a,test_size=.3,random_state=SEED,stratify=a.sex)
 runs=[('cycle_transfer',a,b),('within_1999',tr,te)]
 rows=[];pred=[];sub=[];comparisons=[]
 for evaluation,train,test in runs:
  split={'train_ids':train.SEQN.astype(int).tolist(),'test_ids':test.SEQN.astype(int).tolist()}
  (OUT/(evaluation+'_split.json')).write_text(json.dumps(split))
  assert set(split['train_ids']).isdisjoint(split['test_ids'])
  for modelname in ['ridge','extra_trees']:
   predictions={}
   for feat,cols in sets.items():
    # Multi-output fit shares feature processing, never uses test data.
    model=make_pipeline(StandardScaler(),Ridge(alpha=10)) if modelname=='ridge' else ExtraTreesRegressor(n_estimators=160,min_samples_leaf=5,max_features=1.0,random_state=SEED,n_jobs=2)
    model.fit(train[cols],train[list(TARGETS)])
    p=model.predict(test[cols]);predictions[feat]=p
    for j,target in enumerate(TARGETS):
     base={'evaluation':evaluation,'model':modelname,'features':feat,'target':target,'unit':TARGETS[target]}
     rows.append(base|metrics(test[target],p[:,j]))
     for seq,y,yhat in zip(test.SEQN,test[target],p[:,j]):pred.append(base|{'SEQN':int(seq),'reference':float(y),'prediction':float(yhat)})
     if evaluation=='cycle_transfer':
      groups={'sex':test.sex.astype(int).astype(str),'age':pd.cut(test.age,[17,29,39,49],labels=['18–29','30–39','40–49']),'bmi':pd.cut(test.bmi,[-np.inf,25,30,np.inf],right=False,labels=['<25','25–<30','≥30']),'RIDRETH1':test.RIDRETH1.astype(int).astype(str)}
      for group,values in groups.items():
       for label in values.unique():
        mask=np.asarray(values==label)
        if mask.sum()>1:sub.append(base|{'group':group,'label':str(label),'small_group':bool(mask.sum()<50)}|metrics(test.loc[mask,target],p[mask,j]))
    print(evaluation,modelname,feat,'done',flush=True)
   rng=np.random.default_rng(SEED);indices=rng.integers(0,len(test),size=(2000,len(test)))
   for before,after in [('waist','waist_50k'),('waist_50k','waist_spectra'),('expanded','expanded_50k'),('expanded_50k','expanded_spectra')]:
    for j,target in enumerate(TARGETS):
     y=test[target].to_numpy();gain=np.abs(predictions[before][:,j]-y)-np.abs(predictions[after][:,j]-y)
     boot=gain[indices].mean(axis=1)
     comparisons.append({'evaluation':evaluation,'model':modelname,'target':target,'before':before,'after':after,'mae_improvement':float(gain.mean()),'conditional_bootstrap_low':float(np.quantile(boot,.025)),'conditional_bootstrap_high':float(np.quantile(boot,.975))})
 for name,data in [('metrics',rows),('predictions',pred),('subgroups',sub),('paired_comparisons',comparisons)]:pd.DataFrame(data).to_csv(OUT/(name+('.csv.gz' if name=='predictions' else '.csv')),index=False)
 meta={'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__,'seed':SEED,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'protocol_sha256':hashlib.sha256((ROOT/'PROTOCOL.md').read_bytes()).hexdigest(),'no_hyperparameter_selection':True,'survey_weighted':False,'extra_trees_multioutput':True}
 (OUT/'run-metadata.json').write_text(json.dumps(meta,indent=2));print('COMPLETE',len(rows),'metric rows',flush=True)
if __name__=='__main__':main()
