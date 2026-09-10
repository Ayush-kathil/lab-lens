# Data Directory

This directory is intended to hold symbolic links to large datasets, small custom evaluation datasets, and data preparation scripts.

## ChemEq25 Dataset

The primary dataset used for training the object detector is **ChemEq25** (Version 5).
Source: https://data.mendeley.com/datasets/zptphkynt6/5

### Expected Local Directory Structure

Do **NOT** commit the raw dataset to the Git repository.
Download the dataset and extract it. The expected structure is:

```
<project_root>/
└── Dataset/
    └── ChemEq25/
        ├── Metadata.csv
        ├── data.yaml
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
The `.gitignore` is configured to ignore the `Dataset/` folder at the root.

### How to Prepare the Dataset

1. Download the dataset from the Mendeley Data link.
2. Extract the archive.
3. Place the `ChemEq25` folder inside a `Dataset` directory at the project root.
4. Run the validation script to ensure data integrity:
   ```bash
   python -m labcrest validate-dataset
   ```

### Custom Evaluation Data
A separate dataset directory `data/custom_setups/` (tracked by Git) will hold:
- Reference setup images
- Correct setup images
- Intentionally incorrect setups (missing, extra, misplaced objects)
This is used to evaluate the Spatial Verification and Compliance Scoring components.
