import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from run_benchmark import cohort,metrics,TARGETS
P=Path(__file__).resolve().parent/'results'
@pytest.fixture(scope='module')
def cohorts():
 return cohort('1999'),cohort('2001')
@pytest.fixture(scope='module')
def predictions():
 return pd.read_csv(P/'predictions.csv.gz')
def test_cohort_counts_and_observed_labels(cohorts):
 for (df,features,summary),n in zip(cohorts,[1802,2066]):
  assert len(df)==n and df.SEQN.is_unique
  assert (df.DXITOT==0).all() and (df.DXAEXSTS==1).all()
  assert df.RIDAGEYR.between(18,49).all()
  assert df.BIDFIT.isin([0,1]).all()
  assert df.BIAEXSTS.eq(1).all()
  assert df.filter(regex=r'^DXI').eq(0).all().all()
def test_disjoint_splits(cohorts):
 a=cohorts[0][0];b=cohorts[1][0]
 assert set(a.SEQN).isdisjoint(b.SEQN)
 for name in ['cycle_transfer','within_1999']:
  s=json.loads((P/(name+'_split.json')).read_text())
  assert set(s['train_ids']).isdisjoint(s['test_ids'])
  assert len(s['train_ids'])==len(set(s['train_ids']))
def test_predictor_whitelist_and_identical_feature_maps(cohorts):
 assert cohorts[0][1]==cohorts[1][1]
 for cols in cohorts[0][1].values():
  assert len(cols)==len(set(cols))
  assert all(not c.startswith(('DX','BID')) and c!='SEQN' for c in cols)
def test_every_arm_same_test_subjects(predictions):
 for name,g in predictions.groupby('evaluation'):
  expected=set(json.loads((P/(name+'_split.json')).read_text())['test_ids'])
  for _,arm in g.groupby(['model','features','target']):
   assert set(arm.SEQN)==expected and arm.SEQN.is_unique
  assert np.isfinite(g[['reference','prediction']]).all().all()
def test_all_metric_rows_recompute(predictions):
 saved=pd.read_csv(P/'metrics.csv');assert len(saved)==128
 for _,r in saved.iterrows():
  g=predictions[(predictions.evaluation==r.evaluation)&(predictions.model==r.model)&(predictions.features==r.features)&(predictions.target==r.target)]
  actual=metrics(g.reference,g.prediction)
  for key,value in actual.items():assert np.isclose(value,r[key],atol=1e-10)
def test_paired_gain_sign_and_units():
 a=pd.read_csv(P/'paired_comparisons.csv');m=pd.read_csv(P/'metrics.csv')
 assert len(a)==64
 for _,r in a.iterrows():
  base=m[(m.evaluation==r.evaluation)&(m.model==r.model)&(m.target==r.target)].set_index('features')
  assert np.isclose(base.loc[r.before,'mae']-base.loc[r.after,'mae'],r.mae_improvement)
  assert r.conditional_bootstrap_low<=r.conditional_bootstrap_high
 assert set(m[m.target=='fat_pct'].unit)=={'percentage points'}
 assert set(m[m.target!='fat_pct'].unit)=={'kg'}
