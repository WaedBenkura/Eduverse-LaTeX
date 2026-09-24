from pathlib import Path
import re, json, collections, sys

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
AUXROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT

def clean(s):
    return re.sub(r'(?<!\\)%[^\n]*', '', s)

def group(s,i):
    while i<len(s) and s[i].isspace(): i+=1
    assert s[i]=='{', (s[i:i+60],i)
    start=i+1; depth=1; i+=1
    while depth:
        if s[i]=='{' and (i==0 or s[i-1]!='\\'): depth+=1
        elif s[i]=='}' and (i==0 or s[i-1]!='\\'): depth-=1
        i+=1
    return s[start:i-1], i

def commands(s,name,n=1):
    out=[]
    for m in re.finditer(r'\\'+name+r'(?![a-zA-Z])\s*',s):
        try:
            args=[]; end=m.end()
            for _ in range(n):
                a,end=group(s,end); args.append(a)
            out.append((m.start(),args,end))
        except (AssertionError,IndexError): pass
    return out

def lineno(s,pos):return s[:pos].count('\n')+1
def norm(s):
    s=re.sub(r'(\\[A-Za-z]+)\s+(?=\{)',r'\1',s)
    return re.sub(r'\s+', ' ',s).strip()
def no_defs(s):
    # Preserve newlines and offsets so source locations remain meaningful.
    for pos,args,end in reversed(commands(s,'newcommand')):
        p=end
        while p<len(s) and s[p].isspace():p+=1
        if p<len(s) and s[p]=='[':p=s.index(']',p)+1
        try: _,end=group(s,p)
        except (AssertionError,IndexError):continue
        s=s[:pos]+re.sub(r'[^\n]',' ',s[pos:end])+s[end:]
    return s

files=[]
def discover(rel):
    if not rel.endswith('.tex'): rel+='.tex'
    if rel in files:return
    files.append(rel)
    s=clean((ROOT/rel).read_text(encoding='utf8'))
    for _,args,_ in commands(s,'(?:input|include)'):
        discover(args[0])
discover('main.tex')
texts={f:clean((ROOT/f).read_text(encoding='utf8')) for f in files}
active={f:no_defs(s) for f,s in texts.items()}

auxfiles=[]
def auxread(rel):
    auxfiles.append(rel)
    s=(AUXROOT/rel).read_text(encoding='utf8')
    for _,a,_ in commands(s,'@input'):
        auxread(a[0])
auxread('main.aux')
labels={}; dupaux=[]
for f in auxfiles:
    s=(AUXROOT/f).read_text(encoding='utf8')
    for _,a,_ in commands(s,'newlabel',2):
        parts=[]; p=0
        while p<len(a[1]):
            b,p=group(a[1],p);parts.append(b)
        if a[0] in labels:dupaux.append(a[0])
        labels[a[0]]={'number':parts[0],'page':parts[1],'title':parts[2],'anchor':parts[3],'aux':f}

source_labels=[]; refs=[]; cites=[]; headings=[]; figures=[]; tables=[]; openings=[]
for f,s in active.items():
    source_labels.extend({'key':a[0],'file':f,'line':lineno(s,p)} for p,a,_ in commands(s,'label'))
    refs.extend({'key':k.strip(),'command':s[p:s.index('{',p)].strip(),'file':f,'line':lineno(s,p)} for p,a,_ in commands(s,r'(?:ref\*?|pageref\*?|autoref\*?|nameref\*?|eqref|cref|Cref|chaptercontentsitem)') for k in a[0].split(','))
    cites.extend({'key':k.strip(),'file':f,'line':lineno(s,p)} for p,a,_ in commands(s,'cite[a-zA-Z]*') for k in a[0].split(','))
    if f.startswith('chapters/'):
        ch=int(re.search(r'chapter(\d+)',f)[1]); sec=0; sub=0
        wrap=commands(s,'chapterwithopening(?:inline)?',3)[0]
        source_labels.append({'key':wrap[1][1],'file':f,'line':lineno(s,wrap[0])})
        headings.append({'kind':'chapter','number':str(ch),'title':wrap[1][0],'file':f,'line':lineno(s,wrap[0]),'key':wrap[1][1]})
        items=[a[0] for _,a,_ in commands(wrap[1][2],'chaptercontentsitem')]
        sectionkeys=[]
        for p,a,end in commands(s,r'(?:section|subsection|subsubsection)\*?'):
            cmd=s[p:s.index('{',p)].strip().lstrip('\\')
            if cmd.endswith('*'):continue
            if cmd=='section':sec+=1;sub=0;num=f'{ch}.{sec}'
            elif cmd=='subsection':sub+=1;num=f'{ch}.{sec}.{sub}'
            else:raise ValueError(cmd)
            m=re.match(r'\s*\\label\{([^}]+)\}',s[end:])
            key=m[1] if m else None
            if cmd=='section':sectionkeys.append(key)
            headings.append({'kind':cmd,'number':num,'title':norm(a[0]),'file':f,'line':lineno(s,p),'key':key})
        openings.append({'chapter':ch,'title':wrap[1][0],'file':f,'items':items,'sectionkeys':sectionkeys,'matches':items==sectionkeys,'resolved':[dict(key=k,**labels.get(k,{})) for k in items]})
        for p,a,_ in commands(s,'(?:EduUseCasePdfFigure|EduUiFigure|EduActivityFigure(?:Readable|Tall|Compact)?)',3):
            figures.append({'caption':norm(a[1]),'key':a[2],'file':f,'line':lineno(s,p)})
            source_labels.append({'key':a[2],'file':f,'line':lineno(s,p)})
        for p,a,_ in commands(s,'EduSchemaTableStart'):
            tables.append({'caption':r'Schema for Table: \db{'+a[0]+'}','file':f,'line':lineno(s,p)})
        # Explicit floats and longtables are bounded by their end marker.
        for m in re.finditer(r'\\begin\{(figure|table|longtable)\}',s):
            end=s.index('\\end{'+m[1]+'}',m.end())
            body=s[m.end():end]
            caps=commands(body,'caption'); labs=commands(body,'label')
            if not caps:continue
            item={'caption':norm(caps[0][1][0]),'key':labs[0][1][0] if labs else None,'file':f,'line':lineno(s,m.start())}
            (figures if m[1]=='figure' else tables).append(item)

sourcekeys=[x['key'] for x in source_labels]
undefinedrefs=[r for r in refs if r['key'] not in labels]
bib=(ROOT/'references.bib').read_text(encoding='utf8')
bibkeys=re.findall(r'@\w+\s*\{\s*([^,]+),',bib)
undefinedcites=[c for c in cites if c['key'] not in bibkeys]
labelissues=[]
for h in headings:
    if not h['key']:continue
    actual=labels.get(h['key'])
    if not actual or norm(actual['title'])!=h['title'] or actual['number']!=h['number']:
        labelissues.append({'heading':h,'actual':actual})
for fig in figures:
    actual=labels.get(fig['key'])
    # nameref/gettitlestring drops a final period from its auxiliary title.
    # The actual caption and LOF retain the period and are compared exactly.
    if not actual or norm(actual['title']).rstrip('.')!=fig['caption'].rstrip('.') or not actual['anchor'].startswith('figure.'):
        labelissues.append({'figure':fig,'actual':actual})
for tab in tables:
    if not tab.get('key'):continue
    actual=labels.get(tab['key'])
    if not actual or norm(actual['title']).rstrip('.')!=tab['caption'].rstrip('.') or not actual['anchor'].startswith(('table.','table.')):
        labelissues.append({'table':tab,'actual':actual})

toc=(AUXROOT/'main.toc').read_text(encoding='utf8')
tocentries=[]
for _,a,_ in commands(toc,'contentsline',4):
    nums=commands(a[1],'numberline')
    if nums: num=nums[0][1][0];title=a[1][nums[0][2]:]
    else:num='';title=a[1]
    tocentries.append({'kind':a[0],'number':num,'title':norm(title),'page':a[2],'anchor':a[3]})
source_toc=[{k:h[k] for k in ('kind','number','title')} for h in headings]
compiled_toc=[{k:h[k] for k in ('kind','number','title')} for h in tocentries if h['number']]

lists={}
for extension,expected in [('lof',figures),('lot',tables)]:
    entries=[]
    for _,a,_ in commands((AUXROOT/f'main.{extension}').read_text(encoding='utf8'),'contentsline',4):
        nums=commands(a[1],'numberline')[0]
        cap=a[1][nums[2]:].strip()
        if cap.startswith('{'):cap,_=group(cap,0)
        cap=norm(cap.replace('\\ignorespaces',''))
        entries.append({'number':nums[1][0],'caption':cap,'page':a[2],'anchor':a[3]})
    expected=sorted(expected,key=lambda x:(x['file'],x['line']))
    # Files are numbered so lexical order follows document order.
    sequence_issues=[]; label_list_issues=[]; per_chapter=collections.Counter()
    for source,entry in zip(expected,entries):
        ch=re.search(r'chapter(\d+)',source['file'])[1]
        per_chapter[ch]+=1
        wanted=f'{ch}.{per_chapter[ch]}'
        if entry['number']!=wanted:
            sequence_issues.append({'entry':entry,'expected_number':wanted})
        if source.get('key'):
            label=labels.get(source['key'])
            if not label or label['number']!=entry['number'] or label['page']!=entry['page'] or label['anchor']!=entry['anchor']:
                label_list_issues.append({'source':source,'entry':entry,'label':label})
    lists[extension]={'source_count':len(expected),'compiled_count':len(entries),'captions_match':[x['caption'] for x in expected]==[x['caption'] for x in entries],'sequence_issues':sequence_issues,'label_list_issues':label_list_issues,'entries':entries,'source':expected}

paragraphs=[]
for f,s in active.items():
    for m in re.finditer(r'(?:^|\n\s*\n)([^\n].*?)(?=\n\s*\n|\Z)',s,re.S):
        para=norm(m[1])
        if len(para)>140 and not para.startswith('\\') and not '\\EduSchema' in para and not '&' in para:
            paragraphs.append({'text':para,'file':f,'line':lineno(s,m.start())})
counts=collections.Counter(p['text'] for p in paragraphs)
duplicates=[p for p in paragraphs if counts[p['text']]>1]
result={'active_files':files,'aux_files':auxfiles,'counts':{'active_source_files':len(files),'source_labels':len(source_labels),'aux_labels':len(labels),'reference_commands':len(refs),'unique_reference_targets':len(set(r['key'] for r in refs)),'citation_uses':len(cites),'unique_citations':len(set(c['key'] for c in cites)),'bib_keys':len(bibkeys),'numbered_headings':len(headings),'toc_entries':len(tocentries),'chapter_opening_items':sum(len(x['items']) for x in openings),'paragraphs_screened':len(paragraphs)},'openings':openings,'source_aux_label_key_match':set(sourcekeys)==set(labels),'missing_source_labels':list(set(labels)-set(sourcekeys)),'missing_aux_labels':list(set(sourcekeys)-set(labels)),'duplicate_source_labels':[k for k,v in collections.Counter(sourcekeys).items() if v>1],'duplicate_aux_labels':dupaux,'unsafe_label_names':[k for k in sourcekeys if not re.fullmatch(r'[A-Za-z0-9:_.-]+',k)],'unused_unnumbered_label_numeric_values':[dict(key=k,**v) for k,v in labels.items() if '*' in v['anchor'] and v['number'] and k not in set(r['key'] for r in refs)],'undefined_references':undefinedrefs,'undefined_citations':undefinedcites,'label_attachment_issues':labelissues,'numbered_toc_matches_source':source_toc==compiled_toc,'source_toc':source_toc,'compiled_toc':compiled_toc,'toc':tocentries,'lists':lists,'duplicate_paragraphs':duplicates,'source_labels':source_labels,'references':refs,'unused_labels':[k for k in labels if k not in set(r['key'] for r in refs)]}
(OUT/'source-audit.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in result.items() if k not in ('source_toc','compiled_toc','toc','lists','source_labels','references','unused_labels','openings')},indent=2))
print(json.dumps([{k:v for k,v in x.items() if k!='resolved'} for x in openings],indent=2))
print(json.dumps({k:{kk:vv for kk,vv in v.items() if kk not in ('entries','source')} for k,v in lists.items()},indent=2))
