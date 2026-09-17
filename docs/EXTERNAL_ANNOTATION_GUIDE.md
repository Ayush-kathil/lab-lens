# External Annotation Guide

## Objective
The `ExternalLabBench` dataset relies on strictly independent human review. Model predictions (e.g., from `best.pt`) MUST NEVER be used to generate ground truth labels. This ensures the benchmark measures real-world generalization objectively.

## Launching the Tool
Use the scaffolded CLI tool:
```bash
python scripts/annotate_external_cli.py
```

## How to Inspect an Image
The CLI will open each pending image in an OpenCV window.
Review the image at full resolution. Look for objects belonging to the ChemEq25 taxonomy.

## Annotation Workflow
In the terminal, press one of the following keys based on the image content:
- **y (POSITIVE)**: The image contains one or more valid ChemEq25 objects. (Currently prompts for placeholder bounding box action. In a full UI, you would draw the boxes here).
- **n (NEGATIVE)**: The image contains NO ChemEq25 objects. This includes empty benches, unrelated equipment, or plain household glassware. This automatically creates an empty label file (`.txt`).
- **o (OUT_OF_TAXONOMY)**: The image contains valid laboratory equipment that is NOT part of the 25 classes.
- **a (AMBIGUOUS)**: The objects cannot be confidently classified by a human. Do NOT invent or force a label.
- **r (REJECT)**: The image is unusable (e.g., corrupted, watermark obscuring objects, synthetic collage).
- **q (QUIT)**: Save progress and exit.

## Drawing Bounding Boxes
*Note: Due to terminal limitations, exact box drawing requires extending the CLI with `cv2.selectROI` or a dedicated UI tool (like LabelImg/CVAT).*
For POSITIVE images, ensure you:
1. Select the exact ChemEq25 class.
2. Draw a tight bounding box around the visible extent of the object.
3. Record annotation notes (e.g., "partially occluded").
4. Log the reviewer name and timestamp.

## Strict Rules
- Do NOT run YOLO or any model to "pre-label" the images.
- A negative image must genuinely contain 0 targets.
- Do not fabricate annotations if an image is ambiguous.
