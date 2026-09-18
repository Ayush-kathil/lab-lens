# End-to-End Pipeline User Guide

## Architecture
The end-to-end pipeline consolidates image preprocessing, YOLOv8 object detection, normalized coordinate translation, and geometric spatial reasoning. By adhering to a rigorous set of YAML-configured spatial rules, the system evaluates laboratory scenes deterministically for structural compliance. See `END_TO_END_ARCHITECTURE.md` for internal dependencies.

## Installation & Model Requirements
A trained YOLO checkpoint mapped to the 25-class ChemEq25 vocabulary is required for full physical inference.
```bash
pip install -r requirements.txt
```

## CLI Usage
The standard entry point exposes the `infer` command.

**Human-Readable Output**
```bash
python -m lab_lens infer --image path/to/image.jpg --model weights/best.pt --setup configs/spatial_rules.yaml
```

**JSON Structured Output**
```bash
python -m lab_lens infer --image path/to/image.jpg --model weights/best.pt --setup configs/spatial_rules.yaml --json
```

## Spatial Setup Specification
The pipeline processes YAML specifications describing intended experiments.
```yaml
setup_name: fractional_distillation
required_objects:
  Beaker: 1
  Round_Bottom_Flask_Borosilicate_Glass_1_Neck: 1
spatial_rules:
  - rule_type: above
    subject_class: Round_Bottom_Flask_Borosilicate_Glass_1_Neck
    target: Beaker
```

## Compliance Semantics
- **COMPLIANT**: All required objects are present exactly in configured quantities, and zero spatial violations were raised.
- **NON_COMPLIANT**: A required object is missing, an extra object violates a strict limit, or an observed geometric relation violates a specific spatial rule.
- **UNSPECIFIED**: No setup configuration was supplied. No arbitrary safety rating is hallucinated.
- **AMBIGUOUS**: Used in data ingestion schemas when specific safety rules cannot be verified directly from the photograph.
- **ERROR**: File corruptions, invalid image bounds, or failed model loading gracefully halts pipeline progression.

## Error Handling
The pipeline guarantees fail-safe executions. Errors like `UNREADABLE_IMAGE`, `MODEL_NOT_LOADED`, and `FILE_NOT_FOUND` cleanly interrupt inference. No exception acts as a silent pass for `COMPLIANT`.

## Limitations & Reproducibility
- **Model Inference Nondeterminism**: GPU inference hardware or floating-point variations may subtly alter boundary detections between separate system invocations.
- **AI Silver Annotations vs Real-World Accuracy**: The included `SpatialComplianceReal` pilot dataset contains AI-generated silver labels, NOT human-validated benchmarks. Do NOT confuse metrics calculated against synthetic fixtures with human-level accuracy claims.
- **Synthetic Metrics**: The `synthetic_fixtures.json` tests demonstrate mathematically correct spatial engine geometry but do not indicate real-world laboratory application readiness.
