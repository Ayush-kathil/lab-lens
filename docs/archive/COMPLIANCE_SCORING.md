# EXPLAINABLE COMPLIANCE SCORING

## 1. Status Semantics
The authoritative representation of compliance in Lab Lens is the categorical `status`.

- **COMPLIANT**: All explicitly required setup conditions (counts, boundaries, and spatial rules) are successfully met. No violations are present.
- **NON_COMPLIANT**: At least one explicit required condition is violated.
- **UNSPECIFIED**: No setup specification was supplied, or the supplied specification contains zero explicitly required conditions.
- **AMBIGUOUS**: The setup is insufficient to determine compliance (e.g. missing crucial definitions for required targets).
- **ERROR**: Internal pipeline execution failed (unreadable file, detector crash, poor image quality).

## 2. Score Definition & Formula
A `0-100` deterministic score is calculated ONLY when status is `COMPLIANT` or `NON_COMPLIANT`. For `UNSPECIFIED`, `AMBIGUOUS`, or `ERROR`, the score is `null`.

The score represents deterministic condition coverage, defined strictly as:

```
Score = (Satisfied Conditions / Total Conditions) * 100
```

Where:
- **Total Conditions** = `len(required_objects) + len(spatial_rules)`
- **Satisfied Conditions** = `(required objects exactly matching expected count) + (rules with zero violations)`

## 3. Handling Specific Violation Types

### Missing Objects
- Tracked when `detected_count < expected_count`.
- Fails the condition requirement for that object class.
- Reported explicitly as a `MISSING_OBJECT` violation in the JSON payload, along with the expected and detected counts.

### Extra Objects
- Tracked when `detected_count > expected_count` for an object explicitly named in `required_objects`.
- Fails the condition requirement for that object class.
- Objects completely absent from the setup spec are strictly ignored for compliance scoring (preserving the open-world paradigm of the lab without failing a setup just because a random beaker is on the side).

### Misplaced Objects / Spatial Violations
- Tracked if an object fails a geometric check (e.g. `inside`, `left_of`).
- Fails the condition requirement for that spatial rule.
- Reported as `MISPLACED_OBJECT` or `SPATIAL_RELATION_VIOLATION`. 
- If a target region is undefined or a target subject is completely missing, the rule explicitly yields a `SPATIAL_RELATION_VIOLATION`.

## 4. Confidence Separation
Detector confidence (`ai_confidence`) is intentionally excluded from the compliance score. 
The score measures *rule fulfillment*, not *statistical probability*. 
Detector metrics are exposed separately under the `detections` array.

## 5. Mathematical Invariants
- `0.0 <= score <= 100.0`.
- Missing objects, missing targets, or missing boundaries will strictly trigger a violation and prevent a `100.0` score (no silent fallbacks).
- Bit-perfect determinism: Repeating inference over the same mock-detections yields the exact same numeric score without permutation dependency.

## 6. Worked Example

**Setup configuration:**
```yaml
required_objects:
  Beaker: 1
  Stand: 1
spatial_rules:
  - rule_type: "left_of"
    subject_class: "Beaker"
    target: "Stand"
```

**Total Conditions:** 3 (Beaker count, Stand count, 1 spatial rule).

**Observed State A (Compliant):**
- 1 Beaker found. 1 Stand found. Beaker is left of Stand.
- Satisfied: 3.
- **Score:** (3 / 3) * 100 = `100.0`

**Observed State B (Missing & Misplaced):**
- 1 Beaker found. 0 Stands found.
- Satisfied count for Beaker: 1
- Satisfied count for Stand: 0 (Missing)
- Rule `left_of`: Failed (Stand is missing, rule un-evaluable).
- Satisfied: 1.
- **Score:** (1 / 3) * 100 = `33.3`

## 7. Limitations & Disclaimers
1. **Not a Safety Probability**: The score reflects condition coverage, not a statistical guarantee of physical lab safety.
2. **ChemEq25 Baseline**: True detector benchmarking is performed separately on the protected 455-image ChemEq25 test split. 
3. **Real-World AI-Silver Pilot**: The 16 real-world evaluations in this phase use `AI_GENERATED` bounds as a demonstration of pipeline throughput. They DO NOT represent human-validated ground-truth compliance accuracy.
