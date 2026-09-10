import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help="Path to trained model weights")
    parser.add_argument('--dataset', required=True, help="Path to evaluation dataset")
    args = parser.parse_args()

    model_path = Path(args.model)
    if not model_path.exists():
        print(f"Error: Model weights not found at {args.model}")
        sys.exit(1)
        
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"Error: Dataset not found at {args.dataset}")
        sys.exit(1)

    print("========================================")
    print("         EVALUATION SCAFFOLD            ")
    print("========================================")
    print(f"Model   : {args.model}")
    print(f"Dataset : {args.dataset}")
    print("\nError: Evaluation implementation is not authorized in this phase.")
    sys.exit(1)

if __name__ == '__main__':
    main()
