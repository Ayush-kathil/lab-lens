import pytest
import cv2
import os
import json
from lab_lens.detection.inference import YOLODetector
from lab_lens.pipeline import LabLensPipeline

@pytest.fixture
def baseline_model_path():
    path = "runs/detect/outputs/baseline_training_final/weights/best.pt"
    if not os.path.exists(path):
        pytest.skip(f"Baseline model not found at {path}")
    return path

@pytest.fixture
def test_image():
    path = "test-lab.jpg"
    if not os.path.exists(path):
        pytest.skip(f"Test image not found at {path}")
    img = cv2.imread(path)
    if img is None:
        pytest.skip(f"Failed to load {path}")
    return img

def test_inference_bug_conf_forwarding(baseline_model_path, test_image):
    detector = YOLODetector()
    detector.load_model(baseline_model_path)
    
    # 1. Forwarding correctly & changing threshold changes output
    # At conf=0.5, we expect fewer detections than at conf=0.01 for test-lab.jpg
    dets_0_5 = detector.predict(test_image, conf_threshold=0.5)
    dets_0_01 = detector.predict(test_image, conf_threshold=0.01)
    
    count_high = len(dets_0_5)
    count_low = len(dets_0_01)
    
    assert count_low > count_high, f"Expected more detections at conf=0.01 than 0.5. Got {count_low} vs {count_high}"
    
    # 3. No cross-call state leaks
    # Consecutive calls should not leak
    dets_0_5_again = detector.predict(test_image, conf_threshold=0.5)
    assert len(dets_0_5_again) == count_high, "Cross-call state leakage detected for conf_threshold"
    
    # 4. Default behavior (0.25) remains unchanged
    dets_default = detector.predict(test_image)
    dets_0_25 = detector.predict(test_image, conf_threshold=0.25)
    assert len(dets_default) == len(dets_0_25), "Default conf_threshold is not 0.25"

def test_pipeline_json_consistency(baseline_model_path, test_image, tmp_path):
    pipeline = LabLensPipeline(model_path=baseline_model_path, conf_threshold=0.01)
    
    # We call run so the pipeline does the full path including to_dict
    cv2.imwrite(str(tmp_path / "test.jpg"), test_image)
    result = pipeline.run(str(tmp_path / "test.jpg"))
    
    report_dict = result.to_dict()
    
    # Check that output JSON has exactly the same detections as the detector object
    saved_img = cv2.imread(str(tmp_path / "test.jpg"))
    detector_dets = pipeline.detector.predict(saved_img, conf_threshold=0.01)
    assert len(report_dict['detections']) == len(detector_dets), "JSON output count mismatches detector output count"
