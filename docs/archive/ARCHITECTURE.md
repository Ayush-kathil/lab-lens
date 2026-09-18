# Lab Lens Architecture

## Overview
Lab Lens is structured as a modular Python package `lab_lens` providing core capabilities for image analysis, spatial verification, and configuration-driven compliance scoring for laboratory setups.

## Component Responsibilities

- **`config`**: Handles loading YAML configurations defining dataset paths, thresholds, and expected spatial arrangements.
- **`preprocessing`**: Responsible for input quality checks (blur, illumination) and necessary image enhancements prior to detection.
- **`detection`**: Abstraction layer for object detection models (e.g., YOLO).
- **`features`**: Classic CV feature matching (e.g., SIFT, homography).
- **`spatial`**: Maps object bounding boxes to normalized regions and verifies against the configured expectations.
- **`scoring`**: The compliance engine that computes the final score and determines MISSING, MISPLACED, or EXTRA components.
- **`reporting`**: Generates machine-readable JSON and annotated images summarizing the pipeline results.
- **`utils`**: Common logic such as robust input validation and logging.

## Data Flow
1. **Input**: Image path and YAML Config.
2. **Validation**: Check image decodability and extensions.
3. **Quality Check**: Reject or warn on poor image quality.
4. **Detection**: Identify apparatus and confidence scores.
5. **Spatial Mapping**: Map detections to regions (e.g., `center`, `top_left`).
6. **Verification**: Compare detected regions with expected setup regions.
7. **Scoring**: Output an explainable JSON report.

## Implemented (Phase 2)
- Core directory structure and Python package.
- YAML configuration loader and setup definitions.
- Initial validation utilities (image, extensions, decodability).
- Dataset validation and inspection CLI tools.

## Planned
- Image quality metrics.
- Object detector integration.
- SIFT/Homography perspective correction.
- Spatial verification engine.

## Not Yet Evaluated
- Spatial classification accuracy.
- End-to-end latency.
- Overall compliance precision/recall.
