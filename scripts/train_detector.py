import argparse
import sys
import yaml
from pathlib import Path

try:
    from ultralytics import YOLO
    import torch
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False

def validate_config(config_path):
    if not Path(config_path).exists():
        print(f"Error: Configuration file not found at {config_path}")
        sys.exit(1)
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def validate_dataset(dataset_path):
    dataset_dir = Path(dataset_path)
    if not dataset_dir.exists():
        print(f"Error: Dataset directory not found at {dataset_path}")
        sys.exit(1)
    
    data_yaml = dataset_dir / "data.yaml"
    if not data_yaml.exists():
        print(f"Error: data.yaml not found at {data_yaml}")
        sys.exit(1)

    train_dir = dataset_dir / "train" / "images"
    valid_dir = dataset_dir / "valid" / "images"
    test_dir = dataset_dir / "test" / "images"
    
    train_count = len(list(train_dir.iterdir())) if train_dir.exists() else 0
    valid_count = len(list(valid_dir.iterdir())) if valid_dir.exists() else 0
    test_count = len(list(test_dir.iterdir())) if test_dir.exists() else 0
    
    return {
        "train": train_count,
        "valid": valid_count,
        "test": test_count,
        "total": train_count + valid_count + test_count
    }

def get_framework_versions():
    versions = {}
    try:
        import torch
        versions['torch'] = torch.__version__
    except ImportError:
        versions['torch'] = "NOT INSTALLED"
        
    try:
        import ultralytics
        versions['ultralytics'] = ultralytics.__version__
    except ImportError:
        versions['ultralytics'] = "NOT INSTALLED"
        
    return versions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True, help="Path to training dataset directory")
    parser.add_argument('--config', required=True, help="Path to training configuration yaml")
    parser.add_argument('--dry-run', action='store_true', help="Print configuration without training")
    parser.add_argument('--smoke-test', action='store_true', help="Run a 1-epoch tiny training run")
    args = parser.parse_args()

    config = validate_config(args.config)
    counts = validate_dataset(args.dataset)
    versions = get_framework_versions()
    
    print("========================================")
    print("       TRAINING CONFIGURATION           ")
    print("========================================")
    print(f"Dataset             : {args.dataset}")
    print(f"Train/Valid/Test    : {counts['train']} / {counts['valid']} / {counts['test']}")
    print(f"Model               : {config.get('model', 'Unknown')}")
    print(f"Epochs              : {config.get('epochs', 'Unknown')}")
    print(f"Batch Size          : {config.get('batch_size', 'Unknown')}")
    print(f"Image Size          : {config.get('image_size', 'Unknown')}")
    print(f"Device              : {config.get('device', 'Unknown')}")
    print(f"Seed                : {config.get('seed', 'Unknown')}")
    print(f"Project             : {config.get('project', 'Unknown')}")
    print(f"Name                : {config.get('name', 'Unknown')}")
    print(f"Deterministic       : {config.get('deterministic', True)}")
    print("--- Frameworks ---")
    print(f"PyTorch             : {versions['torch']}")
    print(f"Ultralytics         : {versions['ultralytics']}")
    print("========================================")
    
    if args.dry_run:
        print("\nDry-run completed. No training started.")
        sys.exit(0)
        
    if not ULTRALYTICS_AVAILABLE:
        print("Error: ultralytics is required for real training.")
        sys.exit(1)

    # Resolve actual paths relative to current working directory
    data_yaml_path = Path(args.dataset) / "data.yaml"
    model_name = config.get('model', 'yolov8n.pt')
    
    epochs = config.get('epochs', 1)
    batch = config.get('batch_size', 16)
    imgsz = config.get('image_size', 640)
    name = config.get('name', 'baseline_training')
    
    if args.smoke_test:
        print("\n--- SMOKE TEST OVERRIDE ---")
        epochs = 1
        batch = 2
        name = "smoke_test"
        print(f"Forcing Epochs: {epochs}, Batch Size: {batch}, Name: {name}")

    print("\nInitializing YOLO model...")
    import torch
    import ultralytics
    # PyTorch 2.6 defaults to weights_only=True which breaks older Ultralytics weights
    original_torch_load = torch.load
    def safe_torch_load(*args, **kwargs):
        kwargs["weights_only"] = False
        return original_torch_load(*args, **kwargs)
    torch.load = safe_torch_load
        
    model = YOLO(model_name)
    
    print("\nStarting training...")
    try:
        results = model.train(
            data=str(data_yaml_path.resolve()),
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            device=config.get('device', 'cpu'),
            seed=config.get('seed', 42),
            deterministic=config.get('deterministic', True),
            project=config.get('project', 'outputs'),
            name=name,
            workers=config.get('workers', 4),
            fraction=config.get('fraction', 1.0),
            val=True
        )
        print("\nTraining completed successfully.")
    except Exception as e:
        print(f"\nError during training: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
