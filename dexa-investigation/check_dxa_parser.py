"""Bounded synthetic robustness check, not patient-PDF validation.
Loads selected functions by AST to avoid executing GUI setup or installing its dependencies.
Assertions document CURRENT KNOWN BEHAVIOR, including a reproduced defect.
"""
import ast, re, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'dxa-extractor/dxa_extractor_gui.py'
tree=ast.parse(p.read_text())
names={'fix_doubled_chars','needs_dedup','clean_text','detect_report_type','parse_body_comp_vat'}
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
ns={'re':re}
exec(compile(ast.Module(body=funcs,type_ignores=[]),str(p),'exec'),ns)
texts=['L Arm 1000.0 4000.0 5000.0 20.0','L Arm 10000.0 40000.0 50000.0 20.0','L Arm 1,000.0 4,000.0 5,000.0 20.0']
rows=[]
for text in texts:
 cleaned=ns['clean_text'](text)
 rows.append({'synthetic_input':text,'cleaned':cleaned,'parsed':ns['parse_body_comp_vat'](cleaned)})
assert rows[0]['parsed']['L_Arm_Fat_Mass_g']==1000
assert rows[1]['parsed']['L_Arm_Fat_Mass_g']==100, 'Known defect behavior changed; re-review.'
assert rows[2]['parsed']=={}, 'Comma-handling behavior changed; re-review.'
(ROOT/'dxa-extractor-synthetic-checks.json').write_text(json.dumps(rows,indent=2)+'\n')
print('3 synthetic cases checked: baseline parses; repeated-digit corruption and comma rejection reproduced. This is NOT a passing clinical parser validation.')
