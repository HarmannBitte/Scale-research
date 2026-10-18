"""Independent input decoder cross-check. Requires pyreadstat; no model fitting."""
from pathlib import Path
import gzip,tempfile,os,json,pyreadstat,numpy as np
from cohort_loader import load,TCOLS,ROOT
raw=gzip.decompress((ROOT/'DXX_C.xpt.gz').read_bytes())
with tempfile.NamedTemporaryFile(suffix='.xpt',delete=False) as f:
 f.write(raw);name=f.name
try:q,meta=pyreadstat.read_xport(name)
finally:os.unlink(name)
p,_=load(ROOT/'DXX_C.xpt.gz')
assert q.columns.tolist()==p.columns.tolist()
for c in ['SEQN','_MULT_','DXITOT','DXAEXSTS']+TCOLS:
 assert np.allclose(q[c],p[c],rtol=0,atol=1e-50,equal_nan=True),c
m=q[(q.DXAEXSTS==1)&(q.DXITOT==0)]
bad=m.groupby('SEQN')[TCOLS].nunique(dropna=False).gt(1).any(axis=1)
j={'reader':'pyreadstat '+pyreadstat.__version__,'agreement':'All IDs, imputation/version/status flags and target values agree with normalized pandas within absolute 1e-50, rtol0, equalNaN','independently_found_inconsistent_ids':int(bad.sum()),'reason':'Conservative exclusion; source inconsistency observed, cause not established. Not proof of CDC error or clinical measurement failure.'}
(ROOT/'independent-reader-check.json').write_text(json.dumps(j,indent=2))
print(json.dumps(j,indent=2))
