# Final Report Results & Timings

This document aggregates the quantitative benchmarks and output statuses from the Lab Lens prototype for inclusion in the final VITyarthi report.

### A. Detector Validation Results (Epoch 3)
| Metric | Value |
|:---|:---|
| **Precision** | 0.86165 |
| **Recall** | 0.85265 |
| **mAP50** | 0.89721 |
| **mAP50-95** | 0.61170 |

### B. Detector Held-Out Test Results
| Metric | Value |
|:---|:---|
| **Precision** | 0.83925 |
| **Recall** | 0.83862 |
| **mAP50** | 0.88067 |
| **mAP50-95** | 0.59600 |

### C. Synthetic Spatial Exact-Match Result
- **Fixture Count**: 21 Canonical Fixtures
- **Accuracy**: 100% exact-match (deterministic geometry coverage). 
- *Note*: This validates the spatial reasoning mathematics. It is NOT a real-world spatial accuracy benchmark.

### D. Compliance Demonstration A (Compliant Setup)
- **Input**: `Dataset/SpatialComplianceReal/images/rw_001.jpg`
- **Config**: 1 Beaker, 1 Flask. Rule: Beaker `right_of` Volumetric_Flask
- **Outcome**: `COMPLIANT`
- **Score**: 100.0 / 100 (3 of 3 conditions satisfied)

### E. Compliance Demonstration B (Non-Compliant Setup)
- **Input**: `Dataset/SpatialComplianceReal/images/rw_001.jpg`
- **Config**: 1 Beaker, 1 Stand, 1 Flask. Rule: Beaker `left_of` Volumetric_Flask
- **Outcome**: `NON_COMPLIANT`
- **Score**: 50.0 / 100 (2 of 4 conditions satisfied, Missing Stand, Rule Failed)

### F. Compliance Demonstration C (Unspecified Setup)
- **Input**: `Dataset/SpatialComplianceReal/images/rw_001.jpg`
- **Config**: None
- **Outcome**: `UNSPECIFIED`
- **Score**: `null`

### G. Test Suite Result
- **Execution Command**: `pytest -q`
- **Total Tests**: 94
- **Passed**: 94
- **Failed**: 0
- **Skipped**: 0

### H. Measured Execution Timing (Demonstration Baseline)
*Recorded on CPU for Demonstration B. Excludes initial PyTorch model allocation overhead.*
- **Image Quality Analysis**: ~0.2146 s
- **Detector Inference**: ~1.2731 s
- **Spatial Reasoning**: ~0.0001 s
- **Compliance Scoring**: ~0.0000 s
- **Total Pipeline Execution**: ~1.5772 s
