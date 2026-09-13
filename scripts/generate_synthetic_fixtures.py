import json
from pathlib import Path

def create_sample(sample_id, objects, required_objects, regions, rules, expected_compliant, expected_violations):
    return {
        "sample_id": sample_id,
        "image_ref": "synthetic",
        "image_width": 1000,
        "image_height": 1000,
        "setup_specification": {
            "setup_name": f"setup_{sample_id}",
            "required_objects": required_objects,
            "regions": regions,
            "spatial_rules": rules
        },
        "objects": objects,
        "expected_output": {
            "compliant": expected_compliant,
            "violations": expected_violations
        }
    }

def box(x1, y1, x2, y2):
    return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

samples = []
samples.append(create_sample("test_001_compliant", [{"class_name": "Beaker", "box": box(0.4, 0.4, 0.6, 0.6), "confidence": 1.0}], {"Beaker": 1}, {"work_zone": box(0.1, 0.1, 0.9, 0.9)}, [{"rule_type": "inside", "subject_class": "Beaker", "target": "work_zone", "threshold": 0.8}], True, []))
samples.append(create_sample("test_002_missing", [], {"Beaker": 1}, {}, [], False, [{"type": "MISSING_OBJECT", "target": "Beaker"}]))
samples.append(create_sample("test_003_extra", [{"class_name": "Beaker", "box": box(0.2, 0.2, 0.3, 0.3), "confidence": 1.0}, {"class_name": "Beaker", "box": box(0.6, 0.6, 0.7, 0.7), "confidence": 1.0}], {"Beaker": 1}, {}, [], False, [{"type": "EXTRA_OBJECT", "target": "Beaker"}]))
samples.append(create_sample("test_004_misplaced", [{"class_name": "Beaker", "box": box(0.0, 0.0, 0.1, 0.1), "confidence": 1.0}], {"Beaker": 1}, {"work_zone": box(0.2, 0.2, 0.8, 0.8)}, [{"rule_type": "inside", "subject_class": "Beaker", "target": "work_zone", "threshold": 0.5}], False, [{"type": "MISPLACED_OBJECT", "target": "Beaker"}]))

rel_pairs = [
    ("test_005_left_of_sat", "left_of", box(0.1, 0.1, 0.2, 0.2), box(0.8, 0.1, 0.9, 0.2), True, None),
    ("test_006_left_of_viol", "left_of", box(0.8, 0.1, 0.9, 0.2), box(0.1, 0.1, 0.2, 0.2), False, {"type": "SPATIAL_RELATION_VIOLATION", "target": "Beaker"}),
    ("test_007_right_of_sat", "right_of", box(0.8, 0.1, 0.9, 0.2), box(0.1, 0.1, 0.2, 0.2), True, None),
    ("test_008_right_of_viol", "right_of", box(0.1, 0.1, 0.2, 0.2), box(0.8, 0.1, 0.9, 0.2), False, {"type": "SPATIAL_RELATION_VIOLATION", "target": "Beaker"}),
    ("test_009_above_sat", "above", box(0.1, 0.1, 0.2, 0.2), box(0.1, 0.8, 0.2, 0.9), True, None),
    ("test_010_above_viol", "above", box(0.1, 0.8, 0.2, 0.9), box(0.1, 0.1, 0.2, 0.2), False, {"type": "SPATIAL_RELATION_VIOLATION", "target": "Beaker"}),
    ("test_011_below_sat", "below", box(0.1, 0.8, 0.2, 0.9), box(0.1, 0.1, 0.2, 0.2), True, None),
    ("test_012_below_viol", "below", box(0.1, 0.1, 0.2, 0.2), box(0.1, 0.8, 0.2, 0.9), False, {"type": "SPATIAL_RELATION_VIOLATION", "target": "Beaker"}),
    ("test_013_overlaps_sat", "overlaps", box(0.1, 0.1, 0.3, 0.3), box(0.2, 0.2, 0.4, 0.4), True, None),
    ("test_014_overlaps_viol", "overlaps", box(0.1, 0.1, 0.2, 0.2), box(0.8, 0.8, 0.9, 0.9), False, {"type": "SPATIAL_RELATION_VIOLATION", "target": "Beaker"}),
    ("test_015_near_sat", "near", box(0.1, 0.1, 0.2, 0.2), box(0.15, 0.15, 0.25, 0.25), True, None),
    ("test_016_near_viol", "near", box(0.1, 0.1, 0.2, 0.2), box(0.8, 0.8, 0.9, 0.9), False, {"type": "SPATIAL_RELATION_VIOLATION", "target": "Beaker"}),
    ("test_017_far_sat", "far", box(0.1, 0.1, 0.2, 0.2), box(0.8, 0.8, 0.9, 0.9), True, None),
    ("test_018_far_viol", "far", box(0.1, 0.1, 0.2, 0.2), box(0.2, 0.2, 0.3, 0.3), False, {"type": "SPATIAL_RELATION_VIOLATION", "target": "Beaker"}),
]

for s_id, rule_type, b1, b2, compliant, v in rel_pairs:
    violations = [v] if v else []
    samples.append(create_sample(
        s_id,
        objects=[
            {"class_name": "Beaker", "box": b1, "confidence": 1.0},
            {"class_name": "Funnel", "box": b2, "confidence": 1.0}
        ],
        required_objects={"Beaker": 1, "Funnel": 1},
        regions={},
        rules=[{"rule_type": rule_type, "subject_class": "Beaker", "target": "Funnel", "threshold": 0.1 if rule_type == 'overlaps' else None}],
        expected_compliant=compliant,
        expected_violations=violations
    ))

samples.append(create_sample("test_019_multiple_violations", [{"class_name": "Beaker", "box": box(0.0, 0.0, 0.1, 0.1), "confidence": 1.0}], {"Beaker": 1, "Funnel": 1}, {"work_zone": box(0.5, 0.5, 0.9, 0.9)}, [{"rule_type": "inside", "subject_class": "Beaker", "target": "work_zone", "threshold": 0.5}], False, [{"type": "MISSING_OBJECT", "target": "Funnel"}, {"type": "MISPLACED_OBJECT", "target": "Beaker"}]))
samples.append(create_sample("test_020_multiple_same_class", [{"class_name": "Beaker", "box": box(0.1, 0.1, 0.2, 0.2), "confidence": 1.0}, {"class_name": "Beaker", "box": box(0.8, 0.1, 0.9, 0.2), "confidence": 1.0}], {"Beaker": 2}, {}, [], True, []))
samples.append(create_sample("test_021_boundary_condition", [{"class_name": "Beaker", "box": box(0.0, 0.0, 0.5, 0.5), "confidence": 1.0}], {"Beaker": 1}, {"work_zone": box(0.0, 0.0, 0.5, 0.5)}, [{"rule_type": "inside", "subject_class": "Beaker", "target": "work_zone", "threshold": 0.99}], True, []))

# 22. invalid/ambiguous geometry -> Handled by validator, but let's test a valid geometry logic
samples.append(create_sample("test_022_invalid_ambiguous", [{"class_name": "Beaker", "box": box(0.5, 0.5, 0.5, 0.5), "confidence": 1.0}], {"Beaker": 1}, {}, [], True, []))


Path('Dataset/SpatialCompliance').mkdir(parents=True, exist_ok=True)
with open('Dataset/SpatialCompliance/synthetic_fixtures.json', 'w') as f:
    json.dump(samples, f, indent=2)

print('Generated dataset')
