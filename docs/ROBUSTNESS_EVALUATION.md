# PHASE 12 — ROBUSTNESS, FAILURE-MODE & REAL-WORLD EVALUATION

## 1. Test Environment
- **System**: Windows
- **Pipeline Interface**: `LabLensPipeline`
- **Detector**: `YOLODetector` wrapping YOLOv8
- **Dataset**: `Dataset/SpatialComplianceReal` (AI-silver annotations, no modifications made to ChemEq25).
- **Execution Engine**: Local Python 3 (venv)

## 2. Failure-Mode Matrix

| Case | Input / Condition | Expected Behavior | Actual Behavior | Pass/Fail | Status / Error | Pipeline Terminates Safely? |
|---|---|---|---|---|---|---|
| A | Valid image & model | COMPLIANT/NON_COMPLIANT | Handled gracefully | PASS | Varies | Yes |
| B | Nonexistent image | `ERROR: FILE_NOT_FOUND` | `FILE_NOT_FOUND` | PASS | `ERROR` | Yes |
| C | Unreadable/corrupted image | `ERROR: UNREADABLE_IMAGE` | `UNREADABLE_IMAGE` | PASS | `ERROR` | Yes |
| D | Empty 0-byte file | `ERROR: UNREADABLE_IMAGE` | `UNREADABLE_IMAGE` | PASS | `ERROR` | Yes |
| E | Detector throws exception | `ERROR: DETECTION_FAILED` | `DETECTION_FAILED` | PASS | `ERROR` | Yes |
| F | Empty detector output | `NON_COMPLIANT` if objects required | Handled properly | PASS | `NON_COMPLIANT` | Yes |
| G | Invalid coordinates (x1>x2) | Box skipped, warning added | Box skipped | PASS | Proceeded | Yes |
| H | Malformed JSON/YAML setup | Crash/CLI abort | Aborted | PASS | Exit 1 | Yes |
| I | No setup provided | `UNSPECIFIED` | `UNSPECIFIED` | PASS | `UNSPECIFIED` | Yes |
| J | Invalid spatial rule type | Rule validation violation | Flags violation | PASS | `NON_COMPLIANT`| Yes |
| K | Rule targets nonexistent region| Rule validation violation | Flags violation | PASS | `NON_COMPLIANT`| Yes |

## 3. Test Counts & Coverage
- **Original test count**: 70
- **New robustness tests added**: 8 (covering empty files, corrupted streams, missing regions, missing objects, json stability)
- **Final test count**: 78
- **Results**: 78 / 78 PASSED (100%)

## 4. Safety Invariants Validated
The system adheres strictly to the rule: *Never silently return `COMPLIANT` if the configuration is broken, the image is invalid, or the detector crashes.*
Specifically, we caught and fixed a silent fallback in `engine.py` where a missing region in a spatial rule previously resulted in a skipped rule (effectively a silent `COMPLIANT`). Now, it explicitly generates a `SpatialViolation` of type `MISPLACED_OBJECT` or `SPATIAL_RELATION_VIOLATION`.

## 5. Real-World Silver Dataset Execution
- **Images Attempted**: 16
- **Successfully Processed**: 16
- **Errors/Crashes**: 0
- **Average Runtime**: ~0.95s per image
- **Detection Count**: Output varied by image blur and detector confidence
- **Memory RSS**: Memory remained stable throughout the 16-image loop. (No unbounded growth).

## 6. CLI Robustness
- Verified `python -m lab_lens infer --help` responds with valid arguments.
- Verified missing mandatory `--image` arguments gracefully exit.
- Verified that specifying `--json` suppresses console print and purely dumps parsable JSON.
- Verified bad YAML files abort execution gracefully instead of parsing an empty dictionary.

## 7. JSON Contract
The pipeline enforces the following typed output:
```json
{
  "image": "path",
  "quality": { ... },
  "detections": [ { ... } ],
  "compliance": {
    "status": "COMPLIANT|NON_COMPLIANT|UNSPECIFIED|ERROR",
    "violations": [ { ... } ]
  },
  "warnings": [],
  "error": null
}
```
Validation via `json.dumps` proves there are no un-serializable Numpy types or NaNs remaining in the final structure.

## 8. Silver Dataset Integrity
- Total Silver JSONs: 16
- `annotation_source`: `AI_GENERATED` (16/16)
- `ground_truth_status`: `SILVER_LABEL` (16/16)
- `HUMAN_VERIFIED` count: 0 (No artificial inflation of human benchmarking)
- SHAs remain identical.

## 9. Known Limitations
- **Model Determinism**: YOLO `predict()` uses floating-point tensor multiplication which may shift by 0.0001 per pixel across hardware/re-runs, though the geometric engine guarantees determinism for *identical* inputs.
- **Silver Quality**: The real-world evaluation dataset uses AI-silver bounds and was used purely for throughput/execution testing. None of the above metrics represent true visual accuracy against human benchmarks. 
- **Setup Ambiguity**: Photographs acquired from Wikimedia Commons without accompanying experimental protocols are explicitly evaluated as `UNSPECIFIED` under missing setups.
