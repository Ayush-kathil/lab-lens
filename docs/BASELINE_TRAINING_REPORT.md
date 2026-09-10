# Experimental 3-Epoch CPU Baseline

**Date/Time:** 2026-09-11
**Git Commit SHA:** 9b76e6d
**Model:** YOLOv8n
**Dataset Path:** Dataset/ChemEq25_training/data.yaml

## A. Environment
- **Python:** 3.12.10
- **PyTorch:** 2.12.0+cpu
- **Ultralytics:** 8.4.146
- **Torchvision:** 0.27.0
- **Hardware:** Windows 11 CPU (Intel Core Ultra 5 125H)

## B. Dataset
- **Train:** 3,103 images
- **Valid:** 900 images
- **Test:** 455 images (Explicitly untouched and protected)

## C. Model
- **Architecture:** YOLOv8n.pt (Nano)

## D. Configuration
- **Fraction:** 1.0 (Full training split)
- **Epochs:** 3
- **Batch Size:** 16
- **Image Size:** 640
- **Device:** cpu
- **Workers:** 0 (Required to prevent Windows CPU dataloader freezing)
- **Seed:** 42

## E. Why 3 epochs were selected
3 epochs was selected as an operational CPU-constrained experimental baseline, not as a convergence target. The pre-flight analysis demonstrated that 100 epochs would consume approximately 26 continuous hours on this CPU-only environment.

## F. Actual training duration
- **Duration per epoch:** ~13 minutes 19 seconds (Epoch 1)
- **Validation duration:** ~1 minute 22 seconds
- **Total duration:** Run aborted prematurely after Epoch 1 validation.

## G. Actual validation metrics
*(From Epoch 1 before crash)*
- **Validation Images:** 900
- **Instances:** 1360
- **Precision (P):** 0.507
- **Recall (R):** 0.570
- **mAP@50:** 0.599
- **mAP@50-95:** 0.373

## H. Training-loss progression
*(Final batch of Epoch 1)*
- **box_loss:** 1.527
- **cls_loss:** 3.837
- **dfl_loss:** 1.690

## I. Known limitations (Run Failure)
The training run failed at the conclusion of Epoch 1 validation. 
- **Exact Exception:** `Error during training: No module named 'polars'`
- **Cause:** Ultralytics `8.4.146` requires the `polars` library to generate metric plots during validation. Because `ultralytics` was installed with `--no-deps` to avoid the massive `polars_runtime` download hanging the environment, the plotting logic threw an `ImportError`, crashing the training loop before Epoch 2 could commence.
- **Local Artifact Path:** `C:\Users\shiva\OneDrive\Documents\GitHub\Lab-lens\runs\detect\outputs\baseline_training` (Intentionally kept outside Git via `.gitignore`).

## J. Statement on Convergence
This is NOT a converged benchmark. It serves purely as an experimental mechanical verification of the pipeline.

## K. Statement on Test Split
The 455-image test split remains absolutely untouched. No metrics were derived from it, and it did not influence any hyperparameter or checkpoint decisions.

---
### Historical Data: Pipeline Smoke/Diagnostic Training Run (5% Fraction)
*(Previous run logs preserved)*
- **Date/Time:** 2026-09-11 (Commit: 0bc52d8)
- **Subset Definition:** 5% fraction (155 training images) due to CPU constraints
- **Duration:** ~45 seconds for 1 epoch on 5% fraction (10 batches)
- **Validation Metrics:** N/A (Validation step crashed due to missing torchvision C++ ops)
