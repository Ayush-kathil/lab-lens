# Real-World Annotation Workbench

This document describes how to use the local Annotation Workbench for Lab Lens Phase 10R-C.2.

## Overview

The workbench is a lightweight local web application built with Flask and HTML5 Canvas. It allows a human annotator to:
1. View real-world licensed laboratory photographs.
2. Draw normalized bounding boxes (0 to 1) around objects.
3. Assign class names and unique object IDs.
4. Modify the `annotation_status` (e.g., set to `HUMAN_VERIFIED`).
5. Set the spatial compliance `ground_truth` to `true`, `false`, or `null` (unreviewed).
6. Specify the `setup_name`.

## Requirements
- Python 3.x
- Flask (`pip install flask`)

## Installation and Launch

1. Activate the project virtual environment (if not already active):
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. Install Flask (if required):
   ```bash
   pip install flask
   ```

3. Run the workbench script:
   ```bash
   python scripts/annotation_workbench.py
   ```

4. Open a web browser and navigate to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage Instructions

1. **Select a Sample:** Click on a sample ID in the left sidebar to load it. The `[NEEDS_REVIEW]` or `[HUMAN_VERIFIED]` status is shown.
2. **Add Objects:** Type a class name (e.g., `beaker`, `flask`) in the "New Object Class" input. Click and drag on the image canvas to draw a bounding box. The object will be added to the object list with a normalized bounding box and unique ID.
3. **Delete Objects:** Click the `X` button next to an object in the list to remove it.
4. **Update Status & Ground Truth:** Change the dropdowns for "Annotation Status" and "Compliant". An unreviewed sample should be kept as "null".
5. **Save:** Click the "Save Annotation" button to overwrite the JSON file in `Dataset/SpatialComplianceReal/annotations/`. The sidebar will update the status immediately.

## Data Schema Compliance
The workbench natively reads and writes the Phase 9 Real-World Annotation Schema, ensuring that coordinates are written as `[x1, y1, x2, y2]` floats between 0 and 1, and that `compliant` defaults to `null` rather than a false negative.
