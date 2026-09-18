import fitz  # PyMuPDF
import os

pdf_path = 'docs/PROJECT_REPORT.pdf'
doc = fitz.open(pdf_path)

print(f"Total Pages: {len(doc)}")
has_todos = False
for i in range(len(doc)):
    page = doc[i]
    text = page.get_text()
    if 'TODO' in text or 'PLACEHOLDER' in text or 'TBD' in text or 'INSERT IMAGE' in text:
        print(f"Found placeholder text on page {i+1}")
        has_todos = True
    
    # Render page to image to satisfy visual inspection requirement
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale
    pix.save(f'docs/figures/pdf_page_{i+1}.png')

if not has_todos:
    print("No placeholder text found.")
print("All pages rendered for visual inspection.")
