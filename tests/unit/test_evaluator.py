import pytest
from pathlib import Path
from lab_lens.detection.evaluator import DetectorEvaluator, EvaluationConfig

def test_evaluator_config_validation(tmp_path):
    # Setup mock files
    weights = tmp_path / "best.pt"
    dataset = tmp_path / "data.yaml"
    
    # Test 1: Missing weights
    config = EvaluationConfig(str(weights), str(dataset), 'test')
    evaluator = DetectorEvaluator(config)
    with pytest.raises(FileNotFoundError, match="Model weights not found"):
        evaluator.validate_environment()
        
    weights.touch()
    
    # Test 2: Missing dataset
    with pytest.raises(FileNotFoundError, match="Dataset YAML not found"):
        evaluator.validate_environment()
        
    dataset.touch()
    
    # Test 3: Invalid split
    config_invalid_split = EvaluationConfig(str(weights), str(dataset), 'invalid_split')
    evaluator_invalid = DetectorEvaluator(config_invalid_split)
    with pytest.raises(ValueError, match="Invalid split"):
        evaluator_invalid.validate_environment()
        
    # Test 4: Valid configuration passes validation
    config_valid = EvaluationConfig(str(weights), str(dataset), 'test')
    evaluator_valid = DetectorEvaluator(config_valid)
    evaluator_valid.validate_environment()  # Should not raise
