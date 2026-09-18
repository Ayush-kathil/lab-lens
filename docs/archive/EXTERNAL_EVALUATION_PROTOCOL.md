# External Evaluation Protocol

## 1. Overview
This protocol dictates the process for manually annotating and programmatically evaluating the `ExternalLabBench` benchmark against the `baseline_training_final` model. 

## 2. Annotation Rules
- Ground truth must be constructed by independent human review. 
- **DO NOT** use the `best.pt` model (or any ML model) to auto-generate the ground truth.
- Annotations will be saved in standard YOLO format inside `Dataset/ExternalLabBench/labels/`. Image and label files must be deterministically paired by filename.
- If full annotation is impractical, limit the image count rather than accepting partial annotations as complete.
- Explicit "no target object" images will have an empty label file.
- Canny edge outputs must remain structurally isolated and cannot be used to aid or manipulate the YOLO ground-truth annotations.

## 3. Threshold Policy
Evaluations will be conducted statically at specific confidence thresholds:
- `0.50`, `0.25`, `0.10`, `0.05`
- The `ExternalLabBench` dataset is **EVALUATION_ONLY**. You must **NOT** tune thresholds based on performance over this set. If threshold optimization is required in the future, a separate external development set must be compiled.

## 4. Evaluation Metrics
An automated evaluation script will parse the model predictions against the human ground-truth labels and report:
- Overall Precision & Recall
- mAP50 & mAP50-95
- Per-class Precision, Recall, and AP
- Standard Confusion Matrix
- False Positives, False Negatives, Missed Objects, Duplicate Detections, and Class Confusions.

## 5. Error Taxonomy
During human review of challenging external failures, predictions must be assigned to one of the following error categories:
- `TRUE_POSITIVE`: Valid object and correct class.
- `FALSE_POSITIVE`: Non-target or background incorrectly localized.
- `FALSE_NEGATIVE`: Target object entirely missed by the detector.
- `DUPLICATE_DETECTION`: Multiple predictions for the same physical object.
- `CLASS_CONFUSION`: Object correctly localized, but assigned the wrong class (e.g., Beaker vs Volumetric_Flask).
- `OUT_OF_TAXONOMY`: Prediction on a valid laboratory object that does not exist in the 25-class `ChemEq25` taxonomy.
- `AMBIGUOUS`: Human reviewer cannot ascertain the ground-truth class.

## 6. Special Subsets Analysis
Targeted diagnostic subsets will be evaluated specifically to detect known failure patterns:
- **Beaker Confusion Subset**: Tracks the confusion matrix strictly across `Beaker`, `Conical_Flask`, `Volumetric_Flask`, and `Round_Bottom_Flask`.
- **Measurement / Support Glassware Subset**: Tracks the confusion across `Pipette` vs `Volumetric_Pipet`, and `Funnel` vs `Buchner_Funnel` vs `Separating_Funnel`.

## 7. Limitations & Final Decisions
This protocol is intended to determine the necessity of future ML cycles. Following evaluation, the status will be escalated from `MORE_EXTERNAL_DATA_REQUIRED` to one of the following outcomes:
A. Baseline is adequate for project scope.
B. Targeted retraining is justified (Experimental mode only, changing minimal variables).
C. Additional training data is required.
D. Taxonomy redesign is required.
E. Evidence insufficient.
