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

    args = parser.parse_args()

    if args.command == "validate-dataset":
        # Call the script
        script_path = Path(__file__).parent.parent.parent / "scripts" / "validate_dataset.py"
        subprocess.run([sys.executable, str(script_path), "--dataset", args.dataset])
    elif args.command == "inspect-dataset":
        # Basic inspection, same script with different logic or just print info
        script_path = Path(__file__).parent.parent.parent / "scripts" / "inspect_dataset.py"
        subprocess.run([sys.executable, str(script_path), "--dataset", args.dataset])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
