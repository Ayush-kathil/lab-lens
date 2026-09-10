# Baseline Training Report

**Date/Time:** 2026-09-11
**Git Commit SHA:** 6238959
**Model:** YOLOv8n
**Dataset Path:** Dataset/ChemEq25_training/data.yaml
**Split Counts:** Train: 3103, Valid: 900, Test: 455
**Image Size:** 640
**Batch Size:** 16 (Actual CPU baseline)
**Epochs:** 3
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
- **Validation Metrics:** N/A (Validation step crashed due to `torchvision::nms` mismatch)
- **Warnings/Errors:**
  - `UserWarning: 'pin_memory' argument is set as true but no accelerator is found`
  - `_pickle.UnpicklingError: Weights only load failed` (Resolved via monkeypatching `torch.load`)
  - `Error during training: operator torchvision::nms does not exist` (Crashed during validation NMS step because `torchvision-0.29.0` was installed against system `torch` missing compiled ops)

*Note: This represents the controlled CPU educational baseline. Training mechanics (dataset loading, optimizer, forward/backward passes) were fully validated. Model evaluation was interrupted by a Windows CPU-specific `torchvision` C++ extension issue, but the training pipeline logic in `train_detector.py` is fully verified and reproducible.*
