# Report Screenshot Checklist

To finalize your VITyarthi Project Report, you must manually capture the following screenshots and embed them into your PDF. 

**IMPORTANT**: Ensure your terminal background is clean. Do not expose personal directories or API keys.

### 1. GitHub Repository Homepage
- **Command/Page**: Open your browser to `https://github.com/{username}/Lab-lens`
- **What must be visible**: The repository name, the clean folder structure, and the top of the README containing the project title.
- **Suggested Caption**: *Figure: Lab Lens repository root and file structure.*

### 2. Architecture & Workflow Diagrams
- **Command/Page**: Scroll down your GitHub README to the Mermaid diagrams (Sections 7 & 8).
- **What must be visible**: The rendered flowchart graphics for "System Workflow" and "System Architecture".
- **Suggested Caption**: *Figure: Lab Lens system workflow and modular pipeline architecture.*

### 3. CLI Help Output
- **Command/Page**: Run `python -m lab_lens --help` in your terminal.
- **What must be visible**: The available commands (`infer`, `quality`, `evaluate`, etc.).
- **Suggested Caption**: *Figure: Command Line Interface (CLI) configuration options.*

### 4. Compliant E2E Result (Demo A)
- **Command/Page**: 
  `python -m lab_lens infer --image Dataset/SpatialComplianceReal/images/rw_001.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/demo_compliant.yaml`
- **What must be visible**: The `COMPLIANT` status, the `100.0 / 100` score, and the breakdown of Satisfied Conditions.
- **Suggested Caption**: *Figure: Successful pipeline execution evaluating a compliant setup configuration.*

### 5. Non-Compliant E2E Result (Demo B)
- **Command/Page**: 
  `python -m lab_lens infer --image Dataset/SpatialComplianceReal/images/rw_001.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/demo_non_compliant.yaml`
- **What must be visible**: The `NON_COMPLIANT` status, the `50.0 / 100` score, and the specific explicit violations (Missing Stand, Failed Rule).
- **Suggested Caption**: *Figure: Pipeline identifying spatial violations and missing objects in a non-compliant setup.*

### 6. Unspecified Result (Demo C)
- **Command/Page**: 
  `python -m lab_lens infer --image Dataset/SpatialComplianceReal/images/rw_001.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt`
- **What must be visible**: The `UNSPECIFIED` status and `null` score, proving safe fallback when no configuration is passed.
- **Suggested Caption**: *Figure: Graceful fallback handling when inference lacks a geometric configuration.*

### 7. JSON Serialization Output
- **Command/Page**: 
  `python -m lab_lens infer --image Dataset/SpatialComplianceReal/images/rw_001.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/demo_compliant.yaml --json`
- **What must be visible**: A portion of the structured JSON block containing `compliance_status` and `timing`.
- **Suggested Caption**: *Figure: Machine-readable JSON output for downstream integrations.*

### 8. Test Suite Result
- **Command/Page**: `pytest -q`
- **What must be visible**: The `94 passed` (or current count) green terminal output block.
- **Suggested Caption**: *Figure: Automated test suite verification across 94 unit and integration boundaries.*

### 9. Detector Evaluation Log
- **Command/Page**: Run `python -m lab_lens evaluate --model runs/detect/outputs/baseline_training_final/weights/best.pt --dataset Dataset/ChemEq25` (Note: Requires the ChemEq25 dataset locally).
- **What must be visible**: The YOLO validation metrics block showing Precision, Recall, and mAP50.
- **Suggested Caption**: *Figure: Baseline object detector evaluation on the held-out validation split.*
