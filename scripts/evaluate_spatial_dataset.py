import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))
from lab_lens.spatial import DatasetValidator, SpatialEvaluationHarness

def main():
    parser = argparse.ArgumentParser(description="Evaluate spatial reasoning engine against custom dataset.")
    parser.add_argument('--dataset', required=True, help="Path to independent ground-truth JSON dataset")
    args = parser.parse_args()

    # 1. Validate dataset
    try:
        DatasetValidator.validate_file(args.dataset)
        print(f"Dataset validation passed for {args.dataset}")
    except Exception as e:
        print(f"Dataset validation failed: {e}")
        sys.exit(1)

    # 2. Evaluate
    report = SpatialEvaluationHarness.evaluate_dataset(args.dataset)
    
    print("========================================")
    print("      SPATIAL REASONING EVALUATION      ")
    print("========================================")
    print(f"Total Samples Tested : {report.total_samples}")
    print(f"Exact Matches        : {report.exact_matches}")
    print(f"Synthetic Fixture Exact-Match Accuracy  : {report.compliance_accuracy * 100:.2f}%")
    
    if report.incorrect_samples:
        print("\n--- Failed Samples ---")
        for s in report.incorrect_samples:
            print(f"  [-] {s}")
            
if __name__ == '__main__':
    main()
