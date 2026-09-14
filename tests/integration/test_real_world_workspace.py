import pytest
import json
import os
from pathlib import Path

def test_source_manifest_integrity():
    manifest_path = "Dataset/SpatialComplianceReal/metadata/source_manifest.json"
    assert os.path.exists(manifest_path)
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert len(data) >= 16
    
    seen_hashes = set()
    for item in data:
        assert "sample_id" in item
        assert "session_id" in item
        assert "license" in item
        assert "original_sha256" in item
        
        # Duplicate detection check
        assert item["original_sha256"] not in seen_hashes
        seen_hashes.add(item["original_sha256"])

def test_annotation_workspace_status():
    ann_dir = "Dataset/SpatialComplianceReal/annotations"
    assert os.path.exists(ann_dir)
    
    files = list(Path(ann_dir).glob("*.json"))
    assert len(files) >= 16
    
    for ann_file in files:
        with open(ann_file, "r", encoding="utf-8") as f:
            ann = json.load(f)
            
        assert ann["annotation_status"] in ("NEEDS_REVIEW", "AI_GENERATED")
        assert "HUMAN_VERIFIED" not in ann["annotation_status"]
        assert ann.get("ground_truth", {}).get("compliant") is None
