import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Optional

try:
    from ultralytics import YOLO
    import torch
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

@dataclass
class EvaluationConfig:
    weights_path: str
    dataset_yaml: str
    split: str = 'test'
    imgsz: int = 640
    device: str = 'cpu'
    batch: int = 8

class DetectorEvaluator:
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.model = None

    def validate_environment(self):
        if not ULTRALYTICS_AVAILABLE:
            raise RuntimeError("Ultralytics library is not installed.")
            
        weights = Path(self.config.weights_path)
        if not weights.exists():
            raise FileNotFoundError(f"Model weights not found at: {weights}")
            
        dataset = Path(self.config.dataset_yaml)
        if not dataset.exists():
            raise FileNotFoundError(f"Dataset YAML not found at: {dataset}")
            
        valid_splits = ['train', 'val', 'test']
        if self.config.split not in valid_splits:
            raise ValueError(f"Invalid split '{self.config.split}'. Must be one of {valid_splits}")

    def load_model(self):
        self.validate_environment()
        self.model = YOLO(self.config.weights_path)

    def evaluate(self) -> Dict[str, Any]:
        if self.model is None:
            self.load_model()
            
        # Run Ultralytics evaluation using standard test mode
        # By passing split='test', Ultralytics forces the dataloader to use test split
        results = self.model.val(
            data=self.config.dataset_yaml,
            split=self.config.split,
            imgsz=self.config.imgsz,
            device=self.config.device,
            batch=self.config.batch,
            plots=True,          # Will generate PR curves and Confusion matrix in run dir
            save_json=False
        )
        
        # Results contain metrics
        return {
            "overall": {
                "precision": results.results_dict['metrics/precision(B)'],
                "recall": results.results_dict['metrics/recall(B)'],
                "map50": results.results_dict['metrics/mAP50(B)'],
                "map50_95": results.results_dict['metrics/mAP50-95(B)']
            },
            "per_class": self._extract_per_class(results),
            "save_dir": str(results.save_dir),
            "speed": results.speed
        }
        
    def _extract_per_class(self, results) -> Dict[int, Dict[str, Any]]:
        # Results box metric class contains arrays for each class
        # p, r, f1, ap50, ap are accessible but we need to map them to class names
        class_metrics = {}
        names = results.names
        ap50 = results.box.ap50
        ap = results.box.ap
        
        # Ultralytics results.box has:
        # .p, .r, .f1, .ap50, .ap, .ap_class (class indices that were evaluated)
        ap_classes = results.box.ap_class_index if hasattr(results.box, 'ap_class_index') else results.box.ap_class
        p = results.box.p
        r = results.box.r
        
        for i, c in enumerate(ap_classes):
            class_metrics[c] = {
                "name": names[c],
                "precision": p[i],
                "recall": r[i],
                "map50": ap50[i],
                "map50_95": ap[i]
            }
            
        return class_metrics
