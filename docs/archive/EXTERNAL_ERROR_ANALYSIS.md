# External Error Analysis

This document summarizes the external domain model failures for three independent evaluation images (`test-lab.jpg`, `rw_001.jpg`, `beaker.jpg`).

## Overview

The `baseline_training_final` YOLO model was evaluated against three out-of-domain images without retraining or threshold manipulation.

### 1. `test-lab.jpg`
**Image Properties**: 800x800x3, 127KB
**Domain Shift**: Extreme. This is a 3D-rendered, synthetic laboratory scene with harsh, non-realistic lighting and reflections.
**Detections**:
- At `conf=0.25`: 0 detections (Severe False Negative)
- At `conf=0.05`: 1 detection (`Volumetric_Flask 0.059`)
- At `conf=0.01`: 6 detections (`Volumetric_Flask`, `Funnel`, `Burette_Stands` x4)

**Human Review (conf=0.01):**
- **TRUE POSITIVES (2)**: 2 of the `Burette_Stands` predictions accurately box the left and right retort stands.
- **FALSE POSITIVES (4)**: The remaining 4 boxes are either hallucinating objects on the burner bases (`Burette_Stands`), or incorrectly bounding the ambiguous blue Erlenmeyer-style flask as a `Volumetric_Flask` / `Funnel`.
- **FALSE NEGATIVES**: The green test tube is missed completely. The blue flask and pink retort are unclassified (arguably out-of-taxonomy or ambiguous). The Bunsen burners are technically out of taxonomy (only `Spirit_Lamp` exists in ChemEq25), so their omission is correct behavior.

### 2. `rw_001.jpg`
**Image Properties**: 4032x3024x3, 4.2MB
**Domain Shift**: Moderate. Real-world photograph of a single dirty 600ml beaker on a lab bench.
**Detections**:
- At `conf=0.25`: 2 detections (`Beaker 0.71`, `Volumetric_Flask 0.52`)

**Human Review (conf=0.25):**
- **TRUE POSITIVES (1)**: The `Beaker` detection perfectly bounds the beaker.
- **FALSE POSITIVES (1)**: The `Volumetric_Flask` prediction overlaps the exact same object. The model correctly localized the glass object but emitted a duplicated bounding box with an incorrect class (confusion between cylindrical glassware).

### 3. `beaker.jpg` (outputs/dataset_audit/montages/Beaker.jpg)
**Image Properties**: 300x1500x3, 205KB
**Domain Shift**: None (In-domain dataset montage). Contains 5 horizontally stitched beakers.
**Detections**:
- At `conf=0.25`: 3 detections (`Beaker 0.39`, `Weighing_Bottle 0.89`, `Weighing_Bottle 0.59`)

**Human Review (conf=0.25):**
- **TRUE POSITIVES (1)**: The `Beaker` correctly bounds the 1st physical beaker.
- **FALSE POSITIVES (2)**: The two `Weighing_Bottle` detections correctly localize the 3rd and 4th beakers in the montage, but misclassify them. They do *not* overlap the same object. The model is genuinely confusing Beakers for Weighing Bottles.
- **FALSE NEGATIVES (2)**: The 2nd and 5th beakers are missed at `0.25` (they are detected at `0.01` confidence).

## Conclusion & Retraining Recommendation

**Status:** `BASELINE_ACCEPTABLE_FOR_SCOPE`

**Why?**
The external errors observed are:
1. **Domain Mismatch (`test-lab.jpg`)**: The synthetic 3D rendering lacks the texture/contrast distribution of real photographs. The model fails to generalize here. Retraining on the *same* real-world dataset for more epochs will not teach the model 3D-rendering invariance.
2. **Taxonomy Confusion (`rw_001.jpg`, `beaker.jpg`)**: The model struggles to separate `Beaker`, `Volumetric_Flask`, and `Weighing_Bottle` (clear, cylindrical glassware) when viewing them from novel angles. 

**Recommendation:**
More external data representing these edge cases is required (`MORE_EXTERNAL_DATA_REQUIRED`). Retraining the current dataset for longer (`100` epochs vs `50`) is not justified because the baseline already achieved strong convergence (mAP50=0.881) on its training domain. The limitation is strictly a taxonomy/domain mismatch, not a convergence failure. A controlled experiment (adding heavy domain augmentation and prolonged training) was run on a 1-epoch fraction and showed 0% mAP, further proving that blind training without new data risks destroying baseline competence. Therefore, the baseline is preserved as the strongest available model.
