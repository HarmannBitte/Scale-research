"""Fixed fresh-cycle replication and sensitivity checks. See PROTOCOL.md."""
from pathlib import Path
import importlib.util,hashlib,json,platform
import numpy as np
import pandas as pd
import sklearn
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import ExtraTreesRegressor
from cohort_loader import cohort,SEED,TARGETS
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('original',ROOT.parent/'dexa-benchmark/run_benchmark.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def metric(y,p,w):
 d=old.metrics(y,p);d['mec_weighted_mae_sensitivity']=float(np.average(np.abs(p-y),weights=w));return d

def main():
 cohorts={};summaries=[]
 for label,fit,expanded in [('strict',(0,1),True),('marginal',(0,1,2),True),('core',(0,1),False)]:
  for c in ['1999','2001','2003']:
   df,features,summary=cohort(c,fit,expanded);df['cycle']=c
   assert np.isfinite(df.WTMEC2YR).all() and df.WTMEC2YR.gt(0).all()
   assert df.SEQN.is_unique and df.DXITOT.eq(0).all()
   cohorts[label,c]=(df,features);summary['sensitivity']=label;summaries.append(summary)
 for c in ['1999','2001']:
  a,f,_=old.cohort(c);b,f2=cohorts['strict',c]
  assert f==f2;pd.testing.assert_series_equal(a.SEQN,b.SEQN,check_names=True)
  pd.testing.assert_frame_equal(a[list(TARGETS)],b[list(TARGETS)])
  for cols in f.values():pd.testing.assert_frame_equal(a[cols],b[cols])
 for typ in ['strict','marginal','core']:
  ids=[set(cohorts[typ,c][0].SEQN) for c in ['1999','2001','2003']]
  assert all(ids[i].isdisjoint(ids[j]) for i in range(3) for j in range(i+1,3))
 (OUT/'cohorts.json').write_text(json.dumps(summaries,indent=2))
 plans=[('primary_1999_to_2003','strict',['1999'],False),('pooled_to_2003','strict',['1999','2001'],False),('marginal_fit_sensitivity','marginal',['1999','2001'],False),('core_anthro_sensitivity','core',['1999','2001'],False),('mec_weight_sensitivity','strict',['1999','2001'],True)]
 rows=[];pred=[];comparisons=[];groupsout=[];splits={}
 for run,typ,traincycles,weighted in plans:
  train=pd.concat([cohorts[typ,c][0] for c in traincycles],ignore_index=True);test,features=cohorts[typ,'2003']
  splits[run]={'train_ids':train.SEQN.astype(int).tolist(),'test_ids':test.SEQN.astype(int).tolist()}
  weights=train.WTMEC2YR/train.groupby('cycle').WTMEC2YR.transform('mean')
  grouping={'sex':test.sex.astype(int).astype(str),'bmi':pd.cut(test.bmi,[-np.inf,25,30,np.inf],right=False,labels=['<25','25–<30','≥30']).astype(str),'RIDRETH1':test.RIDRETH1.astype(int).astype(str)}
  grouping['sex_bmi']=grouping['sex']+' / '+grouping['bmi']
  for modelname in ['ridge','extra_trees']:
   preds={}
   for arm,cols in features.items():
    model=make_pipeline(StandardScaler(),Ridge(alpha=10)) if modelname=='ridge' else ExtraTreesRegressor(n_estimators=160,min_samples_leaf=5,max_features=1.0,random_state=SEED,n_jobs=2)
    kw={}
    if weighted:kw={'standardscaler__sample_weight':weights,'ridge__sample_weight':weights} if modelname=='ridge' else {'sample_weight':weights}
    model.fit(train[cols],train[list(TARGETS)],**kw);p=model.predict(test[cols]);preds[arm]=p
    for j,target in enumerate(TARGETS):
     base={'run':run,'model':modelname,'features':arm,'target':target,'unit':TARGETS[target],'n_train':len(train)}
     y=test[target].to_numpy();rows.append(base|metric(y,p[:,j],test.WTMEC2YR))
     for seq,y0,p0 in zip(test.SEQN,y,p[:,j]):pred.append(base|{'SEQN':int(seq),'reference':float(y0),'prediction':float(p0)})
     for kind,labels in grouping.items():
      for label in labels.unique():
       mask=np.asarray(labels==label)
       if mask.sum()>1:groupsout.append(base|{'group':kind,'label':str(label),'small_group':bool(mask.sum()<50)}|metric(y[mask],p[mask,j],test.WTMEC2YR[mask]))
   pairs=[('waist','waist_50k'),('waist_50k','waist_spectra')]
   if 'expanded' in features:pairs += [('expanded','expanded_50k'),('expanded_50k','expanded_spectra')]
   for before,after in pairs:
    for j,target in enumerate(TARGETS):
     y=test[target].to_numpy();gain=np.abs(preds[before][:,j]-y)-np.abs(preds[after][:,j]-y)
     allgroups=[('overall','all',np.ones(len(test),dtype=bool))]
     for group in ['sex','bmi','sex_bmi']:
      allgroups += [(group,str(label),np.asarray(grouping[group]==label)) for label in grouping[group].unique()]
     for group,label,mask in allgroups:
      g=gain[mask];rng=np.random.default_rng(SEED);idx=rng.integers(0,len(g),size=(2000,len(g)));boot=g[idx].mean(axis=1)
      comparisons.append({'run':run,'model':modelname,'target':target,'before':before,'after':after,'group':group,'label':label,'n':len(g),'small_group':bool(len(g)<50),'mae_improvement':float(g.mean()),'conditional_bootstrap_low':float(np.quantile(boot,.025)),'conditional_bootstrap_high':float(np.quantile(boot,.975)),'mec_weighted_improvement_sensitivity':float(np.average(g,weights=test.WTMEC2YR[mask]))})
   print(run,modelname,'complete',len(train),len(test),flush=True)
 for n,data in [('metrics',rows),('predictions',pred),('paired_comparisons',comparisons),('subgroups',groupsout)]:pd.DataFrame(data).to_csv(OUT/(n+('.csv.gz' if n=='predictions' else '.csv')),index=False)
 (OUT/'splits.json').write_text(json.dumps(splits))
 meta={'date':'2026-10-17','python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__,'seed':SEED,'earlier_cohort_feature_target_equality_checked':True,'frozen_scientific_settings':True,'weighted_results_are_not_design_corrected':True,'hashes':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['PROTOCOL.md','run_followup.py','cohort_loader.py']},'original_script_sha256':hashlib.sha256((ROOT.parent/'dexa-benchmark/run_benchmark.py').read_bytes()).hexdigest()}
 (OUT/'metadata.json').write_text(json.dumps(meta,indent=2));print('DONE',len(rows),'metrics',len(pred),'predictions',flush=True)
if __name__=='__main__':main()
