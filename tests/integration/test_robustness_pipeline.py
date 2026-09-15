import pytest
import os
import json
import numpy as np
import cv2
from lab_lens.pipeline import LabLensPipeline, LabLensResult
from lab_lens.spatial.engine import SetupSpecification, SpatialRule
from lab_lens.spatial.core import BoundingBox
from lab_lens.detection.detector import Detection

class MockDetector:
    def __init__(self, detections, fail=False):
        self._detections = detections
        self.model = True
        self.fail = fail
        
    def predict(self, img, conf_threshold=0.25):
        if self.fail:
            raise RuntimeError("Injected detector failure")
        return self._detections
        
    def load_model(self, path):
        pass

@pytest.fixture
def dummy_image(tmp_path):
    p = tmp_path / "valid.jpg"
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(str(p), img)
    return str(p)

def test_robustness_corrupted_image(tmp_path):
    p = tmp_path / "corrupted.jpg"
    with open(p, "wb") as f:
        f.write(b"random garbage bytes")
        
    pipeline = LabLensPipeline()
    result = pipeline.run(str(p))
    assert result.compliance_status == "ERROR"
    assert result.error == "UNREADABLE_IMAGE"

def test_robustness_empty_file(tmp_path):
    p = tmp_path / "empty.jpg"
    with open(p, "wb") as f:
        pass
    pipeline = LabLensPipeline()
    result = pipeline.run(str(p))
    assert result.compliance_status == "ERROR"
    assert result.error == "UNREADABLE_IMAGE"

def test_robustness_detector_exception(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([], fail=True)
    result = pipeline.run(dummy_image)
    assert result.compliance_status == "ERROR"
    assert "DETECTION_FAILED" in result.error

def test_robustness_detector_invalid_coordinates(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    # reversed boxes, zero area boxes
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 50.0, 50.0, 10.0, 10.0), # reversed
        Detection(1, "Stand", 0.9, 10.0, 10.0, 10.0, 10.0), # zero area
        Detection(2, "Flask", 1.5, 10.0, 10.0, 20.0, 20.0) # conf out of bounds, currently no check but spatial handles it
    ])
    result = pipeline.run(dummy_image)
    assert len(result.detections) == 1 # Only Flask gets through normalization since coordinate checks skip first two
    assert any("Invalid bounding box skipped" in w or "Zero-area normalized box" in w for w in result.warnings)

def test_robustness_setup_malformed_threshold(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0)
    ])
    setup = SetupSpecification("test", {"Beaker": 1})
    # Threshold < 0 or something, though spatial engine might just fail gracefully.
    rules = [SpatialRule("inside", "Beaker", "work_zone", -1.0)] 
    # Usually we just want to ensure it doesn't crash or return compliant on invalid rule
    # Actually wait, if work_zone is not defined, spatial engine handles missing regions gracefully.
    result = pipeline.run(dummy_image, setup, rules)
    assert result.compliance_status == "ERROR"
    assert result.error == "CONFIGURATION_ERROR"

def test_robustness_multiple_same_objects(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 20.0, 20.0),
        Detection(0, "Beaker", 0.9, 30.0, 30.0, 40.0, 40.0),
        Detection(0, "Beaker", 0.9, 50.0, 50.0, 60.0, 60.0)
    ])
    setup = SetupSpecification("multi", {"Beaker": 2})
    result = pipeline.run(dummy_image, setup, [])
    # 3 beakers found, 2 expected => NON_COMPLIANT
    assert result.compliance_status == "NON_COMPLIANT"
    ids = [d.id for d in result.detections]
    assert len(set(ids)) == 3
    assert all(i.startswith("Beaker_") for i in ids)

def test_robustness_json_serialization(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 20.0, 20.0)
    ])
    setup = SetupSpecification("multi", {"Beaker": 1})
    result = pipeline.run(dummy_image, setup, [])
    json_data = json.dumps(result.to_dict())
    assert "Beaker_1" in json_data
    assert "COMPLIANT" in json_data

def test_safety_invariant_missing_setup(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([Detection(0, "Beaker", 0.9, 10.0, 10.0, 20.0, 20.0)])
    result = pipeline.run(dummy_image, None, None)
    assert result.compliance_status == "UNSPECIFIED"
    assert result.compliance_status != "COMPLIANT"
