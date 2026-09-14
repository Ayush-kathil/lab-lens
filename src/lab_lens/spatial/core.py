import math
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum

class ViolationType(str, Enum):
    MISSING_OBJECT = "MISSING_OBJECT"
    EXTRA_OBJECT = "EXTRA_OBJECT"
    MISPLACED_OBJECT = "MISPLACED_OBJECT"
    SPATIAL_RELATION_VIOLATION = "SPATIAL_RELATION_VIOLATION"

@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float
    normalized: bool = True

    def __post_init__(self):
        # Enforce valid box
        self.x1 = min(self.x1, self.x2)
        self.y1 = min(self.y1, self.y2)
        self.x2 = max(self.x1, self.x2)
        self.y2 = max(self.y1, self.y2)

    @property
    def center_x(self) -> float: return (self.x1 + self.x2) / 2.0
    @property
    def center_y(self) -> float: return (self.y1 + self.y2) / 2.0
    @property
    def width(self) -> float: return max(0.0, self.x2 - self.x1)
    @property
    def height(self) -> float: return max(0.0, self.y2 - self.y1)
    @property
    def area(self) -> float: return self.width * self.height

    def iou(self, other: 'BoundingBox') -> float:
        ix1 = max(self.x1, other.x1)
        iy1 = max(self.y1, other.y1)
        ix2 = min(self.x2, other.x2)
        iy2 = min(self.y2, other.y2)
        inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
        union = self.area + other.area - inter
        return inter / union if union > 0 else 0.0

    def intersection_over_self(self, other: 'BoundingBox') -> float:
        ix1 = max(self.x1, other.x1)
        iy1 = max(self.y1, other.y1)
        ix2 = min(self.x2, other.x2)
        iy2 = min(self.y2, other.y2)
        inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
        return inter / self.area if self.area > 0 else 0.0

    def distance_to(self, other: 'BoundingBox') -> float:
        return math.hypot(self.center_x - other.center_x, self.center_y - other.center_y)

@dataclass
class DetectionPosition:
    box: BoundingBox
    class_name: str
    confidence: float
    id: str = ""

@dataclass
class SpatialViolation:
    violation_type: ViolationType
    message: str
    related_classes: List[str] = field(default_factory=list)

@dataclass
class ComplianceResult:
    compliant: bool
    violations: List[SpatialViolation]
    missing_objects: List[str]
    extra_objects: List[str]
    misplaced_objects: List[str]
    spatial_relation_violations: List[str]
    satisfied_rules: List[str] = field(default_factory=list)
    score: Optional[float] = None
    total_conditions: int = 0
    satisfied_conditions: int = 0

class GeometricRelations:
    @staticmethod
    def left_of(a: BoundingBox, b: BoundingBox) -> bool:
        # A is completely to the left of B's center
        return a.center_x < b.center_x

    @staticmethod
    def right_of(a: BoundingBox, b: BoundingBox) -> bool:
        return a.center_x > b.center_x

    @staticmethod
    def above(a: BoundingBox, b: BoundingBox) -> bool:
        # Smaller Y is higher in image coords
        return a.center_y < b.center_y

    @staticmethod
    def below(a: BoundingBox, b: BoundingBox) -> bool:
        return a.center_y > b.center_y

    @staticmethod
    def inside_region(a: BoundingBox, region: BoundingBox, threshold: float = 0.5) -> bool:
        # True if a's area is >= threshold inside region
        return a.intersection_over_self(region) >= threshold

    @staticmethod
    def overlaps(a: BoundingBox, b: BoundingBox, threshold: float = 0.1) -> bool:
        return a.iou(b) >= threshold

    @staticmethod
    def near(a: BoundingBox, b: BoundingBox, distance_threshold: float = 0.2) -> bool:
        return a.distance_to(b) <= distance_threshold

    @staticmethod
    def far(a: BoundingBox, b: BoundingBox, distance_threshold: float = 0.5) -> bool:
        return a.distance_to(b) >= distance_threshold
