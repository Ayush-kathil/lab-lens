import pytest
import json
import os
from pathlib import Path

def test_ai_generated_status():
    ann_dir = "Dataset/SpatialComplianceReal/annotations"
    files = list(Path(ann_dir).glob("*.json"))
    
    for ann_file in files:
        with open(ann_file, "r", encoding="utf-8") as f:
            ann = json.load(f)
            
        if ann.get("annotation_source") == "AI_GENERATED":
            assert ann.get("ground_truth_status") == "SILVER_LABEL"
            assert "HUMAN_VERIFIED" not in ann.get("annotation_status", "")
            
def test_ai_boxes_valid():
    ann_dir = "Dataset/SpatialComplianceReal/annotations"
    files = list(Path(ann_dir).glob("*.json"))
    
    for ann_file in files:
        with open(ann_file, "r", encoding="utf-8") as f:
            ann = json.load(f)
            
        for obj in ann.get("objects", []):
            box = obj["box"]
            assert 0.0 <= box["x1"] < box["x2"] <= 1.0
            assert 0.0 <= box["y1"] < box["y2"] <= 1.0
            
def test_unique_object_ids():
    ann_dir = "Dataset/SpatialComplianceReal/annotations"
    files = list(Path(ann_dir).glob("*.json"))
    
    for ann_file in files:
        with open(ann_file, "r", encoding="utf-8") as f:
            ann = json.load(f)
            
        obj_ids = [obj["object_id"] for obj in ann.get("objects", [])]
        assert len(obj_ids) == len(set(obj_ids))
        
def test_spatial_references_valid():
    ann_dir = "Dataset/SpatialComplianceReal/annotations"
    files = list(Path(ann_dir).glob("*.json"))
    
    for ann_file in files:
        with open(ann_file, "r", encoding="utf-8") as f:
            ann = json.load(f)
            
        obj_ids = {obj["object_id"] for obj in ann.get("objects", [])}
        rules = ann.get("setup_specification", {}).get("spatial_rules", [])
        
        for rule in rules:
            if "subject_id" in rule:
                assert rule["subject_id"] in obj_ids
            if "target_id" in rule:
                assert rule["target_id"] in obj_ids
