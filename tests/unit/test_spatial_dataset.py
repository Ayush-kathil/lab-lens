import pytest
import json
from pathlib import Path
from lab_lens.spatial import DatasetValidator, SpatialEvaluationHarness

def write_tmp_json(tmp_path, name, data):
    p = tmp_path / name
    with open(p, 'w') as f: json.dump(data, f)
    return str(p)

def base_sample():
    return {
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
    }

def test_dataset_validator_success(tmp_path):
    assert DatasetValidator.validate_file(write_tmp_json(tmp_path, "valid.json", [base_sample()]))

def test_dataset_validator_missing_keys(tmp_path):
    data = base_sample()
    del data["sample_id"]
    with pytest.raises(ValueError, match="missing required key"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "inv.json", [data]))

def test_dataset_validator_duplicate_id(tmp_path):
    with pytest.raises(ValueError, match="Duplicate sample_id"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "dup.json", [base_sample(), base_sample()]))

def test_dataset_validator_invalid_geometry(tmp_path):
    # Zero area x
    s1 = base_sample()
    s1["objects"] = [{"class_name": "A", "box": {"x1": 0.5, "y1": 0.1, "x2": 0.5, "y2": 0.2}}]
    with pytest.raises(ValueError, match="x1 >= x2"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "z1.json", [s1]))

    # Zero area y
    s2 = base_sample()
    s2["objects"] = [{"class_name": "A", "box": {"x1": 0.1, "y1": 0.5, "x2": 0.2, "y2": 0.5}}]
    with pytest.raises(ValueError, match="y1 >= y2"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "z2.json", [s2]))

    # Reversed x
    s3 = base_sample()
    s3["objects"] = [{"class_name": "A", "box": {"x1": 0.8, "y1": 0.1, "x2": 0.2, "y2": 0.2}}]
    with pytest.raises(ValueError, match="x1 >= x2"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "rev.json", [s3]))
        
    # Out of bounds > 1
    s4 = base_sample()
    s4["objects"] = [{"class_name": "A", "box": {"x1": 0.1, "y1": 0.1, "x2": 1.5, "y2": 0.2}}]
    with pytest.raises(ValueError, match="outside \\[0,1\\]"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "oob1.json", [s4]))

    # Out of bounds < 0
    s5 = base_sample()
    s5["objects"] = [{"class_name": "A", "box": {"x1": -0.1, "y1": 0.1, "x2": 0.5, "y2": 0.2}}]
    with pytest.raises(ValueError, match="outside \\[0,1\\]"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "oob2.json", [s5]))

def test_dataset_validator_invalid_region_geometry(tmp_path):
    s = base_sample()
    s["setup_specification"]["regions"] = {"zone": {"x1": 0.5, "y1": 0.1, "x2": 0.5, "y2": 0.2}}
    with pytest.raises(ValueError, match="invalid geometry"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "r1.json", [s]))

def test_dataset_validator_invalid_counts(tmp_path):
    s = base_sample()
    s["setup_specification"]["required_objects"] = {"A": -1}
    with pytest.raises(ValueError, match="non-negative integer"):
        DatasetValidator.validate_file(write_tmp_json(tmp_path, "c1.json", [s]))

def test_evaluation_harness(tmp_path):
    s = base_sample()
    s["setup_specification"]["required_objects"] = {"Beaker": 1}
    s["objects"] = [{"class_name": "Beaker", "box": {"x1": 0, "y1": 0, "x2": 0.5, "y2": 0.5}}]
    report = SpatialEvaluationHarness.evaluate_dataset(write_tmp_json(tmp_path, "test.json", [s]))
    assert report.total_samples == 1
    assert report.exact_matches == 1
    assert report.compliance_accuracy == 1.0

def test_actual_synthetic_fixtures_dataset():
    path = "Dataset/SpatialCompliance/synthetic_fixtures.json"
    assert DatasetValidator.validate_file(path)
    report = SpatialEvaluationHarness.evaluate_dataset(path)
    assert report.total_samples == 21
    assert report.exact_matches == 21
    assert report.compliance_accuracy == 1.0
