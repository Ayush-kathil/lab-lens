def create_readme():
    content = """<h1 align="center">Lab Lens</h1>
<h3 align="center">Vision-Based Laboratory Equipment Verification &amp; Spatial Compliance</h3>

> **Note on Styling:** GitHub explicitly sanitizes custom CSS text colors in Markdown (e.g., `#FACC15` and `#3B82F6`) for security. The semantic HTML layout is maintained above as a clean, compliant fallback without relying on unsupported CSS hacks.

## 1. Introduction
Safety and compliance in physical laboratory environments rely not just on the presence of equipment, but on its correct spatial arrangement. **Lab Lens** addresses the laboratory equipment perception problem by decoupling object detection from spatial safety validation. Rather than relying on black-box end-to-end models to predict "safe" or "unsafe" setups, this project introduces a hybrid pipeline: a deep-learning perception layer combined with a configurable, deterministic geometric rule engine. This ensures that safety validation remains transparent, explicitly configurable, and easily interpretable.

## 2. Overview
Lab Lens is an automated visual verification system designed to evaluate laboratory workstations. It ingests an image of a lab setup alongside a structured JSON/YAML compliance schema. The system detects the equipment, computes spatial relations (e.g., inside, above, near), and deterministically scores the setup against the required rules.

## 3. Problem Statement
Traditional neural networks are highly capable of object perception but lack the strict interpretability required for safety-critical spatial reasoning. End-to-end models struggle to learn hard geometric constraints and cannot easily adapt to new safety rules without extensive retraining.

## 4. Motivation
In chemistry labs, equipment arrangement dictates safety (e.g., a glass rod must be *inside* a beaker, not just placed near it). Decoupling perception from rule validation allows human experts to define explicit safety rules, ensuring reliable compliance without depending on a model's latent understanding of "correctness".

## 5. Objectives
1. Train a lightweight object detector (YOLOv8n) for laboratory equipment.
2. Develop a deterministic spatial reasoning engine to parse bounding box geometries.
3. Build a configurable compliance ruleset evaluator.
4. Provide structured, reproducible compliance reporting.

## 6. Scope
The project covers 2D spatial compliance for 25 categories of laboratory equipment based on the ChemEq25 taxonomy. It focuses on geometric reasoning from monocular images and does not currently support 3D perspective correction or temporal video tracking.

## 7. System Capabilities
- **Object Detection (Input/Output):** Ingests an image; outputs bounding boxes, class labels, and confidence scores for 25 equipment types.
- **Spatial Reasoning (Input/Output):** Ingests bounding boxes; outputs explicit relations (`left_of`, `right_of`, `above`, `below`, `inside_region`, `overlaps`, `near`, `far`).
- **Compliance Evaluation (Input/Output):** Ingests relations and a schema; outputs `COMPLIANT` / `NON_COMPLIANT` / `ERROR`.

## 8. Functional Modules
- `lab_lens.detection`: Handles YOLOv8n initialization, image preprocessing, and inference.
- `lab_lens.spatial`: Computes bounding box intersections, distances, and normalized geometry.
- `lab_lens.config`: Ingests and validates user-defined JSON/YAML setup schemas.
- `lab_lens.scoring`: Evaluates rules and calculates explicit condition coverage.
- `lab_lens.pipeline`: Orchestrates end-to-end execution from image input to JSON report.

## 9. Functional Requirements
1. The system must ingest an image and a setup schema configuration.
2. The system must detect laboratory equipment and output bounding boxes.
3. The system must evaluate explicit spatial relationships between detected objects.
4. The system must report a final compliance status based strictly on the provided rules.

## 10. Non-Functional Requirements
1. **Configurability**: Safety rules must be defined externally via schemas without code changes.
2. **Determinism**: Identical bounding box coordinates must yield identical compliance scores.
3. **Robustness**: The pipeline must handle missing schemas or unreadable images gracefully.
4. **Efficiency**: Inference and rule evaluation must be executable on standard CPU hardware.

## 11. System Architecture
The architecture enforces a strict boundary between perception and logic:
- **YOLOv8n**: Performs learned equipment detection, returning class labels and coordinates.
- **Rule Engine**: Evaluates deterministic spatial rules and required object counts.
*Note: YOLOv8n performs object detection only; it does not learn setup correctness or experiment recognition.*

![System Architecture](docs/figures/system_architecture.png)

## 12. Workflow
1. **Input:** User provides an image and a configuration schema.
2. **Quality Assessment:** System verifies image integrity and readability.
3. **Detection:** YOLOv8n infers bounding boxes and class IDs.
4. **Normalization:** Coordinates are scaled for resolution-independent reasoning.
5. **Spatial Reasoning:** Geometric relations are explicitly calculated.
6. **Rule Engine:** Conditions are evaluated against the required schema.
7. **Reporting:** A structured JSON summary is emitted.

![End-to-End Workflow](docs/figures/system_workflow.png)

## 13. Technologies
- **Python 3.12**: Core runtime.
- **Ultralytics (YOLOv8)**: Object detection backbone.
- **OpenCV**: Image manipulation and bounding box rendering.
- **Pytest**: Deterministic test validation.
- **uv**: Reproducible dependency management.

## 14. Dataset
**Development Dataset (Final Verified):**
- Total Images: 4224
- The ChemEq25 dataset provides bounding box annotations for object detection. It does not provide setup-compliance ground truth.

## 15. Dataset Engineering
The original dataset suffered from leakage and duplicate corruption. A rigorous data-engineering pipeline was applied: exact duplicate auditing via SHA-256, near-duplicate review via dHash, deterministic bounding box repair, and strict quarantine for empty labels. This guaranteed a completely isolated test set.

## 16. Final Dataset Statistics
- **Train**: 2891
- **Validation**: 878
- **Held-Out Test**: 455
- **Instances**: 6377
*(Note: 4458 was a historical intermediate state; 4224 is the authoritative final count).*

## 17. ChemEq25 25-Class Taxonomy
The system explicitly supports the following 25 authoritative classes derived from the validated dataset source:

| ID | Class | ID | Class |
|---:|---|---:|---|
| 0 | Beaker | 13 | Reagent Bottle |
| 1 | Buchner Funnel | 14 | Round Bottom Flask Borosilicate Glass 1 Neck |
| 2 | Burette Stands | 15 | Round Bottom Flask Borosilicate Glass 2 Neck |
| 3 | Calorimeter | 16 | Round Bottom Flask Borosilicate Glass 3 Neck |
| 4 | Conical Flask | 17 | Separating Funnel |
| 5 | Funnel | 18 | Spirit Lamp |
| 6 | Glass Rod | 19 | TestTube Holder |
| 7 | Measuring Cylinder | 20 | Test Tube |
| 8 | Mechanical Balance Scale | 21 | Volumetric Flask |
| 9 | Nessler Reagent Bottle | 22 | Volumetric Pipet |
| 10 | Pipette | 23 | Wash Bottle |
| 11 | Porcelain Mortar Pestle | 24 | Weighing Bottle |
| 12 | Precision Weight Scale | | |

## 18. Model Selection
YOLOv8n was chosen due to its optimal balance of fast CPU inference and high recall. A deterministic rule-based spatial engine was chosen over an end-to-end classification network to ensure safety rules remain explicitly verifiable, explainable, and configurable.

## 19. Training Configuration
- **Model**: YOLOv8n
- **Image Size**: 640
- **Batch Size**: 8
- **Epochs**: 3
- **Device**: CPU
- **Workers**: 0
- **Cache**: false
- **Seed**: 42

## 20. Model Evaluation
**Validation Split:**
- Precision: 0.86165
- Recall: 0.85265
- mAP50: 0.89721
- mAP50-95: 0.61170

**Held-Out Test Split:**
- Precision: 0.83925
- Recall: 0.83862
- mAP50: 0.88067
- mAP50-95: 0.59600

## 21. Spatial Reasoning
The engine computes bounding box overlaps and distances using normalized geometry [0,1]. Supported relations include `left_of`, `right_of`, `above`, `below`, `inside_region`, `overlaps`, `near`, and `far`.

## 22. Rule-Based Compliance
The engine evaluates the detected layout against explicit spatial rules defined in JSON/YAML. It calculates missing objects, extra objects, and verifies if required geometric constraints (e.g., `["Glass_Rod", "inside_region", "Beaker"]`) hold true.

## 23. Compliance States
- `COMPLIANT`: All explicit rules and required counts are fully satisfied.
- `NON_COMPLIANT`: One or more explicit constraints failed.
- `UNSPECIFIED`: Zero explicit conditions were requested or no schema was provided.
- `AMBIGUOUS`: Conflicting structural geometries detected.
- `ERROR`: System-level fault (e.g., invalid schema or unreadable image).

## 24. Scoring
**Condition Coverage Score** = `(Satisfied Explicit Conditions / Total Explicit Conditions) × 100`

![Compliance Flow](docs/figures/compliance_flow.png)

*(Note: If zero conditions exist, the state is UNSPECIFIED. This score strictly represents configuration coverage, not detector confidence or a calibrated safety probability).*

## 25. Robustness/Error Handling
The pipeline is designed with explicit fallback states. Unreadable images, missing schemas, invalid bounding boxes, missing targets, or internal detector exceptions return structured error states rather than panicking. 

## 26. End-to-End Pipeline
The `LabLensPipeline` orchestrates the flow: it initializes the detector, parses schemas, processes frames, executes spatial logic, and emits unified JSON compliance reports.

## 27. Installation
The repository uses `uv` for reproducible environments.
```bash
git clone https://github.com/Ayush-kathil/lab-lens.git
cd lab-lens
uv sync
uv run python -m lab_lens --help
```
*Note: Due to repository sizing, trained weights should be generated locally by executing the training pipeline or requested via the project maintainers.*

## 28. Configuration
Schemas use strict JSON/YAML arrays. Example `configs/spatial_rules.yaml`:
```yaml
required_objects:
  Beaker: { min: 1, max: 1 }
  Glass_Rod: { min: 1, max: 1 }
spatial_rules:
  - ["Glass_Rod", "inside_region", "Beaker"]
```

## 29. CLI Usage
Basic perception inference:
```bash
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt
```
Compliance evaluation:
```bash
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/spatial_rules.yaml
```

## 30. JSON Output
To output structured compliance data for downstream systems:
```bash
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/spatial_rules.yaml --json
```

## 31. Example Results
Testing fixtures demonstrate successful evaluation of `COMPLIANT` states when objects satisfy counts/rules, and `NON_COMPLIANT` states when objects are missing or misplaced. See the PDF report for visual evidence.

## 32. Testing
The project leverages a robust Pytest suite for deterministic logic verification.
```bash
uv run pytest -q
# Expect 100 passed
```

## 33. Project Structure
```text
.
├── configs/          # Compliance schemas
├── docs/             # Technical reports and documentation
├── report_tools/     # Validation and rendering scripts
├── scripts/          # ML lifecycle and dataset engineering
├── src/
│   └── lab_lens/     # Core application modules
└── tests/            # Deterministic test suite
```

## 34. Engineering Challenges
Initial CPU training runs suffered from severe intra-epoch RSS memory growth, necessitating strict batch size limits and zero-worker DataLoader configurations. A critical regression involving confidence-threshold forwarding in the Ultralytics interface also required forensic debugging and repair.

## 35. Design Decisions & Trade-offs
Decoupling perception from rules sacrifices the simplicity of an end-to-end classifier but guarantees explainability. The spatial engine strictly relies on 2D bounding box proxies, trading 3D precision for extreme computational efficiency on standard CPUs.

## 36. Reproducibility
All dataset splits, validation metrics, and test evaluations are strictly reproducible via frozen `uv.lock` dependencies and deterministic random seeds (`seed=42`).

## 37. ExternalLabBench
- External candidates: 10
- Human annotations: 0
- Dev/Test: 0
- Metrics: N/A
*The ExternalLabBench infrastructure exists, but independent external evaluation remains intentionally incomplete pending human annotation.*

## 38. Limitations
Spatial geometry is limited to 2D normalized bounding boxes. External real-world generalization remains unverified until human annotations for the ExternalLabBench are populated.

## 39. Future Work
- Completion of human annotation for the ExternalLabBench.
- Expansion of the rule engine to support 3D perspective correction and complex rotational setups.

## 40. Documentation
- [Project Report (PDF)](docs/PROJECT_REPORT.pdf)
- [Project Report (Markdown)](docs/PROJECT_REPORT.md)
- [Statement](statement.md)

## 41. References
- *ChemEq25 Dataset Specification*
- *Ultralytics YOLOv8 Documentation*
(For extensive academic citations, see `docs/PROJECT_REPORT.pdf`).

## 42. Academic/Safety Disclaimer
This project is an academic research prototype. Calculated compliance scores represent configuration condition coverage, not certified safety probabilities for real-world physical laboratories.

## 43. VITyarthi Submission Checklist
- [x] Comprehensive requirements, architecture, and documentation.
- [x] Deterministic evaluation methodology.
- [x] External generalization explicitly noted as incomplete.
- [x] Reproducible modular architecture.
"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    create_readme()
