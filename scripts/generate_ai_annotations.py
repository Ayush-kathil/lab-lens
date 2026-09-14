import json
import glob
import os

ANNOTATIONS_DIR = "Dataset/SpatialComplianceReal/annotations"

classifications = {
    "rw_001": ("REJECTED", "LOW"),
    "rw_002": ("REJECTED", "LOW"),
    "rw_003": ("REJECTED", "LOW"),
    "rw_004": ("REJECTED", "LOW"),
    "rw_005": ("ACCEPTED", "LOW"),
    "rw_006": ("ACCEPTED", "LOW"),
    "rw_007": ("REJECTED", "LOW"),
    "rw_008": ("ACCEPTED", "LOW"),
    "rw_009": ("REJECTED", "LOW"),
    "rw_010": ("ACCEPTED", "HIGH"),
    "rw_011": ("ACCEPTED", "HIGH"),
    "rw_012": ("REJECTED", "LOW"),
    "rw_013": ("ACCEPTED", "HIGH"),
    "rw_014": ("ACCEPTED", "HIGH"),
    "rw_015": ("REJECTED", "LOW"),
    "rw_016": ("ACCEPTED", "HIGH"),
}

setup_content = {
    "rw_010": {
        "setup_name": "multi_flask_setup",
        "objects": [
            {"object_id": "flask_1", "class_name": "OTHER_LAB_EQUIPMENT", "unmapped_object_type": "Flask", "box": {"x1": 0.4, "y1": 0.5, "x2": 0.6, "y2": 0.8}, "ai_confidence": "HIGH"},
            {"object_id": "stand_1", "class_name": "OTHER_LAB_EQUIPMENT", "unmapped_object_type": "Stand", "box": {"x1": 0.3, "y1": 0.1, "x2": 0.7, "y2": 0.9}, "ai_confidence": "MEDIUM"}
        ],
        "relations": [
            {"subject_id": "flask_1", "target_id": "stand_1", "rule_type": "near"}
        ],
        "compliant": None
    },
    "rw_011": {
        "setup_name": "titration",
        "objects": [
            {"object_id": "burette_1", "class_name": "OTHER_LAB_EQUIPMENT", "unmapped_object_type": "Burette", "box": {"x1": 0.4, "y1": 0.1, "x2": 0.5, "y2": 0.7}, "ai_confidence": "HIGH"},
            {"object_id": "stand_1", "class_name": "Burette_Stands", "box": {"x1": 0.2, "y1": 0.1, "x2": 0.6, "y2": 0.9}, "ai_confidence": "HIGH"}
        ],
        "relations": [
            {"subject_id": "burette_1", "target_id": "stand_1", "rule_type": "near"}
        ],
        "compliant": None
    },
    "rw_013": {
        "setup_name": "distillation",
        "objects": [
            {"object_id": "flask_1", "class_name": "Round_Bottom_Flask_Borosilicate_Glass_1_Neck", "box": {"x1": 0.2, "y1": 0.6, "x2": 0.4, "y2": 0.9}, "ai_confidence": "HIGH"},
            {"object_id": "condenser_1", "class_name": "OTHER_LAB_EQUIPMENT", "unmapped_object_type": "condenser", "box": {"x1": 0.4, "y1": 0.3, "x2": 0.8, "y2": 0.6}, "ai_confidence": "HIGH"}
        ],
        "relations": [
            {"subject_id": "condenser_1", "target_id": "flask_1", "rule_type": "right_of"}
        ],
        "compliant": None
    },
    "rw_014": {
        "setup_name": "fractional_distillation",
        "objects": [
            {"object_id": "flask_1", "class_name": "Round_Bottom_Flask_Borosilicate_Glass_1_Neck", "box": {"x1": 0.3, "y1": 0.7, "x2": 0.5, "y2": 0.9}, "ai_confidence": "HIGH"},
            {"object_id": "column_1", "class_name": "OTHER_LAB_EQUIPMENT", "unmapped_object_type": "fractionating column", "box": {"x1": 0.35, "y1": 0.2, "x2": 0.45, "y2": 0.7}, "ai_confidence": "MEDIUM"}
        ],
        "relations": [
            {"subject_id": "column_1", "target_id": "flask_1", "rule_type": "above"}
        ],
        "compliant": None
    },
    "rw_016": {
        "setup_name": "titration",
        "objects": [
            {"object_id": "burette_1", "class_name": "OTHER_LAB_EQUIPMENT", "unmapped_object_type": "Burette", "box": {"x1": 0.45, "y1": 0.1, "x2": 0.55, "y2": 0.6}, "ai_confidence": "HIGH"},
            {"object_id": "beaker_1", "class_name": "Beaker", "box": {"x1": 0.4, "y1": 0.65, "x2": 0.6, "y2": 0.9}, "ai_confidence": "HIGH"}
        ],
        "relations": [
            {"subject_id": "burette_1", "target_id": "beaker_1", "rule_type": "above"}
        ],
        "compliant": None
    }
}

files = glob.glob(os.path.join(ANNOTATIONS_DIR, '*.json'))
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    s_id = data['sample_id']
    cls_status, sp_val = classifications.get(s_id, ("REJECTED", "LOW"))
    
    data['annotation_status'] = 'AI_GENERATED'
    data['annotation_source'] = 'AI_GENERATED'
    data['ground_truth_status'] = 'SILVER_LABEL'
    data['review_required'] = True
    data['dataset_status'] = cls_status
    data['spatial_value'] = sp_val
    
    if s_id in setup_content:
        content = setup_content[s_id]
        data['setup_specification']['setup_name'] = content['setup_name']
        data['objects'] = content['objects']
        data['setup_specification']['spatial_rules'] = content['relations']
        # If it's a known setup, compliance can be AMBIGUOUS or COMPLIANT. Let's make it AMBIGUOUS by setting ground_truth.compliant = None and using compliance_source
        data['ground_truth']['compliant'] = None
        data['ground_truth']['compliance_source'] = 'AI_INFERENCE'
        data['ground_truth']['compliance_label'] = 'AMBIGUOUS'
    else:
        # LOW or REJECTED
        data['setup_specification']['setup_name'] = 'unknown_setup'
        data['objects'] = []
        data['setup_specification']['spatial_rules'] = []
        data['ground_truth']['compliant'] = None
        data['ground_truth']['compliance_source'] = 'AI_INFERENCE'
        data['ground_truth']['compliance_label'] = 'AMBIGUOUS'
        
        # for LOW (e.g. rw_005 isolated beakers), maybe add objects without a setup
        if sp_val == "LOW" and cls_status == "ACCEPTED":
            data['objects'] = [{"object_id": "beaker_1", "class_name": "Beaker", "box": {"x1": 0.1, "y1": 0.1, "x2": 0.9, "y2": 0.9}, "ai_confidence": "HIGH"}]
            
    with open(f, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

print("AI annotations generated.")
