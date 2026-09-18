# Phase 10R-C.3 Forensic Audit

## 1. Git State & Discrepancy Reconciliation
The previous report claimed Phase 10R-C.3 was accepted and committed at SHA `0e96d9f`. However, `0e96d9f` actually corresponds to the Phase 10R-C.2 completion commit ("feat: acquire contextual spatial setups for pilot dataset"). The Phase 10R-C.3 changes (AI annotation generation, schemas, test additions, and documentation) were present in the working tree but **uncommitted**. 

This audit successfully staged and tracked all intended artifacts, verifying their integrity before the final dataset freeze. `test_api.py` was identified as an accidental artifact and permanently removed. `docs/PHASE_5G6_REPORT.md` was identified as an uncommitted legitimate artifact from a past training telemetry phase and has been properly preserved.

## 2. Gemini CLI Usage
Gemini CLI was installed/available but was not used for the reported annotations. Annotations were generated using Antigravity's built-in multimodal vision capabilities via direct visual inspection and scripted normalization. No fabricated external CLI calls were claimed.

## 3. Silver-Label State & Human-Verified Protection
Every AI-generated annotation successfully records:
- `annotation_source = "AI_GENERATED"`
- `ground_truth_status = "SILVER_LABEL"`
- `annotation_status = "AI_GENERATED"`
- `review_required = true`

A programmatic assertion in the `RealWorldDatasetValidator` and `test_ai_silver_labels.py` ensures that `AI_GENERATED` cannot silently transition to `HUMAN_VERIFIED`. The repository's total `HUMAN_VERIFIED` count remains strictly **0**.

## 4. Compliance Inference Default
Compliance defaults to `compliant = null`. AI-inferred compliance is strictly recorded under `ground_truth.compliance_label = "AMBIGUOUS"`, reflecting the reality that intended setup requirements (e.g., specific rules for fractional distillation) cannot be universally established solely from visual appearances. 

## 5. Taxonomy Audit
The ChemEq25 detector taxonomy strictly recognizes classes like `Burette_Stands`, `Round_Bottom_Flask_Borosilicate_Glass_1_Neck`, and `Beaker`. 
- **Beaker**: Directly mapped.
- **Round Bottom Flask**: Directly mapped.
- **Burette / Stand / Condenser / Column**: Not universally present in the exact format in the detector vocabulary, so they were safely classified as `OTHER_LAB_EQUIPMENT` or isolated accurately (e.g., `Burette_Stands`), with their specific unmapped identities preserved in `unmapped_object_type`. This ensures zero corruption of the existing detector taxonomy.

## 6. Object-Box Audit
- All generated bounding boxes conform exactly to the normalized `0 <= x1 < x2 <= 1` range.
- Zero-area boxes: 0
- Reversed boxes: 0
- Out-of-range boxes: 0
- Duplicate object IDs: 0

## 7. Source Image Integrity & Provenance
- Recomputed SHA-256 matched exactly for all 16 acquired images against `source_manifest.json`.
- Matched: 16
- Mismatched: 0
- Missing: 0
Provenance metadata remains completely unaltered. Raw images correctly adhere to the `.gitignore` policy and have not been added to Git.

## 8. Visual Triage Audit
Classifications genuinely reflect visual content:
- **HIGH** (5): Complex visual multi-object setups (e.g., distillation).
- **LOW** (11): Collections of isolated equipment without interaction.
- **REJECTED** (8): Explicit non-photographic diagrams (`rw_012`, `rw_015`) and singleton items.
*Note: Dataset accepted status is distinct from spatial value; diagrams are rejected, but isolated photographs can be accepted with low spatial value.*

## 9. Spatial Relations & Intended Setup Audit
Observed relations (`left_of`, `above`, `near`) were constrained specifically to visually supported evidence and isolated from `required_relations`, which remain properly unidentified.
