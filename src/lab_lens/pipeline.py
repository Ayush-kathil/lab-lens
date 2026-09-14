import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import cv2
import numpy as np

from .detection.detector import Detection
from .detection.inference import YOLODetector
from .spatial.core import BoundingBox, DetectionPosition, ComplianceResult, SpatialViolation, ViolationType
from .spatial.engine import RuleEngine, SetupSpecification, SpatialRule
from .preprocessing.image_quality import analyze_image_quality, ImageQualityResult

@dataclass
class LabLensResult:
    image_path: str
    quality: ImageQualityResult
    detections: List[DetectionPosition]
    compliance_status: str
    compliance_result: Optional[ComplianceResult]
    warnings: List[str]
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image": self.image_path,
            "quality": asdict(self.quality) if self.quality else None,
            "detections": [asdict(d) for d in self.detections] if self.detections else [],
            "compliance": {
                "status": self.compliance_status,
                "violations": [asdict(v) for v in self.compliance_result.violations] if self.compliance_result else []
            },
            "warnings": self.warnings,
            "error": self.error
        }

class LabLensPipeline:
    def __init__(self, model_path: Optional[str] = None, conf_threshold: float = 0.25):
        self.conf_threshold = conf_threshold
        self.detector = YOLODetector()
        self.model_loaded = False

        if model_path and os.path.exists(model_path):
            try:
                self.detector.load_model(model_path)
                self.model_loaded = True
            except Exception as e:
                # Do not crash; record that the model failed to load
                self.model_loaded = False

    def run(self, image_path: str, setup_specification: Optional[SetupSpecification] = None, rules: Optional[List[SpatialRule]] = None) -> LabLensResult:
        warnings = []
        if not os.path.exists(image_path):
            return LabLensResult(
                image_path=image_path,
                quality=None,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=["Image path does not exist"],
                error="FILE_NOT_FOUND"
            )

        img = cv2.imread(image_path)
        if img is None:
            return LabLensResult(
                image_path=image_path,
                quality=None,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=["Unreadable image"],
                error="UNREADABLE_IMAGE"
            )

        # 1. Quality Check
        quality_res = analyze_image_quality(img, {})
        warnings.extend(quality_res.warnings)
        if quality_res.status == "FAIL":
            return LabLensResult(
                image_path=image_path,
                quality=quality_res,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=warnings,
                error="IMAGE_QUALITY_FAIL"
            )

        # 2. Detection
        if not self.model_loaded:
            return LabLensResult(
                image_path=image_path,
                quality=quality_res,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=warnings,
                error="MODEL_NOT_LOADED"
            )

        try:
            raw_detections = self.detector.predict(img, self.conf_threshold)
        except Exception as e:
            return LabLensResult(
                image_path=image_path,
                quality=quality_res,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=warnings,
                error=f"DETECTION_FAILED: {str(e)}"
            )

        # 3. Detection Normalization & ID Generation
        height, width = img.shape[:2]
        spatial_detections = []
        class_counters = {}

        for det in raw_detections:
            # Check valid coordinates
            if det.x1 >= det.x2 or det.y1 >= det.y2:
                warnings.append(f"Invalid bounding box skipped: {det}")
                continue

            # Normalize
            nx1 = max(0.0, det.x1 / width)
            ny1 = max(0.0, det.y1 / height)
            nx2 = min(1.0, det.x2 / width)
            ny2 = min(1.0, det.y2 / height)

            if nx1 >= nx2 or ny1 >= ny2:
                warnings.append(f"Zero-area normalized box skipped: {det}")
                continue

            box = BoundingBox(nx1, ny1, nx2, ny2, normalized=True)

            class_name = det.class_name
            class_counters[class_name] = class_counters.get(class_name, 0) + 1
            obj_id = f"{class_name}_{class_counters[class_name]}"

            spatial_detections.append(DetectionPosition(
                box=box,
                class_name=class_name,
                confidence=det.confidence,
                id=obj_id
            ))

        # 4. Compliance Decision
        if setup_specification is None:
            return LabLensResult(
                image_path=image_path,
                quality=quality_res,
                detections=spatial_detections,
                compliance_status="UNSPECIFIED",
                compliance_result=None,
                warnings=warnings,
                error=None
            )

        if rules is None:
            rules = []

        engine = RuleEngine(setup_specification, rules)
        comp_res = engine.evaluate(spatial_detections)

        if comp_res.compliant:
            final_status = "COMPLIANT"
        else:
            final_status = "NON_COMPLIANT"

        return LabLensResult(
            image_path=image_path,
            quality=quality_res,
            detections=spatial_detections,
            compliance_status=final_status,
            compliance_result=comp_res,
            warnings=warnings,
            error=None
        )
