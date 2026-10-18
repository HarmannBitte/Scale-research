# Extended from the pinned first benchmark; original code unchanged.
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

def cohort(cycle, fit_codes=(0,1), require_expanded=True):
 tiny={};tables={}
 for name in ['DEMO','BMX','BIX','DXX']:
  suffix={'1999':'','2001':'_B','2003':'_C'}[cycle]
  folder=ROOT if cycle=='2003' else ROOT.parent/'dexa-benchmark'
  path=folder/(name+suffix+'.xpt.gz')
  if cycle=='1999' and name in ['BIX','DXX']:path=ROOT.parent/'dexa-investigation/data'/(name+'.xpt.gz')
  tables[name],tiny[name]=load(path)
 d=tables['DXX']; measured=d[(d.DXAEXSTS==1)&(d.DXITOT==0)]
 consistent=measured.groupby('SEQN')[TCOLS].nunique(dropna=False).eq(1).all(axis=1) & measured.groupby('SEQN').size().eq(5)
 inconsistent_ids=consistent[~consistent].index
 d=d[d._MULT_==1].copy();assert d.SEQN.is_unique
 demo=tables['DEMO'][['SEQN','RIDAGEYR','RIAGENDR','RIDEXPRG','RIDRETH1','WTMEC2YR','SDMVPSU','SDMVSTRA']]
 df=d.merge(tables['BIX'],on='SEQN',validate='one_to_one').merge(demo,on='SEQN',validate='one_to_one').merge(tables['BMX'][['SEQN']+ANTH],on='SEQN',validate='one_to_one')
 flow=[{'stage':'one-to-one merged unique participants','n':len(df)}]
 def keep(mask,label):
  nonlocal df
  before=len(df);df=df.loc[mask].copy();flow.append({'stage':label,'n':len(df),'excluded':before-len(df)})
 keep(df.RIDAGEYR.between(18,49),'adults 18–49')
 keep(df.RIDEXPRG.ne(1),'not known pregnant')
 keep(df.DXAEXSTS.eq(1)&df.DXITOT.eq(0),'DXA complete and no region imputed')
 keep(~df.SEQN.isin(inconsistent_ids),'exclude inconsistent measured-flag target copies')
 keep(df[TCOLS].notna().all(axis=1),'all target components present')
 keep(df.BIAEXSTS.eq(1)&df.BIDFIT.isin(fit_codes),'BIA complete, fit codes '+str(fit_codes))
 rcols=[c for c in df if c.startswith('BIXS')];xcols=[c for c in df if c.startswith('BIXC')]
 assert len(rcols)==len(xcols)==50
 keep(np.isfinite(df[rcols+xcols]).all(axis=1)&df[rcols].gt(0).all(axis=1),'all 100 raw channels finite, resistance positive')
 required=ANTH if require_expanded else ['BMXWT','BMXHT','BMXWAIST']
 keep(np.isfinite(df[required]).all(axis=1)&df[required].gt(0).all(axis=1),'complete positive required anthropometry')
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
 if not require_expanded:sets={k:v for k,v in sets.items() if not k.startswith('expanded')}
 for cols in sets.values():assert not any(c in TCOLS or c.startswith('BID') or c=='SEQN' for c in cols)
 summary={'cycle':cycle,'flow':flow,'tiny_zero_corrections':tiny,'n':len(df),'recorded_sex':df.sex.value_counts().to_dict(),'age_min':float(df.age.min()),'age_max':float(df.age.max()),'bmi_min':float(df.bmi.min()),'bmi_max':float(df.bmi.max()),'negative_reactance_values':int(df[xcols].lt(0).sum().sum()),'targets':df[list(TARGETS)].describe().to_dict()}
 return df,sets,summary

