# Lab Lens Project Statement

## Problem Statement
Laboratory setup verification often requires checking whether expected equipment is present and whether detected equipment satisfies explicitly defined spatial constraints. Manual verification can be repetitive, error-prone, and difficult to standardize across different operators. There is a need for an automated, configurable system that can analyze a laboratory workspace image, identify the equipment present, and verify its spatial arrangement against a reference configuration.

## Project Scope
Lab Lens is a Vision-Based Laboratory Equipment Verification & Spatial Compliance System prototype. It takes an image of a lab workspace, detects standard laboratory apparatus (using the ChemEq25 taxonomy), normalizes their coordinates, evaluates configured geometric spatial rules, and scores the setup based on rule fulfillment. The system strictly serves as a prototype for research and academic demonstration, calculating logical condition coverage rather than certifying physical laboratory safety.

## Target Users
- **Laboratory Technicians & Managers**: To aid in verifying setups before experiments begin via automated checks.
- **Students & Instructors**: For educational labs to review if student experiment setups match required reference configurations.
- **Computer Vision Researchers**: As a baseline for integrating object detection with deterministic spatial reasoning logic.

## High-Level Features
- **Configurable Workspace Layouts**: Users can define their expected lab setups and spatial rules via YAML configuration files.
- **Explainable Compliance Engine**: The system outputs specific reasons for failure (e.g., missing objects, extra objects, or spatial relation violations like "Beaker fails left_of relation with Stand").
- **Deterministic Scoring**: Generates a 0-100 score based explicitly on the percentage of satisfied configured conditions, distinct from statistical detector confidence.
- **Integrated Pipeline**: An end-to-end Python API and CLI that orchestrates image quality analysis, object detection, spatial reasoning, and JSON/human-readable reporting.
