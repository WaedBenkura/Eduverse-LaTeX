from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader
base=Path('tmp/audit-20260923/visual-audit')
r=PdfReader('tmp/audit-20260923/baseline-main.pdf')
lines=[]
for i,p in enumerate(r.pages):
 text=p.extract_text(extraction_mode='layout') or ''
 lines.append(f'\n\n=== Physical {i+1} printed {i-11} ===\n{text}')
(base/'baseline-text.txt').write_text(''.join(lines), encoding='utf-8')
for offset in range(32,138,12):
 pages=list(range(offset,min(138,offset+12)))
 w,h=380,566
 canvas=Image.new('RGB',(w*4,h*3),(215,215,215))
 d=ImageDraw.Draw(canvas)
 for idx,n in enumerate(pages):
  f=base/f'baseline-{n:03d}.png'
  if not f.exists():
   continue
  im=Image.open(f).convert('RGB')
  im.thumbnail((w-12,h-28))
  x=(idx%4)*w+(w-im.width)//2
  y=(idx//4)*h+24
  canvas.paste(im,(x,y))
  d.text(((idx%4)*w+8,(idx//4)*h+5),f'Printed p{n-12} | PDF {n}',fill='black')
 canvas.save(base/f'contact-{offset-12:03d}-{pages[-1]-12:03d}.png')
print('text pages',len(r.pages))
