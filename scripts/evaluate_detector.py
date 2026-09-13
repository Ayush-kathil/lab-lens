import argparse
import sys
import json
from pathlib import Path

# Add src to path so we can import internal modules easily if run directly
sys.path.append(str(Path(__file__).parent.parent / "src"))

from lab_lens.detection.evaluator import DetectorEvaluator, EvaluationConfig

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help="Path to trained model weights (.pt)")
    parser.add_argument('--dataset', required=True, help="Path to evaluation dataset YAML")
    parser.add_argument('--split', default='test', choices=['train', 'val', 'test'], help="Dataset split to evaluate")
    parser.add_argument('--imgsz', type=int, default=640, help="Image size for inference")
    parser.add_argument('--batch', type=int, default=8, help="Batch size for evaluation dataloader")
    parser.add_argument('--device', default='cpu', help="Device to run on (e.g., cpu, cuda:0)")
    args = parser.parse_args()

    config = EvaluationConfig(
        weights_path=args.model,
        dataset_yaml=args.dataset,
        split=args.split,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device
    )
    
    evaluator = DetectorEvaluator(config)
    
    print("========================================")
    print("      HELD-OUT DETECTOR EVALUATION      ")
    print("========================================")
    print(f"Model   : {args.model}")
    print(f"Dataset : {args.dataset}")
    print(f"Split   : {args.split}")
    print("========================================")
    
    try:
        results = evaluator.evaluate()
        
        print("\n--- OVERALL METRICS ---")
        overall = results["overall"]
        print(f"Precision : {overall['precision']:.5f}")
        print(f"Recall    : {overall['recall']:.5f}")
        print(f"mAP@50    : {overall['map50']:.5f}")
        print(f"mAP@50:95 : {overall['map50_95']:.5f}")
        
        print("\n--- PER-CLASS METRICS ---")
        per_class = results["per_class"]
        for c, m in sorted(per_class.items()):
            print(f"{c:2d} | {m['name']:<45} | P: {m['precision']:.5f} | R: {m['recall']:.5f} | AP50: {m['map50']:.5f} | AP50-95: {m['map50_95']:.5f}")
            
        print("\n--- ARTIFACTS ---")
        print(f"Artifacts (including Confusion Matrix) saved to: {results['save_dir']}")
        
    except Exception as e:
        print(f"\nEvaluation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
