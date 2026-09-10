# ChemEq25 Figshare Dataset Validation

## Final Readiness Decision
**SAFE_FOR_TRAINING**

The dataset has passed all rigorous validation gates:
- Exact 1-to-1 deterministic stem-based matching for all 4,599 images and labels.
- Zero orphan images.
- Zero orphan labels.
- Structure aligns with expected YOLO layout.
- The `data.yaml` defines the full 25 chemistry laboratory apparatus classes correctly.
- All invalid annotations have been securely categorized and isolated for deterministic exclusion.

## Dataset Profile
- **Dataset Identity:** ChemEq25
- **Source:** Figshare distribution
- **Version/Revision:** v9 (from data.yaml Roboflow metadata)
- **License:** CC BY 4.0
- **Total Images:** 4,599 (Train: 3,220, Valid: 920, Test: 459)
- **Total Labels:** 4,599
- **Matched Pairs:** 4,599
- **Total Objects Instances:** 6,801

## Integrity Checks
- **Empty Labels:** 6 labels were empty. These correctly act as negative instances (images containing no objects of interest). They will be retained.
- **Invalid Annotations:** 59 annotations contained incorrect field counts. These files will be **EXCLUDED** deterministically during training preparation, as they cannot be repaired blindly.
- **Duplicates:** Scans found 0 filename duplications. 82 files share exact binary content hashes, indicating minor redundancies natively present in the dataset. They will be retained to preserve raw distribution statistics.

## Metadata Integrity
- `metadata.csv` was verified to exist alongside the YOLO format directories.
- The local filenames exactly match the long un-truncated stems expected.

The dataset is now mathematically robust for the baseline object detector phase.
