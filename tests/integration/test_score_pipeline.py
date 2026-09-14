import pytest
import numpy as np
import cv2
import json
from lab_lens.pipeline import LabLensPipeline
from lab_lens.spatial.engine import SetupSpecification, SpatialRule
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

def test_pipeline_score_a_compliant(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0),
        Detection(1, "Stand", 0.9, 60.0, 10.0, 90.0, 90.0)
    ])
    setup = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    rules = [SpatialRule("left_of", "Beaker", "Stand")]
    res = pipeline.run(dummy_image, setup, rules)
    assert res.compliance_status == "COMPLIANT"
    assert res.compliance_result.score == 100.0

def test_pipeline_score_b_missing_object(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0)
    ])
    setup = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    res = pipeline.run(dummy_image, setup, [])
    assert res.compliance_status == "NON_COMPLIANT"
    assert res.compliance_result.score == 50.0

def test_pipeline_score_c_spatial_violation(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(1, "Stand", 0.9, 10.0, 10.0, 40.0, 40.0),
        Detection(0, "Beaker", 0.9, 60.0, 10.0, 90.0, 90.0)
    ])
    setup = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    rules = [SpatialRule("left_of", "Beaker", "Stand")]
    res = pipeline.run(dummy_image, setup, rules)
    assert res.compliance_status == "NON_COMPLIANT"
    assert abs(res.compliance_result.score - 66.6666) < 1.0 # 2/3 * 100

def test_pipeline_score_d_no_setup(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0)
    ])
    res = pipeline.run(dummy_image, None, None)
    assert res.compliance_status == "UNSPECIFIED"
    assert res.compliance_result is None

def test_pipeline_score_e_ambiguous_setup(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0)
    ])
    # Total conditions 0 -> UNSPECIFIED and score None
    setup = SetupSpecification("test", {})
    res = pipeline.run(dummy_image, setup, [])
    assert res.compliance_status == "UNSPECIFIED"
    assert res.compliance_result.score is None

def test_pipeline_score_f_malformed_setup(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0)
    ])
    setup = SetupSpecification("test", {"Beaker": 1})
    # Malformed rule: threshold = -1
    rules = [SpatialRule("inside", "Beaker", "work_zone", -1.0)]
    res = pipeline.run(dummy_image, setup, rules)
    assert res.compliance_status == "NON_COMPLIANT"
    assert res.compliance_result.score == 50.0

def test_score_invariants(dummy_image):
    pipeline = LabLensPipeline()
    pipeline.model_loaded = True
    pipeline.detector = MockDetector([
        Detection(0, "Beaker", 0.9, 10.0, 10.0, 40.0, 40.0)
    ])
    setup = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    res = pipeline.run(dummy_image, setup, [])
    
    assert res.compliance_result.score is not None
    assert 0.0 <= res.compliance_result.score <= 100.0
    
    # Determinism
    res2 = pipeline.run(dummy_image, setup, [])
    assert res.compliance_result.score == res2.compliance_result.score
