def rewrite_readme():
    content = """<h1 align="center">Lab Lens</h1>
<h3 align="center">Vision-Based Laboratory Equipment Verification &amp; Spatial Compliance</h3>

> **Note on Styling:** GitHub sanitizes custom text colors in Markdown (e.g., `#FACC15` yellow and `#3B82F6` blue) for security and accessibility reasons. The semantic HTML structure is preserved above as a clean, compatible fallback.

## 2. Overview
**Lab Lens** provides robust laboratory equipment detection combined with a configurable, deterministic rule-based engine to verify spatial compliance. It evaluates the physical arrangement of lab equipment to determine whether a given experimental setup satisfies explicitly defined safety or operational rules.

## 3. Problem Statement
Neural networks are powerful for object perception but lack the interpretability and strict configurability required for safety-critical spatial reasoning. End-to-end models often fail to capture hard geometric constraints and cannot be easily updated with new safety rules without retraining.

## 4. What the System Does
Lab Lens separates perception from compliance:
- **Perception:** Uses YOLOv8n to locate equipment in an image (bounding boxes and class labels).
- **Reasoning:** A deterministic rule engine evaluates the spatial relationships between the detected objects based on a user-provided configuration.

## 5. Key Features
- **Deterministic Geometric Reasoning:** Evaluates explicit relationships (`left_of`, `right_of`, `above`, `below`, `inside_region`, `overlaps`, `near`, `far`).
- **Configurable Setup Requirements:** Define min/max counts and relationships in simple YAML/JSON schemas.
- **Explainable Compliance:** Explicitly reports which required objects are missing, extra, or misplaced, outputting `COMPLIANT`, `NON_COMPLIANT`, `UNSPECIFIED`, `AMBIGUOUS`, or `ERROR`.
- **Condition Coverage Scoring:** Calculates `(Satisfied Explicit Conditions / Total Explicit Conditions) × 100`. (Note: This is condition coverage, *not* detector confidence or a calibrated safety probability).

## 6. System Architecture
The architecture strictly distinguishes learned perception from deterministic compliance reasoning.
- **YOLOv8n**: Learned equipment detection (outputs classes, bounding boxes, confidence).
- **Configuration + Deterministic Rule Engine**: Defines setup requirements, evaluates spatial relationships, and determines final compliance.

*Note: YOLO does not learn setup correctness or experiment recognition.*

## 7. End-to-End Workflow
1. **Input:** Image and configuration schema.
2. **Quality Assessment:** Evaluates image readability.
3. **Detection:** YOLOv8n infers bounding boxes.
4. **Spatial Reasoning:** Calculates geometric relations.
5. **Rule Engine:** Evaluates counts and relationships against the schema.
6. **Compliance Scorer:** Assigns final status and condition coverage score.
7. **Reporting:** Outputs JSON or human-readable CLI summary.

## 8. Functional Modules
- `lab_lens.detection`: YOLOv8 wrapper and inference logic.
- `lab_lens.spatial`: Geometric computation and relation evaluation.
- `lab_lens.config`: YAML/JSON schema loading.
- `lab_lens.reporting`: JSON and text-based compliance formatting.
- `lab_lens.pipeline`: End-to-end coordination.

## 9. Technologies
- **Python 3.12**
- **Ultralytics (YOLOv8)**
- **OpenCV**
- **Pytest** (for deterministic validation)
- **uv** (dependency management)

## 10. Dataset
**Development Dataset (Final Verified):**
- Total Images: 4224 (Train: 2891, Validation: 878, Test: 455)
- Total Instances: 6377
- ChemEq25 contains 25 equipment categories.
- *ChemEq25 supervises object detection only. It is not setup-compliance ground truth.*

## 11. Model
**YOLOv8n**
- Verified baseline configuration: image size 640, batch size 8, epochs 3, CPU, seed 42.

## 12. Verified Results
**Validation Metrics:**
- Precision: 0.86165
- Recall: 0.85265
- mAP50: 0.89721
- mAP50-95: 0.61170

**Held-Out Test Metrics:**
- Precision: 0.83925
- Recall: 0.83862
- mAP50: 0.88067
- mAP50-95: 0.59600

## 13. Compliance Reasoning
Outputs: `COMPLIANT`, `NON_COMPLIANT`, `UNSPECIFIED`, `AMBIGUOUS`, `ERROR`.
Score: Satisfied Explicit Conditions / Total Explicit Conditions × 100.

## 14. CLI Quick Start
```bash
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/example.json
```

## 15. Installation
```bash
git clone https://github.com/Ayush-kathil/lab-lens.git
cd lab-lens
uv sync
uv run python -m lab_lens --help
```

## 16. Configuration
Configure required objects and spatial rules via JSON/YAML. Omitting the setup configuration defaults to `UNSPECIFIED` compliance.

## 17. Running Inference
**Basic inference:**
```bash
uv run python -m lab_lens infer --image IMAGE_PATH --model MODEL_PATH
```
**Compliance inference:**
```bash
uv run python -m lab_lens infer --image IMAGE_PATH --model MODEL_PATH --setup CONFIG_PATH
```
**JSON output:**
```bash
uv run python -m lab_lens infer --image IMAGE_PATH --model MODEL_PATH --setup CONFIG_PATH --json
```

## 18. Testing
Verified deterministic testing suite (100 passed).
```bash
uv run pytest -q
```
For verbose output:
```bash
uv run pytest tests/ -v
```

## 19. Project Structure
```text
├── configs/
├── docs/
├── scripts/
├── src/
│   └── lab_lens/
└── tests/
```

## 20. Reproducibility / Engineering Notes
The system gracefully handles unreadable images, missing targets, YAML failures, and detector failures, providing deterministic outputs.

## 21. Limitations
The external benchmark infrastructure exists, but independent external evaluation is intentionally incomplete pending human annotation.

## 22. Future Work
- Human annotation of the ExternalLabBench.
- Expansion of supported geometric rules.

## 23. Documentation
- [Project Report (PDF)](docs/PROJECT_REPORT.pdf)
- [Project Report (Markdown)](docs/PROJECT_REPORT.md)
- [Statement](statement.md)
- [External Annotation Guide](docs/EXTERNAL_ANNOTATION_GUIDE.md)

## 24. References
Refer to `docs/PROJECT_REPORT.pdf` for a full list of academic citations and architectural inspiration.

## 25. Academic/Safety Disclaimer
This system is an academic research prototype. Condition coverage scores are not certified safety probabilities.

## 26. Submission Checklist
- [x] External generalization explicitly marked incomplete.
- [x] Modular codebase.
- [x] Verified metrics.
"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    rewrite_readme()
