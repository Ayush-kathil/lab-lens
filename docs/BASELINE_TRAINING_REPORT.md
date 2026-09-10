# Pipeline Smoke/Diagnostic Training Run

**Date/Time:** 2026-09-11
**Git Commit SHA:** 0bc52d8
**Model:** YOLOv8n
**Dataset Path:** Dataset/ChemEq25_training/data.yaml
**Subset Definition:** 5% fraction (155 training images) due to CPU constraints
**Image Size:** 640
**Batch Size:** 16 (Actual CPU baseline)
**Epochs:** 1
**Device:** CPU
**Seed:** 42

## Software Versions
- **Python:** 3.12
- **PyTorch:** 2.12.0+cpu
- **Ultralytics:** 8.2.0
- **NumPy:** 1.26.x
- **OpenCV:** 4.13.0
- **PyYAML:** 6.0.3

## Hardware Information
- **OS:** Windows 11
- **CPU:** Intel64 Family 6
- **RAM:** 15.61 GB
- **GPU:** NOT AVAILABLE

## Training Run
- **Output Location:** `outputs/baseline_training/`
- **Duration:** ~45 seconds for 1 epoch on 5% fraction (10 batches)
- **Validation Metrics:** N/A (Validation step crashed)
- **Warnings/Errors:**
  - `UserWarning: 'pin_memory' argument is set as true but no accelerator is found`
  - `_pickle.UnpicklingError: Weights only load failed` (Resolved via monkeypatching `torch.load` initially)
  - `Error during training: operator torchvision::nms does not exist`

### Root Cause Analysis & Remediation
The crash occurred during the validation NMS step because `torchvision-0.29.0` (which requires PyTorch 2.14) was installed against the system's PyTorch `2.12.0+cpu`. This ABI mismatch meant compiled C++ operators (like NMS) were missing. 

**Remediation:**
1. Installed `torchvision==0.27.0` which is perfectly binary-compatible with `torch==2.12.0+cpu`.
2. Verified `torchvision.ops.nms` executes successfully.
3. Upgraded `ultralytics` to `8.4.146` (with `--no-deps`) which natively handles the PyTorch 2.6 `weights_only=True` unpickling behavior, safely eliminating the need for any `torch.load` monkeypatch.
4. Set `workers: 0` explicitly in the baseline config to prevent Windows CPU dataloader freezing.
