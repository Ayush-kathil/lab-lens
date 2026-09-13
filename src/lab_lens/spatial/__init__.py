from .core import BoundingBox, DetectionPosition, SpatialViolation, ComplianceResult, ViolationType, GeometricRelations
from .engine import SetupSpecification, SpatialRule, RuleEngine
from .dataset import DatasetValidator
from .evaluation import SpatialEvaluationHarness, EvaluationReport

__all__ = [
    'BoundingBox',
    'DetectionPosition',
    'SpatialViolation',
    'ComplianceResult',
    'ViolationType',
    'GeometricRelations',
    'SetupSpecification',
    'SpatialRule',
    'RuleEngine',
    'DatasetValidator',
    'SpatialEvaluationHarness',
    'EvaluationReport'
]
