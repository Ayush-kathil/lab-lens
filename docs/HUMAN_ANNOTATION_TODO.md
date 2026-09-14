# HUMAN ANNOTATION TODO

The autonomous agent has successfully acquired and verified the provenance of real-world laboratory photographs from Wikimedia Commons. A visual triage has been performed, and an Annotation Workbench has been created.

To prepare this pilot benchmark for spatial engine evaluation, the **USER** must manually review the HIGH value images and complete the annotation.

## Instructions for the Human Annotator

You can now use the local annotation workbench to perform this task rapidly.

1. Launch the workbench: `python scripts/annotation_workbench.py`
2. Open http://127.0.0.1:5000 in your browser.
3. Select a HIGH value sample (e.g., `rw_010`, `rw_011`, `rw_013`, `rw_014`, `rw_016`).
4. **Annotate Objects**: Draw bounding boxes directly on the image and assign classes.
5. **Establish Setup Specification & Ground Truth**: 
   - Enter the `setup_name` and indicate whether the setup is `true` or `false` (compliant).
   - *Note*: If the setup is too occluded, messy, or ambiguous, you may change the annotation status to "AMBIGUOUS" or "REJECTED".
6. **Finalize**: 
   - Change Annotation Status to "HUMAN_VERIFIED" and save.

See `docs/REAL_WORLD_ANNOTATION_WORKBENCH.md` for more details on the workbench UI.

**WARNING**: Do NOT mark an annotation as HUMAN_VERIFIED unless a human has explicitly reviewed and approved it. AI proposals must be kept separate.
