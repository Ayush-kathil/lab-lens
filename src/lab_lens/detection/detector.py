from dataclasses import dataclass
from typing import List, Dict, Any, Protocol
import numpy as np

@dataclass
class Detection:
    class_id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float

class Detector(Protocol):
    def load_model(self, model_path: str) -> None:
        """Load the model from the given path."""
        ...

    def predict(self, image: np.ndarray, conf_threshold: float = 0.25) -> List[Detection]:
        """Run inference on a numpy image array and return typed detections."""
        ...

    def get_class_names(self) -> Dict[int, str]:
        """Return the class ID to name mapping."""
        ...

    def get_model_info(self) -> Dict[str, Any]:
        """Return metadata about the loaded model."""
        ...
