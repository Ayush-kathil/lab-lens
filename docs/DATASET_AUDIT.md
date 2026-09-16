# Dataset Forensic Audit

## 1. Provenance & Versions
- **Original Dataset Claim Verification**: The original `Dataset/ChemEq25` zip extraction suffered catastrophic DOS 8.3 short-name file truncation locally during decompression/filesystem handling (e.g., `2000C8~1.JPG`). This is NOT a claim that the published source archive was corrupted. The local truncation caused 4,294 structural missing labels out of 4,598 files.
- **Verified Clean Dataset**: `Dataset/ChemEq25_training`. This split retains proper, untruncated Roboflow filename stems, proving its structural integrity.

## 2. Structural Validation (ChemEq25_training)
- **Total Images**: 4458 (Train: 3103, Valid: 900, Test: 455)
  *(Note: A previous typographical error in an earlier report listed Valid as 897 and Test as 458. A full Git history and disk reconciliation confirms the physical split has always been 900/455. Zero files were moved.)*
- **Total Labels**: 6699 annotations
- **Structural Missing Labels**: 0
- **Empty-Label Images**: 6 images (0.13%) contain empty `.txt` labels. These were explicitly verified as true `VALID_NEGATIVE` background images with no target apparatus.
- **Exact Hash Duplicates**: 0 SHA-256 collisions leaked between Train, Valid, and Test splits.
- **Bad Coordinates / OOB**: 0
- **Malformed Lines**: 0

## 3. Semantic & Bounding Box Quality
- **Methodology**: SAMPLED AUDIT. 5 instances per class were visually verified via generated montage. The entire dataset was NOT independently reviewed manually.
- **Review Required**: 22 annotations were mathematically flagged due to extreme areas (<0.001 or >0.95) or severe aspect ratios. 
- **Wrong-Image Count**: 0 found in the sampled audit. Misclassifications are network generalization errors.
- **Missing-Annotation Count**: 0 structurally missing. Semantic missing annotations (unannotated background objects) were rare in the sample but the exact count across the 4,458 images remains AMBIGUOUS/UNKNOWN pending full manual review.

## 4. Class Distribution
The 6699 instances are well-distributed across 25 classes. The class mapping is derived purely from the PyTorch model metadata (`model.names`), ensuring no drift with hardcoded lists.

## 5. Duplicate Leakage
No exact image collisions exist across Train/Valid/Test splits, protecting the benchmark integrity.

## 6. Final Decision Matrix
- **Status**: Structurally Valid, Domain-Constrained.
- **Verdict**: Outcome D. The dataset is structurally clean, but the domain coverage (background diversity) is insufficient for zero-shot real-world transfer.
- **Quarantined**: 0 images.
- **Action**: Retain dataset. Retraining is authorized provided strong domain-randomization augmentations are applied.
