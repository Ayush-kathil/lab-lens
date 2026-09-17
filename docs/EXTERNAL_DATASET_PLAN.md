# External Dataset Design Plan

## 1. Purpose
The purpose of the `ExternalLabBench` dataset is to provide a rigorous, independent benchmark measuring the production `baseline_training_final` model's ability to generalize to novel laboratory environments. It aims to quantify exact domain-shift and taxonomy-confusion failures outside of the 4224-image core `ChemEq25` dataset. 

## 2. Target Size
- Minimum: 50 fully annotated real laboratory images.
- Preferred: 75–100 images.

## 3. Inclusion Criteria
Images will be included if they contain:
- Known `ChemEq25` taxonomy classes.
- Visually similar or confusable classes (e.g., Beaker vs. Weighing Bottle).
- Multiple-object, cluttered laboratory scenes.
- Novel laboratory backgrounds, workbenches, or lighting setups.
- Different perspectives/viewpoints and partial occlusion.
- Objects at various scales (close-ups vs wide bench shots).
- Some empty or pure background images to act as hard negatives.
- Out-of-taxonomy laboratory equipment that is frequently encountered in the same environment.

## 4. Exclusion Criteria
- Generated collages or diagnostic montages (e.g., `beaker.jpg` from the dataset audit).
- Synthetic or 3D rendered models lacking real-world material reflectance, unless specifically partitioned into a synthetic evaluation suite.
- Images lacking clear provenance, source URLs, or appropriate licenses.
- Images that are duplicates or near-duplicates of the existing `ChemEq25` dataset splits.

## 5. Class Coverage Plan
We must capture challenging inter-class boundaries and ensure adequate coverage of:
- **Cylindrical clear glassware**: `Beaker`, `Conical_Flask`, `Volumetric_Flask`, `Round_Bottom_Flask` variants.
- **Delivery/Filtration glassware**: `Funnel`, `Buchner_Funnel`, `Separating_Funnel`.
- **Measurement glassware**: `Pipette`, `Volumetric_Pipet`, `Measuring_Cylinder`.
- **Bottles**: `Test_Tube`, `Nessler_Reagent_Bottle`, `Reagent_Bottle`, `Wash_Bottle`.
- **Support apparatus**: `Burette_Stands`, `TestTube_Holder`.

*Note: Uniform distribution is not required. The empirical distribution will be recorded.*

## 6. Hard-Negative Plan
The external dataset will deliberately introduce adversarial or "hard-negative" images:
- **No target apparatus**: General laboratory benches with no objects from the 25 classes.
- **Visual distractors**: Cylindrical shapes, plain drinking glasses, reflections in glass cabinets.
- **Unrelated equipment**: Multimeters, hot plates, generic lab stands not matching `Burette_Stands`.
- These objects must remain **unannotated** (or explicitly marked as out-of-taxonomy) to test the model's false-positive rejection.

## 7. Leakage Prevention
To guarantee absolute benchmark independence:
- No overlap with `Dataset/ChemEq25_training`, `Dataset/ChemEq25_training_verified_v2`, `Dataset/ChemEq25_training_verified_final`, or the protected 455-image `ChemEq25` test set.
- A cryptographic SHA256 exact-match check and an SSIM-based near-duplicate check against the protected test set will be strictly enforced prior to ingestion.

## 8. Provenance Policy
Each file must populate `outputs/external_evaluation/external_manifest.csv` with:
- `image_id`
- `path`
- `source` & `license` (Requires explicit open license or permission)
- `sha256`
- `width` & `height`
- `target_classes`
- `ground_truth_status`
