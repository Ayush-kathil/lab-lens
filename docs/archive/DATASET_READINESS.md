# Dataset Readiness Gate

This document summarizes the dataset pairing investigation and malformed annotation audit for Phase 3 and Phase 4. 

## Dataset vs Model Quality

**DATASET QUALITY** refers to the structural integrity, physical file mapping, annotation validities, and correct formatting of the training data.
**MODEL QUALITY** refers to the accuracy (mAP, Precision, Recall) of a detector trained on this data. 

*They are not the same thing.* The findings below pertain strictly to **Dataset Quality**.

## Dataset Pairing Confidence (Phase 4 Audit)

**Finding:** The original dataset archive `ChemEq25 (Main paper Scientific Data journal, Titl.zip` was successfully located in `Downloads` and extracted to a clean directory `Dataset/ChemEq25_clean`.

However, an audit of this cleanly extracted archive reveals a critical issue:
- **The archive itself contains Windows 8.3 short-names** (e.g. `IM1A7B~1.JPG`) for the majority of the image and label files. 
- The truncation is physically baked into the Mendeley zip archive, not a local extraction artifact.
- Because string-based deterministic matching (excluding extensions) fails natively on these files, pairing images to their ground-truth labels is impossible without relying on fragile alphabetical or sequential sorting assumptions.
- **Readiness Decision:** UNSAFE for direct training. 

**Required Action Before Training:** 
Since the official archive itself is corrupted with truncated filenames, we cannot safely train a detector without establishing a deterministic workaround (e.g., sequentially re-pairing and renaming all files, which the current Phase 4 constraints strictly forbid). We require an uncorrupted dataset source, or explicit permission to enforce a sequential alphabetical re-pairing script.

## Malformed Annotations (Clean Archive Audit)

An audit of the clean archive revealed the exact same 66 malformed annotation files.

**Summary of Errors:**
- `empty_file`: 6 instances
- `wrong_number_of_fields`: 60 instances

**Treatment Policy:**
- YOLO considers empty `.txt` files as legitimate negative samples (images with no objects). These 6 `empty_file` instances should theoretically be retained as background images, provided the image-label pairing is correct.
- The 60 `wrong_number_of_fields` files likely contain malformed data. These must be deterministically deleted or skipped by the dataset generator. 
