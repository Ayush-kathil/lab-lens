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
                    violations.append(SpatialViolation(ViolationType.MISPLACED_OBJECT, f"Region {rule.target} not found in setup", [rule.subject_class]))
                    continue

                thresh = rule.threshold if rule.threshold is not None else 0.5
                if thresh < 0:
                    violations.append(SpatialViolation(ViolationType.MISPLACED_OBJECT, f"Invalid threshold {thresh} for rule {rule.rule_type}", [rule.subject_class]))
                    continue

                for sub in subjects:
                    if not GeometricRelations.inside_region(sub.box, region, thresh):
                        misplaced.append(rule.subject_class)
                        violations.append(SpatialViolation(ViolationType.MISPLACED_OBJECT, f"{rule.subject_class} not inside {rule.target}", [rule.subject_class]))
                    else:
                        satisfied.append(f"{rule.subject_class} is inside {rule.target}")

            elif rule.rule_type in ['left_of', 'right_of', 'above', 'below', 'overlaps', 'near', 'far']:
                targets = [d for d in detections if d.class_name == rule.target]
                if not subjects or not targets:
                    # If the objects are completely absent, count matching already handles it if they were required.
                    # But if they aren't even required or present, the rule is technically un-evaluable.
                    # To be strict on ambiguous setups, we flag it if subjects/targets are missing.
                    violations.append(SpatialViolation(
                        ViolationType.SPATIAL_RELATION_VIOLATION,
                        f"Cannot evaluate {rule.rule_type}: missing {rule.subject_class} or {rule.target}",
                        [rule.subject_class, rule.target]
                    ))
                    continue

                rel_func = getattr(GeometricRelations, rule.rule_type, None)
                if not rel_func:
                    violations.append(SpatialViolation(
                        ViolationType.SPATIAL_RELATION_VIOLATION,
                        f"Unsupported spatial relation {rule.rule_type}",
                        [rule.subject_class, rule.target]
                    ))
                    continue

                for sub in subjects:
                    for tgt in targets:
                        kwargs = {}
                        if rule.threshold is not None:
                            if rule.threshold < 0:
                                violations.append(SpatialViolation(
                                    ViolationType.SPATIAL_RELATION_VIOLATION,
                                    f"Invalid threshold {rule.threshold} for rule {rule.rule_type}",
                                    [rule.subject_class, rule.target]
                                ))
                                continue
                            if rule.rule_type in ['near', 'far']:
                                kwargs['distance_threshold'] = rule.threshold
                            elif rule.rule_type in ['overlaps']:
                                kwargs['threshold'] = rule.threshold

                        if not rel_func(sub.box, tgt.box, **kwargs):
                            relation_v.append(f"{rule.subject_class} not {rule.rule_type} {rule.target}")
                            violations.append(SpatialViolation(
                                ViolationType.SPATIAL_RELATION_VIOLATION,
                                f"{rule.subject_class} fails {rule.rule_type} relation with {rule.target}",
                                [rule.subject_class, rule.target]
                            ))
                        else:
                            satisfied.append(f"{rule.subject_class} {rule.rule_type} {rule.target} satisfied")
            else:
                violations.append(SpatialViolation(
                    ViolationType.SPATIAL_RELATION_VIOLATION,
                    f"Unknown rule type {rule.rule_type}",
                    [rule.subject_class]
                ))

        return ComplianceResult(
            compliant=len(violations) == 0,
            violations=violations,
            missing_objects=missing,
            extra_objects=extra,
            misplaced_objects=misplaced,
            spatial_relation_violations=relation_v,
            satisfied_rules=satisfied
        )
