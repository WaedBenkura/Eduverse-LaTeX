from pathlib import Path
import hashlib, json, subprocess, re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
head_pdf = OUT / 'git-head-main.pdf'
if not head_pdf.exists():
    head_pdf.write_bytes(subprocess.check_output(['git', 'show', 'HEAD:main.pdf'], cwd=ROOT))
head_ch3 = subprocess.check_output(['git','show','HEAD:chapters/chapter3_methodology.tex'],cwd=ROOT).decode('utf-8')
(OUT / 'git-head-chapter3.tex').write_text(head_ch3,encoding='utf-8')
paths = {
    'pre-audit-main': ROOT/'tmp/audit-20260923/baseline-main.pdf',
    'git-head': head_pdf,
    'build': ROOT/'build/main.pdf',
    'output': ROOT/'output/pdf/main.pdf',
    'thesischeck': ROOT/'thesischeck.pdf',
    'thesisfinalcheck': ROOT/'thesisfinalcheck.pdf',
    'thesisfinalcheck2': ROOT/'thesisfinalcheck2.pdf',
}
if '--current' in __import__('sys').argv:
    paths['current'] = ROOT/'main.pdf'
summaries={}
for name,path in paths.items():
    pdf=PdfReader(path)
    labels=pdf.page_labels
    destinations={}
    for key,dest in pdf.named_destinations.items():
        idx=pdf.get_destination_page_number(dest)
        if idx is not None:
            destinations[key]={'physical_page':idx+1,'page_label':labels[idx]}
    start=pdf.get_destination_page_number(pdf.named_destinations['chapter.3']) if 'chapter.3' in pdf.named_destinations else None
    end=pdf.get_destination_page_number(pdf.named_destinations['chapter.4']) if 'chapter.4' in pdf.named_destinations else None
    chapter3_pages=[]
    if start is not None and end is not None:
        for idx in range(start,end):
            chapter3_pages.append({'physical_page':idx+1,'page_label':labels[idx],'text':pdf.pages[idx].extract_text()})
    summaries[name]={'path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'metadata':{str(k):str(v) for k,v in pdf.metadata.items()},'page_count':len(pdf.pages),'page_labels':labels,'destinations':destinations,'chapter3_pages':chapter3_pages}
    (OUT/f'{name}-chapter3.txt').write_text('\n\n'.join(f"--- Physical page {p['physical_page']}, thesis page {p['page_label']} ---\n{p['text']}" for p in chapter3_pages), encoding='utf-8')
    print(name,len(pdf.pages),pdf.metadata.get('/CreationDate'),summaries[name]['sha256'][:12], flush=True)
(OUT/'baselines.json').write_text(json.dumps(summaries,indent=2,ensure_ascii=False),encoding='utf-8')
comparisons={}
target='current' if 'current' in summaries else 'pre-audit-main'
current=summaries[target]['destinations']
for name,summary in summaries.items():
    if name==target: continue
    dest=summary['destinations']
    differences=[]
    for key,val in current.items():
        if not re.match(r'(chapter|section|subsection|figure|table)\.',key): continue
        if key not in dest:
            differences.append({'destination':key,'old':None,'new':val['page_label']})
        elif dest[key]['page_label']!=val['page_label']:
            differences.append({'destination':key,'old':dest[key]['page_label'],'new':val['page_label']})
    removed=[key for key in dest if re.match(r'(chapter|section|subsection|figure|table)\.',key) and key not in current]
    comparisons[name]={'changed_destinations':differences,'removed_destinations':removed}
(OUT/'baseline-comparisons.json').write_text(json.dumps(comparisons,indent=2,ensure_ascii=False),encoding='utf-8')
for name,data in comparisons.items():
    print(name,':',len(data['changed_destinations']),'changes;',len(data['removed_destinations']),'removed')
    if name in ['git-head','pre-audit-main']: print(json.dumps(data,indent=2))
