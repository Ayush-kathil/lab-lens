# SPATIAL ENGINE EVALUATION

## 1. Scope
This phase focuses strictly on the deterministic evaluation and mathematical property validation of the RuleEngine against the immutable canonical synthetic fixtures. It does not introduce new features or layout predictions.

## 2. Canonical Dataset Description
The dataset resides at Dataset/SpatialCompliance/synthetic_fixtures.json. It is a static, explicitly authored oracle comprising 21 bounding box configurations that span expected valid setups, isolated single-rule failures, multiple violations, missing objects, and boundary alignments. 

## 3. Evaluation Protocol
The SpatialEvaluationHarness executes a strict evaluation cycle:
1. **Load**: Read the JSON fixture.
2. **Validate**: Assert structural schema correctness.
3. **Construct**: Build RuleEngine configurations dynamically.
4. **Evaluate**: Process pseudo-detections yielding a ComplianceResult.
5. **Compare**: Compare predictions explicitly against the independent oracle fields.

## 4. Exact-Match Result
- **Total Fixtures**: 21
- **Exact Matches**: 21
- **Synthetic Fixture Exact-Match Accuracy**: 100.00%
- Hash immutability verified prior to and post-evaluation in automated testing.

## 5. Relation Coverage
All 8 implemented relations were verified via synthetic fixtures and explicit mathematical tests:
- left_of: Positive/negative (tested in harness & unit)
- ight_of: Positive/negative (tested in harness & unit)
- bove: Positive/negative (tested in harness & unit)
- elow: Positive/negative (tested in harness & unit)
- inside_region: Positive/negative (tested in harness & unit)
- overlaps: Positive/negative (tested in harness & unit)
- 
ear: Positive/negative (tested in harness & unit)
- ar: Positive/negative (tested in harness & unit)

## 6. Boundary Semantics
Boundaries behave exactly according to the defined math:
- left_of / ight_of: Strict inequality (<, >). Identical centers yield False.
- bove / elow: Strict inequality (<, >). Identical centers yield False.
- inside_region / overlaps: Inclusive threshold inequality (>=). Exactly meeting the threshold yields True.
- 
ear / ar: Inclusive threshold (<=, >=).

## 7. Mathematical Invariants Tested
- **Bounding Box properties**: width >= 0, height >= 0, rea > 0. Valid object centers mathematically rest within box edges.
- **IoU & Intersections**: Symmetricity (A iou B == B iou A), clamped rigorously into bounds [0,1].
- **Exclusivity**: left_of and ight_of are mutually exclusive for distinct centers.

## 8. Count Semantics
- Zero Expected vs Zero Detected = Compliant.
- Zero Expected vs Positive Detected = EXTRA_OBJECT.
- Positive Expected vs Zero Detected = MISSING_OBJECT.
- Classes omitted entirely from equired_objects dictionary do not participate in counting. They coexist invisibly as background elements without triggering violations.

## 9. Multiple-Object Semantics
When spatial rules define constraints across multi-instanced classes (e.g. 2 Beakers left_of 2 Funnels), the engine calculates the Cartesian product. Every single instance of the subject class must satisfy the geometric relation against every single instance of the target class. 

## 10. Determinism Results
Tested via 	est_spatial_evaluation.py. Executing the API iteratively over the same dataset produces perfectly identical serialized ComplianceResult reports across arbitrary repetitions.

## 11. Limitations
The Cartesian product behavior for multiple objects simplifies calculations but sacrifices uniqueness matching (e.g., Hungarian algorithm 1:1 mapping). 

## 12. Explicit Statement
This evaluation validates deterministic agreement between the spatial engine and a static synthetic ground-truth fixture. It does not establish real-world spatial-compliance accuracy.
