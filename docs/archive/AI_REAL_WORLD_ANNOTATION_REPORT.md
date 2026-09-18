# AI Real-World Annotation Report

**SCIENTIFIC DISCLAIMER:**
This dataset contains AI-generated silver annotations and is not a human-validated ground-truth benchmark. AI-generated compliance labels must not be interpreted as experimentally validated laboratory safety or procedural compliance.

## Overview
This report details the results of fully automating the annotation of 16 acquired real-world laboratory photographs using AI multimodal vision inference.

## Image Classification
- **Total images processed:** 16
- **ACCEPTED:** 8
- **AMBIGUOUS:** 0
- **REJECTED:** 8 (due to being non-photographic diagrams or isolated equipment lacking spatial context)

## Spatial Value Distribution
- **HIGH spatial-value:** 5 (Complex setups such as distillation and titration)
- **MEDIUM spatial-value:** 0
- **LOW spatial-value:** 11 (Isolated equipment)

## Annotation Statistics
- **Total objects detected:** 13
- **Object classes:** `Beaker`, `Burette`, `Flask`, `Stand`, `OTHER_LAB_EQUIPMENT`
- **Spatial relations observed:** 5
- **Unmapped equipment:** `condenser`, `fractionating column` (mapped safely to `OTHER_LAB_EQUIPMENT` to prevent taxonomy corruption)
- **AI confidence distribution:** `HIGH` (11), `MEDIUM` (2), `LOW` (0)
- **Invalid proposals:** 0 (all bounding boxes strictly normalized to `[0,1]`)
- **Corrected proposals:** 0

## Compliance Evaluation
- **Compliance labels:** `AMBIGUOUS` (16)
- **Ambiguous compliance count:** 16
*Reasoning*: While the AI successfully identified setups like "fractional distillation" and "titration", the AI lacks the specific human-intended setup requirements to definitively conclude if the setup is `COMPLIANT` or `NON_COMPLIANT` with arbitrary rules. Therefore, compliance defaults to `AMBIGUOUS` with `compliance_source = "AI_INFERENCE"`.

## Testing & Integrity
All 16 annotations successfully passed the `RealWorldDatasetValidator`. The `annotation_status` was updated to `AI_GENERATED` and the `ground_truth_status` to `SILVER_LABEL`. 
No annotations were falsely upgraded to `HUMAN_VERIFIED`. The original image SHA-256 hashes and provenance records in `source_manifest.json` remain untouched.
