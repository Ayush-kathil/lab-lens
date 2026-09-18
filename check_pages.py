import os
from PyPDF2 import PdfReader

pdf_path = 'docs/PROJECT_REPORT.pdf'
if os.path.exists(pdf_path):
    reader = PdfReader(pdf_path)
    pages = len(reader.pages)
    print(f"Total Pages: {pages}")
else:
    print("PDF not generated yet.")
