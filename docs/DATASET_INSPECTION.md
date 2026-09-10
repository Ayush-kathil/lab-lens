# Dataset Inspection Report

## Overview
Inspection of the existing workspace at `c:\Users\shiva\OneDrive\Documents\GitHub\Lab-lens` revealed an existing dataset located in the `Dataset/ChemEq25/` directory.

## Directory Structure
The dataset directory structure is as follows:
```
Dataset/
└── ChemEq25/
    ├── Metadata.csv (904.9 KB)
    ├── data.yaml (835 Bytes)
    ├── test/
    │   ├── images/
    │   └── labels/
    ├── train/
    │   ├── images/
    │   └── labels/
    └── valid/
        ├── images/
        └── labels/
```

## Dataset Configuration
The `data.yaml` file indicates this is a Roboflow-exported dataset:
- **Format**: YOLO format
- **Workspace**: dip-project-cktfe
- **Project**: chemistry-lab-apparatus-detn
- **Version**: 8
- **License**: CC BY 4.0
- **URL**: https://universe.roboflow.com/dip-project-cktfe/chemistry-lab-apparatus-detn/dataset/8

## File Counts & Splits
A file count on the directories produced the following actual figures:

| Split  | Images | Labels |
|--------|--------|--------|
| Train  | 3,220  | 3,220  |
| Valid  | 920    | 920    |
| Test   | 458    | 459    |
| **Total** | **4,598** | **4,599** |

*Note: There is a discrepancy of 1 file in the test set (458 images vs 459 labels), which must be handled during data loading.*

## Classes
The `data.yaml` defines `nc: 25` (25 classes). The actual class names found:
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

## Repository Status
- The repository was not previously initialized as a Git repository.
- There are no pre-existing code files or architectures to preserve in the current branch.
- The raw dataset is located within the workspace and must be excluded from Git versioning to prevent repository bloat.
