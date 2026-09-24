from pathlib import Path
from pypdf import PdfReader
import json,re,difflib
OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'baselines.json').read_text(encoding='utf-8'))
versions=['git-head','pre-audit-main']
pages={}
for version in versions:
    pdf=PdfReader(data[version]['path'])
    extracted=[page.extract_text() for page in pdf.pages]
    pages[version]=extracted
    (OUT/f'{version}-fulltext.json').write_text(json.dumps(extracted,ensure_ascii=False),encoding='utf-8')
    print('Extracted',version,flush=True)
diff=[]
changed=[]
for i,(old,new) in enumerate(zip(*[pages[v] for v in versions])):
    if re.sub(r'\s+','',old)!=re.sub(r'\s+','',new):
        changed.append({'physical_page':i+1,'thesis_page':data['pre-audit-main']['page_labels'][i]})
        diff.append('\n'.join(difflib.unified_diff(old.splitlines(),new.splitlines(),fromfile=f'HEAD page {i+1}',tofile=f'current page {i+1}',lineterm='')))
(OUT/'head-to-preaudit-text.diff').write_text('\n\n'.join(diff),encoding='utf-8')
(OUT/'head-to-preaudit-text-pages.json').write_text(json.dumps(changed,indent=2),encoding='utf-8')
print('Changed pages:',json.dumps(changed))
