# Lab Lens Command Reference

```bash
# Sync dependencies
uv sync --all-extras

# Run test suite
uv run pytest -q

# Run inference without setup (outputs detections only)
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt

# Run inference with a compliant demo configuration
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/config.yaml

# Output explicit JSON reports
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/config.yaml --json

# Generate Canny + YOLO visualizations
uv run python scripts/visualize_detection.py --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --canny-lower 50 --canny-upper 150 --aperture-size 3

# Check human review semantic status
uv run python scripts/review_cli.py status

# Update a specific bbox human verdict
uv run python scripts/review_cli.py bbox BBOX-001 CORRECT "Class matches visible object"
```
