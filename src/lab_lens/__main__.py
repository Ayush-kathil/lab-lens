import argparse
import sys
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(prog="lab_lens", description="Lab Lens CLI")
    subparsers = parser.add_subparsers(dest="command")

    # validate-dataset
    val_parser = subparsers.add_parser("validate-dataset", help="Validate a dataset structure and annotations")
    val_parser.add_argument("--dataset", required=True, help="Path to dataset")

    # inspect-dataset
    ins_parser = subparsers.add_parser("inspect-dataset", help="Inspect dataset class distribution")
    ins_parser.add_argument("--dataset", required=True, help="Path to dataset")

    # audit-dataset-pairs
    adt_parser = subparsers.add_parser("audit-dataset-pairs", help="Audit dataset pairing 8.3 filenames")
    adt_parser.add_argument("--dataset", required=True, help="Path to dataset")

    # quality
    q_parser = subparsers.add_parser("quality", help="Run image quality analysis")
    q_parser.add_argument("--input", required=True, help="Path to input image")
    q_parser.add_argument("--config", default="configs/default.yaml", help="Path to config file")

    # system-info
    sys_parser = subparsers.add_parser("system-info", help="Print system and hardware information")
    
    # prepare-dataset
    prep_parser = subparsers.add_parser("prepare-dataset", help="Deterministically repair and prepare dataset")
    prep_parser.add_argument("--source", required=True, help="Path to source dataset")
    prep_parser.add_argument("--output", required=True, help="Path to output derived dataset")
    
    # verify-dataset
    vf_parser = subparsers.add_parser("verify-dataset", help="Verify the prepared dataset")
    vf_parser.add_argument("--dataset", required=True, help="Path to derived dataset")

    # train
    tr_parser = subparsers.add_parser("train", help="Train the detector")
    tr_parser.add_argument("--dataset", required=True, help="Path to dataset")
    tr_parser.add_argument("--config", required=True, help="Path to training config")
    tr_parser.add_argument("--dry-run", action="store_true", help="Print config without training")

    # evaluate
    ev_parser = subparsers.add_parser("evaluate", help="Evaluate the detector")
    ev_parser.add_argument("--model", required=True, help="Path to model weights")
    ev_parser.add_argument("--dataset", required=True, help="Path to evaluation dataset")

    # predict
    pr_parser = subparsers.add_parser("predict", help="Run detector prediction")
    pr_parser.add_argument("--model", required=True, help="Path to model weights")
    pr_parser.add_argument("--input", required=True, help="Path to input image")

    args = parser.parse_args()

    def run_script(script_name, *args_list):
        script_path = Path(__file__).parent.parent.parent / "scripts" / script_name
        result = subprocess.run([sys.executable, str(script_path), *args_list])
        if result.returncode != 0:
            sys.exit(result.returncode)

    if args.command == "validate-dataset":
        run_script("validate_dataset.py", "--dataset", args.dataset)
    elif args.command == "inspect-dataset":
        run_script("inspect_dataset.py", "--dataset", args.dataset)
    elif args.command == "audit-dataset-pairs":
        run_script("audit_dataset_pairs.py", "--dataset", args.dataset)
    elif args.command == "system-info":
        run_script("system_info.py")
    elif args.command == "prepare-dataset":
        run_script("prepare_training_dataset.py", "--source", args.source, "--output", args.output)
    elif args.command == "verify-dataset":
        run_script("verify_training_dataset.py", "--dataset", args.dataset)
    elif args.command == "train":
        cmd = ["--dataset", args.dataset, "--config", args.config]
        if args.dry_run: cmd.append("--dry-run")
        run_script("train_detector.py", *cmd)
    elif args.command == "evaluate":
        run_script("evaluate_detector.py", "--model", args.model, "--dataset", args.dataset)
    elif args.command == "predict":
        # inline predict scaffold
        import cv2
        from lab_lens.detection.inference import YOLODetector
        try:
            detector = YOLODetector()
            detector.load_model(args.model)
            img = cv2.imread(args.input)
            if img is None:
                print(f"Error: Could not load image {args.input}")
                sys.exit(1)
            detections = detector.predict(img)
            print("Detected equipment:")
            for d in detections:
                print(f"{d.class_name.ljust(20)} {d.confidence:.2f} ({d.x1:.1f}, {d.y1:.1f}, {d.x2:.1f}, {d.y2:.1f})")
        except Exception as e:
            print(f"Error during prediction: {e}")
            sys.exit(1)
    elif args.command == "quality":
        from lab_lens.config.loader import load_config
        from lab_lens.preprocessing.image_quality import analyze_image_quality
        import cv2
        
        try:
            config = load_config(args.config)
            img = cv2.imread(args.input)
            if img is None:
                print(f"Error: Could not load image {args.input}")
                sys.exit(1)
                
            res = analyze_image_quality(img, config)
            print("LAB LENS — IMAGE QUALITY ANALYSIS\n")
            print(f"Image: {args.input}")
            print(f"Resolution: {res.width}x{res.height}")
            print(f"Brightness: {res.brightness:.2f}")
            print(f"Contrast: {res.contrast:.2f}")
            print(f"Blur: {res.blur_score:.2f}\n")
            print(f"Overall quality: {res.status}")
            print(f"Warnings: {', '.join(res.warnings) if res.warnings else 'None'}")
            
            if res.status == "FAIL":
                sys.exit(1)
        except Exception as e:
            print(f"Error processing image: {e}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
