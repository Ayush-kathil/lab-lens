# Phase 5G.5 Memory Forensics Report

## 1. Environment
The environment was synced using uv sync. The authoritative uv.lock initially enforced 	orch==2.14.0 and 	orchvision==0.29.0. This default PyPI CUDA resolution resulted in a critical OSError: [WinError 1114] A dynamic link library (DLL) initialization routine failed. on c10.dll upon any import of PyTorch or Ultralytics.

## 2. Historical OOM
Historically observed to crash at Epoch 3 during baseline training. Checkpoints for Epoch 1 and 2 exist in outputs/baseline_training-3/weights/.

## 3. Measurement methodology
Planned to use psutil hooking into Ultralytics callbacks (on_train_epoch_end, on_train_batch_end).

## 4. Actual measurements
None could be taken initially. Python exited immediately upon import torch due to the DLL initialization failure.

## 5. Controlled experiments
Blocked by the environment failure.

## 6. Evidence
- uv.lock previously contained 	orch==2.14.0.
- Calling import torch threw OSError (WinError 1114).
- Testing 	orch==2.12.0+cpu (the alleged historical version) still resulted in WinError 1114 on this machine.
- Testing 	orch==2.2.0+cpu alongside 
umpy<2 resulted in successful import and CPU NMS execution.

## 7. Root-cause classification
- OOM Root Cause: UNRESOLVED.
- Environment Root Cause: CONFIRMED. Incompatible PyTorch version specified in the project lockfile. The default PyPI resolution pulled CUDA wheels, and older CPU wheels (2.12.0+cpu) also failed to initialize c10.dll on this host.

## 8. Fix / Phase 5G.1R Resolution
The environment was fixed by adding an explicit CPU index to pyproject.toml and pinning the verified working combination of 	orch==2.2.0+cpu, 	orchvision==0.17.0+cpu, and 
umpy<2.0. The uv.lock was regenerated and the test suite passes successfully.

## 9. Remaining limitations
Memory telemetry pending Phase 5G.5 implementation.

## 10. Recommended training configuration
Original baseline configuration (16 batch size, 640 imgsz, 3 epochs).
