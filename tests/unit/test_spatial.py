import pytest
from lab_lens.spatial import (
    BoundingBox, DetectionPosition, GeometricRelations,
    SetupSpecification, SpatialRule, RuleEngine, ViolationType
)

def test_bounding_box_properties():
    # SYNTHETIC TEST FIXTURE — NOT CHEMEQ25 GROUND TRUTH
    box = BoundingBox(x1=0.1, y1=0.2, x2=0.5, y2=0.6)
    assert pytest.approx(box.width) == 0.4
    assert pytest.approx(box.height) == 0.4
    assert pytest.approx(box.area) == 0.16
    assert pytest.approx(box.center_x) == 0.3
    assert pytest.approx(box.center_y) == 0.4
    
    # Enforces min/max fixing
    box2 = BoundingBox(x1=0.5, y1=0.6, x2=0.1, y2=0.2)
    assert box2.x1 == 0.1
    assert box2.y1 == 0.2

def test_geometric_relations():
    # SYNTHETIC TEST FIXTURE
    box_a = BoundingBox(0.1, 0.1, 0.3, 0.3)  # Center (0.2, 0.2)
    box_b = BoundingBox(0.4, 0.1, 0.6, 0.3)  # Center (0.5, 0.2)
    box_c = BoundingBox(0.1, 0.4, 0.3, 0.6)  # Center (0.2, 0.5)
    
    assert GeometricRelations.left_of(box_a, box_b)
    assert not GeometricRelations.left_of(box_b, box_a)
    assert GeometricRelations.right_of(box_b, box_a)
    
    assert GeometricRelations.above(box_a, box_c)
    assert GeometricRelations.below(box_c, box_a)
    
    box_overlap = BoundingBox(0.2, 0.2, 0.4, 0.4)
    assert GeometricRelations.overlaps(box_a, box_overlap, threshold=0.1)
    
    # Inside region
    region = BoundingBox(0.0, 0.0, 1.0, 1.0)
    assert GeometricRelations.inside_region(box_a, region, threshold=0.9)
    assert not GeometricRelations.inside_region(box_a, BoundingBox(0.5, 0.5, 1.0, 1.0), threshold=0.1)

def test_rule_engine_counts():
    # SYNTHETIC TEST FIXTURE
    spec = SetupSpecification("synth_test", required_objects={"Beaker": 1, "Funnel": 2})
    engine = RuleEngine(spec, rules=[])
    
    # Missing objects
    dets_missing = [DetectionPosition(BoundingBox(0,0,0,0), "Beaker", 0.9)]
    res = engine.evaluate(dets_missing)
    assert not res.compliant
    assert "Funnel" in res.missing_objects
    
    # Exact objects
    dets_exact = [
        DetectionPosition(BoundingBox(0,0,0,0), "Beaker", 0.9),
        DetectionPosition(BoundingBox(0,0,0,0), "Funnel", 0.9),
        DetectionPosition(BoundingBox(0,0,0,0), "Funnel", 0.9)
    ]
    res2 = engine.evaluate(dets_exact)
    assert res2.compliant
    
    # Extra objects
    dets_extra = dets_exact + [DetectionPosition(BoundingBox(0,0,0,0), "Beaker", 0.9)]
    res3 = engine.evaluate(dets_extra)
    assert not res3.compliant
    assert "Beaker" in res3.extra_objects

def test_rule_engine_misplacement_and_relations():
    # SYNTHETIC TEST FIXTURE
    spec = SetupSpecification(
        setup_name="synth_spatial",
        required_objects={"Beaker": 1, "Funnel": 1},
        regions={"work_area": BoundingBox(0.0, 0.0, 0.5, 0.5)}
    )
    rules = [
        SpatialRule('inside', 'Beaker', 'work_area'),
        SpatialRule('left_of', 'Beaker', 'Funnel')
    ]
    engine = RuleEngine(spec, rules)
    
    # Perfect configuration
    dets_good = [
        DetectionPosition(BoundingBox(0.1, 0.1, 0.2, 0.2), "Beaker", 0.9), # inside work_area, center 0.15
        DetectionPosition(BoundingBox(0.6, 0.1, 0.8, 0.3), "Funnel", 0.9)  # center 0.7
    ]
    res1 = engine.evaluate(dets_good)
    assert res1.compliant
    
    # Misplaced (Beaker outside work_area)
    dets_misplaced = [
        DetectionPosition(BoundingBox(0.6, 0.6, 0.8, 0.8), "Beaker", 0.9), # outside work_area
        DetectionPosition(BoundingBox(0.8, 0.1, 0.9, 0.3), "Funnel", 0.9)  
    ]
    res2 = engine.evaluate(dets_misplaced)
    assert not res2.compliant
    assert "Beaker" in res2.misplaced_objects
    assert any(v.violation_type == ViolationType.MISPLACED_OBJECT for v in res2.violations)
    
    # Relation violation (Beaker right of Funnel instead of left of)
    dets_rel_bad = [
        DetectionPosition(BoundingBox(0.3, 0.1, 0.4, 0.2), "Beaker", 0.9), # inside work_area, center 0.35
        DetectionPosition(BoundingBox(0.1, 0.1, 0.2, 0.3), "Funnel", 0.9)  # center 0.15
    ]
    res3 = engine.evaluate(dets_rel_bad)
    assert not res3.compliant
    assert len(res3.spatial_relation_violations) > 0
