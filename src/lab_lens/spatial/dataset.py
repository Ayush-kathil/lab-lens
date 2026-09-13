import json
from pathlib import Path
from typing import Dict, List, Any

class DatasetValidator:
    REQUIRED_KEYS = ['sample_id', 'image_ref', 'image_width', 'image_height', 'setup_specification', 'objects', 'expected_output']
    
    @classmethod
    def validate_file(cls, json_path: str) -> bool:
        path = Path(json_path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {json_path}")
            
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Malformed JSON in {json_path}: {e}")
            
        if not isinstance(data, list):
            raise ValueError("Root of dataset must be a list of samples.")
            
        sample_ids = set()
        
        for idx, sample in enumerate(data):
            if not isinstance(sample, dict):
                raise ValueError(f"Sample at index {idx} is not an object/dictionary.")
                
            for key in cls.REQUIRED_KEYS:
                if key not in sample:
                    raise ValueError(f"Sample at index {idx} missing required key '{key}'")
                    
            s_id = sample['sample_id']
            if not s_id or not isinstance(s_id, str):
                raise ValueError(f"Sample at index {idx} has missing or empty sample_id.")
            if s_id in sample_ids:
                raise ValueError(f"Duplicate sample_id found: {s_id}")
            sample_ids.add(s_id)
            
            if not isinstance(sample['image_width'], (int, float)) or sample['image_width'] <= 0:
                raise ValueError(f"Sample {s_id} has invalid image_width.")
            if not isinstance(sample['image_height'], (int, float)) or sample['image_height'] <= 0:
                raise ValueError(f"Sample {s_id} has invalid image_height.")
            
            if not isinstance(sample['objects'], list):
                raise ValueError(f"Sample {s_id} 'objects' must be a list.")
                
            cls._validate_objects(sample['objects'], s_id)
            cls._validate_setup(sample['setup_specification'], s_id)
            cls._validate_expected(sample['expected_output'], s_id)
            
        return True

    @classmethod
    def _validate_objects(cls, objects: List[Dict[str, Any]], s_id: str):
        for obj in objects:
            if 'class_name' not in obj or not obj['class_name']:
                raise ValueError(f"Sample {s_id} has invalid object missing class_name.")
            if 'box' not in obj:
                raise ValueError(f"Sample {s_id} object missing box.")
            
            box = obj['box']
            for k in ['x1', 'y1', 'x2', 'y2']:
                if k not in box:
                    raise ValueError(f"Sample {s_id} has malformed box missing {k}.")
                val = box[k]
                if not isinstance(val, (int, float)):
                    raise ValueError(f"Sample {s_id} box coordinate {k} must be numeric.")
                if not (0.0 <= val <= 1.0):
                    raise ValueError(f"Sample {s_id} has box coordinate {k}={val} outside [0,1].")
            
            # Strict boundary constraint: x1 < x2 and y1 < y2
            if box['x1'] >= box['x2']:
                raise ValueError(f"Sample {s_id} box has x1 >= x2 (zero-area or reversed).")
            if box['y1'] >= box['y2']:
                raise ValueError(f"Sample {s_id} box has y1 >= y2 (zero-area or reversed).")
                
            if 'confidence' in obj:
                conf = obj['confidence']
                if not isinstance(conf, (int, float)) or not (0.0 <= conf <= 1.0):
                    raise ValueError(f"Sample {s_id} object has invalid confidence.")

    @classmethod
    def _validate_setup(cls, setup: Dict[str, Any], s_id: str):
        if 'setup_name' not in setup or not setup['setup_name']:
            raise ValueError(f"Sample {s_id} setup_name is missing or empty.")
        if 'required_objects' not in setup or not isinstance(setup['required_objects'], dict):
            raise ValueError(f"Sample {s_id} required_objects missing or not a dictionary.")
        if 'regions' not in setup or not isinstance(setup['regions'], dict):
            raise ValueError(f"Sample {s_id} regions missing or not a dictionary.")
        if 'spatial_rules' not in setup or not isinstance(setup['spatial_rules'], list):
            raise ValueError(f"Sample {s_id} spatial_rules missing or not a list.")
            
        for count in setup['required_objects'].values():
            if not isinstance(count, int) or count < 0:
                raise ValueError(f"Sample {s_id} required_objects count must be non-negative integer.")
                
        for r_name, r_box in setup['regions'].items():
            for k in ['x1', 'y1', 'x2', 'y2']:
                if k not in r_box:
                    raise ValueError(f"Sample {s_id} region {r_name} missing {k}.")
                if not (0.0 <= r_box[k] <= 1.0):
                    raise ValueError(f"Sample {s_id} region coordinate outside [0,1].")
            if r_box['x1'] >= r_box['x2'] or r_box['y1'] >= r_box['y2']:
                raise ValueError(f"Sample {s_id} region {r_name} has invalid geometry.")
            
        for rule in setup['spatial_rules']:
            if 'rule_type' not in rule or 'subject_class' not in rule or 'target' not in rule:
                raise ValueError(f"Sample {s_id} has invalid spatial rule.")
            if not rule['subject_class'] or not rule['target']:
                raise ValueError(f"Sample {s_id} rule missing subject or target string.")
            if rule['rule_type'] not in ['left_of', 'right_of', 'above', 'below', 'inside', 'overlaps', 'near', 'far']:
                raise ValueError(f"Sample {s_id} uses invalid relation: {rule['rule_type']}")
            if 'threshold' in rule and rule['threshold'] is not None:
                if not isinstance(rule['threshold'], (int, float)):
                    raise ValueError(f"Sample {s_id} rule threshold must be numeric.")

    @classmethod
    def _validate_expected(cls, expected: Dict[str, Any], s_id: str):
        if 'compliant' not in expected or not isinstance(expected['compliant'], bool):
            raise ValueError(f"Sample {s_id} expected_output missing or invalid 'compliant' boolean.")
        if 'violations' not in expected or not isinstance(expected['violations'], list):
            raise ValueError(f"Sample {s_id} expected_output missing or invalid 'violations' list.")
            
        for v in expected['violations']:
            if 'type' not in v:
                raise ValueError(f"Sample {s_id} violation missing 'type'.")
            if v['type'] not in ['MISSING_OBJECT', 'EXTRA_OBJECT', 'MISPLACED_OBJECT', 'SPATIAL_RELATION_VIOLATION']:
                raise ValueError(f"Sample {s_id} has unknown violation type: {v['type']}")
