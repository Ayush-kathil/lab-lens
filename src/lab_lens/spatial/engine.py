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
        for rule in self.rules:
            if rule.threshold is not None and rule.threshold < 0:
                raise ValueError(f"Invalid negative threshold {rule.threshold} for rule {rule.rule_type}")

    def evaluate(self, detections: List[DetectionPosition]) -> ComplianceResult:
        violations = []
        missing = []
        extra = []
        misplaced = []
        relation_v = []
        satisfied = []

        total_conditions = len(self.spec.required_objects) + len(self.rules)
        satisfied_conditions = 0

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
                satisfied_conditions += 1

        # 2. Evaluate Spatial Rules
        for rule in self.rules:
            rule_violation_count = 0
            subjects = [d for d in detections if d.class_name == rule.subject_class]

            if rule.rule_type == 'inside':
                region = self.spec.regions.get(rule.target)
                if not region:
                    v = SpatialViolation(ViolationType.MISPLACED_OBJECT, f"Region {rule.target} not found in setup", [rule.subject_class])
                    violations.append(v)
                    rule_violation_count += 1
                    continue

                thresh = rule.threshold if rule.threshold is not None else 0.5
                if thresh < 0:
                    v = SpatialViolation(ViolationType.MISPLACED_OBJECT, f"Invalid threshold {thresh} for rule {rule.rule_type}", [rule.subject_class])
                    violations.append(v)
                    rule_violation_count += 1
                    continue

                if not subjects:
                    v = SpatialViolation(ViolationType.MISPLACED_OBJECT, f"Cannot evaluate {rule.rule_type}: missing {rule.subject_class}", [rule.subject_class])
                    violations.append(v)
                    rule_violation_count += 1
                    continue

                for sub in subjects:
                    if not GeometricRelations.inside_region(sub.box, region, thresh):
                        misplaced.append(rule.subject_class)
                        violations.append(SpatialViolation(ViolationType.MISPLACED_OBJECT, f"{rule.subject_class} not inside {rule.target}", [rule.subject_class]))
                        rule_violation_count += 1
                    else:
                        satisfied.append(f"{rule.subject_class} is inside {rule.target}")

            elif rule.rule_type in ['left_of', 'right_of', 'above', 'below', 'overlaps', 'near', 'far']:
                targets = [d for d in detections if d.class_name == rule.target]
                if not subjects or not targets:
                    v = SpatialViolation(
                        ViolationType.SPATIAL_RELATION_VIOLATION,
                        f"Cannot evaluate {rule.rule_type}: missing {rule.subject_class} or {rule.target}",
                        [rule.subject_class, rule.target]
                    )
                    violations.append(v)
                    rule_violation_count += 1
                    continue

                rel_func = getattr(GeometricRelations, rule.rule_type, None)
                if not rel_func:
                    v = SpatialViolation(
                        ViolationType.SPATIAL_RELATION_VIOLATION,
                        f"Unsupported spatial relation {rule.rule_type}",
                        [rule.subject_class, rule.target]
                    )
                    violations.append(v)
                    rule_violation_count += 1
                    continue

                for sub in subjects:
                    for tgt in targets:
                        kwargs = {}
                        if rule.threshold is not None:
                            if rule.threshold < 0:
                                v = SpatialViolation(
                                    ViolationType.SPATIAL_RELATION_VIOLATION,
                                    f"Invalid threshold {rule.threshold} for rule {rule.rule_type}",
                                    [rule.subject_class, rule.target]
                                )
                                violations.append(v)
                                rule_violation_count += 1
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
                            rule_violation_count += 1
                        else:
                            satisfied.append(f"{rule.subject_class} {rule.rule_type} {rule.target} satisfied")
            else:
                v = SpatialViolation(
                    ViolationType.SPATIAL_RELATION_VIOLATION,
                    f"Unknown rule type {rule.rule_type}",
                    [rule.subject_class]
                )
                violations.append(v)
                rule_violation_count += 1

            if rule_violation_count == 0:
                satisfied_conditions += 1

        score = None
        if total_conditions > 0:
            score = (satisfied_conditions / total_conditions) * 100.0

        return ComplianceResult(
            compliant=len(violations) == 0,
            violations=violations,
            missing_objects=missing,
            extra_objects=extra,
            misplaced_objects=misplaced,
            spatial_relation_violations=relation_v,
            satisfied_rules=satisfied,
            score=score,
            total_conditions=total_conditions,
            satisfied_conditions=satisfied_conditions
        )
