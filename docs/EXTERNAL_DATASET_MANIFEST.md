# External Dataset Manifest & Documentation

## Overview
This document serves as the high-level summary and registry protocol for the `ExternalLabBench` benchmark. The actual dataset records will be maintained programmatically in `outputs/external_evaluation/external_manifest.csv`.

## 1. Data Sources and Licensing
Images are sourced exclusively from documented sources (e.g., Wikimedia Commons, educational open datasets, or explicitly licensed private collections). Every image must have a recorded `source_url` and an open `license` (such as CC-BY, CC0, or public domain). Images lacking verifiable provenance are strictly forbidden.

## 2. Annotation Policy
All ground-truth labels are created via **manual human review**. 
- ML models (including `best.pt`) are **never** used to generate the annotations.
- Every visible object belonging to the ChemEq25 taxonomy must be annotated.
- If an object is severely ambiguous, it is recorded as `AMBIGUOUS`.
- Completely empty/negative images receive an empty label file (`.txt`).
- Due to the strict human-annotation requirement, dataset status remains `EXTERNAL_DATASET_INCOMPLETE` until manual curation and labeling are physically completed by human annotators.

## 3. Class Coverage
The dataset specifically targets challenging cylindrical glassware (`Beaker`, `Conical_Flask`, `Volumetric_Flask`), Funnels, Pipettes, Bottles, and Stands to evaluate known taxonomy confusion boundaries.

## 4. Negative Examples
Hard-negative examples are deliberately included. These encompass plain drinking glasses, unrelated laboratory equipment (e.g., multimeters), and cluttered lab benches devoid of any ChemEq25 targets. They verify the model's false-positive rejection capability.

## 5. Split Policy
The external dataset is logically partitioned:
- **External Development**: (~30-50 images) Available for post-evaluation experimental tuning, error analysis, and targeted model improvement decisions.
- **External Final Test**: (~20-50 images) Absolutely immutable. It serves strictly as the final evaluation benchmark and must never be used for threshold tuning, hyperparameter search, or architecture selection.

## 6. Leakage Policy
Every incoming image is subjected to a cryptographic SHA256 exact-match check and an SSIM-based near-duplicate check against the existing `ChemEq25` datasets (Train, Valid, and the protected 455-image Test set). Duplicates are rejected automatically.

## 7. Evaluation Metrics
The evaluation script (`scripts/evaluate_external.py`) calculates:
- Precision, Recall, mAP50, mAP50-95
- Per-class metrics
- Confusion matrices (including targeted subsets for glassware confusion)
- Discrete error counts (False Positives, False Negatives, Class Confusions, Duplicate Detections, Out-of-Taxonomy)

## 8. Threshold Policy
The model is strictly evaluated at standard thresholds (`0.50`, `0.25`, `0.10`, `0.05`). Threshold tuning is strictly forbidden on the `External Final Test` subset.

## 9. Limitations
- **Acquisition Bottleneck**: Locating high-variance, real-world, openly-licensed laboratory imagery requires significant manual curation.
- **Annotation Bottleneck**: Human review is mandatory, preventing automated scale-up.
- **Current Status**: Due to the inability to circumvent the manual annotation and provenance rules using AI, the dataset is currently in an `INCOMPLETE` holding state pending human execution.
