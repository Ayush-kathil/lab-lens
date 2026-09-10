import pytest
import numpy as np
from lab_lens.detection.detector import Detection
from lab_lens.detection.inference import YOLODetector

def test_detection_dataclass():
    d = Detection(
        class_id=0,
        class_name="Beaker",
        confidence=0.95,
        x1=10.0,
        y1=10.0,
        x2=100.0,
        y2=100.0
    )
    assert d.class_id == 0
    assert d.class_name == "Beaker"
    assert d.confidence == 0.95
    assert d.x1 == 10.0

def test_yolo_detector_unloaded():
    detector = YOLODetector()
    with pytest.raises(RuntimeError):
        detector.predict(np.zeros((100, 100, 3), dtype=np.uint8))
        
    with pytest.raises(RuntimeError):
        detector.get_class_names()
        
    with pytest.raises(RuntimeError):
        detector.get_model_info()

def test_yolo_detector_invalid_path():
    detector = YOLODetector()
    try:
        from ultralytics import YOLO
    except ImportError:
        pytest.skip("Ultralytics not installed")
        
    with pytest.raises(FileNotFoundError):
        detector.load_model("nonexistent_model.pt")
