# Dataset Forensic Audit

## 1. Provenance & Versions
- **Original Dataset**: `Dataset/ChemEq25` (Structurally corrupted: 4294 missing labels out of 4598 images due to 8.3 shortname truncation and mismatch).
- **Verified Clean Dataset**: `Dataset/ChemEq25_training` (Structurally intact, labels match).

## 2. Structural Validation (ChemEq25_training)
- **Total Images**: 4458 (Train: 3103, Valid: 897, Test: 458)
- **Total Labels**: 6699 annotations
- **Missing Labels**: 0
- **Empty-Label Images**: 6 (0.13%)
- **Exact Hash Duplicates**: 0
- **Bad Coordinates / OOB**: 0
- **Malformed Lines**: 0

## 3. Semantic & Bounding Box Quality
- **Suspicious Bounding Boxes flagged**: 22 (Extreme areas < 0.001 or > 0.95, or severe aspect ratio outliers).
- **Montage Generation**: Visual montages generated in `outputs/dataset_audit/montages/` for all 25 classes.
- **Semantic Findings**: Visual inspection indicates bounding boxes generally tightly wrap the apparatus. However, the dataset suffers from homogeneous backgrounds and tight cropping. 
- **Missing Annotations**: Rare, mostly affecting multi-apparatus setups where one minor object is ignored.
- **Empty Labels**: The 6 empty labels are true background negatives.

## 4. Class Distribution
The 6699 instances are well-distributed across 25 classes, ranging from 174 (Volumetric_Pipet) to 398 (Conical_Flask). No single class dominates >10% of the dataset, and no class is starved (<2% of dataset).

## 5. Duplicate Leakage
No exact image collisions exist across Train/Valid/Test splits, protecting the benchmark integrity.

## 6. Final Decision Matrix
- **Status**: Structurally Valid, Domain-Constrained.
- **Verdict**: Outcome D. The dataset is structurally clean and semantically acceptable, but the domain coverage (background diversity) is insufficient for zero-shot real-world transfer.
- **Quarantined**: 0 images.
- **Action**: Retain dataset. Retraining is authorized provided strong domain-randomization augmentations are applied and training duration is increased from the baseline 3 epochs.
