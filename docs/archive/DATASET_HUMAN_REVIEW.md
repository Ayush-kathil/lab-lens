# Dataset Human Review Dashboard

This dashboard tracks the status of the required human review for dataset anomalies prior to retraining.

## Dataset Integrity Status
- **TRAIN**: 3103
- **VALID**: 900
- **TEST**: 455
- **TOTAL**: 4458

*All physical files and labels remain 100% byte-for-byte unmodified. The protected test split is preserved.*

## Near-Duplicate Candidates
- **Coarse Candidates (dHash)**: 225
- **Strong Candidates (SSIM > 0.90)**: 220
  - **Train ↔ Test (Priority 1)**: 71
  - **Train ↔ Valid (Priority 2)**: 133
  - **Valid ↔ Test (Priority 3)**: 16
- **Confirmed Leakage**: 0 (Automated count pending human verification)
- **Human Reviewed**: 0

*Review Interface*: `outputs/dataset_audit/montages/train_test/` (etc.)
*Verdict CSV*: `outputs/dataset_audit/near_duplicate_human_review.csv`

## Geometric BBox Outliers
- **Suspicious BBoxes**: 16 pending review
- **Empty Labels**: 6 pending review

## Overall Retraining Status
**RETRAINING = BLOCKED**
*Retraining is suspended until the high-risk Train ↔ Test candidate review is resolved by a human.*
