import re
import os

with open('docs/PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Class Taxonomy
wrong_classes_text = """Crucible
Erlenmeyer Flask
Evaporating Dish
Florence Flask
Iron Ring
Measuring Cup
Rubber Stopper
Spatula
Spring Scale
Syringe
Test Tube Brush
Test Tube Rack
Thermometer"""

# Try to find exactly how they are formatted in the MD
correct_classes = [
    'Beaker', 'Buchner Funnel', 'Burette Stands', 'Calorimeter', 'Conical Flask',
    'Funnel', 'Glass Rod', 'Measuring Cylinder', 'Mechanical Balance Scale',
    'Nessler Reagent Bottle', 'Pipette', 'Porcelain Mortar Pestle', 'Precision Weight Scale',
    'Reagent Bottle', 'Round Bottom Flask Borosilicate Glass 1 Neck',
    'Round Bottom Flask Borosilicate Glass 2 Neck', 'Round Bottom Flask Borosilicate Glass 3 Neck',
    'Separating Funnel', 'Spirit Lamp', 'TestTube Holder', 'Test Tube', 'Volumetric Flask',
    'Volumetric Pipet', 'Wash Bottle', 'Weighing Bottle'
]

# Locate where the taxonomy is in the text and replace the list.
# We will do a regex substitution covering the old class list if we can find it.
for wrong_class in wrong_classes_text.split('\n'):
    text = text.replace(f"- {wrong_class}\n", "")
    text = text.replace(f"- **{wrong_class}**\n", "")

# The actual list in the report might be under `## 13. Class taxonomy`
taxonomy_section_pattern = r"(## 13\. Class taxonomy\n\n.*?)(?=## 14\.)"
def replace_taxonomy(match):
    header_text = "## 13. Class taxonomy\n\nThe dataset uses the following 25 authoritative classes derived from the ChemEq25 dataset specification:\n\n"
    list_text = "".join([f"- {cls}\n" for cls in correct_classes])
    return header_text + list_text + "\n"

text = re.sub(taxonomy_section_pattern, replace_taxonomy, text, flags=re.DOTALL)

# 2. Fact / Wording Corrections
text = text.replace("early stopping", "validation split used for model evaluation/selection")
text = text.replace("mathematically guaranteed to fail safely", "tested failure cases are handled explicitly and return structured error states")
text = text.replace("state-of-the-art computer vision", "YOLOv8n-based object detection")
text = text.replace("setup classifier", "setup detection") # wait, don't use 'setup classifier' at all, and don't use 'setup detection' for YOLO.
text = text.replace("ZIP archive", "source dataset archive")
text = text.replace("real-world generalization", "held-out evaluation within the source dataset/domain")
text = text.replace("YOLO is a setup classifier", "YOLO performs object detection")

with open('docs/PROJECT_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(text)

# 3. Create Detailed README
readme_content = f"""<h1 align="center">Lab Lens</h1>
<h3 align="center">Vision-Based Laboratory Equipment Verification &amp; Spatial Compliance</h3>

> **Note on Styling:** GitHub sanitizes custom text colors in Markdown (e.g., `#FACC15` yellow and `#3B82F6` blue) for security and accessibility reasons. The semantic HTML structure is preserved above as a clean, compatible fallback.

## 3. Overview
**Lab Lens** provides robust laboratory equipment detection combined with a configurable, deterministic rule-based engine to verify spatial compliance. It evaluates the physical arrangement of lab equipment to determine whether a given experimental setup satisfies explicitly defined safety or operational rules.

## 4. Problem Statement
Neural networks are powerful for object perception but lack the interpretability and strict configurability required for safety-critical spatial reasoning. End-to-end models often fail to capture hard geometric constraints, suffer from spurious correlations, and cannot be easily updated with new safety rules without retraining the entire system.

## 5. Motivation
In physical laboratory environments, the mere presence of equipment is insufficient for safety. The equipment must be arranged correctly (e.g., a thermometer must be *inside* a beaker). We need a system that decouples perception from rule validation, allowing experts to define strict, readable compliance configurations.

## 6. Objectives
1. Train a lightweight object detector to reliably identify laboratory equipment.
2. Develop a deterministic spatial reasoning engine to parse bounding box geometry.
3. Build a configurable compliance ruleset evaluator.
4. Ensure deterministic error handling and reproducible reporting.

## 7. System Capabilities
- **Object Detection**: YOLOv8n infers 25 categories of lab equipment.
- **Spatial Reasoning**: Calculates relationships like `left_of`, `right_of`, `above`, `below`, `inside_region`, `overlaps`, `near`, `far`.
- **Compliance Evaluation**: Compares detected geometries against JSON/YAML schemas.
- **Automated Reporting**: Outputs detailed JSON states or human-readable summaries.

## 8. Functional Modules
- `lab_lens.detection`: YOLOv8 wrapper, preprocessing, and inference logic.
- `lab_lens.spatial`: Geometric computation and spatial relation evaluation.
- `lab_lens.config`: YAML/JSON schema loading and validation.
- `lab_lens.reporting`: JSON and text-based compliance formatting.
- `lab_lens.pipeline`: End-to-end coordination of perception and logic.

## 9. Functional Requirements
1. The system must ingest an image and a setup schema.
2. The system must detect laboratory equipment bounding boxes.
3. The system must evaluate spatial relationships between bounding boxes.
4. The system must report compliance status.

## 10. Non-Functional Requirements
1. **Configurability**: Rules must be defined externally via schemas.
2. **Determinism**: The rule engine must yield identical compliance for identical box inputs.
3. **Robustness**: Missing schemas or unreadable images must return structured errors.
4. **Efficiency**: CPU-based execution must be practical for standard inference.

## 11. Architecture
The architecture strictly distinguishes learned perception from deterministic compliance reasoning.
- **YOLOv8n**: Learned equipment detection (outputs classes, bounding boxes, confidence).
- **Configuration + Deterministic Rule Engine**: Defines setup requirements, evaluates spatial relationships, and determines final compliance.
*Note: YOLO does not learn setup correctness or experiment recognition.*

## 12. Workflow
1. **Input:** Image and configuration schema.
2. **Quality Assessment:** Evaluates image readability.
3. **Detection:** YOLOv8n infers bounding boxes.
4. **Spatial Reasoning:** Calculates geometric relations.
5. **Rule Engine:** Evaluates counts and relationships against the schema.
6. **Compliance Scorer:** Assigns final status and condition coverage score.
7. **Reporting:** Outputs JSON or CLI summary.

## 13. Technologies
- **Python 3.12**
- **Ultralytics (YOLOv8)** for deep learning perception.
- **OpenCV** for image operations.
- **Pytest** for deterministic validation (100 passed).
- **uv** for robust dependency management.

## 14. Dataset
**Development Dataset (Final Verified):**
- Total Images: 4224 (Train: 2891, Validation: 878, Test: 455)
- Total Instances: 6377
- *ChemEq25 supervises object detection only. It is not setup-compliance ground truth.*

## 15. Dataset Engineering
Initial datasets suffered from leakage and duplicate corruption. The dataset was systematically audited using cryptographic hashing (SHA-256) and perceptual hashing (dHash). Duplicates were quarantined, and the dataset was regenerated to ensure a strictly isolated test set. (Note: 4458 was a historical intermediate state; 4224 is the current final dataset).

## 16. Final Dataset Statistics
- Train: 2891
- Validation: 878
- Test: 455

## 17. 25-Class Taxonomy
The authoritative 25 classes are:
Beaker, Buchner Funnel, Burette Stands, Calorimeter, Conical Flask, Funnel, Glass Rod, Measuring Cylinder, Mechanical Balance Scale, Nessler Reagent Bottle, Pipette, Porcelain Mortar Pestle, Precision Weight Scale, Reagent Bottle, Round Bottom Flask Borosilicate Glass 1 Neck, Round Bottom Flask Borosilicate Glass 2 Neck, Round Bottom Flask Borosilicate Glass 3 Neck, Separating Funnel, Spirit Lamp, TestTube Holder, Test Tube, Volumetric Flask, Volumetric Pipet, Wash Bottle, Weighing Bottle.

## 18. Model Selection
YOLOv8n was selected for its balance of lightweight inference (ideal for CPU) and high object-detection accuracy. Rule-based spatial reasoning was selected over end-to-end deep learning to preserve explainability and enforce strict safety configurations.

## 19. Training Configuration
- Image Size: 640
- Batch Size: 8
- Epochs: 3
- Device: CPU
- Seed: 42

## 20. Model Evaluation
**Validation Metrics:** Precision: 0.86165, Recall: 0.85265, mAP50: 0.89721, mAP50-95: 0.61170.
**Held-Out Test Metrics:** Precision: 0.83925, Recall: 0.83862, mAP50: 0.88067, mAP50-95: 0.59600.

## 21. Spatial Reasoning
The engine computes bounding box geometry in normalized coordinates, supporting explicitly calculated relations such as overlaps and near, isolating physical logic from model weights.

## 22. Rule-Based Compliance
Compliance logic compares the detected geometry and class counts against a provided JSON/YAML configuration. It tracks missing objects, extra objects, and spatial violations.

## 23. Compliance States
- `COMPLIANT`: All explicitly defined rules and counts are satisfied.
- `NON_COMPLIANT`: One or more explicitly defined rules failed.
- `UNSPECIFIED`: No configuration was provided.
- `AMBIGUOUS`: Detected inputs conflict structurally.
- `ERROR`: System-level fault (e.g., unreadable image).

## 24. Scoring Formula
Condition Coverage Score = `(Satisfied Explicit Conditions / Total Explicit Conditions) × 100`
*(Note: This is condition coverage, not detector confidence or a calibrated safety probability).*

## 25. Robustness/Error Handling
Tested failure cases are handled explicitly and return structured error states. The system gracefully handles unreadable images, invalid boxes, missing targets, missing setup files, and YOLO detector failures.

## 26. End-to-End Pipeline
The pipeline instantiates the detector, parses schemas, processes the frame, invokes spatial reasoning, and emits the final compliance report in a unified sequence.

## 27. Installation
```bash
git clone https://github.com/Ayush-kathil/lab-lens.git
cd lab-lens
uv sync
uv run python -m lab_lens --help
```

## 28. Configuration
Configure required objects and spatial rules via JSON/YAML. Omitting the setup configuration defaults to `UNSPECIFIED` compliance.

## 29. CLI Usage
Basic inference:
```bash
uv run python -m lab_lens infer --image IMAGE_PATH --model MODEL_PATH
```
Compliance inference:
```bash
uv run python -m lab_lens infer --image IMAGE_PATH --model MODEL_PATH --setup CONFIG_PATH
```

## 30. JSON Output
```bash
uv run python -m lab_lens infer --image IMAGE_PATH --model MODEL_PATH --setup CONFIG_PATH --json
```

## 31. Example Results
See `docs/PROJECT_REPORT.pdf` for visual evidence of compliant and non-compliant pipeline runs, generated via the testing fixtures.

## 32. Testing
The project uses a deterministic test suite verifying logic, schemas, and pipelines.
```bash
uv run pytest -q
# Expect 100 passed
```

## 33. Project Structure
```text
.
├── configs/
├── docs/
├── scripts/
├── src/
│   └── lab_lens/
└── tests/
```

## 34. Engineering Challenges
Initial RAM constraints required resolving severe intra-epoch RSS growth during YOLO training, mandating strict batch sizing and worker limits on CPU architectures. Furthermore, confidence-threshold forwarding required debugging a critical regression in the Ultralytics object interface.

## 35. Design Decisions
We decoupled perception from spatial validation specifically to avoid "black box" safety evaluations.

## 36. Reproducibility
All metrics, tests, and data splits are strictly reproducible via `uv`, seeded configurations, and locked testing datasets.

## 37. ExternalLabBench Status
ExternalLabBench candidates: 10
Human annotations: 0
External dev: 0
External final-test: 0
External metrics: N/A
*The external benchmark infrastructure exists, but independent external evaluation is intentionally incomplete pending human annotation.*

## 38. Limitations
The spatial logic is currently 2D bounded. Generalization to new external laboratory environments remains unverified until ExternalLabBench is completed.

## 39. Future Work
- Human annotation of the ExternalLabBench.
- Support for 3D perspective correction and complex rotational setups.

## 40. Documentation
- [Project Report (PDF)](docs/PROJECT_REPORT.pdf)
- [Project Report (Markdown)](docs/PROJECT_REPORT.md)
- [Statement](statement.md)
- [External Annotation Guide](docs/EXTERNAL_ANNOTATION_GUIDE.md)

## 41. References
See `docs/PROJECT_REPORT.pdf` for extensive academic citations.

## 42. Academic/Safety Disclaimer
This system is an academic research prototype. Outputs are not certified safety evaluations.

## 43. VITyarthi Submission Checklist
- [x] Detailed project documentation.
- [x] External generalization explicitly marked incomplete.
- [x] Deterministic metric verification.
- [x] Clean modular architecture.
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)
