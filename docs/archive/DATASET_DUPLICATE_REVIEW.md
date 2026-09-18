# Dataset Cross-Split Duplicate Review

## Review Summary
- **Total candidates**: 220
- **Confirmed duplicates**: 220
- **Human reviewer status**: COMPLETE

*These 220 candidates were confirmed by human visual review as identical or effectively identical visual samples that incorrectly crossed benchmark splits.*

## Breakdown
- **Train ↔ Test**: 71
- **Train ↔ Valid**: 133
- **Valid ↔ Test**: 16
- **Confirmed cross-split duplication**: 220

## Duplicate Resolution Rules Applied
To ensure a robust, non-contaminated benchmark while strictly protecting the test set, the following reproducible derivation rules were applied:
1. **Train ↔ Test**: Kept TEST image, quarantined TRAIN image.
2. **Train ↔ Valid**: Preserved VALID image, quarantined TRAIN image.
3. **Valid ↔ Test**: Kept TEST image intact. Preserved VALID image. Documented contamination.

*Rule: The 455-image TEST benchmark remains 100% byte-for-byte untouched.*

## Dataset Counts

### Original Dataset
- **Train**: 3103
- **Valid**: 900
- **Test**: 455
- **Total**: 4458

### Verified Derivative (`Dataset/ChemEq25_training_verified`)
- **Train**: 2900 (203 unique contaminated training samples quarantined)
- **Valid**: 900
- **Test**: 455 (Strictly unchanged)
- **Total**: 4255

A detailed resolution trace exists in `outputs/dataset_audit/duplicate_resolution_manifest.csv`.
