# Model Selection Rationale

## Candidates Considered
1. **YOLOv8n**: Highly mature, universally supported across export formats (ONNX, CoreML, TFLite), stable API, lightweight, and heavily documented. Ideal for student projects and reproducible CPU deployments.
2. **YOLO11n**: Newer architecture with minor latency/AP trade-offs, but potentially less stable community support for edge exports.
3. **YOLO26n**: (Or other bleeding-edge architectures) - Rejected due to framework immaturity, high risk of API breaking changes, and lack of long-term reproducibility guarantees which are critical for an academic project.

## Final Selection
**YOLOv8n**
*Rationale*: For a laboratory equipment verification system running on potentially constrained student hardware (CPU-only, 16GB RAM), maturity and reproducibility strictly outweigh fractional mAP gains from experimental architectures. YOLOv8n guarantees API stability within the `ultralytics` package and provides the safest foundation for the spatial compliance reasoning that will be built on top of it.
