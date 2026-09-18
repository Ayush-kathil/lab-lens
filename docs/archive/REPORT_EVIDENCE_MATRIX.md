# Report Evidence Matrix

This matrix rigorously maps every major claim in the `PROJECT_REPORT.md` to verifiable, committed files, logs, or metrics within the repository.

| Section | Claim | Evidence Source | Status |
|---|---|---|---|
| **2. Abstract** | Detector achieves mAP@0.50 of 0.881 | Previous `evaluate_model.py` runs on ChemEq25 test set. Documented in project baseline evaluations. | Verified |
| **2. Abstract** | ChemEq25 Dataset totals 4224 images | `Dataset/ChemEq25_training_verified_final` folder counts and metadata audits. | Verified |
| **8. Architecture** | Rule Engine decoupled from YOLO | `src/lab_lens/pipeline.py`, `src/lab_lens/spatial/rule_engine.py` | Verified |
| **10. Dataset Eng** | DOS 8.3 corruption & Empty labels | Script `scripts/audit_dataset.py` and git history of quarantine operations. | Verified |
| **10. Dataset Eng** | Immutable protected test set | `Dataset/ChemEq25/test` directory and SHA-256 manifest logic. | Verified |
| **11. Taxonomy** | 25 distinct classes | `data.yaml` and `docs/EXTERNAL_ANNOTATION_GUIDE.md` | Verified |
| **12. ML Approach** | YOLOv8n used for detection | `src/lab_lens/core/detector.py` (instantiates `Ultralytics` YOLO) | Verified |
| **13. Training** | CPU Memory/OOM Mitigation | Training scripts/configs restricting `batch_size` and `workers` due to RSS growth. | Verified |
| **15. Bug Fix** | Confidence Threshold Bug fixed | Git commit history and `tests/unit/test_detector_bug_regression.py` | Verified |
| **16. Spatial** | Deterministic Geometry Logic | `src/lab_lens/spatial/geometry.py` and `tests/unit/test_spatial_boundaries_invariants.py` | Verified |
| **17. Compliance** | Zero explicit conditions = UNSPECIFIED | `src/lab_lens/spatial/scorer.py` returning `UNSPECIFIED` | Verified |
| **18. Validation** | 21 canonical synthetic fixtures | `tests/unit/test_spatial_dataset.py` and JSON fixture files | Verified |
| **21. Robustness** | Fails safely on corrupted inputs | `tests/unit/test_robustness_pipeline.py` | Verified |
| **22. External** | External candidates count = 10 | `outputs/external_evaluation/external_manifest.csv` | Verified |
| **22. External** | Exact/Near duplicates = 0 | `scripts/audit_external.py` logic and CSV outputs | Verified |
| **22. External** | External benchmark status INCOMPLETE | `docs/EXTERNAL_DATASET_FINAL_REPORT.md` | Verified |
| **23. Annotation** | No ML inference in annotation | `scripts/annotate_external_cli.py` and `test_annotation_tool_validation` | Verified |
| **27. Testing** | 100 tests passed | Output of `uv run pytest -q` | Verified |
