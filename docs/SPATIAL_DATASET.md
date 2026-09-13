# CUSTOM SPATIAL DATASET

## 1. Overview
The Dataset/SpatialCompliance/ dataset evaluates the deterministic spatial reasoning implementation. 
This dataset validates the deterministic spatial reasoning implementation under controlled examples. **It does not establish real-world laboratory spatial compliance accuracy.**

## 2. Why ChemEq25 is Excluded
ChemEq25 is an object-detection dataset containing bounding boxes around equipment. It does not provide setup requirements, spatial relations, or compliance status. Retrofitting ChemEq25 to act as spatial ground truth would fabricate non-existent scientific truth.

## 3. Dataset Structure
Currently, the dataset consists of an independent, static oracle file:
Dataset/SpatialCompliance/synthetic_fixtures.json

This file is explicitly authored. While a generator script exists in scripts/, it is restricted to an optional development utility and does not overwrite the canonical fixtures automatically.

## 4. Annotation Schema
Each example implements the following JSON schema:
- sample_id: Unique string identifier
- image_ref: Origin of the image ("synthetic" for pure coordinate tests)
- setup_specification: Object comprising setup_name, equired_objects, egions, and spatial_rules.
- objects: Ground truth object detections containing class_name and ox (x1, y1, x2, y2).
- expected_output: A static, independent oracle containing compliant (boolean) and a list of expected iolations.

## 5. Evaluation Harness
The SpatialEvaluationHarness parses the configuration and objects, processes them through the engine, and explicitly compares the resulting ComplianceResult against the independent expected_output.
It produces a metric termed **"Synthetic Fixture Exact-Match Accuracy"**. It does not generate expected outputs or modify the ground truth.
