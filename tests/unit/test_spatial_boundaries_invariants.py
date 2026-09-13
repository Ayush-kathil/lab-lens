import pytest
from lab_lens.spatial import (
    BoundingBox, GeometricRelations, DetectionPosition,
    SetupSpecification, SpatialRule, RuleEngine, ViolationType
)

# ---------------------------------------------------------
# BOUNDARY SEMANTICS
# ---------------------------------------------------------

def test_boundary_left_right():
    # Equal center_x
    a = BoundingBox(0.1, 0.1, 0.3, 0.3) # center (0.2, 0.2)
    b = BoundingBox(0.1, 0.4, 0.3, 0.6) # center (0.2, 0.5)
    
    assert not GeometricRelations.left_of(a, b)
    assert not GeometricRelations.right_of(a, b)
    
    # Infinitesimally different center_x
    c = BoundingBox(0.10001, 0.1, 0.30001, 0.3) # center (0.20001, 0.2)
    assert GeometricRelations.left_of(a, c)
    assert GeometricRelations.right_of(c, a)

def test_boundary_above_below():
    # Equal center_y
    a = BoundingBox(0.1, 0.2, 0.3, 0.4) # center (0.2, 0.3)
    b = BoundingBox(0.4, 0.2, 0.6, 0.4) # center (0.5, 0.3)
    
    assert not GeometricRelations.above(a, b)
    assert not GeometricRelations.below(a, b)
    
    # Infinitesimally different
    c = BoundingBox(0.1, 0.20001, 0.3, 0.40001) # center (0.2, 0.30001)
    assert GeometricRelations.above(a, c)
    assert GeometricRelations.below(c, a)

def test_boundary_inside_region():
    a = BoundingBox(0.1, 0.1, 0.3, 0.3) # area 0.04
    
    # Exactly threshold (0.5)
    reg_exact = BoundingBox(0.1, 0.1, 0.2, 0.3) # area 0.02 (intersection is 0.02 -> 0.02/0.04 = 0.5)
    assert GeometricRelations.inside_region(a, reg_exact, threshold=0.5)
    
    # Just below
    reg_below = BoundingBox(0.1, 0.1, 0.199, 0.3) # intersection < 0.02
    assert not GeometricRelations.inside_region(a, reg_below, threshold=0.5)
    
    # Just above
    reg_above = BoundingBox(0.1, 0.1, 0.201, 0.3) 
    assert GeometricRelations.inside_region(a, reg_above, threshold=0.5)
    
    # Completely inside
    reg_full = BoundingBox(0.0, 0.0, 0.4, 0.4)
    assert GeometricRelations.inside_region(a, reg_full, threshold=0.5)
    
    # Completely outside
    reg_out = BoundingBox(0.5, 0.5, 0.9, 0.9)
    assert not GeometricRelations.inside_region(a, reg_out, threshold=0.5)

def test_boundary_overlaps():
    a = BoundingBox(0.0, 0.0, 0.2, 0.2) # area 0.04
    b = BoundingBox(0.1, 0.0, 0.3, 0.2) # area 0.04, intersection = 0.02, union = 0.06, iou = 0.333
    
    # Exactly threshold
    assert GeometricRelations.overlaps(a, b, threshold=1/3)
    
    # Just below
    assert not GeometricRelations.overlaps(a, b, threshold=0.34)
    
    # Just above
    assert GeometricRelations.overlaps(a, b, threshold=0.32)
    
    # Touching zero intersection
    c = BoundingBox(0.2, 0.0, 0.4, 0.2)
    assert not GeometricRelations.overlaps(a, c, threshold=0.0001)

def test_boundary_near_far():
    a = BoundingBox(0.1, 0.1, 0.3, 0.3) # c=(0.2, 0.2)
    b = BoundingBox(0.1, 0.4, 0.3, 0.6) # c=(0.2, 0.5)
    # dist = 0.3
    
    # Near exactly threshold
    assert GeometricRelations.near(a, b, distance_threshold=0.3)
    assert not GeometricRelations.near(a, b, distance_threshold=0.299)
    assert GeometricRelations.near(a, b, distance_threshold=0.301)
    
    # Far exactly threshold
    assert GeometricRelations.far(a, b, distance_threshold=0.3)
    assert not GeometricRelations.far(a, b, distance_threshold=0.301)
    assert GeometricRelations.far(a, b, distance_threshold=0.299)

# ---------------------------------------------------------
# INVARIANT TESTING
# ---------------------------------------------------------

def test_invariants_bounding_box():
    b = BoundingBox(0.1, 0.2, 0.3, 0.6)
    
    assert b.width >= 0
    assert b.height >= 0
    assert b.area > 0
    
    assert b.x1 <= b.center_x <= b.x2
    assert b.y1 <= b.center_y <= b.y2
    
    c = BoundingBox(0.2, 0.3, 0.8, 0.9)
    assert pytest.approx(b.iou(c)) == pytest.approx(c.iou(b))
    assert 0.0 <= b.iou(c) <= 1.0
    assert 0.0 <= b.intersection_over_self(c) <= 1.0

def test_invariants_geometric_relations():
    a = BoundingBox(0.1, 0.1, 0.2, 0.2)
    b = BoundingBox(0.3, 0.1, 0.4, 0.2)
    
    # Mutually exclusive
    assert GeometricRelations.left_of(a, b) != GeometricRelations.right_of(a, b)
    
    c = BoundingBox(0.1, 0.3, 0.2, 0.4)
    assert GeometricRelations.above(a, c) != GeometricRelations.below(a, c)

# ---------------------------------------------------------
# COUNT SEMANTICS
# ---------------------------------------------------------

def test_count_semantics():
    spec = SetupSpecification("test", {"Req": 1, "Zero": 0})
    engine = RuleEngine(spec, [])
    
    # exp 0, det 0
    dets1 = [DetectionPosition(BoundingBox(0,0,0.1,0.1), "Req", 1.0)]
    res1 = engine.evaluate(dets1)
    assert res1.compliant
    assert "Zero" not in res1.extra_objects
    assert "Zero" not in res1.missing_objects
    
    # exp 0, det > 0
    dets2 = dets1 + [DetectionPosition(BoundingBox(0,0,0.1,0.1), "Zero", 1.0)]
    res2 = engine.evaluate(dets2)
    assert not res2.compliant
    assert "Zero" in res2.extra_objects
    
    # exp > 0, det 0
    res3 = engine.evaluate([])
    assert "Req" in res3.missing_objects
    
    # exp > det
    dets4 = [] # 0 < 1
    res4 = engine.evaluate(dets4)
    assert "Req" in res4.missing_objects
    
    # exp < det
    dets5 = [DetectionPosition(BoundingBox(0,0,0.1,0.1), "Req", 1.0), DetectionPosition(BoundingBox(0,0,0.1,0.1), "Req", 1.0)]
    res5 = engine.evaluate(dets5)
    assert "Req" in res5.extra_objects
    
    # omitted class
    dets6 = [DetectionPosition(BoundingBox(0,0,0.1,0.1), "Req", 1.0), DetectionPosition(BoundingBox(0,0,0.1,0.1), "Omitted", 1.0)]
    res6 = engine.evaluate(dets6)
    assert res6.compliant # omitted classes ignored

# ---------------------------------------------------------
# MULTIPLE-OBJECT SEMANTICS (CARTESIAN PRODUCT)
# ---------------------------------------------------------

def test_multiple_object_semantics():
    spec = SetupSpecification("test", {"A": 2, "B": 2})
    rules = [SpatialRule("left_of", "A", "B")]
    engine = RuleEngine(spec, rules)
    
    # Two A's (x=0.1, x=0.3), Two B's (x=0.5, x=0.7)
    # Both A's are left of both B's
    dets_good = [
        DetectionPosition(BoundingBox(0.05,0,0.15,0.1), "A", 1.0), # cx=0.1
        DetectionPosition(BoundingBox(0.25,0,0.35,0.1), "A", 1.0), # cx=0.3
        DetectionPosition(BoundingBox(0.45,0,0.55,0.1), "B", 1.0), # cx=0.5
        DetectionPosition(BoundingBox(0.65,0,0.75,0.1), "B", 1.0), # cx=0.7
    ]
    res_good = engine.evaluate(dets_good)
    assert res_good.compliant
    
    # One A (cx=0.6) is NOT left of one B (cx=0.5)
    dets_bad = [
        DetectionPosition(BoundingBox(0.05,0,0.15,0.1), "A", 1.0), # cx=0.1
        DetectionPosition(BoundingBox(0.55,0,0.65,0.1), "A", 1.0), # cx=0.6 !
        DetectionPosition(BoundingBox(0.45,0,0.55,0.1), "B", 1.0), # cx=0.5
        DetectionPosition(BoundingBox(0.65,0,0.75,0.1), "B", 1.0), # cx=0.7
    ]
    res_bad = engine.evaluate(dets_bad)
    assert not res_bad.compliant
    assert any(v.violation_type == ViolationType.SPATIAL_RELATION_VIOLATION for v in res_bad.violations)
