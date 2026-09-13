# REAL-WORLD SPATIAL ANNOTATION PROTOCOL

## 1. Image Selection
Images must be representative laboratory setups captured in real physical spaces.

## 2. Setup/Session Identification
Each image must be assigned a session_id corresponding to the physical laboratory apparatus arrangement. Any burst captures or viewpoint variations of the same physical layout share this ID.

## 3. Object Annotation
Annotators draw bounding boxes around equipment.
- Each object receives a unique object_id (e.g., lask_3).
- Each object receives a class_name matching the valid taxonomy.

## 4. Bounding-Box Rules
- Coordinates must be normalized to [0,1].
- Origin (0,0) is top-left.
- x1 < x2 and y1 < y2 must be strictly maintained (no zero-area boxes).

## 5. Object Identity Rules
Unlike synthetic rules that rely purely on subject_class (evaluating Cartesian products), real-world rules support explicit subject_id and 	arget_id. This allows specifying that a *specific* flask belongs in a *specific* zone.

## 6. Spatial Relation Annotation
Relations (left_of, ight_of, bove, elow, inside, overlaps, 
ear, ar) are documented explicitly. Annotators must distinguish between mathematically derived relations (e.g., box geometry happens to be left-of) and human-authored setup rules (e.g., the safety protocol mandates it MUST be left-of).

## 7. Setup Specification Annotation
The intended layout logic must be explicitly defined in the setup_specification block per image/session.

## 8. Compliance Annotation
Annotators must provide a strict boolean compliant flag determining if the setup physically meets the documented specification.

## 9. Violation Annotation
If compliant is false, a list of iolations must be provided specifying the exact failure (e.g., MISSING_OBJECT, MISPLACED_OBJECT).

## 10. Ambiguity/Rejection Rules
Images with severe occlusion, indistinguishable boundaries, or unresolvable setup intent must be labeled with an nnotation_status of AMBIGUOUS or REJECTED. Ambiguous images are excluded from benchmark ground truth.

## 11. Double Annotation
Stage 1: Annotator A completes the annotation.
Stage 2: Annotator B completes the annotation independently.

## 12. Inter-Annotator Agreement Methodology & Adjudication
- **Bounding Boxes**: Measured via average Intersection-over-Union (IoU).
- **Classification**: Measured via standard agreement rate.
- **Compliance Status**: Measured via Cohen's Kappa.
Stage 3 & 4: If Kappa falls below a defined threshold or a strict disagreement occurs on compliance status, a senior adjudicator reviews and finalizes the ground truth.

## 13. Quality Control
The dataset undergoes programmatic validation via RealWorldDatasetValidator checking schema constraints before integration.

## 14. Split Assignment
Assigned at the session_id level.

## 15. Versioning
Dataset versioning will follow SemVer based on significant additions or corrections to ground truth.
