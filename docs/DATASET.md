# ChemEq25 Dataset

## Provenance
- **Dataset Name**: ChemEq25
- **Source**: Mendeley Data (https://data.mendeley.com/datasets/zptphkynt6/5)
- **Version**: 5
- **License**: CC BY 4.0
- **Format**: YOLO / COCO-compatible annotations

## Dataset Provenance

*   **Original Mendeley artifact:** REJECTED FOR TRAINING
    *   *The downloaded Mendeley archive was unsuitable for deterministic image-annotation pairing because the extracted filenames were irreversibly truncated.*
*   **Roboflow distribution:** UNAVAILABLE / NOT USED
*   **Official Figshare artifact:** CURRENT CANDIDATE
    *   *Source: https://figshare.com/articles/dataset/_b_Chemistry_Lab_Image_Dataset_Covering_25_Apparatus_Categories_b_/29110433*
    *   *Structure: Contains full length un-truncated filenames allowing exact 1-to-1 mapping.*

## Characteristics
The dataset is intended for laboratory apparatus detection.
According to the source, the dataset characteristics are:
- 4,599 annotated images
- 25 laboratory apparatus categories
- 6,960 annotated instances
- Split: ~70% training, ~20% validation, ~10% testing

*Local inspection confirms 4,598 images and 4,599 labels.*

## Local Directory Structure
```
Dataset/
└── ChemEq25/
    ├── Metadata.csv
    ├── data.yaml
    ├── test/
    ├── train/
    └── valid/
```

## Classes
The following 25 classes are annotated in this dataset:
1. Beaker
2. Buchner_Funnel
3. Burette_Stands
4. Calorimeter
5. Conical_Flask
6. Funnel
7. Glass_Rod
8. Measuring_Cylinder
9. Mechanical_Balance_Scale
10. Nessler_Reagent_Bottle
11. Pipette
12. Porcelain_Mortar Pestle
13. Precision_Weight_Scale
14. Reagent_Bottle
15. Round_Bottom_Flask_Borosilicate_Glass_1_Neck
16. Round_Bottom_Flask_Borosilicate_Glass_2_Neck
17. Round_Bottom_Flask_Borosilicate_Glass_3_Neck
18. Separating_Funnel
19. Spirit_Lamp
20. TestTube_Holder
21. Test_Tube
22. Volumetric_Flask
23. Volumetric_Pipet
24. Wash_Bottle
25. Weighing_Bottle

## Intended Use
This dataset is strictly used for training and evaluating the **Object Detection** module of Lab Lens. 
It provides the bounding boxes to detect WHAT apparatus is present.

## Limitations
ChemEq25 provides **object-detection annotations only**. It does NOT provide ground truth for spatial correctness, missing objects, or overall setup compliance. 
Therefore, spatial verification and compliance scoring must be evaluated on a separate, custom evaluation dataset that contains reference setups and intentionally incorrect configurations.

## Ethical & Reproducibility Notes
- This dataset is not created or owned by the author of this project.
- It must not be committed to this Git repository to maintain reproducibility without bloating the repository history.
- Ensure the `Dataset/` directory remains locally cached or is symlinked as `data/raw/` (or similar) when developing.
