from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
BIN = Path(r'C:\Users\HP\AppData\Local\Programs\MiKTeX\miktex\bin\x64')
OUTPUT = AUDIT / 'build-evidence-staged'
OUTPUT.mkdir(parents=True, exist_ok=True)
BUILD = AUDIT / 'staged-build'
BUILD.mkdir(parents=True, exist_ok=True)
for folder in ('chapters', 'frontmatter', 'backmatter'):
    (BUILD / folder).mkdir(exist_ok=True)
for source in (ROOT/'main.tex', ROOT/'references.bib'):
    shutil.copy2(source, BUILD/source.name)
for folder in ('chapters', 'frontmatter', 'backmatter', 'figures'):
    for source in (ROOT/folder).rglob('*'):
        if source.is_file() and source.suffix.lower() not in ('.aux','.log','.toc','.lof','.lot','.out'):
            target=BUILD/source.relative_to(ROOT)
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,target)
# Shadow root auxiliaries on the initial isolated build so it starts clean.
if not (BUILD / 'main.aux').exists():
    for ext in ('aux','toc','lof','lot','out','bbl'):
        (BUILD / ('main.'+ext)).write_text('')
    for folder in ('chapters','frontmatter','backmatter'):
        for source in (ROOT/folder).glob('*.tex'):
            (BUILD/folder/source.with_suffix('.aux').name).write_text('')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def state():
    paths = [BUILD / ('main.' + ext) for ext in ('aux','toc','lof','lot','out','bbl')]
    for folder in ('chapters','frontmatter','backmatter'):
        paths.extend((BUILD / folder).glob('*.aux'))
    return {str(p.relative_to(BUILD)): digest(p) for p in paths if p.exists()}

sources = list(ROOT.glob('*.tex')) + list(ROOT.glob('*.bib'))
for folder in ('chapters','frontmatter','backmatter','figures'):
    sources.extend((ROOT / folder).rglob('*.tex'))
(OUTPUT / 'source-hashes-before.json').write_text(json.dumps({str(p.relative_to(ROOT)):digest(p) for p in sources}, indent=2))

if '--clean' in sys.argv:
    backup = OUTPUT / 'generated-before-clean'
    generated = [ROOT / ('main.' + ext) for ext in ('aux','toc','lof','lot','out','bbl','blg','fls','fdb_latexmk','synctex.gz')]
    for folder in ('chapters','frontmatter','backmatter'):
        generated.extend((ROOT / folder).glob('*.aux'))
    for path in generated:
        if path.is_file():
            relative = path.relative_to(ROOT)
            target = backup / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            path.unlink()
    print('Backed up and removed only allowlisted generated LaTeX files.', flush=True)

records = []
def run(tool, args, tag):
    started = time.monotonic()
    with (OUTPUT / (tag + '.stdout.txt')).open('wb') as output:
        process = subprocess.run([str(BIN / (tool+'.exe')), *args], cwd=BUILD, stdout=output, stderr=subprocess.STDOUT)
    record = {'step':tag,'returncode':process.returncode,'seconds':round(time.monotonic()-started,2),'state':state()}
    records.append(record)
    (OUTPUT/'passes.json').write_text(json.dumps(records,indent=2))
    print(f'{tag}: exit {process.returncode}, {record["seconds"]} seconds', flush=True)
    if process.returncode:
        print((OUTPUT / (tag+'.stdout.txt')).read_text(errors='replace')[-6000:])
        raise SystemExit(process.returncode)
    if tool == 'pdflatex':
        shutil.copy2(BUILD/'main.log',OUTPUT/(tag+'.log'))
    return record['state']

args = ['-interaction=nonstopmode','-halt-on-error','-synctex=1','-recorder','main.tex']
run('pdflatex',args,'latex-pass-1')
run('bibtex',['main'],'bibtex')
previous = None
stable = False
for n in range(2,9):
    current = run('pdflatex',args,f'latex-pass-{n}')
    log = (BUILD/'main.log').read_text(errors='replace')
    warnings = [s for s in ('Rerun to get cross-references right','There were undefined references','There were undefined citations','multiply defined','Rerun to get outlines right','Table widths have changed') if s in log]
    if n >= 4 and current == previous and not warnings:
        stable = True
        break
    previous = current
if not stable:
    raise SystemExit('No stable reference state after eight LaTeX passes.')
(OUTPUT/'source-hashes-after.json').write_text(json.dumps({str(p.relative_to(ROOT)):digest(p) for p in sources},indent=2))
print(f'Build stable after {n} LaTeX passes and BibTeX. PDF SHA256 {digest(BUILD/"main.pdf")}',flush=True)
generated=[BUILD/('main.'+ext) for ext in ('pdf','aux','log','toc','lof','lot','out','bbl','blg','fls','synctex.gz')]
for folder in ('chapters','frontmatter','backmatter'):
    generated.extend((BUILD/folder).glob('*.aux'))
for path in generated:
    if path.is_file():
        destination = ROOT/path.relative_to(BUILD)
        shutil.copy2(path,destination)
print('Copied verified PDF and refreshed generated build files to project root.',flush=True)
