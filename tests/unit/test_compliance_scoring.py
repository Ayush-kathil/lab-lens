import pytest
from lab_lens.spatial.engine import RuleEngine, SetupSpecification, SpatialRule
from lab_lens.spatial.core import BoundingBox, DetectionPosition

def create_det(cls_name, x1, y1, x2, y2, id=""):
    return DetectionPosition(BoundingBox(x1, y1, x2, y2), cls_name, 0.9, id)

def test_score_all_conditions_satisfied():
    spec = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    rules = [SpatialRule("left_of", "Beaker", "Stand")]
    engine = RuleEngine(spec, rules)
    # Total conditions = 2 objects + 1 rule = 3
    
    dets = [
        create_det("Beaker", 0.1, 0.1, 0.4, 0.4, "Beaker_1"),
        create_det("Stand", 0.6, 0.1, 0.9, 0.9, "Stand_1")
    ]
    res = engine.evaluate(dets)
    assert res.compliant is True
    assert res.total_conditions == 3
    assert res.satisfied_conditions == 3
    assert res.score == 100.0

def test_score_half_conditions():
    # 2 required objects. No spatial rules. 1 missing.
    spec = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    engine = RuleEngine(spec, [])
    
    dets = [
        create_det("Beaker", 0.1, 0.1, 0.4, 0.4, "Beaker_1")
    ]
    res = engine.evaluate(dets)
    assert res.compliant is False
    assert res.total_conditions == 2
    assert res.satisfied_conditions == 1
    assert res.score == 50.0

def test_score_all_violated():
    spec = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    rules = [SpatialRule("left_of", "Beaker", "Stand")]
    engine = RuleEngine(spec, rules)
    
    dets = []
    res = engine.evaluate(dets)
    assert res.compliant is False
    assert res.total_conditions == 3
    assert res.satisfied_conditions == 0
    assert res.score == 0.0

def test_score_zero_conditions():
    spec = SetupSpecification("test", {})
    engine = RuleEngine(spec, [])
    dets = [create_det("Beaker", 0.1, 0.1, 0.4, 0.4)]
    res = engine.evaluate(dets)
    assert res.total_conditions == 0
    assert res.score is None

def test_score_missing_object():
    spec = SetupSpecification("test", {"Beaker": 2})
    engine = RuleEngine(spec, [])
    dets = [create_det("Beaker", 0.1, 0.1, 0.4, 0.4)]
    res = engine.evaluate(dets)
    assert res.score == 0.0 # Expected 2, got 1, so count condition fails
    assert res.satisfied_conditions == 0

def test_score_extra_object():
    spec = SetupSpecification("test", {"Beaker": 1})
    engine = RuleEngine(spec, [])
    dets = [
        create_det("Beaker", 0.1, 0.1, 0.2, 0.2),
        create_det("Beaker", 0.3, 0.3, 0.4, 0.4)
    ]
    res = engine.evaluate(dets)
    assert res.score == 0.0
    assert res.satisfied_conditions == 0

def test_score_spatial_violation():
    spec = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    rules = [SpatialRule("left_of", "Beaker", "Stand")]
    engine = RuleEngine(spec, rules)
    # Beaker is right of Stand
    dets = [
        create_det("Stand", 0.1, 0.1, 0.4, 0.4),
        create_det("Beaker", 0.6, 0.1, 0.9, 0.9)
    ]
    res = engine.evaluate(dets)
    assert res.total_conditions == 3
    assert res.satisfied_conditions == 2 # The two objects are present correctly
    assert abs(res.score - (2/3)*100) < 1e-5

def test_score_deterministic_repeated():
    spec = SetupSpecification("test", {"Beaker": 1, "Stand": 1})
    rules = [SpatialRule("left_of", "Beaker", "Stand")]
    engine = RuleEngine(spec, rules)
    
    dets = [
        create_det("Stand", 0.1, 0.1, 0.4, 0.4),
        create_det("Beaker", 0.6, 0.1, 0.9, 0.9)
    ]
    res1 = engine.evaluate(dets)
    res2 = engine.evaluate(dets)
    assert res1.score == res2.score
    assert res1.total_conditions == res2.total_conditions

def test_score_bounds():
    spec = SetupSpecification("test", {"Beaker": 1})
    engine = RuleEngine(spec, [])
    dets = [create_det("Beaker", 0.1, 0.1, 0.4, 0.4)]
    res = engine.evaluate(dets)
    assert 0 <= res.score <= 100
    assert not isinstance(res.score, float) or res.score == res.score # Not NaN

