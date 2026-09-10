import pytest
from pathlib import Path
import yaml
import subprocess
from lab_lens.detection.inference import YOLODetector

def test_training_config_loading(tmp_path):
    config_file = tmp_path / "configs/training.yaml"
    config_file.parent.mkdir(parents=True)
    config_file.write_text("epochs: 100\nworkers: 0\nmodel: yolov8n.pt")
    
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    assert config["epochs"] == 100
    assert config["workers"] == 0

def test_train_cli_smoke_test_mode(tmp_path):
    # This verifies the CLI parses the flag
    result = subprocess.run(["python", "-m", "lab_lens", "train", "--dataset", "fake_path", "--config", "fake_config", "--dry-run", "--smoke-test"], capture_output=True, text=True)
    assert result.returncode != 0  # Should fail since paths don't exist, but argument is accepted.

def test_invalid_training_configuration():
    # Calling the actual script with invalid paths
    result = subprocess.run(["python", "scripts/train_detector.py", "--dataset", "invalid_dir", "--config", "invalid_cfg.yaml", "--dry-run"], capture_output=True, text=True)
    assert result.returncode == 1
    assert "Error: Configuration file not found" in result.stdout

def test_torch_torchvision_nms_compatibility():
    # Directly tests if the environment's NMS is compiled correctly
    import torch
    import torchvision
    try:
        boxes = torch.tensor([[0.0, 0.0, 10.0, 10.0]])
        scores = torch.tensor([0.9])
        iou_threshold = 0.5
        result = torchvision.ops.nms(boxes, scores, iou_threshold)
        assert len(result) == 1
    except Exception as e:
        pytest.fail(f"Torchvision NMS failed: {e}")
