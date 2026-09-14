import pytest
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from lab_lens.spatial import SpatialEvaluationHarness

def get_file_hash(filepath: str) -> str:
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def test_canonical_fixture_immutability_and_evaluation():
    fixture_path = "Dataset/SpatialCompliance/synthetic_fixtures.json"
    
    # 1. Pre-evaluation hash
    hash_before = get_file_hash(fixture_path)
    
    # 2. Evaluate API multiple times for determinism
    report1 = SpatialEvaluationHarness.evaluate_dataset(fixture_path)
    report2 = SpatialEvaluationHarness.evaluate_dataset(fixture_path)
    report3 = SpatialEvaluationHarness.evaluate_dataset(fixture_path)
    
    # 3. Post-evaluation hash
    hash_after = get_file_hash(fixture_path)
    
    # Assert Immutability
    assert hash_before == hash_after, "Canonical fixture was mutated during evaluation!"
    
    # Assert Correctness
    assert report1.total_samples == 21
    assert report1.exact_matches == 21
    assert report1.compliance_accuracy == 1.0
    
    # Assert Determinism
    assert report1 == report2 == report3, "Evaluations are non-deterministic"

def test_cli_api_consistency():
    fixture_path = "Dataset/SpatialCompliance/synthetic_fixtures.json"
    
    # API
    report = SpatialEvaluationHarness.evaluate_dataset(fixture_path)
    
    # CLI
    result = subprocess.run(
        [sys.executable, "scripts/evaluate_spatial_dataset.py", "--dataset", fixture_path],
        capture_output=True, text=True
    )
    
    assert result.returncode == 0
    assert "Total Samples Tested : 21" in result.stdout
    assert "Exact Matches        : 21" in result.stdout
    assert "Synthetic Fixture Exact-Match Accuracy  : 100.00%" in result.stdout
