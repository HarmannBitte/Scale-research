from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests, json, hashlib
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent/'web-evidence';ROOT.mkdir(exist_ok=True)
URLS={
 'iscd-positions':'https://iscd.org/official-positions-2023/',
 'iscd-precision':'https://iscd.org/resources/precision-assessment-calculator-faqs/',
 'nhanes-imputation':'https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx',
 'nhanes-bix-1999':'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/1999/DataFiles/BIX.htm',
 'nhanes-dxx-2017':'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DXX_J.htm',
 'bodym-registry':'https://registry.opendata.aws/bodym/',
 'styku-pricing':'https://help.styku.com/what-are-styku-s-business-pricing-plans/',
 'bodymetrix-faq':'https://bodymetrix.com/pages/faqs',
 'bodycomposition-models-638d8e2':'https://raw.githubusercontent.com/fohofmann/BodyComposition/638d8e28dcb80aba25233569a1c4786b51221ea4/docs/models.md',
 'bodycomposition-readme-638d8e2':'https://raw.githubusercontent.com/fohofmann/BodyComposition/638d8e28dcb80aba25233569a1c4786b51221ea4/README.md',
 'totalsegmentator-readme':'https://raw.githubusercontent.com/wasserth/TotalSegmentator/master/README.md',
 'clarius-cast-readme':'https://raw.githubusercontent.com/clariusdev/cast/master/README.md',
 'deepacsa-zenodo-code':'https://zenodo.org/api/records/19130694',
 'deepacsa-zenodo-assets':'https://zenodo.org/api/records/7568384',
}
def save(x):
 key,url=x
 try:
  r=requests.get(url,timeout=35);r.raise_for_status()
  if 'text/html' in r.headers.get('content-type',''):
   soup=BeautifulSoup(r.content,'html.parser')
   for n in soup(['script','style','nav']):n.decompose()
   text=soup.get_text('\n',strip=True)
  else:text=r.text
  path=ROOT/(key+'.txt');path.write_text(text)
  return {'name':key,'url':url,'final_url':r.url,'access_date':'2026-10-17','status':r.status_code,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'file':path.name}
 except Exception as e:return {'name':key,'url':url,'error':str(e)}
rows=list(ThreadPoolExecutor(max_workers=6).map(save,URLS.items()))
(ROOT/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
