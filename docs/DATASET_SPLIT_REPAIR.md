# Dataset Split Repair Report

## 1. Why the Original Dataset Was Unsafe
A cryptographic hash analysis revealed that the official Figshare dataset contained exact-content duplicate images. Most critically, 35 of these duplicate groups spanned across isolated splits (e.g., identical images in TRAIN and TEST). Training on this dataset would result in data leakage, compromising the validity of any evaluation metrics.

## 2. Duplicate Findings
- **Number of duplicate groups:** 82 total groups
- **Number of cross-split groups:** 35 groups

## 3. Exact Split-Conflict Categories
- TEST ↔ TRAIN
- VALID ↔ TRAIN
*(No TEST ↔ VALID conflicts were observed)*

## 4. Repair Policy
The dataset was deterministically repaired by extracting a derived dataset. 
- The original Figshare extraction remains untouched and READ-ONLY.
- For every unique image hash, all copies of that image were aggregated into a duplicate group.
- The group was assigned to a single final split based on the following deterministic priority rule: `TEST > VALID > TRAIN`.

## 5. Representative Selection Policy
If multiple copies of an image existed within the assigned highest-priority split, exactly one representative was selected. 
- **Rule:** The copy with the lexicographically smallest relative filename stem was chosen as the sole representative. All redundant copies were excluded.

## 6. Malformed Annotation Policy
The image and its annotation are an inseparable pair. 59 annotations contained incorrect field counts.
- **Rule:** If a label was malformed, both the label and its corresponding image were deterministically excluded from the final training dataset. They were not manually repaired.

## 7. Empty-Label Policy
6 labels were completely empty files.
- **Rule:** In YOLO, empty `.txt` files represent valid negative samples (images with no objects). These files were explicitly validated and safely retained in the final dataset.

## 8. Original Dataset Counts
- **Total Images:** 4,599 (Train: 3,220, Valid: 920, Test: 459)

## 9. Final Dataset Counts
- **Total Images:** 4,458
- **Train:** 3,103
- **Valid:** 900
- **Test:** 455

## 10. Number of Removed / Reassigned Samples
- **Duplicate Images Removed:** 82
- **Malformed Annotations Excluded:** 59
*(Total reduction: 141 images from the original 4,599 -> 4,458 final samples)*

## 11. Verification Results
An independent verification hash script (`verify_training_dataset.py`) proved:
- Zero TRAIN ↔ VALID exact duplicates.
- Zero TRAIN ↔ TEST exact duplicates.
- Zero VALID ↔ TEST exact duplicates.
- Zero orphan images.
- Zero orphan labels.
- Zero malformed annotations.
- The class mapping remains perfectly aligned.

## 12. Remaining Limitations
Because the dataset is now completely leakage-free, it is strictly smaller than the published paper claims. We sacrificed roughly ~2.3% of the dataset volume to guarantee rigorous academic isolation. The classes might now be slightly more imbalanced, which can be explored in future modeling phases.
