import asyncio
from playwright.async_api import async_playwright
import os

html_content = """
<!DOCTYPE html>
<html>
<head>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true, theme: 'default' });
    </script>
    <style>
        body { padding: 20px; font-family: sans-serif; }
        .diagram-container { display: inline-block; padding: 20px; background: white; margin-bottom: 20px; }
    </style>
</head>
<body>

<div class="diagram-container" id="arch">
    <div class="mermaid">
    flowchart TD
        A[Input Image + Config] --> B[Quality Assessment]
        B --> C[YOLOv8n Detector]
        C --> D[Detection Normalization]
        D --> E[Spatial Reasoning]
        E --> F[Rule Engine]
        F --> G[Compliance Scorer]
        G --> H[JSON/CLI Reporting]
        
        Config[(SetupSpecification)] --> F
    </div>
</div>

<div class="diagram-container" id="workflow">
    <div class="mermaid">
    flowchart TD
        Start((Start)) --> Load[Load Image & Schema]
        Load --> Valid{Is Valid?}
        Valid -- No --> Err[Return ERROR]
        Valid -- Yes --> Infer[YOLOv8n Inference]
        Infer --> Detect{Detections?}
        Detect -- No --> Score[Score: 0 / UNSPECIFIED]
        Detect -- Yes --> Spatial[Compute Spatial Relations]
        Spatial --> Rules[Evaluate Rules]
        Rules --> Status{All Satisfied?}
        Status -- Yes --> Comp[COMPLIANT]
        Status -- No --> NonComp[NON_COMPLIANT]
        Comp --> Rep[Generate JSON Report]
        NonComp --> Rep
        Err --> Rep
        Score --> Rep
    </div>
</div>

<div class="diagram-container" id="compliance">
    <div class="mermaid">
    flowchart LR
        D[Detections] --> C[Counts]
        S[Setup Specification] --> C
        C --> R[Relations]
        R --> V[Violations]
        V --> Stat[Status]
        Stat --> Score[Score]
    </div>
</div>

</body>
</html>
"""

async def generate_diagrams():
    with open('temp_diagrams.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f'file:///{os.path.abspath("temp_diagrams.html")}')
        
        # Wait for mermaid to render
        await page.wait_for_timeout(3000)
        
        # Take screenshots
        arch = await page.query_selector('#arch')
        await arch.screenshot(path='docs/figures/system_architecture.png')
        
        workflow = await page.query_selector('#workflow')
        await workflow.screenshot(path='docs/figures/system_workflow.png')
        
        comp = await page.query_selector('#compliance')
        await comp.screenshot(path='docs/figures/compliance_flow.png')
        
        await browser.close()
    
    os.remove('temp_diagrams.html')

if __name__ == '__main__':
    asyncio.run(generate_diagrams())
