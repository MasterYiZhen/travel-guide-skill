from reportlab.pdfgen import canvas
from pathlib import Path
import json, hashlib
r=Path('/private/tmp/travel-guide-rc8-delivery')
for version in (1,2):
 c=canvas.Canvas(str(r/f'candidate-v{version}.pdf'),pagesize=(540,720))
 for page in range(1,3):
  c.setFont('Helvetica',24);c.drawString(40,650,f'Candidate v{version} - page {page}')
  c.setFont('Helvetica',15);c.drawString(40,590,'Museum -> exit -> rail station')
  c.drawString(40,560,f'Depart museum: {"15:00" if version==1 else "15:21"}')
  c.drawString(40,530,'Approved version: v2. Simulation fixture.')
  c.showPage()
 c.save()
manifest={'candidate':'v2','accepted':'simulated user accepted v2','pages':2,'local_file':str(r/'candidate-v2.pdf'),'sha256':hashlib.sha256((r/'candidate-v2.pdf').read_bytes()).hexdigest(),'pdf_link':'http://127.0.0.1:18768/current.pdf','archive_link':'http://127.0.0.1:18768/materials.zip','long_term_save':'tool failure: simulated storage unavailable'}
(r/'handoff.json').write_text(json.dumps(manifest,indent=2))
