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
            # Check required keys
            for key in cls.REQUIRED_KEYS:
                if key not in sample:
                    raise ValueError(f"Sample at index {idx} missing required key '{key}'")
                    
            s_id = sample['sample_id']
            if s_id in sample_ids:
                raise ValueError(f"Duplicate sample_id found: {s_id}")
            sample_ids.add(s_id)
            
            cls._validate_objects(sample['objects'], s_id)
            cls._validate_setup(sample['setup_specification'], s_id)
            cls._validate_expected(sample['expected_output'], s_id)
            
        return True

    @classmethod
    def _validate_objects(cls, objects: List[Dict[str, Any]], s_id: str):
        for obj in objects:
            if 'class_name' not in obj or 'box' not in obj:
                raise ValueError(f"Sample {s_id} has invalid object definition.")
            box = obj['box']
            for k in ['x1', 'y1', 'x2', 'y2']:
                if k not in box:
                    raise ValueError(f"Sample {s_id} has malformed box missing {k}.")
                val = box[k]
                if not (0.0 <= val <= 1.0):
                    raise ValueError(f"Sample {s_id} has box coordinate {k}={val} outside [0,1].")

    @classmethod
    def _validate_setup(cls, setup: Dict[str, Any], s_id: str):
        if 'setup_name' not in setup or 'required_objects' not in setup or 'regions' not in setup or 'spatial_rules' not in setup:
            raise ValueError(f"Sample {s_id} setup specification missing required fields.")
            
        for rule in setup['spatial_rules']:
            if 'rule_type' not in rule or 'subject_class' not in rule or 'target' not in rule:
                raise ValueError(f"Sample {s_id} has invalid spatial rule.")
            if rule['rule_type'] not in ['left_of', 'right_of', 'above', 'below', 'inside', 'overlaps', 'near', 'far']:
                raise ValueError(f"Sample {s_id} uses invalid relation: {rule['rule_type']}")

    @classmethod
    def _validate_expected(cls, expected: Dict[str, Any], s_id: str):
        if 'compliant' not in expected or 'violations' not in expected:
            raise ValueError(f"Sample {s_id} expected_output missing compliant/violations fields.")
