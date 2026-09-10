import argparse
import sys
import yaml
from pathlib import Path

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
    print(f"Output Directory    : {config.get('output_directory', 'Unknown')}")
    print("--- Frameworks ---")
    print(f"PyTorch             : {versions['torch']}")
    print(f"Ultralytics         : {versions['ultralytics']}")
    print("========================================")
    
    if args.dry_run:
        print("\nDry-run completed. No training started.")
        sys.exit(0)
        
    print("\nError: Real training is not authorized in this phase.")
    print("Please use --dry-run for testing.")
    sys.exit(1)

if __name__ == '__main__':
    main()
