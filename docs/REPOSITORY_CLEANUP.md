# Repository Cleanup Audit

| Path | Classification | Reason | Deleted | Replacement / Reference |
|---|---|---|---|---|
| `runs/detect/outputs/` | REQUIRED_FOR_REPRODUCIBILITY | Baseline training artifacts required by README | NO | N/A |
| `runs/detect/predict/` | HISTORICAL_EVIDENCE | Historical prediction outputs | NO | N/A |
| `runs/detect/val/` | HISTORICAL_EVIDENCE | Validation metrics | NO | N/A |
| `outputs/dataset_audit/` | REQUIRED_FOR_REPRODUCIBILITY | All dataset duplicate verification CSVs and manifests | NO | N/A |
| `Dataset/ChemEq25_training/` | REQUIRED_FOR_REPRODUCIBILITY | Raw source dataset | NO | N/A |
| `Dataset/ChemEq25_training_verified_v2/` | HISTORICAL_EVIDENCE | Intermediate leakage-clean dataset | NO | `ChemEq25_training_verified_final` |

**Conclusion:** All existing artifacts have been classified as either REQUIRED_FOR_REPRODUCIBILITY or HISTORICAL_EVIDENCE. No files met the criteria for SAFE_TO_DELETE (disposable scratch artifacts).
