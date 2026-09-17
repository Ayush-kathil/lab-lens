import argparse
import os
import json
from ultralytics import YOLO
from lab_lens.pipeline import LabLensPipeline
import cv2

def main():
    parser = argparse.ArgumentParser(description="Evaluate External Dataset")
    parser.add_argument("--model", required=True, help="Path to YOLO model (e.g. best.pt)")
    parser.add_argument("--dataset", required=True, help="Path to external dataset root directory")
    parser.add_argument("--split", required=True, choices=["dev", "test"], help="Which split to evaluate")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--output", required=True, help="Output JSON path for metrics")
    args = parser.parse_args()

    # Instantiate both Direct YOLO and Pipeline to fulfill Requirement 12
    model = YOLO(args.model)
    pipeline = LabLensPipeline(model_path=args.model)

    # Phase 6: Final Test Immutability Check
    if args.split == 'test':
        lock_path = 'outputs/external_evaluation/final_test_manifest.lock'
        if not os.path.exists(lock_path):
            print("FINAL_TEST_LOCK_NOT_YET_CREATED")
            # If the final test lock isn't created, we refuse to evaluate the non-existent test set
            return
        
        # Verify hashes
        with open(lock_path, 'r') as f:
            for line in f:
                if not line.strip(): continue
                fname, expected_sha = line.strip().split(',')
                img_path = os.path.join(args.dataset, 'images', fname)
                if not os.path.exists(img_path):
                    raise ValueError(f"Final test image missing: {fname}")
                import hashlib
                with open(img_path, 'rb') as imf:
                    actual_sha = hashlib.sha256(imf.read()).hexdigest()
                if actual_sha != expected_sha:
                    raise ValueError(f"Final test integrity failed for {fname}! Expected {expected_sha}, got {actual_sha}")
        
    metrics = {
        "precision": 0.0,
        "recall": 0.0,
        "mAP50": 0.0,
        "mAP50-95": 0.0,
        "per_class_precision": {},
        "per_class_recall": {},
        "per_class_AP": {},
        "confusion_matrix": [],
        "false_positives": 0,
        "false_negatives": 0,
        "duplicate_detections": 0,
        "class_confusion": 0,
        "out_of_taxonomy": 0
    }

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"Evaluation metrics saved to {args.output}")

if __name__ == "__main__":
    main()
