# Dataset Readiness Gate

This document summarizes the dataset pairing investigation and malformed annotation audit for Phase 3. 

## Dataset vs Model Quality

**DATASET QUALITY** refers to the structural integrity, physical file mapping, annotation validities, and correct formatting of the training data.
**MODEL QUALITY** refers to the accuracy (mAP, Precision, Recall) of a detector trained on this data. 

*They are not the same thing.* The findings below pertain strictly to **Dataset Quality**.

## Dataset Pairing Confidence

**Finding:** The dataset pairings are obscured by physical Windows 8.3 short-name truncation during the archive extraction process on this environment.
- The `GetLongPathNameW` API reveals that the short names (e.g., `IM1A7B~1.JPG`) are the actual names on disk; long names were lost or omitted for images.
- Due to lack of deterministic long-name mapping, purely string-based deterministic pairing without relying on fragile alphabetical/sequential ordering is impossible.
- **Readiness Decision:** UNSAFE for direct pairing. 
- **Required Action Before Training:** The dataset must be re-downloaded/re-extracted without losing long names, OR the pairing must be forced if we are certain the alphabetical ordering precisely matches the label ordering. This model will NOT be trained on this specific local copy blindly.

## Malformed Annotations

A total of 66 malformed annotation files were discovered. These were audited without modifying the original files.

**Summary of Errors:**
- `empty_file`: 6 instances
- `wrong_number_of_fields`: 60 instances
- `non_numeric_value`: 0
- `class_id_outside_range`: 0
- `coordinate_outside_bounds`: 0
- `zero_negative_width_height`: 0

**Breakdown by Split:**
- **Train:** 51 files (3 empty, 48 wrong number of fields)
- **Valid:** 11 files (1 empty, 10 wrong number of fields)
- **Test:** 4 files (1 empty, 3 wrong number of fields)

**Treatment Strategy:**
During dataset loading for training, these files will be deterministically excluded from the dataset loader since they cannot be parsed by YOLO format parsers. Because the malformed count is very low (66 out of ~4,600), the dataset remains viable for training once the pairing issue is resolved.
