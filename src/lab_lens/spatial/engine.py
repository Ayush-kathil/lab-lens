from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from .core import BoundingBox, DetectionPosition, ComplianceResult, SpatialViolation, ViolationType, GeometricRelations

@dataclass
class SetupSpecification:
    setup_name: str
    required_objects: Dict[str, int]  # class_name -> expected count
    regions: Dict[str, BoundingBox] = field(default_factory=dict)
    
@dataclass
class SpatialRule:
    rule_type: str  # e.g., 'inside', 'left_of'
    subject_class: str
    target: str     # Can be a region name or another class name
    threshold: Optional[float] = None
    
    def evaluate(self, detections: List[DetectionPosition], spec: SetupSpecification) -> Tuple[bool, Optional[SpatialViolation]]:
        # This is overridden by concrete rules or handled centrally in RuleEngine
        pass

class RuleEngine:
    def __init__(self, spec: SetupSpecification, rules: List[SpatialRule]):
        self.spec = spec
        self.rules = rules

    def evaluate(self, detections: List[DetectionPosition]) -> ComplianceResult:
        violations = []
        missing = []
        extra = []
        misplaced = []
        relation_v = []
        satisfied = []
        
        # 1. Count matching
        class_counts = {}
        for d in detections:
            class_counts[d.class_name] = class_counts.get(d.class_name, 0) + 1
            
        # Check missing/extra
        for cls_name, expected in self.spec.required_objects.items():
            detected = class_counts.get(cls_name, 0)
            if detected < expected:
                missing.append(cls_name)
                violations.append(SpatialViolation(ViolationType.MISSING_OBJECT, f"Expected {expected} of {cls_name}, found {detected}", [cls_name]))
            elif detected > expected:
                extra.append(cls_name)
                violations.append(SpatialViolation(ViolationType.EXTRA_OBJECT, f"Expected {expected} of {cls_name}, found {detected}", [cls_name]))
            else:
                satisfied.append(f"Count satisfied for {cls_name}")
                
        # 2. Evaluate Spatial Rules
        for rule in self.rules:
            subjects = [d for d in detections if d.class_name == rule.subject_class]
            
            if rule.rule_type == 'inside':
                region = self.spec.regions.get(rule.target)
                if not region:
                    continue # Ignore rule if region isn't defined
                
                # For every subject, it must be inside the region
                thresh = rule.threshold if rule.threshold is not None else 0.5
                for sub in subjects:
                    if not GeometricRelations.inside_region(sub.box, region, thresh):
                        misplaced.append(rule.subject_class)
                        violations.append(SpatialViolation(ViolationType.MISPLACED_OBJECT, f"{rule.subject_class} not inside {rule.target}", [rule.subject_class]))
                    else:
                        satisfied.append(f"{rule.subject_class} is inside {rule.target}")
                        
            elif rule.rule_type in ['left_of', 'right_of', 'above', 'below']:
                targets = [d for d in detections if d.class_name == rule.target]
                if not subjects or not targets:
                    continue # Can't evaluate if missing objects
                
                # Simple logic: all subjects must satisfy relation with all targets
                # (For complex setups, would need explicit ID matching)
                rel_func = getattr(GeometricRelations, rule.rule_type)
                
                for sub in subjects:
                    for tgt in targets:
                        if not rel_func(sub.box, tgt.box):
                            relation_v.append(f"{rule.subject_class} not {rule.rule_type} {rule.target}")
                            violations.append(SpatialViolation(
                                ViolationType.SPATIAL_RELATION_VIOLATION, 
                                f"{rule.subject_class} fails {rule.rule_type} relation with {rule.target}",
                                [rule.subject_class, rule.target]
                            ))
                        else:
                            satisfied.append(f"{rule.subject_class} {rule.rule_type} {rule.target} satisfied")

        return ComplianceResult(
            compliant=len(violations) == 0,
            violations=violations,
            missing_objects=missing,
            extra_objects=extra,
            misplaced_objects=misplaced,
            spatial_relation_violations=relation_v,
            satisfied_rules=satisfied
        )
