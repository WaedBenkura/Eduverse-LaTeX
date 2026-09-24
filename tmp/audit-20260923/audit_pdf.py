from pathlib import Path
import collections
import csv
import json
import re
import sys
import unicodedata
import pdfplumber
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PDF = ROOT/'main.pdf'

def group(text, pos):
    while pos < len(text) and text[pos].isspace(): pos += 1
    assert text[pos] == '{', text[pos:pos+60]
    start = pos+1; depth=1; pos+=1
    while depth:
        if text[pos]=='{' and text[pos-1]!='\\': depth+=1
        elif text[pos]=='}' and text[pos-1]!='\\': depth-=1
        pos+=1
    return text[start:pos-1], pos

def groups(text):
    pos=0; result=[]
    while pos<len(text):
        if text[pos:].strip()=='':break
        part,pos=group(text,pos); result.append(part)
    return result

def commands(text, name, argc):
    for match in re.finditer(r'\\'+name+r'(?![A-Za-z])\s*',text):
        pos=match.end(); args=[]
        try:
            for _ in range(argc):
                arg,pos=group(text,pos);args.append(arg)
            yield args
        except (AssertionError,IndexError): pass

def plain(text):
    text=re.sub(r'\\(?:ignorespaces|protect)\s*','',text)
    text=re.sub(r'\\(?:db|texttt|textbf|emph|textit|textrm|textnormal)\s*\{([^{}]*)\}',r'\1',text)
    text=text.replace('\\&','&').replace('\\_','_').replace('~',' ')
    return re.sub(r'\s+',' ',text.replace('{','').replace('}','')).strip()

def canon(text):
    text=unicodedata.normalize('NFKD',text)
    return ''.join(c for c in text if c.isalnum())

def read_index(ext):
    rows=[]
    for kind,raw,page,anchor in commands((ROOT/f'main.{ext}').read_text(encoding='utf-8'),'contentsline',4):
        match=re.match(r'\\numberline\s*',raw)
        number=''
        if match:
            number,pos=group(raw,match.end());raw=raw[pos:]
        rows.append({'list':ext,'kind':kind,'number':number,'title':plain(raw),'page':page,'anchor':anchor})
    return rows

reader=PdfReader(PDF)
destinations=reader.named_destinations
page_labels=reader.page_labels
anchor_pages={name:reader.get_destination_page_number(dest) for name,dest in destinations.items()}
pages=[]
if '--cached' in sys.argv:
    # Only use when the caller has verified that main.pdf is unchanged since extraction.
    pages=json.loads((OUT/'pdf-pages.json').read_text(encoding='utf-8'))
else:
    print('Extracting every PDF page and printed page number...',flush=True)
    with pdfplumber.open(PDF) as pdf:
        for i,page in enumerate(pdf.pages):
            words=page.extract_words()
            text=page.extract_text() or ''
            # Fancyhdr main-matter page numbers are upper-right; plain style is centered below the text.
            upper=[w['text'] for w in words if w['top']<115 and w['x0']>465 and re.fullmatch(r'\d+|[ivxlcdm]+',w['text'])]
            lower=[w['text'] for w in words if w['top']>685 and 280<w['x0']<325 and re.fullmatch(r'\d+|[ivxlcdm]+',w['text'])]
            printed=(upper+lower)
            pages.append({'physical_page':i+1,'pdf_page_label':page_labels[i],'printed_candidates':printed,'text':text,
                          'words':words,'width':page.width,'height':page.height})
            page.close()
            if (i+1)%20==0:print(f'Extracted {i+1}/{len(pdf.pages)}',flush=True)
    (OUT/'pdf-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')

issues=[]
def issue(kind,**details):issues.append(dict(kind=kind,**details))

for i,page in enumerate(pages):
    if i==0:
        if page['printed_candidates']:issue('unexpected_cover_number',page=1)
        continue
    if page['printed_candidates']!=[page['pdf_page_label']]:
        issue('printed_page_mismatch',physical_page=i+1,printed=page['printed_candidates'],metadata=page['pdf_page_label'])
    if '??' in page['text']:issue('visible_question_marks',physical_page=i+1,page=page['pdf_page_label'])
    if not page['text'].strip():issue('empty_page',physical_page=i+1)

entries=sum([read_index(ext) for ext in ('toc','lof','lot')],[])
index_ranges={'toc':range(3,7),'lof':range(7,10),'lot':range(10,12)}
index_texts={ext:canon(' '.join(pages[i]['text'] for i in indices)) for ext,indices in index_ranges.items()}

for entry in entries:
    anchor=entry['anchor']; page_index=anchor_pages.get(anchor)
    if page_index is None:
        issue('missing_destination',entry=entry);continue
    entry['physical_page']=page_index+1
    entry['actual_printed_page']=pages[page_index]['pdf_page_label']
    entry['destination_page_matches']=entry['page']==entry['actual_printed_page']
    if not entry['destination_page_matches']:issue('wrong_index_page',entry=entry)
    expected=canon(entry['title'])
    actual=canon(pages[page_index]['text'])
    entry['heading_or_caption_present']=expected in actual
    if not entry['heading_or_caption_present']:issue('title_not_found_on_destination',entry=entry)
    if entry['kind'] in ('figure','table'):
        full=canon(entry['kind'].capitalize()+' '+entry['number']+' '+entry['title'])
        entry['numbered_caption_present']=full in actual
        if not entry['numbered_caption_present']:issue('caption_number_mismatch',entry=entry)
    elif entry['number'] and entry['kind']!='chapter':
        entry['numbered_heading_present']=canon(entry['number']+' '+entry['title']) in actual
        if not entry['numbered_heading_present']:issue('heading_number_mismatch',entry=entry)
    indexed=canon(entry['number']+entry['title']+entry['page'])
    entry['visible_index_row_present']=indexed in index_texts[entry['list']]
    if not entry['visible_index_row_present']:issue('visible_index_row_not_found',entry=entry)

for ext in ('toc','lof','lot'):
    rows=[e for e in entries if e['list']==ext]
    anchors=[e['anchor'] for e in rows]
    if len(anchors)!=len(set(anchors)):issue('duplicate_index_anchor',list=ext)
    numeric=[e for e in rows if e['number']]
    if [e['physical_page'] for e in rows]!=sorted(e['physical_page'] for e in rows):issue('index_page_order',list=ext)
    if len({(e['kind'],e['number']) for e in numeric})!=len(numeric):issue('duplicate_index_number',list=ext)
    if ext in ('lof','lot'):
        counters=collections.defaultdict(int)
        for entry in numeric:
            chapter,number=map(int,entry['number'].split('.'));counters[chapter]+=1
            if number!=counters[chapter]:issue('nonsequential_float_number',entry=entry)

labels={}
for path in [ROOT/'main.aux', *sum([list((ROOT/folder).glob('*.aux')) for folder in ('frontmatter','chapters','backmatter')],[])]:
    for name,values in commands(path.read_text(encoding='utf-8'),'newlabel',2):
        parts=groups(values)
        if name in labels:issue('duplicate_aux_label',label=name)
        labels[name]=dict(number=parts[0],page=parts[1],title=plain(parts[2]),anchor=parts[3])

label_checks=[]
for name,value in labels.items():
    target=anchor_pages.get(value['anchor'])
    row={'key':name,**value,'destination_page':None if target is None else page_labels[target]}
    label_checks.append(row)
    if target is None:issue('label_missing_destination',label=row)
    elif value['page']!=page_labels[target]:issue('label_page_mismatch',label=row)
    matched=[e for e in entries if e['anchor']==value['anchor']]
    if matched:
        entry=matched[0]
        if value['number']!=entry['number']:issue('label_number_mismatch',label=row,index=entry)
        if canon(value['title'])!=canon(entry['title']):issue('label_title_mismatch',label=row,index=entry)

source=json.loads((OUT/'source-audit/source-audit.json').read_text(encoding='utf-8'))
opening_checks=[]
for opening in source['openings']:
    chapter=opening['chapter']; page_index=anchor_pages[f'chapter.{chapter}']
    text=pages[page_index]['text']
    for key in opening['items']:
        value=labels[key]
        ref=canon(value['number']+', p. '+value['page'])
        ref_present=ref in canon(text)
        title_words=plain(value['title']).split()
        # On a wrapping row, the right-hand number can occur between two lines of its title.
        pattern='.*?'.join(re.escape(canon(w)) for w in title_words)
        title_present=bool(re.search(pattern,canon(text)))
        row={'chapter':chapter,'opening_page':page_labels[page_index],'key':key,**value,'visible_reference':ref_present,'visible_title':title_present}
        opening_checks.append(row)
        if not ref_present or not title_present:issue('opening_visible_mismatch',item=row)

links=[]
for i,page in enumerate(reader.pages):
    for annotation in page.get('/Annots',[]):
        obj=annotation.get_object()
        action=obj.get('/A',{})
        if action.get('/S')!='/GoTo':continue
        destination=action.get('/D')
        if isinstance(destination,str):
            target=anchor_pages.get(destination)
            links.append({'from_physical_page':i+1,'anchor':destination,'target_physical_page':None if target is None else target+1})
            if target is None:issue('broken_internal_pdf_link',physical_page=i+1,anchor=destination)

# Locate actual captions independently on body pages, then compare their complete set to LOF/LOT.
found_captions=[]
for page in pages[12:]:
    for match in re.finditer(r'(?m)^\s*(Figure|Table)\s*(\d+\.\d+)\s*[.:]',page['text']):
        found_captions.append({'kind':match[1].lower(),'number':match[2],'page':page['pdf_page_label'],'physical_page':page['physical_page']})
for caption in found_captions:
    matches=[e for e in entries if e['kind']==caption['kind'] and e['number']==caption['number']]
    if not matches:issue('caption_missing_from_index',caption=caption)
for entry in [e for e in entries if e['list'] in ('lof','lot')]:
    found=[c for c in found_captions if c['kind']==entry['kind'] and c['number']==entry['number']]
    if not found:issue('indexed_caption_missing_in_body',entry=entry)
    # Continued longtables may repeat the caption on subsequent pages.
    elif found[0]['page']!=entry['page']:issue('caption_first_page_mismatch',entry=entry,actual=found)

log=(ROOT/'main.log').read_text(errors='replace')
warnings=[line for line in log.splitlines() if 'Warning' in line or line.startswith('!')]
reference_warning_terms=('undefined','multiply defined','Label(s) may have changed','Rerun','destination with the same')
reference_warnings=[line for line in log.splitlines() if not line.startswith('Package:') and any(term in line for term in reference_warning_terms)]
result={'pdf_pages':len(pages),'front_matter':'i-xi','main_matter':'1-125','entry_counts':dict(collections.Counter(e['list'] for e in entries)),
        'labels':len(labels),'chapter_opening_entries':len(opening_checks),'internal_pdf_links':len(links),
        'actual_caption_occurrences':len(found_captions),'issues':issues,'warnings':warnings,'reference_warnings':reference_warnings,
        'overfull_boxes':len(re.findall(r'^Overfull',log,re.M)),'underfull_boxes':len(re.findall(r'^Underfull',log,re.M)),
        'ignored_glue_shrinkage_diagnostics':len(re.findall(r'^ignored error: Infinite glue shrinkage',log,re.M)),
        'entries':entries,'label_checks':label_checks,'opening_checks':opening_checks,'links':links,'found_captions':found_captions}
(OUT/'pdf-audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
with (OUT/'index-verification.csv').open('w',newline='',encoding='utf-8-sig') as stream:
    fields=['list','kind','number','title','page','actual_printed_page','physical_page','anchor','destination_page_matches','heading_or_caption_present','visible_index_row_present']
    writer=csv.DictWriter(stream,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(entries)
print(json.dumps({key:value for key,value in result.items() if key not in ('entries','label_checks','opening_checks','links','found_captions')},indent=2))
