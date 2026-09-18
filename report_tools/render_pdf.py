import markdown
import os
import asyncio
from playwright.async_api import async_playwright

with open('docs/PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
    text = f.read()

html = markdown.markdown(text, extensions=['tables', 'fenced_code'])
html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body {{ font-family: 'Times New Roman', serif; margin: 40px; font-size: 16px; line-height: 1.6; }}
h1, h2, h3 {{ font-family: 'Arial', sans-serif; page-break-after: avoid; }}
h1 {{ font-size: 24px; border-bottom: 2px solid #ccc; padding-bottom: 5px; }}
h2 {{ font-size: 20px; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; page-break-inside: avoid; }}
th, td {{ border: 1px solid #ddd; padding: 8px; font-size: 14px; }}
th {{ padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #f2f2f2; }}
p, li {{ page-break-inside: avoid; }}
pre {{ background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd; overflow-x: auto; font-family: Consolas, monospace; }}
img {{ display: block; margin: 20px auto; max-width: 100%; height: auto; border: 1px solid #ccc; box-shadow: 1px 1px 3px rgba(0,0,0,0.1); }}
</style>
</head>
<body>
{html}
</body>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{ startOnLoad: true }});
  // Find all pre > code.mermaid and render them
  document.querySelectorAll('code.language-mermaid').forEach((block, index) => {{
    let rawCode = block.textContent;
    let div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = rawCode;
    block.parentNode.replaceWith(div);
  }});
</script>
</html>
"""
with open('temp.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f'file:///{os.path.abspath("temp.html").replace("\\", "/")}')
        await page.wait_for_timeout(2000)  # Wait for Mermaid to render
        await page.pdf(
            path='docs/PROJECT_REPORT.pdf', 
            format='A4', 
            print_background=True, 
            margin={'top': '20mm', 'bottom': '20mm', 'left': '20mm', 'right': '20mm'},
            display_header_footer=True,
            header_template='<div style="font-size: 10px; text-align: center; width: 100%;">Lab Lens Project Report</div>',
            footer_template='<div style="font-size: 10px; text-align: right; width: 100%; padding-right: 20mm;"><span class="pageNumber"></span></div>'
        )
        await browser.close()

asyncio.run(main())
