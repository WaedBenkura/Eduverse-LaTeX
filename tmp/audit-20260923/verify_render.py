from pathlib import Path
import hashlib,json
import pypdfium2 as pdfium
from pypdf import PdfReader
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'final-visual'
OUT.mkdir(exist_ok=True)
old_path=ROOT/'tmp/audit-20260923/baseline-main.pdf'
new_path=ROOT/'main.pdf'
old_reader=PdfReader(old_path);new_reader=PdfReader(new_path)
old=pdfium.PdfDocument(old_path);new=pdfium.PdfDocument(new_path)
rows=[]
for i in range(len(new)):
    a=old[i].render(scale=1).to_pil().convert('RGB')
    b=new[i].render(scale=1).to_pil().convert('RGB')
    changed=a.size!=b.size or a.tobytes()!=b.tobytes()
    old_text=old_reader.pages[i].extract_text() or ''
    new_text=new_reader.pages[i].extract_text() or ''
    row={'physical_page':i+1,'printed_page':new_reader.page_labels[i], 'pixels_identical':not changed,'text_identical':old_text==new_text,
         'render_sha256':hashlib.sha256(b.tobytes()).hexdigest()}
    rows.append(row)
    b.save(OUT/f'page-{i+1:03}.png')
    if (i+1)%25==0:print(f'Compared {i+1}/{len(new)} rendered pages',flush=True)
old.close();new.close()
for start in range(1,138,4):
    canvas=Image.new('RGB',(1264,1650),'#dddddd');draw=ImageDraw.Draw(canvas)
    for j,n in enumerate(range(start,min(start+4,138))):
        im=Image.open(OUT/f'page-{n:03}.png')
        x=(j%2)*632+10;y=(j//2)*825+28
        canvas.paste(im,(x,y))
        label='Cover' if n==1 else new_reader.page_labels[n-1]
        draw.text((x,y-20),f'Printed: {label} | PDF page: {n}',fill='black')
    canvas.save(OUT/f'contact-{start:03}-{min(start+3,137):03}.png')
result={'pages':len(new_reader.pages),'pixel_changed_pages':[r for r in rows if not r['pixels_identical']],
        'text_changed_pages':[r for r in rows if not r['text_identical']],'pages_detail':rows}
(OUT/'render-verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='pages_detail'},indent=2),flush=True)
