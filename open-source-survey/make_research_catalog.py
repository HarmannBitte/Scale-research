import csv,hashlib,json,pathlib,zipfile,io
R=pathlib.Path('/home/user/open-projects-collection');V=R/'verification';data=[]
for p in R.glob('*.json'):
 d=json.loads(p.read_text())
 if isinstance(d,dict) and d.get('compact_archive'):d['manifest_file']=p.name;data.append(d)
by={d['repo']:d for d in data if 'required-by-examples' not in d['compact_archive']}
families={
'OpenEIT/EIT_EE':('OpenEIT / Spectra','hardware','ADuCM350; editable older CAD, newer PDF, fabrication files','CC BY-NC-SA 4.0','CAD/PDF/source inspection; no hardware or firmware build'),
'OpenEIT/EIT_Firmware':('OpenEIT / Spectra','firmware','Time series, spectroscopy, multi-electrode EIT','CC BY-NC-SA 4.0 plus vendored notices','Source inspection; no IAR build'),
'OpenEIT/OpenEIT':('OpenEIT / Spectra','dashboard','Serial/BLE, reconstruction, record/playback','CC BY-NC-SA 4.0 plus vendored notices','Seven isolated parser probes; no dashboard runtime'),
'dioptre/EIT_Firmware':('OpenEIT / Spectra','GCC firmware fork','ADuCM350 GCC/startup/linker variation','Mixed CC BY-NC-SA / Apache / third-party','Source/build-script inspection; no full build'),
'openebi/hardware':('OpenEBI','hardware','AD5933 tetrapolar front end; legacy Eagle','CC BY-SA 3.0','File/BOM/PDF inspection; no CAD DRC'),
'openebi/software':('OpenEBI','AVR firmware','UART raw real/imaginary sweeps/free-run','MIT','Source inspection; AVR compiler unavailable'),
'analogdevicesinc/ad5940-examples':('ADI AD5940 ecosystem','reference firmware','BIA, two-wire impedance, EDA and other examples','File-level ADI notices','Exact library gitlink resolved; previous custom builds not rerun'),
'analogdevicesinc/ad5940lib':('ADI AD5940 ecosystem','driver library','AD5940 register/sequencer/calibration primitives','Preserved library notices','Current and exact examples-required revisions collected'),
'melazab/AD5940-BIOZ':('melazab AD5940-BIOZ','GNU firmware + GUI','Two/four-wire sweeps/time series, CSV GUI','Original project-wide licence not located; vendored licence separate','Five GNU builds linked; five mocked GUI tests passed'),
'analogdevicesinc/no-OS':('ADI no-OS MAX30009','driver + example','I/Q FIFO, status/lead-off, programmable configuration','BSD-3-Clause in inspected driver/example; dependencies separate','Scoped source only; no complete target build'),
'analogdevicesinc/MAX32655_MAX30009':('ADI MAX30009 example','reference firmware','GSR/EDA, I/Q and derived output','Custom permissive Maxim notice','Source/setup review only'),
'oscaroflores/UPRM-Multi_Frq-BioZ-Research':('UPRM BioZ','firmware + GUI','Two-frequency MAX30009, BLE/SD/IMU','Custom permissive Maxim notice; contribution/dependency coverage separate','Source and data-path review; no SDK/hardware build'),
'dyarleniber/AD5933-arduino-bioimpedance':('Arduino AD5933 BIA','firmware + thesis','Magnitude and equation-based TBW/FFM/FM','GPLv3 software; thesis provenance retained','55-page thesis reviewed; eight passive comparisons recalculated'),
'ECSHackWeek/impedance.py':('impedance.py','analysis','Circuit fitting, preprocessing, validation, plots','MIT','34 bounded upstream tests + synthetic RC check passed; global-fit receipt separate'),
'vyrjana/DearEIS':('DearEIS / pyimpspec','analysis GUI','Projects, circuits, analysis workbench','GPLv3-or-later','Installed; 43 selected tests passed; GUI not exercised'),
'vyrjana/pyimpspec':('DearEIS / pyimpspec','analysis backend','Parsers, circuits, validation, fitting, simulation','GPLv3-or-later','Installed; 139 selected unittest tests passed; pytest capture difference recorded'),
'eitcom/pyEIT':('pyEIT','EIT analysis','Mesh, forward/inverse solvers, performance tools','BSD-style current text; example exceptions','62 upstream tests passed'),
'oliexdev/openScale':('openScale','Android app','Local scale tracking, BLE handlers, CSV','GPLv3 / file-level notices','Source/build requirements/custom protocol reviewed; no Android build'),
'oliexdev/openScale-sync':('openScale','Android sync companion','External service integration separate from local app','GPLv3','Source/documentation reviewed; no Android build'),
'eayrenk/bioscale-okok-alternative':('BioScale','Python + Flutter app','Chipsea BLE, local storage, equations','MIT','Python tests: four passed, one test/API mismatch failed'),
'TAMU-ESP/BioZPulse-Sim-Platform':('BioZPulse','simulation','MATLAB-generated 3D circuit grid + LTspice','GPLv3 code; separate MATLAB/LTspice terms','Source review; simulations not run'),
'Protocentral/protocentral_max30001':('ProtoCentral MAX30001 ecosystem','hardware','Single-lead ECG and BioZ respiration','CERN-OHL-P v2 hardware; MIT code declaration; CC BY-SA 4.0 docs','CAD/PDF structure reviewed; no physical test'),
'Protocentral/protocentral_max30001_arduino_library':('ProtoCentral MAX30001 ecosystem','Arduino driver','ECG/BioZ, R-R, lead-off, five examples','MIT','Source/examples reviewed; Arduino build not run'),
'Protocentral/protocentral_max30001_zephyr_driver':('ProtoCentral MAX30001 ecosystem','Zephyr driver','Out-of-tree sensor driver and bindings','MIT','Source/config reviewed; Zephyr build not run'),
'Protocentral/protocentral_openview':('ProtoCentral MAX30001 ecosystem','Flutter viewer','Descriptor-based framed acquisition, record/replay','MIT','Architecture/transport/recording reviewed; Flutter build not run')}
rows=[]
for d in sorted(data,key=lambda x:(x['repo'],x['commit'])):
 fam,layer,caps,lic,status=families[d['repo']];source_dir=d['compact_archive'][:-4]
 rows.append({'family':fam,'repo':d['repo'],'commit':d['commit'],'layer':layer,'capabilities':caps,'licence_observation_not_exclusion':lic,'verification':status,'included_files':len(d['source_files']),'omitted_files':len(d['omitted_files']),'scope':d['scope'],'source_directory':'sources/'+source_dir,'manifest':'manifests/'+d['manifest_file'],'upstream_archive_url':d['archive_url'],'upstream_archive_sha256':d.get('upstream_archive_sha256',''),'pinned_source_url':d['url']+'/tree/'+d['commit']})
with (R/'project-catalog.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
findings=[]
def find(repo,path,needle,topic,observation,kind='source inspection'):
 d=by[repo]
 with zipfile.ZipFile(R/d['compact_archive']) as z:txt=z.read(path).decode(errors='replace')
 lines=txt.splitlines();hits=[i for i,s in enumerate(lines,1) if needle in s];i=hits[0] if hits else 1
 findings.append({'repo':repo,'commit':d['commit'],'path':path,'line':i,'topic':topic,'observation':observation,'evidence_kind':kind,'source_url':d['url']+'/blob/'+d['commit']+'/'+path+'#L'+str(i),'excerpt':'\n'.join(lines[max(i-2,0):i+3])})
find('OpenEIT/EIT_Firmware','modes.h','MULTIFREQUENCY_ARRAY_SIZE','frequency configuration','Inspected spectroscopy array has 15 requested frequencies, 200 Hz–70 kHz.')
find('OpenEIT/EIT_Firmware','modes.h','#define FREQ','frequency configuration','Common FREQ macro is 25 kHz; not a measured frequency or a guarantee for all sequences.')
find('OpenEIT/EIT_Firmware','modes.h','SINE_AMPLITUDE_BIPOLAR','excitation review','Bipolar amplitude macro references VPEAK * 40 rather than VPEAK_BIPOLAR; reconcile with sequence/registers before passive testing.')
find('OpenEIT/EIT_Firmware','OpenEIT.c','void bioimpedance_spectroscopy','complex export','Inspected spectroscopy path computes/prints magnitude; phase helper existence does not prove R/X export.')
find('OpenEIT/OpenEIT','OpenEIT/backend/serialhandler.py','def parse_any_line','input quality','Exact function probed: nonfinite values, empty records and missing fields accepted without shape/quality enforcement.','source + seven AST-isolated probes')
find('OpenEIT/OpenEIT','setup.py',"'numpy==1.16.2'",'dependency consistency','setup.py dependency pins differ substantially from requirements.txt.')
find('OpenEIT/OpenEIT','app.py','darwin_xx','BLE maintenance','Source explicitly disables old macOS BLE route with a nonstandard platform string.')
find('OpenEIT/OpenEIT','OpenEIT/reconstruction/pyeit/eit/fem.py','dtype=np.float','dependency compatibility','Bundled older solver contains removed NumPy alias; selected source not a clean current-runtime validation.')
find('openebi/software','main.c','void take_measurement','raw units and validity','Averaged AD5933 register counts and polling; nonzero average/timeout must be validated externally.')
find('openebi/software','main.c','sscanf','parameter validation','Configuration sscanf return count not checked here; not a demonstrated safe command parser.')
find('melazab/AD5940-BIOZ','measure-4wire-bioz/main.c','cfg->SweepCfg.SweepPoints','sweep defaults','40-point linear requested sweep, not verified hardware bandwidth.')
find('melazab/AD5940-BIOZ','gui/main.py','self.record_writer.writerow(self.RECORD_HEADER)','recording','GUI CSV streams to file independently of bounded plot buffers; no transport integrity test claimed.')
find('oscaroflores/UPRM-Multi_Frq-BioZ-Research','src/bioZ.c','void setFreq','frequency scope','Two frequency selections documented, approximately 4 kHz and 131 kHz.')
find('oscaroflores/UPRM-Multi_Frq-BioZ-Research','main.c','samples_discarded == 7','settling','Seven samples discarded between accepted outputs; adequacy not characterized here.')
find('oscaroflores/UPRM-Multi_Frq-BioZ-Research','src/bioZ.c','datsSendData(AppConnIsOpen()','bounds and data path','BLE send precedes snprintf-length validation; review bounded error behavior, no exploitation/hardware failure established.')
find('dyarleniber/AD5933-arduino-bioimpedance','AD5933.ino','FFM = TBW / 0.73','physiological assumption','Fixed hydration conversion; formula validity is separate from electrical validity.')
find('dyarleniber/AD5933-arduino-bioimpedance','AD5933.ino','FM = abs(FM)','invalid outputs','Absolute values can hide impossible negative physiological estimates.')
find('oliexdev/openScale','android_app/app/src/main/java/com/health/openscale/core/bluetooth/scales/CustomOpenScaleHandler.kt',"'F' ->",'record lifecycle','Custom handler clears instrument EEPROM on completion message; bridge must preserve independent raw archive.')
find('oliexdev/openScale','android_app/app/src/main/java/com/health/openscale/core/bluetooth/scales/CustomOpenScaleHandler.kt','idx,year,month','consumer schema','Legacy custom payload contains consumer metrics, not a complete raw BioZ spectrum/calibration schema.')
find('oliexdev/openScale','android_app/app/build.gradle.kts','compileSdk = 37','build requirements','Inspected app uses SDK 37; min SDK31 and Java21 also specified.')
find('eayrenk/bioscale-okok-alternative','calculations/body_composition.py','No published validated formula exists','physiological claim','Visceral-fat implementation describes itself as empirical/unvalidated; not direct imaging.')
find('eayrenk/bioscale-okok-alternative','calculations/body_composition.py','Results ±0.3 kg vs DEXA','physiological claim','Bone helper contains numerical accuracy assertion without a device-level validation established in this investigation.')
find('eayrenk/bioscale-okok-alternative','tests/test_calculations.py',"get_classifications(metrics, 'M', 35)",'test/API mismatch','Upstream call misses current height_cm argument; reproduced as one failure among five tests.','source + upstream test execution')
find('TAMU-ESP/BioZPulse-Sim-Platform','v2.0/spice_netlist_3d_run_fn.m','while status~=0','simulation execution','External simulator retry loop requires bounds/environment checks before unattended use.')
find('Protocentral/protocentral_openview','README.md','# OpenView 3','stale documentation correction','Current OpenView is Flutter-based, not the old Processing viewer referenced by hardware README.')
find('Protocentral/protocentral_openview','docs/ARCHITECTURE.md','There is currently only one test','documentation drift','Architecture document says one test, but collected tree contains additional test files; do not infer test coverage from this sentence.')
(R/'research/technical-findings.json').write_text(json.dumps(findings,indent=2))
with (R/'research/technical-findings.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(findings[0]));w.writeheader();w.writerows(findings)
comparisons=[('1210R',50000,1210,1195.33),('1210R',100000,1210,1182.77),('511R',50000,511,500.17),('511R',100000,511,507.88),('249R',50000,249,242.70),('249R',100000,249,245.81),('2R1C',50000,208.87,213.80),('2R1C',100000,165.56,169.48)]
with (R/'research/thesis-table-recalculation.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['load','frequency_Hz','reported_theoretical_ohm','reported_measured_ohm','recomputed_signed_error_percent','note'])
 for name,hz,ref,val in comparisons:w.writerow([name,hz,ref,val,100*(val-ref)/ref,'Historical thesis table; not new physical measurements and not a calibrated uncertainty statement'])
# Keep separate run receipts for follow-ups executed directly from the shell.
for name,status,detail in [('impedance-py-layout-corrected-tests','pass','34 passed, 1 deselected; upstream repository-name alias supplied, no upstream code edited'),('pyimpspec-upstream-unittest-selected','pass','139 tests passed using upstream runner style; four modules only')]:
 p=V/(name+'.log');(V/(name+'.json')).write_text(json.dumps({'name':name,'status':status,'detail':detail,'log':p.name,'log_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))
# Hash freshly built third-party artifacts without distributing flash images.
paths=json.loads((R/'verification-source-paths.json').read_text());p=pathlib.Path(paths['melazab/AD5940-BIOZ']);art=[]
for f in p.rglob('*.elf'):art.append({'program':f.parent.name,'file':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(V/'gnu-built-artifacts.json').write_text(json.dumps(art,indent=2))
print('catalog snapshots',len(rows),'findings',len(findings),'source files',sum(len(d['source_files']) for d in data),'families',len(set(x['family'] for x in rows)))
