import json
from pathlib import Path
from typing import Dict, List, Any

class RealWorldDatasetValidator:
    REQUIRED_KEYS = [
        'sample_id', 'session_id', 'split', 'annotation_status',
        'image_metadata', 'objects', 'setup_specification', 'ground_truth'
    ]
    
    VALID_STATUSES = {'ACCEPTED', 'REJECTED', 'AMBIGUOUS', 'NEEDS_REVIEW'}
    VALID_SPLITS = {'train', 'validation', 'test', 'unassigned'}
    VALID_VIOLATIONS = {'MISSING_OBJECT', 'EXTRA_OBJECT', 'MISPLACED_OBJECT', 'SPATIAL_RELATION_VIOLATION', 'COUNT_VIOLATION'}
    VALID_RELATIONS = {'left_of', 'right_of', 'above', 'below', 'inside', 'overlaps', 'near', 'far'}

    @classmethod
    def validate_sample(cls, sample: Dict[str, Any], known_sample_ids: set) -> None:
        if not isinstance(sample, dict):
            raise ValueError("Sample must be a dictionary.")
            
        for key in cls.REQUIRED_KEYS:
            if key not in sample:
                raise ValueError(f"Sample missing required key '{key}'")
                
        s_id = sample['sample_id']
        if not isinstance(s_id, str) or not s_id:
            raise ValueError("sample_id must be a non-empty string.")
        if s_id in known_sample_ids:
            raise ValueError(f"Duplicate sample_id: {s_id}")
        known_sample_ids.add(s_id)
        
        if not isinstance(sample['session_id'], str) or not sample['session_id']:
            raise ValueError(f"Sample {s_id} has invalid session_id.")
            
        if sample['split'] not in cls.VALID_SPLITS:
            raise ValueError(f"Sample {s_id} has invalid split: {sample['split']}")
            
        if sample['annotation_status'] not in cls.VALID_STATUSES:
            raise ValueError(f"Sample {s_id} has invalid annotation_status: {sample['annotation_status']}")
            
        cls._validate_image_metadata(sample['image_metadata'], s_id)
        known_object_ids = cls._validate_objects(sample['objects'], s_id)
        cls._validate_setup(sample['setup_specification'], known_object_ids, s_id)
        cls._validate_ground_truth(sample['ground_truth'], sample['annotation_status'], s_id)

    @classmethod
    def _validate_image_metadata(cls, meta: Dict[str, Any], s_id: str):
        if not isinstance(meta, dict):
            raise ValueError(f"Sample {s_id} image_metadata must be dict.")
        if 'filename' not in meta or not meta['filename']:
            raise ValueError(f"Sample {s_id} missing filename.")
        if 'width' not in meta or not isinstance(meta['width'], (int, float)) or meta['width'] <= 0:
            raise ValueError(f"Sample {s_id} invalid width.")
        if 'height' not in meta or not isinstance(meta['height'], (int, float)) or meta['height'] <= 0:
            raise ValueError(f"Sample {s_id} invalid height.")
        if 'viewpoint' not in meta:
            raise ValueError(f"Sample {s_id} missing viewpoint.")

    @classmethod
    def _validate_objects(cls, objects: List[Dict[str, Any]], s_id: str) -> set:
        if not isinstance(objects, list):
            raise ValueError(f"Sample {s_id} objects must be a list.")
            
        obj_ids = set()
        for obj in objects:
            if 'object_id' not in obj or not obj['object_id']:
                raise ValueError(f"Sample {s_id} missing object_id.")
            o_id = obj['object_id']
            if o_id in obj_ids:
                raise ValueError(f"Sample {s_id} has duplicate object_id {o_id}")
            obj_ids.add(o_id)
            
            if 'class_name' not in obj or not obj['class_name']:
                raise ValueError(f"Sample {s_id} object {o_id} missing class_name.")
                
            if 'box' not in obj:
                raise ValueError(f"Sample {s_id} object {o_id} missing box.")
                
            box = obj['box']
            for k in ['x1', 'y1', 'x2', 'y2']:
                if k not in box or not isinstance(box[k], (int, float)):
                    raise ValueError(f"Sample {s_id} object {o_id} box missing or invalid {k}.")
                if not (0.0 <= box[k] <= 1.0):
                    raise ValueError(f"Sample {s_id} object {o_id} box {k} outside [0,1].")
                    
            if box['x1'] >= box['x2'] or box['y1'] >= box['y2']:
                raise ValueError(f"Sample {s_id} object {o_id} has invalid zero-area or reversed box.")
                
        return obj_ids

    @classmethod
    def _validate_setup(cls, setup: Dict[str, Any], known_obj_ids: set, s_id: str):
        if not isinstance(setup, dict):
            raise ValueError(f"Sample {s_id} setup_specification must be dict.")
        if 'setup_name' not in setup:
            raise ValueError(f"Sample {s_id} setup missing name.")
        if 'required_objects' not in setup or not isinstance(setup['required_objects'], dict):
            raise ValueError(f"Sample {s_id} setup missing required_objects.")
        if 'regions' not in setup or not isinstance(setup['regions'], dict):
            raise ValueError(f"Sample {s_id} setup missing regions.")
            
        for k, v in setup['required_objects'].items():
            if not isinstance(v, int) or v < 0:
                raise ValueError(f"Sample {s_id} invalid required count for {k}")
                
        for r_name, r_box in setup['regions'].items():
            for k in ['x1', 'y1', 'x2', 'y2']:
                if k not in r_box or not isinstance(r_box[k], (int, float)):
                    raise ValueError(f"Sample {s_id} region {r_name} missing {k}")
                if not (0.0 <= r_box[k] <= 1.0):
                    raise ValueError(f"Sample {s_id} region {r_name} {k} outside [0,1].")
            if r_box['x1'] >= r_box['x2'] or r_box['y1'] >= r_box['y2']:
                raise ValueError(f"Sample {s_id} region {r_name} has invalid geometry.")
                
        if 'spatial_rules' not in setup or not isinstance(setup['spatial_rules'], list):
            raise ValueError(f"Sample {s_id} missing spatial_rules.")
            
        for rule in setup['spatial_rules']:
            if 'rule_type' not in rule or rule['rule_type'] not in cls.VALID_RELATIONS:
                raise ValueError(f"Sample {s_id} invalid rule_type.")
                
            # Must have either subject_class or subject_id
            if 'subject_class' not in rule and 'subject_id' not in rule:
                raise ValueError(f"Sample {s_id} rule missing subject reference.")
                
            if 'subject_id' in rule and rule['subject_id'] not in known_obj_ids:
                raise ValueError(f"Sample {s_id} rule references unknown subject_id {rule['subject_id']}")
                
            if 'target' not in rule and 'target_id' not in rule:
                raise ValueError(f"Sample {s_id} rule missing target reference.")
                
            if 'target_id' in rule and rule['target_id'] not in known_obj_ids and rule['target_id'] not in setup['regions']:
                raise ValueError(f"Sample {s_id} rule references unknown target_id {rule['target_id']}")

    @classmethod
    def _validate_ground_truth(cls, gt: Dict[str, Any], status: str, s_id: str):
        if not isinstance(gt, dict):
            raise ValueError(f"Sample {s_id} ground_truth must be dict.")
            
        if status == 'ACCEPTED':
            if 'compliant' not in gt or not isinstance(gt['compliant'], bool):
                raise ValueError(f"Sample {s_id} missing compliant boolean for ACCEPTED status.")
            if 'violations' not in gt or not isinstance(gt['violations'], list):
                raise ValueError(f"Sample {s_id} missing violations list.")
                
            for v in gt['violations']:
                if 'type' not in v or v['type'] not in cls.VALID_VIOLATIONS:
                    raise ValueError(f"Sample {s_id} has invalid violation type.")
