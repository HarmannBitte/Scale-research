import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from cohort_loader import cohort
from run_followup import old,metric
ROOT=Path(__file__).resolve().parent
P=ROOT/'results'
@pytest.fixture(scope='module')
def preds():return pd.read_csv(P/'predictions.csv.gz')
def test_original_cohorts_unchanged():
 for c in ['1999','2001']:
  a,f,_=old.cohort(c);b,g,_=cohort(c)
  assert f==g
  pd.testing.assert_series_equal(a.SEQN,b.SEQN)
  pd.testing.assert_frame_equal(a[list(old.TARGETS)],b[list(old.TARGETS)])
def test_new_cohort_and_inconsistent_ids_excluded():
 a,_,_=cohort('2003');assert len(a)==1858
 bad=set(json.loads((ROOT/'input-consistency-audit.json').read_text())[2]['inconsistent_ids'])
 assert len(bad)==80 and set(a.SEQN).isdisjoint(bad)
 assert a.filter(regex='^DXI').eq(0).all().all()
 assert a.BIDFIT.isin([0,1]).all()
def test_independent_reader_receipt():
 d=json.loads((ROOT/'independent-reader-check.json').read_text())
 assert d['independently_found_inconsistent_ids']==80
 assert d['reader'].startswith('pyreadstat')
def test_splits_and_same_subjects_per_arm(preds):
 splits=json.loads((P/'splits.json').read_text())
 for name,g in preds.groupby('run'):
  s=splits[name];assert set(s['train_ids']).isdisjoint(s['test_ids'])
  for _,arm in g.groupby(['model','features','target']):assert arm.SEQN.is_unique and set(arm.SEQN)==set(s['test_ids'])
def test_all_saved_metrics(preds):
 rows=pd.read_csv(P/'metrics.csv');assert len(rows)==296
 groups={k:g for k,g in preds.groupby(['run','model','features','target'])}
 weightmaps={}
 for typ in ['strict','marginal','core']:
  d,_,_=cohort('2003',fit_codes=(0,1,2) if typ=='marginal' else (0,1),require_expanded=typ!='core')
  weightmaps[typ]=d.set_index('SEQN').WTMEC2YR
 for _,r in rows.iterrows():
  g=groups[r.run,r.model,r.features,r.target];typ='marginal' if r.run=='marginal_fit_sensitivity' else 'core' if r.run=='core_anthro_sensitivity' else 'strict'
  vals=metric(g.reference.to_numpy(),g.prediction.to_numpy(),weightmaps[typ].loc[g.SEQN].to_numpy())
  for k,v in vals.items():assert np.isclose(v,r[k],atol=1e-10)
def test_overall_gain_arithmetic():
 a=pd.read_csv(P/'paired_comparisons.csv');m=pd.read_csv(P/'metrics.csv')
 for _,r in a[a.group=='overall'].iterrows():
  g=m[(m.run==r.run)&(m.model==r.model)&(m.target==r.target)].set_index('features')
  assert np.isclose(g.loc[r.before,'mae']-g.loc[r.after,'mae'],r.mae_improvement)
  assert np.isclose(g.loc[r.before,'mec_weighted_mae_sensitivity']-g.loc[r.after,'mec_weighted_mae_sensitivity'],r.mec_weighted_improvement_sensitivity)
 assert (a.conditional_bootstrap_low<=a.conditional_bootstrap_high).all()
def test_finite_predictions_and_units(preds):
 assert len(preds)==553512
 assert np.isfinite(preds[['reference','prediction']]).all().all()
 assert set(preds[preds.target=='fat_pct'].unit)=={'percentage points'}
 assert set(preds[preds.target!='fat_pct'].unit)=={'kg'}
def test_hashes_match_final_sources():
 d=json.loads((P/'metadata.json').read_text())
 for file,expected in d['hashes'].items():assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==expected
 assert hashlib.sha256((ROOT.parent/'dexa-benchmark/run_benchmark.py').read_bytes()).hexdigest()==d['original_script_sha256']
