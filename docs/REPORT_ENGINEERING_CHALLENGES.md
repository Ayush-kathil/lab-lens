# Engineering Challenges & Design Decisions

This document details the genuine technical challenges faced during the development of Lab Lens and the corresponding engineering design decisions.

### 1. Dataset Split Leakage
- **Problem**: Analysis of the original ChemEq25 dataset (4,599 images) revealed a critical data leakage issue: exact duplicate images were present in both the training and held-out evaluation splits.
- **Investigation**: Custom dataset forensic scripts were developed to generate SHA-256 hashes of the pixel arrays, identifying identical images crossing the dataset boundaries.
- **Solution & Result**: A deterministic dataset repair tool was built (`scripts/repair_dataset_leakage.py`) that strictly purged duplicates from the training split while preserving the integrity of the 455-image test split. The repaired dataset (4,458 images) ensures scientifically valid evaluation metrics.

### 2. Malformed Annotations & Defensive Normalization
- **Problem**: The raw bounding box annotations contained instances of mathematically invalid coordinates (e.g., negative widths where `x1 >= x2`).
- **Investigation**: Unchecked, these geometries would cause the spatial reasoning engine to crash or compute infinite areas.
- **Solution & Result**: Defensive geometric parsing was implemented. Bounding boxes are deterministically normalized into a relative 0.0–1.0 Cartesian coordinate plane. Invalid boxes are logged as structural warnings and dynamically excluded from the spatial engine without interrupting pipeline execution.

### 3. CPU-Only Training & Prototyping Constraints
- **Problem**: The project required a functional object detection backend, but needed to run reasonably fast on standard CPU hardware for prototype evaluation.
- **Investigation**: Foundation models and large YOLO variants (YOLOv8l/x) caused excessive memory footprint and extreme inference latency on CPUs.
- **Solution & Result**: The architecture standardized on `YOLOv8n` (nano). The batch size was stabilized at 8, and the image size at 640x640. This design decision successfully balanced acceptable detection accuracy (mAP50 ~0.88) with reasonable end-to-end CPU pipeline latency (~1.5s/image).

### 4. Separation of Detection Ground Truth from Spatial Ground Truth
- **Problem**: The source dataset (ChemEq25) provides labels for object detection but contains absolutely zero ground truth for spatial relationships or compliance rules.
- **Investigation**: Attempting to benchmark the spatial engine against the real-world dataset directly would require fabricating human annotations, compromising scientific validity.
- **Solution & Result**: The architecture explicitly decoupled the evaluations. 
  1. The spatial reasoning logic was mathematically verified against 21 generated synthetic fixtures. 
  2. The real-world E2E integration was tested using explicitly tracked `AI_GENERATED` / `SILVER_LABEL` annotations rather than claiming fake human ground truth.

### 5. Deterministic Explainable Scoring
- **Problem**: How to quantify a setup as "safe" or "compliant" without relying on arbitrary weightings or falsely assuming detector confidence equals physical safety.
- **Investigation**: If a rule targeted an object that YOLO failed to detect, naive implementations simply skipped the rule and falsely scored the setup as compliant.
- **Solution & Result**: Implemented explicit condition coverage scoring. A missing target dynamically yields a `MISPLACED_OBJECT` violation. The score strictly computes `(Satisfied Conditions / Total Configured Conditions) * 100`, providing deterministic transparency without overstating safety probabilities.
