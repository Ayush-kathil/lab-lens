# End-to-End Architecture

## System Diagram
```mermaid
graph TD
    A[Input Image] --> B[Image Quality / Preprocessing]
    B -->|QualityResult| C[Object Detection YOLO]
    C -->|Raw Detections| D[Normalization & ID Assignment]
    D -->|DetectionPosition[]| E[Spatial Reasoning Engine]
    E -->|SpatialViolation[]| F[Compliance Logic]
    F -->|ComplianceResult| G[Structured Result LabLensResult]
    G --> H[JSON Output]
    G --> I[Human Readable CLI]
```

## Module Responsibilities

1. **Configuration**: Loaded via `lab_lens.config.loader` and YAML setup specification parsing in the CLI `__main__.py`.
2. **Image Quality / Preprocessing**: `lab_lens.preprocessing.image_quality` performs blurring, contrast, and brightness checks.
3. **Detector**: `lab_lens.detection.detector` interface (e.g., `YOLODetector`), loads the `best.pt` YOLO model and returns `Detection` models in pixel coordinates.
4. **Detection Normalization**: Internal to `LabLensPipeline`, maps pixel coordinates to mathematically verified `[0,1]` spaces, validates geometry (fails zero-area or reversed boxes), and sequentially tags items with IDs (e.g., `Flask_1`).
5. **Spatial Reasoning**: `lab_lens.spatial.engine` processes `DetectionPosition` inputs using the `GeometricRelations` module.
6. **Real-world Dataset Validation**: Separated into `RealWorldDatasetValidator`, enforcing AI silver label provenance. Used for validating testing sets, isolated from live E2E inference.
7. **Compliance Result**: Combines spatial engine violations and missing/extra objects into a `NON_COMPLIANT` or `COMPLIANT` explicit state. If no setup is requested, strictly returns `UNSPECIFIED` rather than fabricating safety status.
8. **Reporting**: Exists within the `LabLensResult` dataclass which seamlessly provides strict typing for Python integrations, machine-parseable JSON for web services, and CLI formatting for human reviewers.

## Contract / Object Passing
- The pipeline strictly uses internal dataclasses (e.g., `DetectionPosition`, `ImageQualityResult`, `ComplianceResult`) rather than passing massive unstructured python dictionaries.
- Invalid components are flagged into the `warnings` and `error` attributes to guarantee safe failure execution.
