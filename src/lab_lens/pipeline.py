import os
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict, field
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
    timing: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image": self.image_path,
            "quality": asdict(self.quality) if self.quality else None,
            "detections": [asdict(d) for d in self.detections] if self.detections else [],
            "compliance": {
                "status": self.compliance_status,
                "score": self.compliance_result.score if self.compliance_result else None,
                "total_conditions": self.compliance_result.total_conditions if self.compliance_result else None,
                "satisfied_conditions": self.compliance_result.satisfied_conditions if self.compliance_result else None,
                "violations": [asdict(v) for v in self.compliance_result.violations] if self.compliance_result else []
            },
            "warnings": self.warnings,
            "error": self.error,
            "timing": self.timing
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
        import time
        t_start = time.perf_counter()
        timing = {}

        warnings = []
        if not os.path.exists(image_path):
            return LabLensResult(
                image_path=image_path,
                quality=None,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=[],
                error="FILE_NOT_FOUND"
            )

        try:
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
        except Exception as e:
            return LabLensResult(
                image_path=image_path,
                quality=None,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=[f"Image read exception: {str(e)}"],
                error="UNREADABLE_IMAGE"
            )

        # 1. Quality Check
        t0 = time.perf_counter()
        quality_res = analyze_image_quality(img, {})
        timing['quality_time'] = time.perf_counter() - t0

        if quality_res.status == "WARNING":
            warnings.extend(quality_res.warnings)
        elif quality_res.status == "FAIL":
            return LabLensResult(
                image_path=image_path,
                quality=quality_res,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=quality_res.warnings,
                error="POOR_IMAGE_QUALITY"
            )

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

        # 2. Detection
        t0 = time.perf_counter()
        try:
            detections = self.detector.predict(img)
        except Exception as e:
            return LabLensResult(
                image_path=image_path,
                quality=quality_res,
                detections=[],
                compliance_status="ERROR",
                compliance_result=None,
                warnings=warnings + [f"Detector error: {str(e)}"],
                error="DETECTION_FAILED"
            )
        timing['detector_time'] = time.perf_counter() - t0

        # Normalize detections to spatial engine format
        t0 = time.perf_counter()
        height, width = img.shape[:2]
        spatial_detections = []
        for d in detections:
            # Enforce valid box
            if d.x1 >= d.x2 or d.y1 >= d.y2:
                warnings.append(f"Invalid bounding box skipped: {d}")
                continue

            box = BoundingBox(
                x1=d.x1 / width,
                y1=d.y1 / height,
                x2=d.x2 / width,
                y2=d.y2 / height,
                normalized=True
            )
            if box.area <= 0:
                warnings.append(f"Zero-area normalized box for {d.class_name}")
                continue
            spatial_detections.append(DetectionPosition(
                box=box,
                class_name=d.class_name,
                confidence=d.confidence,
                id=f"{d.class_name}_{d.class_id}" if hasattr(d, 'class_id') else f"{d.class_name}_{np.random.randint(1000)}" # Fallback ID logic
            ))

        # Enforce unique sequential IDs for duplicated class names
        class_counters = {}
        for sd in spatial_detections:
            base = sd.class_name
            class_counters[base] = class_counters.get(base, 0) + 1
            sd.id = f"{base}_{class_counters[base]}"

        # 3. Spatial Reasoning & Compliance
        if setup_specification is None:
            timing['spatial_time'] = time.perf_counter() - t0
            timing['scoring_time'] = 0.0
            timing['total_time'] = time.perf_counter() - t_start
            return LabLensResult(
                image_path=image_path,
                quality=quality_res,
                detections=spatial_detections,
                compliance_status="UNSPECIFIED",
                compliance_result=None,
                warnings=warnings,
                error=None,
                timing=timing
            )

        rules = rules or []
        engine = RuleEngine(setup_specification, rules)

        t1 = time.perf_counter()
        timing['spatial_time'] = t1 - t0

        comp_res = engine.evaluate(spatial_detections)
        timing['scoring_time'] = time.perf_counter() - t1

        if comp_res.total_conditions == 0:
            final_status = "UNSPECIFIED"
        elif comp_res.compliant:
            final_status = "COMPLIANT"
        else:
            final_status = "NON_COMPLIANT"

        timing['total_time'] = time.perf_counter() - t_start
        return LabLensResult(
            image_path=image_path,
            quality=quality_res,
            detections=spatial_detections,
            compliance_status=final_status,
            compliance_result=comp_res,
            warnings=warnings,
            error=None,
            timing=timing
        )
