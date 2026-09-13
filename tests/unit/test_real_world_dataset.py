import pytest
import json
from pathlib import Path
from lab_lens.spatial import RealWorldDatasetValidator

def test_real_world_validator_success():
    path = "tests/fixtures/real_world/schema_fixtures.json"
    with open(path, 'r') as f:
        data = json.load(f)
    
    known = set()
    for sample in data:
        RealWorldDatasetValidator.validate_sample(sample, known)

def get_base_sample():
    return {
        "sample_id": "test_1",
        "session_id": "setup_001",
        "split": "train",
        "annotation_status": "ACCEPTED",
        "image_metadata": { "filename": "img1.jpg", "width": 1920, "height": 1080, "viewpoint": "front" },
        "objects": [
            { "object_id": "b1", "class_name": "Beaker", "box": {"x1": 0.1, "y1": 0.1, "x2": 0.3, "y2": 0.3} }
        ],
        "setup_specification": {
            "setup_name": "setup1",
            "required_objects": {"Beaker": 1},
            "regions": {"zone1": {"x1": 0.0, "y1": 0.0, "x2": 0.5, "y2": 0.5}},
            "spatial_rules": [
                {"rule_type": "inside", "subject_id": "b1", "target": "zone1"}
            ]
        },
        "ground_truth": {
            "compliant": True,
            "violations": []
        }
    }

def test_rw_validator_missing_key():
    s = get_base_sample()
    del s['session_id']
    with pytest.raises(ValueError, match="missing required key"):
        RealWorldDatasetValidator.validate_sample(s, set())

def test_rw_validator_duplicate_id():
    s = get_base_sample()
    known = {"test_1"}
    with pytest.raises(ValueError, match="Duplicate sample_id"):
        RealWorldDatasetValidator.validate_sample(s, known)

def test_rw_validator_invalid_geometry():
    s = get_base_sample()
    s['objects'][0]['box']['x1'] = 0.5
    s['objects'][0]['box']['x2'] = 0.5 # zero area
    with pytest.raises(ValueError, match="invalid zero-area or reversed box"):
        RealWorldDatasetValidator.validate_sample(s, set())

def test_rw_validator_unknown_object_ref():
    s = get_base_sample()
    s['setup_specification']['spatial_rules'][0]['subject_id'] = "unknown"
    with pytest.raises(ValueError, match="references unknown subject_id unknown"):
        RealWorldDatasetValidator.validate_sample(s, set())

def test_rw_validator_ambiguous_no_gt_required():
    s = get_base_sample()
    s['annotation_status'] = "AMBIGUOUS"
    s['ground_truth'] = {}
    RealWorldDatasetValidator.validate_sample(s, set()) # Should pass

def test_rw_validator_bad_status():
    s = get_base_sample()
    s['annotation_status'] = "UNKNOWN"
    with pytest.raises(ValueError, match="invalid annotation_status"):
        RealWorldDatasetValidator.validate_sample(s, set())
