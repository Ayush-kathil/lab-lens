# REAL-WORLD SPATIAL DATASET CARD

## 1. Dataset Purpose
The SpatialComplianceReal dataset aims to evaluate the real-world accuracy of the deterministic spatial reasoning engine operating on human-verified ground-truth geometries, and subsequently, to benchmark the end-to-end (detector + spatial engine) compliance accuracy of Lab Lens.

## 2. Intended Use
- **Experiment A**: Oracle-box spatial evaluation (evaluating the rule engine using perfect ground-truth boxes to isolate logic).
- **Experiment B**: End-to-end spatial compliance evaluation (evaluating the rule engine using YOLO detector predictions to assess real-world application performance).

## 3. Non-Intended Use
- Do NOT use this dataset to train the object detector. (ChemEq25 serves that purpose).
- Do NOT fabricate or scrape random internet images.

## 4. Current Status
**WARNING**: Real-world images have NOT yet been collected. This directory establishes the protocol and schema infrastructure only.

## 5. Collection Protocol
- Images must capture physical laboratory setups.
- A "session_id" must group images taken of the exact same physical equipment arrangement, even if viewpoints change slightly, to prevent data leakage.

## 6. Annotation Units
Annotations operate at the *object instance* level (e.g., eaker_1), distinguishing individual identities from class labels (Beaker).

## 7. Split Policy
Splitting must occur strictly at the session_id level. A physical setup cannot appear in both train and test splits. The ChemEq25 test split is strictly excluded from this benchmark.

## 8. Privacy & Licensing Considerations
Future data collection must ensure no personally identifiable information (PII) is captured (e.g., human faces, nametags) and that laboratory policies permit image distribution.
