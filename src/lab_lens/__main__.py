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

    args = parser.parse_args()

    if args.command == "validate-dataset":
        script_path = Path(__file__).parent.parent.parent / "scripts" / "validate_dataset.py"
        subprocess.run([sys.executable, str(script_path), "--dataset", args.dataset])
    elif args.command == "inspect-dataset":
        script_path = Path(__file__).parent.parent.parent / "scripts" / "inspect_dataset.py"
        subprocess.run([sys.executable, str(script_path), "--dataset", args.dataset])
    elif args.command == "audit-dataset-pairs":
        script_path = Path(__file__).parent.parent.parent / "scripts" / "audit_dataset_pairs.py"
        subprocess.run([sys.executable, str(script_path), "--dataset", args.dataset])
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
