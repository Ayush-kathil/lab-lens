import pytest
import json
from pathlib import Path
from lab_lens.spatial import DatasetValidator, SpatialEvaluationHarness

def test_dataset_validator_success(tmp_path):
    data = [{
        "sample_id": "1",
        "image_ref": "synth",
        "image_width": 100,
        "image_height": 100,
        "setup_specification": {
            "setup_name": "s",
            "required_objects": {},
            "regions": {},
            "spatial_rules": []
        },
        "objects": [],
        "expected_output": {"compliant": True, "violations": []}
    }]
    p = tmp_path / "valid.json"
    with open(p, 'w') as f: json.dump(data, f)
    
    assert DatasetValidator.validate_file(str(p))

def test_dataset_validator_failure(tmp_path):
    # Missing required key
    data = [{"sample_id": "1"}]
    p = tmp_path / "invalid.json"
    with open(p, 'w') as f: json.dump(data, f)
    
    with pytest.raises(ValueError, match="missing required key"):
        DatasetValidator.validate_file(str(p))
        
    # Duplicate ID
    data2 = [
        {"sample_id": "1", "image_ref": "", "image_width": 1, "image_height": 1, "setup_specification": {"setup_name": "", "required_objects": {}, "regions": {}, "spatial_rules": []}, "objects": [], "expected_output": {"compliant": True, "violations": []}},
        {"sample_id": "1", "image_ref": "", "image_width": 1, "image_height": 1, "setup_specification": {"setup_name": "", "required_objects": {}, "regions": {}, "spatial_rules": []}, "objects": [], "expected_output": {"compliant": True, "violations": []}}
    ]
    p2 = tmp_path / "dup.json"
    with open(p2, 'w') as f: json.dump(data2, f)
    with pytest.raises(ValueError, match="Duplicate sample_id"):
        DatasetValidator.validate_file(str(p2))

def test_evaluation_harness(tmp_path):
    # Valid setup mapping perfectly to independent oracle
    data = [{
        "sample_id": "1",
        "image_ref": "synth",
        "image_width": 100,
        "image_height": 100,
        "setup_specification": {
            "setup_name": "s",
            "required_objects": {"Beaker": 1},
            "regions": {},
            "spatial_rules": []
        },
        "objects": [{"class_name": "Beaker", "box": {"x1": 0, "y1": 0, "x2": 0.5, "y2": 0.5}}],
        "expected_output": {"compliant": True, "violations": []}
    }]
    p = tmp_path / "test.json"
    with open(p, 'w') as f: json.dump(data, f)
    
    report = SpatialEvaluationHarness.evaluate_dataset(str(p))
    assert report.total_samples == 1
    assert report.exact_matches == 1
    assert report.compliance_accuracy == 1.0

def test_actual_synthetic_fixtures_dataset():
    # Run against the real synthetic dataset we just generated
    path = "Dataset/SpatialCompliance/synthetic_fixtures.json"
    assert DatasetValidator.validate_file(path)
    report = SpatialEvaluationHarness.evaluate_dataset(path)
    assert report.total_samples == 22
    assert report.exact_matches == 22
    assert report.compliance_accuracy == 1.0
