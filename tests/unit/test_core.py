import pytest
from pathlib import Path
from lab_lens.config.loader import load_config, ConfigurationError
from lab_lens.utils.validation import validate_image_path, ValidationError

def test_config_loading(tmp_path):
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("dataset_path: 'Dataset/ChemEq25'\nconfidence_threshold: 0.5")
    
    data = load_config(str(config_file))
    assert data["dataset_path"] == "Dataset/ChemEq25"
    assert data["confidence_threshold"] == 0.5

def test_config_loading_invalid_file():
    with pytest.raises(ConfigurationError):
        load_config("non_existent_file.yaml")

def test_image_path_validation(tmp_path):
    valid_img = tmp_path / "test.jpg"
    valid_img.touch()
    
    validated = validate_image_path(str(valid_img))
    assert validated == valid_img

def test_image_path_invalid_extension(tmp_path):
    invalid_ext = tmp_path / "test.txt"
    invalid_ext.touch()
    
    with pytest.raises(ValidationError, match="Unsupported image extension"):
        validate_image_path(str(invalid_ext))
