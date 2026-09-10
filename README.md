# Lab Lens

Lab-Lens — Vision-Based Laboratory Equipment Verification & Spatial Compliance System.

Lab Lens is a modular Computer Vision system designed to analyze laboratory images, identify equipment, reason about spatial arrangements, and verify compliance against a reference setup. It calculates explainable compliance scores and generates detailed reports, ensuring safety and standard operating procedure adherence in laboratory environments.

## Problem
Manual verification of laboratory setups is error-prone and time-consuming. Incorrect setups can lead to safety hazards or failed experiments. Lab Lens automates this process by applying object detection and spatial reasoning to workspace images.

## Motivation
This project serves as a serious academic and portfolio-grade engineering endeavor. It demonstrates the ability to build a robust, production-quality machine learning system that goes beyond a simple YOLO demo by incorporating spatial verification and explainable compliance reporting.

## Key Features
- **Image Quality Analysis**: Assesses input images for blur, lighting, and resolution.
- **Perspective Correction**: Optionally aligns images using homography and feature matching.
- **Object Detection**: Identifies 25 categories of lab apparatus using a lightweight model.
- **Spatial Reasoning**: Verifies if equipment is placed in the correct normalized workspace regions.
- **Compliance Scoring**: Computes an explainable score based on missing, misplaced, or extra equipment.
- **Report Generation**: Outputs JSON, Markdown, and annotated images.

## Architecture
Lab Lens is built with a modular Python architecture. Key boundaries include:
- `preprocessing/`: Quality checks and image enhancements.
- `detection/`: Abstracted object detection interface.
- `spatial/`: Region logic and workspace verification.
- `scoring/`: Explainable compliance engine.
- `reporting/`: Generators for visual and text reports.

## Computer Vision Techniques
- Feature Matching & Homography (SIFT/RANSAC)
- Histogram/Contrast Enhancement
- Bounding Box Intersection & Spatial Mapping
- Deep Learning-based Object Detection (YOLO-family)

## Dataset
The primary dataset is **ChemEq25** (Version 5), containing 4,599 annotated images of 25 lab apparatus categories. 
*Note: The raw dataset is kept out of Git to maintain repository health.*

## Installation
```bash
git clone https://github.com/Ayush-kathil/Lab-lens.git
cd Lab-lens
pip install -r requirements.txt
```

## Dataset Setup
1. Download ChemEq25 from Mendeley Data.
2. Place it in `Dataset/ChemEq25/` at the project root.
3. Validate: `python -m lab_lens validate-dataset`

## Training
```bash
python -m lab_lens train --config configs/default.yaml
```

## Evaluation
```bash
python -m lab_lens evaluate --model outputs/best.pt
```

## CLI Usage
```bash
python -m lab_lens quality --input path/to/image.jpg
python -m lab_lens audit-dataset-pairs --dataset Dataset/ChemEq25
python -m lab_lens analyze --input path/to/image.jpg --config configs/lab_setup.yaml
```

## Example Output
The system generates:
- An annotated image visualizing boxes and regions.
- A JSON report detailing detection confidences and spatial matches.
- A Markdown summary explaining the compliance score and any warnings.

## Project Structure
- `src/Lab Lens/`: Core application logic.
- `tests/`: Unit and integration tests.
- `configs/`: YAML setup definitions.
- `docs/`: In-depth documentation (Architecture, Algorithms, Dataset).
- `scripts/`: Development and ML lifecycle scripts.

## Testing
```bash
pytest tests/
```

## Limitations
- ChemEq25 provides object detection labels but not spatial compliance ground truth.
- Perspective correction requires a clear reference frame to succeed.

## Future Work
- Support for 3D spatial reasoning.
- Real-time video feed verification.

## Dataset Citation
ChemEq25 Dataset Version 5. Mendeley Data. https://data.mendeley.com/datasets/zptphkynt6/5

## License
[Add License Here]
