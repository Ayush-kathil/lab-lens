# Lab Lens

Lab-Lens — Vision-Based Laboratory Equipment Verification & Spatial Compliance System.

Lab Lens is a modular Computer Vision system designed to analyze laboratory images, identify equipment, reason about spatial arrangements, and verify compliance against a reference setup. It calculates explainable compliance scores and generates detailed reports, ensuring safety and standard operating procedure adherence in laboratory environments.

## Problem
Manual verification of laboratory setups is error-prone and time-consuming. Incorrect setups can lead to safety hazards or failed experiments. Lab Lens automates this process by applying object detection and spatial reasoning to workspace images.

## Motivation
This project serves as a serious academic and portfolio-grade engineering endeavor. It demonstrates the ability to build a robust, production-quality machine learning system that goes beyond a simple YOLO demo by incorporating spatial verification and explainable compliance reporting.

## Key Features
- **Image Quality Analysis** (Implemented): Assesses input images for blur, lighting, and resolution.
- **Dataset Validation & Repair** (Implemented): Mathematically validates and repairs cross-split leakage.
- **Object Detection** (Planned / Foundation built): Identifies 25 categories of lab apparatus.
- **Perspective Correction** (Planned): Optionally aligns images using homography and feature matching.
- **Spatial Reasoning** (Planned): Verifies if equipment is placed in the correct normalized workspace regions.
- **Compliance Scoring** (Planned): Computes an explainable score based on missing, misplaced, or extra equipment.
- **Report Generation** (Planned): Outputs JSON, Markdown, and annotated images.

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

## Dataset Usage

Lab Lens uses the **ChemEq25** dataset as the primary laboratory-equipment detection dataset.

*   **Dataset Source:** Official Figshare distribution ([Link](https://figshare.com/articles/dataset/_b_Chemistry_Lab_Image_Dataset_Covering_25_Apparatus_Categories_b_/29110433))
*   **License:** CC BY 4.0

*Note: The dataset is NOT committed to Git. The project expects the dataset to be located in the local `Dataset/ChemEq25_figshare/` directory.*

## Installation
```bash
git clone https://github.com/Ayush-kathil/Lab-lens.git
cd Lab-lens
pip install -r requirements.txt
```

## Dataset Setup
1. Download the official ChemEq25 dataset from Figshare.
2. Place it in `Dataset/ChemEq25_figshare/` at the project root and extract the `.rar` file inside it.
3. Validate: `python -m lab_lens validate-dataset --dataset Dataset/ChemEq25_figshare`

## Training (Planned / Scaffolded)
The training interface is scaffolded. Real training will be implemented in a future phase.
```bash
python -m lab_lens train --dataset Dataset/ChemEq25_training --config configs/training.yaml --dry-run
```

## Evaluation (Planned / Scaffolded)
```bash
python -m lab_lens evaluate --model outputs/best.pt --dataset Dataset/ChemEq25_training
```

## CLI Usage
```bash
python -m lab_lens quality --input path/to/image.jpg
python -m lab_lens audit-dataset-pairs --dataset Dataset/ChemEq25_figshare
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
ChemEq25: Chemistry Lab Image Dataset Covering 25 Apparatus Categories. Figshare. https://figshare.com/articles/dataset/_b_Chemistry_Lab_Image_Dataset_Covering_25_Apparatus_Categories_b_/29110433

## License
[Add License Here]
