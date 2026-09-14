import pytest
import cv2
import numpy as np
import os
import json
from lab_lens.pipeline import LabLensPipeline, LabLensResult
from lab_lens.spatial.engine import SetupSpecification, SpatialRule
from lab_lens.spatial.core import BoundingBox
from lab_lens.detection.detector import Detection

class MockDetector:
    def __init__(self, detections):
        self._detections = detections
        self.model = True

    def predict(self, img, conf_threshold=0.25):
        if self._detections is None:
            raise ValueError("Detector failed")
        return self._detections

    def load_model(self, path):
        pass

def create_dummy_image(path):
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(path, img)

@pytest.fixture
def dummy_image(tmp_path):
    p = tmp_path / "dummy.jpg"
    create_dummy_image(str(p))
    return str(p)

def test_pipeline_a_valid_compliant(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    # Provide a beaker and a stand, beaker is left of stand
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0),
        Detection(1, "Stand", 0.9, 60.0, 10.0, 90.0, 90.0)
    ])

    setup = SetupSpecification(
        setup_name="test_setup",
        required_objects={"Beaker": 1, "Stand": 1}
    )
    rules = [SpatialRule("left_of", "Beaker", "Stand")]

    result = pipeline.run(dummy_image, setup, rules)
    assert result.compliance_status == "COMPLIANT"

def test_pipeline_b_missing_object(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0),
    ])
    setup = SetupSpecification(
        setup_name="test_setup",
        required_objects={"Beaker": 1, "Stand": 1}
    )
    result = pipeline.run(dummy_image, setup, [])
    assert result.compliance_status == "NON_COMPLIANT"
    assert any(v.violation_type == "MISSING_OBJECT" for v in result.compliance_result.violations)

def test_pipeline_c_spatial_violation(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    # Stand is left of beaker, but rule requires beaker left of stand
    pipeline.detector = MockDetector([
        Detection(1, "Stand", 0.9, 10.0, 10.0, 40.0, 40.0),
        Detection(0, "Beaker", 0.9, 60.0, 10.0, 90.0, 90.0)
    ])
    setup = SetupSpecification(
        setup_name="test_setup",
        required_objects={"Beaker": 1, "Stand": 1}
    )
    rules = [SpatialRule("left_of", "Beaker", "Stand")]
    result = pipeline.run(dummy_image, setup, rules)
    assert result.compliance_status == "NON_COMPLIANT"
    assert any(v.violation_type == "SPATIAL_RELATION_VIOLATION" for v in result.compliance_result.violations)

def test_pipeline_d_no_setup(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0),
    ])
    result = pipeline.run(dummy_image)
    assert result.compliance_status == "UNSPECIFIED"

def test_pipeline_f_invalid_image():
    pipeline = LabLensPipeline()
    result = pipeline.run("does_not_exist.jpg")
    assert result.compliance_status == "ERROR"
    assert result.error == "FILE_NOT_FOUND"

def test_pipeline_g_invalid_coordinates(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    # Invalid x1 >= x2
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 40.0, 10.0, 10.0, 40.0),
    ])
    result = pipeline.run(dummy_image)
    assert len(result.detections) == 0
    assert any("Invalid bounding box skipped" in w for w in result.warnings)

def test_pipeline_h_empty_detections(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([])
    setup = SetupSpecification("test", {"Beaker": 1})
    result = pipeline.run(dummy_image, setup, [])
    assert result.compliance_status == "NON_COMPLIANT"
    assert len(result.detections) == 0

def test_pipeline_i_json_serialization(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([])
    result = pipeline.run(dummy_image)

    # Check if json serialization doesn't throw
    res_str = json.dumps(result.to_dict())
    assert isinstance(res_str, str)
    assert "UNSPECIFIED" in res_str

def test_pipeline_j_determinism(dummy_image):
    pipeline1 = LabLensPipeline()
    pipeline1.model_loaded = True
    pipeline1.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0),
        Detection(1, "Stand", 0.9, 60.0, 10.0, 90.0, 90.0)
    ])

    pipeline2 = LabLensPipeline()
    pipeline2.model_loaded = True
    pipeline2.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0),
        Detection(1, "Stand", 0.9, 60.0, 10.0, 90.0, 90.0)
    ])

    setup = SetupSpecification("test_setup", {"Beaker": 1, "Stand": 1})
    rules = [SpatialRule("left_of", "Beaker", "Stand")]

    res1 = pipeline1.run(dummy_image, setup, rules)
    res2 = pipeline2.run(dummy_image, setup, rules)

    assert json.dumps(res1.to_dict(), sort_keys=True) == json.dumps(res2.to_dict(), sort_keys=True)
