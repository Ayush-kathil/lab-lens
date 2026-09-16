# Model Retraining Report

## 1. Baseline Context
- **Old Baseline**: `runs/detect/outputs/baseline_training_final/weights/best.pt` (Trained on 3 epochs).
- **Dataset Audit Verification**: The dataset is structurally verified and semantically sample-audited; exhaustive semantic correctness was not established.
- **Dataset Used**: `Dataset/ChemEq25_training` (3103 Train, 900 Valid, 455 Test).

## 2. New Training Configuration (Smoke Test)
To verify the training loop while respecting sandbox resource limits, a proof-of-concept pipeline was executed:
- **Epochs**: 1 (Extremely constrained; recommend an explicit budget like `epochs=50` or `100` with `patience=10` for real convergence).
- **Early Stopping Patience**: 1
- **Batch Size**: 32 (Calculated empirically for CPU sandbox limits).
- **Image Size**: 160 (Optimized for smoke test speed. Production must remain at `imgsz=640` unless experimental ablation proves otherwise).
- **Augmentations Applied**:
  - `hsv_h: 0.015`, `hsv_s: 0.7`, `hsv_v: 0.4`
  - `degrees: 10.0`, `translate: 0.1`, `scale: 0.5`
  - `fliplr: 0.5`, `mosaic: 1.0`
- **Hardware**: CPU. (Note: GPU training is highly recommended as a future acceleration path).

## 3. Metrics Comparison
- **Old mAP50**: (From baseline)
- **New mAP50**: `0.288`
- **Classification**: TRAINING PIPELINE SMOKE TEST RESULT (Not a production model).
- **Validation**: Performed on the verified `valid` split.

## 4. Real-World External Evaluation (Phase 16)
These images were explicitly held out and evaluated strictly after model selection:
- **test-lab.jpg**: Raw prediction via smoke test model yields 0 detections at conf 0.25. 
- **Beaker Image**: The false-positive `Volumetric_Flask` remains. 

## 5. Limitations & Future Retraining Strategy
No software inference defect was identified; observed failures are currently attributable to the model's predictions, with insufficient training duration (3 epochs) and domain mismatch as candidate contributing factors. 

When retraining is finally authorized for production, it will be executed in a new versioned repository (e.g., `runs/detect/outputs/domain_augmented_v1/`), preserving the baseline directory untouched. The test set (`test` split) must never be used to tune confidence thresholds, IoU, model sizes, or augmentations.
