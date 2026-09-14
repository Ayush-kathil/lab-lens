# Lab Lens

Lab Lens is a vision-based laboratory equipment verification and spatial-compliance prototype that combines object detection, geometric spatial reasoning, explainable rule-based compliance evaluation, and transparent condition-coverage scoring.

This system is designed to analyze laboratory images, identify equipment, reason about spatial arrangements, and verify compliance against a reference setup. It calculates deterministic compliance scores and generates detailed reports. 

**Disclaimer**: The numerical compliance score represents explicit configured condition coverage and NOT physical safety probability. This is a prototype system and is not certified for physical laboratory safety or real-world safety enforcement.

## Key Features

### Implemented
- **Image Quality Analysis**: Assesses input images for blur, lighting, and resolution before inference.
- **Dataset Validation & Repair**: Mathematically validated, deterministically repaired cross-split leakage for the baseline dataset.
- **Object Detection**: YOLOv8-based detection identifying up to 25 categories of lab apparatus (trained on a CPU-friendly short baseline).
- **Spatial Reasoning**: Verifies spatial relations (e.g., `left_of`, `inside`, `near`) using geometric bounding box analysis. Validated against 21 canonical synthetic spatial exact-match fixtures.
- **Explainable Compliance Scoring**: Evaluates detected setups against explicit setup configurations, emitting a 0-100 score based on condition coverage (missing objects, extra objects, rule violations).
- **Integrated Pipeline**: End-to-end Python API and CLI (`LabLensPipeline`) connecting image reading, quality, detection, spatial reasoning, and compliance reporting.
- **Real-World AI-Silver Pilot**: End-to-end pipeline execution demonstrated on 16 authentic, licensed real-world photographs using AI-generated `SILVER_LABEL` annotations.

### Not Claimed / Limitations
- **No human-validated real-world spatial benchmark**: The AI-generated silver data is used for pipeline integration testing and does NOT represent human-validated ground truth.
- **Not a production deployment certification**: The system remains a research prototype.
- **Not a statistically calibrated safety probability**: Scores strictly reflect logical condition matching.

## Architecture & Computer Vision Techniques
Lab Lens is built with a modular Python architecture. Key boundaries include:
- `preprocessing/`: Quality checks (blur variance, brightness, contrast).
- `detection/`: Object detection interface utilizing Ultralytics YOLO.
- `spatial/`: Geometric relations, rule evaluations, and Cartesian spatial logic.
- `pipeline.py`: Main orchestration interface yielding structured `LabLensResult` datatypes.

## Datasets

### 1. ChemEq25 (Detector Training)
Lab Lens uses the **ChemEq25** dataset as the primary object-detection training resource.
- **Role**: Object detection only (no spatial compliance ground truth).
- **Source**: Official Figshare distribution ([Link](https://figshare.com/articles/dataset/_b_Chemistry_Lab_Image_Dataset_Covering_25_Apparatus_Categories_b_/29110433))
- **Status**: The protected 455-image test split has been retained, isolated, and remains unmodified for proper benchmarking.
- *Note: Raw datasets are ignored via `.gitignore` to prevent repository bloat.*

### 2. Synthetic Spatial Fixtures
- **Role**: Validates the spatial logic engine deterministically. Contains 21 exact-match synthetic geometric tests.

### 3. Real-World Silver Pilot
- **Role**: E2E pipeline integration testing. Contains 16 licensed real-world lab images. Annotations are strictly `AI_GENERATED` and `SILVER_LABEL`.

## Installation
```bash
git clone https://github.com/Ayush-kathil/Lab-lens.git
cd Lab-lens
pip install -r requirements.txt
```

## CLI Usage

Run the integrated end-to-end inference pipeline:
```bash
# Basic evaluation (Unspecified setup)
python -m lab_lens infer --image path/to/image.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt

# Compliance verification against a YAML setup
python -m lab_lens infer --image path/to/image.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/example_setup.yaml

# JSON output
python -m lab_lens infer --image path/to/image.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/example_setup.yaml --json
```

Other utilities:
```bash
python -m lab_lens quality --input path/to/image.jpg
python -m lab_lens audit-dataset-pairs --dataset Dataset/ChemEq25
python -m lab_lens evaluate --model runs/detect/outputs/baseline_training_final/weights/best.pt --dataset Dataset/ChemEq25
```

## Training & Evaluation
The detector was evaluated on the protected ChemEq25 test split. Performance represents a fast, CPU-trained baseline, not a state-of-the-art deployment:
- **Validation (Epoch 3)**: Precision: 0.86, Recall: 0.85, mAP50: 0.90
- **Held-out Test**: Precision: 0.84, Recall: 0.84, mAP50: 0.88

To train the detector (requires pre-configured `Dataset/ChemEq25`):
```bash
python -m lab_lens train --dataset Dataset/ChemEq25 --config configs/training.yaml
```

## Testing
```bash
pytest tests/
```

## Dataset Citation
ChemEq25: Chemistry Lab Image Dataset Covering 25 Apparatus Categories. Figshare. https://figshare.com/articles/dataset/_b_Chemistry_Lab_Image_Dataset_Covering_25_Apparatus_Categories_b_/29110433
