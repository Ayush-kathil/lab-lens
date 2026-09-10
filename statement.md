# LabCrest Project Statement

## Problem Statement
In laboratory environments, ensuring the correct setup of equipment is crucial for safety, experimental accuracy, and compliance with standard operating procedures. Manual verification is error-prone, time-consuming, and difficult to standardize. There is a need for an automated system that can analyze a laboratory workspace, identify the equipment present, and verify its spatial arrangement against a reference configuration.

## Target Users
- **Laboratory Technicians & Managers**: To quickly verify setups before experiments begin.
- **Students & Instructors**: For educational labs to ensure students have set up their experiments safely and correctly.
- **Safety Inspectors**: For auditing laboratory compliance.

## Scope
LabCrest is a Vision-Based Laboratory Equipment Verification & Spatial Compliance System. It takes an image of a lab workspace, detects standard laboratory apparatus, analyzes their spatial distribution, and scores the setup based on a provided configuration file. 
The system focuses on common chemistry lab apparatus (e.g., beakers, flasks, pipettes) using the ChemEq25 dataset for object detection training.

## Objectives
- Build a modular, production-quality Computer Vision pipeline.
- Implement robust object detection for 25 categories of laboratory equipment.
- Develop a spatial verification engine to check for missing, misplaced, or extra equipment.
- Calculate an explainable compliance score.
- Generate machine-readable (JSON) and human-readable (Markdown) reports with annotated image outputs.

## Functional Requirements
1. **Input Validation**: The system must accept and validate image inputs (resolution, format) and configuration files (YAML).
2. **Image Quality Analysis**: The system must evaluate the input image for quality metrics (blur, lighting, resolution) and issue warnings if below thresholds.
3. **Object Detection**: The system must detect laboratory apparatus with bounding boxes and confidence scores.
4. **Spatial Verification**: The system must compare detected bounding boxes against expected regions defined in a setup configuration.
5. **Compliance Scoring**: The system must compute a compliance score based on detection completeness, spatial correctness, confidence, and image quality.
6. **Report Generation**: The system must output a detailed, explainable JSON report, a Markdown summary, and an annotated image.

## Non-Functional Requirements
- **Modularity**: The architecture must be decoupled (e.g., the detector must be an abstraction so the model can be swapped).
- **Command Line Interface (CLI)**: The system must be fully operable via CLI.
- **Performance**: Inference and processing should run reasonably fast on standard CPU hardware, without assuming access to a high-end GPU.
- **Reproducibility**: All experiments, configurations, and evaluation metrics must be trackable and reproducible.
- **Code Quality**: Adherence to PEP 8, comprehensive type hints, docstrings, and unit tests.

## High-Level Features
- **Configurable Workspace Layouts**: Users can define their expected lab setups via YAML.
- **Explainable AI**: The compliance engine outputs specific reasons for failure (e.g., "Beaker missing in the center region").
- **Perspective Correction (Optional)**: Employs homography and feature matching to align skewed images to a reference geometry when applicable.

## Constraints
- The ChemEq25 dataset provides only bounding box annotations. A small custom evaluation dataset must be curated or simulated for evaluating the spatial verification engine.
- System must be installable via standard Python tools (`pip`, `requirements.txt`).

## Expected Outcomes
- A complete, testable software package (`labcrest`).
- A trained object detection model (or clear instructions and scripts to train it).
- Comprehensive documentation, including architectural diagrams and algorithm explanations.
- A suite of automated tests and GitHub Actions CI pipelines.
