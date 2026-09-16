# Complete Project Runbook

This runbook contains the exact commands needed to operate the Lab Lens project from a fresh clone on a Windows PowerShell environment.

### Section 1: Clone repository
*Purpose*: Get the source code.
```powershell
git clone https://github.com/Ayush-kathil/Lab-lens.git
```

### Section 2: Enter directory
*Purpose*: Navigate to project root.
```powershell
cd Lab-lens
```

### Section 3: Install/sync environment
*Purpose*: Install all Python dependencies.
```powershell
uv sync --all-extras
```

### Section 4: Run tests
*Purpose*: Verify core spatial, preprocessing, and detection normalization logic.
```powershell
uv run pytest -q
```

### Section 5: Run inference without setup
*Purpose*: Output pure YOLO object detection results.
```powershell
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt
```

### Section 6: Run inference with compliant configuration
*Purpose*: Execute the full spatial rule engine.
```powershell
uv run python -m lab_lens infer --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt --setup configs/config.yaml
```

### Section 7: Generate combined visualizations
*Purpose*: Produce diagnostic overlays combining YOLO boxes and Canny edges.
```powershell
uv run python scripts/visualize_detection.py --image test-lab.jpg --model runs/detect/outputs/baseline_training_final/weights/best.pt
```

### Section 8: Run human-review status
*Purpose*: Check dataset audit completion.
```powershell
uv run python scripts/review_cli.py status
```
