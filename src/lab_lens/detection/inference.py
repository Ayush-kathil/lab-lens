import os
from typing import List, Dict, Any
import numpy as np

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

from .detector import Detection, Detector

class YOLODetector(Detector):
    def __init__(self):
        self.model = None
        
    def load_model(self, model_path: str) -> None:
        if not ULTRALYTICS_AVAILABLE:
            raise ImportError("Ultralytics package is required to load YOLO models.")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.model = YOLO(model_path)
        
    def predict(self, image: np.ndarray, conf_threshold: float = 0.25) -> List[Detection]:
        if self.model is None:
            raise RuntimeError("Model is not loaded. Call load_model() first.")
            
        results = self.model(image, conf=conf_threshold, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
                
            for box in boxes:
                conf = float(box.conf[0])
                if conf < conf_threshold:
                    continue
                    
                cls_id = int(box.cls[0])
                cls_name = self.model.names.get(cls_id, str(cls_id))
                xyxy = box.xyxy[0].cpu().numpy()
                x1, y1, x2, y2 = float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3])
                
                detections.append(Detection(
                    class_id=cls_id,
                    class_name=cls_name,
                    confidence=conf,
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2
                ))
                
        return detections

    def get_class_names(self) -> Dict[int, str]:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")
        return self.model.names

    def get_model_info(self) -> Dict[str, Any]:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")
        return {
            "type": "YOLO",
            "task": getattr(self.model, "task", "unknown"),
            "classes": len(self.model.names)
        }
