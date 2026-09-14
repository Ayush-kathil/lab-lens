# HUMAN ANNOTATION TODO

The autonomous agent has successfully acquired and verified the provenance of real-world laboratory photographs from Wikimedia Commons. The initial annotation workspace has been created with nnotation_status = "NEEDS_REVIEW".

To prepare this pilot benchmark for spatial engine evaluation, the **USER** must manually review each downloaded image and complete the annotation.

## Instructions for the Human Annotator

For every JSON file in Dataset/SpatialComplianceReal/annotations/:

1. **Verify Visibility**: Ensure the image opens and contains distinguishable laboratory equipment.
2. **Determine Status**: If the setup is too occluded, messy, or ambiguous to determine spatial requirements, change nnotation_status to "AMBIGUOUS" or "REJECTED".
3. **Annotate Objects**:
   - Provide bounding boxes (x1, y1, x2, y2 normalized to [0,1]) for visible equipment.
   - Assign a unique object_id (e.g., "beaker_1").
   - Assign a valid class_name (e.g., "Beaker").
4. **Identify Setup Requirements**:
   - Only if visually defensible, fill in the setup_specification (required objects, regions, and spatial rules).
   - *Note*: Remember to distinguish between what is merely *observed* vs what is *required*.
5. **Establish Ground Truth**:
   - Set compliant to 	rue or alse.
   - If alse, list the exact iolations (e.g., MISSING_OBJECT, MISPLACED_OBJECT).
6. **Finalize**: 
   - Change nnotation_status to "HUMAN_VERIFIED".

**WARNING**: Do NOT mark an annotation as HUMAN_VERIFIED unless a human has explicitly reviewed and approved it. AI proposals must be kept separate.
