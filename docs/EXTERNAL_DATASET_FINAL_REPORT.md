# External Dataset Final Report

## Status
**EXTERNAL_DATASET_INCOMPLETE**

## Forensic Summary
1. **Acquired Candidates Downloaded**: 10 (Halted strictly at 10 due to infrastructure rate-limiting HTTP 429 Too Many Requests from Wikimedia Commons).
2. **Accepted Benchmark Count**: 0 (Pending Human Verification).
3. **Development Count**: 0
4. **Final-Test Count**: 0
5. **Positive/Negative/Out-of-Taxonomy**: N/A (Pending Human Verification).
6. **Class Distribution**: N/A
7. **Annotation Completion**: 0%
8. **Provenance Completeness**: 100% for the 10 downloaded candidates.
9. **License Completeness**: 100% for the 10 downloaded candidates (Creative Commons variants).
10. **Exact Duplicates**: 0 (Initial SHA256 barrier passed).
11. **Near-Duplicate Candidates**: 0
12. **Final-Test SHA/Hash Manifest**: N/A
13. **External Metrics**: N/A

## Human Annotation Workflow
A graphical Human Annotation CLI has been scaffolded at `scripts/annotate_external_cli.py`. It requires human execution to assign ground-truth statuses manually without using YOLO, adhering to the strict rule that machine learning models must not be used to annotate the evaluation sets.

## Generalization & Model Claims
- **Equipment Detection vs Setup Correctness**: ChemEq25 strictly supervises object localization and classification only.
- **Rules Over Learning**: Setup correctness is NOT learned by YOLO. Spatial compliance is determined by an explicit configuration mapping and deterministic geometry rules.
- **External Claim**: No external generalization claims can be asserted until human annotation completes and evaluations are verified.
