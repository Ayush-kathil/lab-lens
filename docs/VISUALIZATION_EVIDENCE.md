# Visualization Evidence

This document details the generation of visual evidence for the VITyarthi project report, utilizing the actual Lab Lens prototype on the provided local image (`test-lab.jpg`).

## Methodology
The visualizations were generated via a dedicated script (`scripts/visualize_detection.py`) which orchestrates the identical inference pipeline components used in the primary Lab Lens CLI. 

- **Input Image**: `test-lab.jpg`
- **Model Checkpoint**: `runs/detect/outputs/baseline_training_final/weights/best.pt`
- **Objects Detected**: 0 (The YOLOv8 baseline model did not detect any equipment exceeding the minimum confidence threshold in this specific frame).

*Note: The script outputs exactly what the model predicts. No fake boxes or fabricated detections were injected to artificially populate the image.*

---

### Figure 1 — YOLO Detection Visualization

**Purpose**: 
Shows the actual equipment detections produced by the trained YOLOv8 model. 

- **Input image**: `test-lab.jpg`
- **Model checkpoint**: `runs/detect/outputs/baseline_training_final/weights/best.pt`
- **Detected classes**: None
- **Confidence values**: N/A
- **Output path**: `outputs/visualizations/test_lab_yolo_detection.jpg`

**Report-Ready Caption**:
> *Figure 1. YOLOv8-based laboratory equipment detection on the demonstration image. Bounding boxes and confidence values are generated directly from the trained detector.*

---

### Figure 2 — Edge/Contour Visualization

**Purpose**: 
Shows image-level edges/contours extracted using deterministic computer-vision processing (Gaussian blur followed by Canny edge detection). 

*Explicit Disclaimer*: This visualization is supplementary computer-vision evidence and is **NOT** used as the object-detection ground truth, nor does it alter the YOLO predictions.

- **Output path**: `outputs/visualizations/test_lab_edges.jpg`

**Report-Ready Caption**:
> *Figure 2. Edge and contour visualization of the same laboratory image using deterministic image-processing operations (Canny). This visualization illustrates image structure and is not used as detection ground truth.*

---

### Figure 3 — Combined Visualization

**Purpose**: 
An overlay showing both the deterministic Canny edges and the YOLO bounding boxes.

- **Output path**: `outputs/visualizations/test_lab_combined.jpg`

**Report-Ready Caption**:
> *Figure 3. Combined edge-contour and YOLOv8 bounding box representation. This overlays structural edges with the trained detection zones.*
