import re
import os

with open('README.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Helper to extract a section's text
def get_section(title, text=text):
    pattern = rf'## {title}\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

# Extract sections
subtitle = get_section("Vision-Based Laboratory Equipment Verification & Spatial Compliance System")
overview = get_section("Project Overview")
problem = get_section("Problem Statement")
objectives = get_section("Objectives")
modules = get_section("Functional Modules")
fr = get_section("Functional Requirements")
nfr = get_section("Non-Functional Requirements")
workflow = get_section("System Workflow")
arch = get_section("System Architecture")
tech = get_section("Technologies Used")
dataset = get_section("Dataset")
model_sel = get_section("Model Selection")
training = get_section("Training Methodology")
det_eval = get_section("Detector Evaluation")
spatial_reasoning = get_section("Spatial Reasoning")
ground_truth = get_section("Spatial Ground-Truth Strategy")
comp_eval = get_section("Compliance Evaluation")
score = get_section("Explainable Compliance Score")
robustness = get_section("Robustness & Error Handling")
proj_struct = get_section("Project Structure")
install = get_section("Installation")
config = get_section("Configuration")
cli_usage = get_section("CLI Usage")
testing = get_section("Testing")
examples = get_section("Example Results")
perf = get_section("Performance")
design = get_section("Design Decisions & Engineering Challenges")
limitations = get_section("Limitations")
future = get_section("Future Enhancements")
refs = get_section("References")
disclaimer = get_section("Academic / Safety Disclaimer")
checklist = get_section("Submission Checklist")

# Reconstruct
new_readme = []
new_readme.append("# Lab Lens\n")
new_readme.append("> **Vision-Based Laboratory Equipment Verification & Spatial Compliance System**\n")

new_readme.append("## Overview\n")
if overview: new_readme.append(overview + "\n")
if problem: new_readme.append("### Problem Statement\n" + problem + "\n")
if objectives: new_readme.append("### Objectives\n" + objectives + "\n")

new_readme.append("## Features\n")
if modules: new_readme.append("### Functional Modules\n" + modules + "\n")
if fr: new_readme.append("### Functional Requirements\n" + fr + "\n")
if nfr: new_readme.append("### Non-Functional Requirements\n" + nfr + "\n")

new_readme.append("## System Architecture & Workflow\n")
if arch: new_readme.append("### Architecture\n" + arch + "\n")
if workflow: new_readme.append("### Workflow\n" + workflow + "\n")
if tech: new_readme.append("### Technologies\n" + tech + "\n")

new_readme.append("## Dataset\n")
if dataset: new_readme.append(dataset + "\n")

new_readme.append("## Model\n")
if model_sel: new_readme.append(model_sel + "\n")
if training: new_readme.append("### Training Methodology\n" + training + "\n")

new_readme.append("## Detection & Evaluation Results\n")
if det_eval: new_readme.append("### Detector Evaluation\n" + det_eval + "\n")
if ground_truth: new_readme.append("### Spatial Ground-Truth Strategy\n" + ground_truth + "\n")

new_readme.append("## Spatial Reasoning\n")
if spatial_reasoning: new_readme.append(spatial_reasoning + "\n")

new_readme.append("## Compliance Evaluation\n")
if comp_eval: new_readme.append(comp_eval + "\n")
if score: new_readme.append("### Explainable Compliance Score\n" + score + "\n")
if robustness: new_readme.append("### Robustness & Error Handling\n" + robustness + "\n")

new_readme.append("## Installation & Configuration\n")
if install: new_readme.append("### Installation\n" + install + "\n")
if config: new_readme.append("### Configuration\n" + config + "\n")

new_readme.append("## Usage & Reporting\n")
if cli_usage: new_readme.append("### CLI Usage\n" + cli_usage + "\n")
if examples: new_readme.append("### Example Results\n" + examples + "\n")
if perf: new_readme.append("### Performance\n" + perf + "\n")

new_readme.append("## Testing\n")
if testing: new_readme.append(testing + "\n")

new_readme.append("## Project Structure\n")
if proj_struct: new_readme.append(proj_struct + "\n")

new_readme.append("## Documentation\n")
if design: new_readme.append("### Design Decisions\n" + design + "\n")

new_readme.append("## Limitations\n")
if limitations: new_readme.append(limitations + "\n")
if future: new_readme.append("### Future Enhancements\n" + future + "\n")

new_readme.append("## References\n")
if refs: new_readme.append(refs + "\n")

new_readme.append("## Academic / Safety Disclaimer\n")
if disclaimer: new_readme.append(disclaimer + "\n")

new_readme.append("## Submission Checklist\n")
if checklist: new_readme.append(checklist + "\n")

with open('README.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_readme))

print("Restructured successfully.")
