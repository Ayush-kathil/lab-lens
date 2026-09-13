# DETECTOR TEST EVALUATION

## 1. Evaluation objective
To perform a single, formal, reproducible evaluation of the trained Lab Lens detector on the completely held-out test split, without test-set tuning or leakage.

## 2. Git SHA
- 837eb83 (feat: complete stabilized detector baseline)

## 3. Environment
- **Python**: 3.12.14 AMD64
- **OS**: Windows 11
- **CPU**: Intel Core Ultra 5 125H
- **torch**: 2.2.0+cpu
- **torchvision**: 0.17.0+cpu
- **ultralytics**: 8.4.150
- **numpy**: 1.26.4

## 4. Model/checkpoint
- uns/detect/outputs/baseline_training_final/weights/best.pt
- YOLOv8n architecture

## 5. Dataset
- Dataset/ChemEq25_training/data.yaml

## 6. Train/valid/test counts
- **Train**: 3103
- **Validation**: 900
- **Test**: 455

## 7. Class mapping
0: Beaker
1: Buchner_Funnel
2: Burette_Stands
3: Calorimeter
4: Conical_Flask
5: Funnel
6: Glass_Rod
7: Measuring_Cylinder
8: Mechanical_Balance_Scale
9: Nessler_Reagent_Bottle
10: Pipette
11: Porcelain_Mortar Pestle
12: Precision_Weight_Scale
13: Reagent_Bottle
14: Round_Bottom_Flask_Borosilicate_Glass_1_Neck
15: Round_Bottom_Flask_Borosilicate_Glass_2_Neck
16: Round_Bottom_Flask_Borosilicate_Glass_3_Neck
17: Separating_Funnel
18: Spirit_Lamp
19: TestTube_Holder
20: Test_Tube
21: Volumetric_Flask
22: Volumetric_Pipet
23: Wash_Bottle
24: Weighing_Bottle

## 8. Exact evaluation configuration
- **Split**: test
- **Batch**: 8
- **Image Size (imgsz)**: 640
- **Device**: cpu

## 9. Overall test metrics
- **Precision**: 0.83925
- **Recall**: 0.83862
- **mAP@50**: 0.88067
- **mAP@50-95**: 0.59600

## 10. Per-class metrics
| Class | Precision | Recall | AP50 | AP50-95 |
| :--- | :--- | :--- | :--- | :--- |
| Beaker | 0.93378 | 1.00000 | 0.99230 | 0.70168 |
| Buchner_Funnel | 0.94007 | 0.90476 | 0.98375 | 0.68713 |
| Burette_Stands | 0.96856 | 1.00000 | 0.99500 | 0.59472 |
| Calorimeter | 0.97811 | 1.00000 | 0.99500 | 0.76342 |
| Conical_Flask | 0.91124 | 1.00000 | 0.98475 | 0.73250 |
| Funnel | 0.94847 | 0.92098 | 0.97107 | 0.67396 |
| Glass_Rod | 0.48256 | 0.87879 | 0.77862 | 0.44171 |
| Measuring_Cylinder | 0.85529 | 0.88889 | 0.90540 | 0.59465 |
| Mechanical_Balance_Scale | 0.93934 | 1.00000 | 0.99500 | 0.64768 |
| Nessler_Reagent_Bottle | 0.94945 | 1.00000 | 0.99500 | 0.74096 |
| Pipette | 0.50246 | 0.16858 | 0.40541 | 0.26051 |
| Porcelain_Mortar Pestle | 0.95912 | 1.00000 | 0.99500 | 0.66748 |
| Precision_Weight_Scale | 0.97816 | 1.00000 | 0.99500 | 0.79716 |
| Reagent_Bottle | 0.94027 | 0.93750 | 0.95988 | 0.61041 |
| Round_Bottom_Flask_Borosilicate_Glass_1_Neck | 0.81365 | 0.23810 | 0.60309 | 0.35271 |
| Round_Bottom_Flask_Borosilicate_Glass_2_Neck | 0.47877 | 0.50000 | 0.53392 | 0.36300 |
| Round_Bottom_Flask_Borosilicate_Glass_3_Neck | 0.62748 | 0.90625 | 0.83987 | 0.53422 |
| Separating_Funnel | 0.78602 | 0.94815 | 0.96526 | 0.66676 |
| Spirit_Lamp | 0.97897 | 1.00000 | 0.99500 | 0.74247 |
| TestTube_Holder | 0.83942 | 1.00000 | 0.98786 | 0.67101 |
| Test_Tube | 0.52918 | 0.37485 | 0.44416 | 0.23248 |
| Volumetric_Flask | 0.76967 | 0.83333 | 0.93341 | 0.61859 |
| Volumetric_Pipet | 0.95195 | 0.55000 | 0.78706 | 0.53413 |
| Wash_Bottle | 1.00000 | 0.91535 | 0.98103 | 0.68589 |
| Weighing_Bottle | 0.91921 | 1.00000 | 0.99500 | 0.58486 |

## 11. Confusion matrix
- Saved to uns/detect/val/confusion_matrix.png (and normalized variant).
- Axes represent True Class (rows) vs Predicted Class (columns).
- Background false positives/false negatives are represented as the last column/row.

## 12. PR curves if generated
- Precision-Recall curves saved to uns/detect/val/PR_curve.png.
- F1-Confidence curves saved to uns/detect/val/F1_curve.png.

## 13. Evaluation runtime
- Total execution was ~1 minute (Speed: 1.0ms preprocess, 98.5ms inference, 0.0ms loss, 1.6ms postprocess per image).

## 14. Comparison with validation metrics
VALIDATION (Epoch 3):
- P: 0.86165
- R: 0.85265
- mAP50: 0.89721
- mAP50-95: 0.61170

TEST (Held-out):
- P: 0.83925
- R: 0.83862
- mAP50: 0.88067
- mAP50-95: 0.59600

The model demonstrates excellent generalization to the held-out test set with minimal performance drop (~1.7 points mAP@50).

## 15. Limitations
- Certain overlapping classes (like varying necks of round bottom flasks or pipettes vs glass rods) show lower precision/recall, suggesting potential ambiguity in features or challenging visual angles.

## 16. Test-set tuning
Test results were purely observational. No model tuning, architectural changes, dataset modifications, or configuration sweeps were performed based on these test results.
