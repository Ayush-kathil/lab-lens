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
    parser.add_argument('--telemetry', action='store_true', help="Enable memory telemetry")
    
    # Diagnostic Overrides
    parser.add_argument('--no-plots', action='store_true')
    parser.add_argument('--no-val', action='store_true')
    parser.add_argument('--no-save', action='store_true')
    parser.add_argument('--cache', action='store_true')
    parser.add_argument('--batch-override', type=int, default=None)
    parser.add_argument('--epochs-override', type=int, default=None)
    parser.add_argument('--fraction-override', type=float, default=None)

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
    
    epochs = args.epochs_override if args.epochs_override is not None else config.get('epochs', 1)
    batch = args.batch_override if args.batch_override is not None else config.get('batch_size', 16)
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
    model = YOLO(model_name)
    
    telemetry = None
    if args.telemetry:
        sys.path.append(str(Path(__file__).parent.resolve()))
        try:
            from telemetry import MemoryTelemetry
            run_dir = Path(config.get('project', 'outputs')) / name
            telemetry = MemoryTelemetry(run_dir)
            telemetry.record("process_start")
            telemetry.attach(model)
            print(f"Memory telemetry attached. Logging to {telemetry.csv_path}")
        except Exception as e:
            print(f"Warning: Failed to attach telemetry: {e}")
    
    print("\nStarting training...")
    try:
        if telemetry:
            telemetry.record("before_model_train")
            
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
            workers=config.get('workers', 0),
            fraction=args.fraction_override if args.fraction_override is not None else config.get('fraction', 1.0),
            val=not args.no_val,
            plots=not args.no_plots,
            save=not args.no_save,
            cache=args.cache,
            patience=config.get('patience', 50),
            hsv_h=config.get('hsv_h', 0.015),
            hsv_s=config.get('hsv_s', 0.7),
            hsv_v=config.get('hsv_v', 0.4),
            degrees=config.get('degrees', 0.0),
            translate=config.get('translate', 0.1),
            scale=config.get('scale', 0.5),
            fliplr=config.get('fliplr', 0.5),
            mosaic=config.get('mosaic', 1.0)
        )
        print("\nTraining completed successfully.")
    except Exception as e:
        if telemetry:
            telemetry.record("exception_oom_path")
        print(f"\nError during training: {e}")
        sys.exit(1)
    finally:
        if telemetry:
            telemetry.record("process_exit")

if __name__ == '__main__':
    main()
