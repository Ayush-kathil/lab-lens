# BASELINE TRAINING REPORT

## 1. Git SHA
- **HEAD / origin/main**: f17c5a0

## 2. Environment
- **Python**: 3.12.14 AMD64
- **OS**: Windows-11-10.0.26200-SP0 (CPU-only)
- **torch**: 2.2.0+cpu
- **torchvision**: 0.17.0+cpu
- **ultralytics**: 8.4.150
- **numpy**: 1.26.4
- **Total RAM**: ~15.61 GB

## 3. Dataset counts
- **Train images**: 3103
- **Validation images**: 900
- **Test images**: 455

## 4. Model
- **Architecture**: YOLOv8n

## 5. Exact configuration
- **Batch size**: 8
- **Epochs**: 3
- **Image size (imgsz)**: 640
- **Workers**: 0
- **Cache**: False
- **Fraction**: 1.0
- **Seed**: 42
- **Device**: cpu

## 6. Run identifier
- outputs/baseline_training_final

## 7. Epoch 1 metrics
- **Train Loss (Box, Cls, DFL)**: 1.5199, 3.7786, 1.6960
- **Validation Metrics**: P: 0.54864, R: 0.61763, mAP50: 0.61676, mAP50-95: 0.38567

## 8. Epoch 2 metrics
- **Train Loss (Box, Cls, DFL)**: 1.3345, 2.4637, 1.5275
- **Validation Metrics**: P: 0.75032, R: 0.79052, mAP50: 0.81954, mAP50-95: 0.53676

## 9. Epoch 3 metrics
- **Train Loss (Box, Cls, DFL)**: 1.2766, 2.0410, 1.4617
- **Validation Metrics**: P: 0.86165, R: 0.85265, mAP50: 0.89721, mAP50-95: 0.6117

## 10. Training duration
- ~62 minutes total execution time (1.034 hours) for 3 complete epochs.

## 11. Validation duration
- ~1.6 minutes per epoch.

## 12. Peak RSS
- **Peak RSS**: 2441.56 MB (Batch 180 of Epoch 0)

## 13. Memory trend
- **Process RSS remained bounded and stable** over the observed training interval. It quickly climbed to ~2.4 GB during Epoch 0 and stayed consistently flat throughout Epoch 1, Epoch 2, and Epoch 3.

## 14. OOM status
- No OOM occurred.

## 15. Whether external interruption occurred
- **No external interruption occurred** during this final 3-epoch baseline run.

## 16. Artifact paths
- uns/detect/outputs/baseline_training_final (Training artifacts, weights)
- outputs/baseline_training_final/memory.csv (Memory telemetry)

## 17. Reproducibility statement
- The test split was not accessed. The historical atch=16 crash has been entirely bypassed by reducing batch size to 8, which establishes a stable, completely reproducible CPU training baseline.

## 18. Limitations
- atch=16 behavior still needs further root-cause isolation if larger batch sizes become strictly necessary in future experiments.
