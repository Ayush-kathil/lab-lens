import argparse
import yaml
import json
import math
from pathlib import Path
from collections import defaultdict
import csv

def validate(dataset_dir: str):
    dataset_root = Path(dataset_dir).resolve()
    if not dataset_root.exists():
        print(f"Error: Dataset path {dataset_root} does not exist.")
        return

    # Find data.yaml
    data_yaml_paths = list(dataset_root.rglob("data.yaml"))
    if not data_yaml_paths:
        print(f"Error: data.yaml not found inside {dataset_root}")
        return
        
    data_yaml_path = data_yaml_paths[0]
    actual_root = data_yaml_path.parent
    print(f"Actual Dataset Root: {actual_root}")
    
    with open(data_yaml_path, 'r') as f:
        data_yaml = yaml.safe_load(f)
        
    # Read classes
    num_classes = data_yaml.get('nc', 0)
    class_names = data_yaml.get('names', [])
    if num_classes != len(class_names):
        print("Warning: 'nc' does not match length of 'names' array in data.yaml")
        
    print(f"Total Classes in YAML: {num_classes}")
    
    # Try find Metadata.csv
    metadata_csv_path = actual_root / "Metadata.csv"
    has_metadata = metadata_csv_path.exists()
    print(f"Metadata.csv present: {has_metadata}")
    
    splits = ['train', 'valid', 'test']
    
    overall_status = "SAFE_FOR_TRAINING"
    stats = {
        'total_images': 0,
        'total_labels': 0,
        'total_empty_labels': 0,
        'total_invalid_annotations': 0,
        'total_paired': 0,
        'total_orphan_images': 0,
        'total_orphan_labels': 0,
        'total_instances': 0
    }
    
    class_distribution = {split: defaultdict(int) for split in splits}
    class_distribution['total'] = defaultdict(int)
    
    invalid_files = []
    
    for split in splits:
        print(f"\n--- Split: {split} ---")
        
        # Read from yaml if possible
        yaml_split_key = split if split != 'valid' else 'val'
        split_rel = data_yaml.get(yaml_split_key, split)
        
        if isinstance(split_rel, str) and 'images' in split_rel:
            proposed_path = (actual_root / Path(split_rel).parent).resolve()
            if not proposed_path.exists():
                # Fallback if Roboflow generated relative paths incorrectly
                proposed_path = actual_root / split
            split_dir = proposed_path
        else:
            split_dir = actual_root / split
            
        img_dir = split_dir / 'images'
        lbl_dir = split_dir / 'labels'
        
        if not img_dir.exists() or not lbl_dir.exists():
            print(f"  Missing images or labels directory: {img_dir} | {lbl_dir}")
            overall_status = "NOT_SAFE_FOR_TRAINING"
            continue
            
        images = {f.stem: f for f in img_dir.iterdir() if f.is_file()}
        labels = {f.stem: f for f in lbl_dir.iterdir() if f.is_file()}
        
        paired = set(images.keys()).intersection(set(labels.keys()))
        orphan_images = set(images.keys()) - set(labels.keys())
        orphan_labels = set(labels.keys()) - set(images.keys())
        
        split_invalid = 0
        split_empty = 0
        split_instances = 0
        
        for stem, f_path in labels.items():
            if f_path.stat().st_size == 0:
                split_empty += 1
                continue
                
            is_invalid = False
            error_reason = ""
            with open(f_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    if len(parts) != 5:
                        is_invalid = True
                        error_reason = "wrong_number_of_fields"
                        break
                        
                    try:
                        cls_id = int(parts[0])
                        x, y, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                        
                        if math.isnan(x) or math.isnan(y) or math.isnan(w) or math.isnan(h) or math.isinf(x) or math.isinf(y):
                            is_invalid = True
                            error_reason = "nan_or_inf"
                            break
                            
                        if not (0 <= cls_id < num_classes):
                            is_invalid = True
                            error_reason = "class_id_out_of_range"
                            break
                            
                        if not (0 <= x <= 1 and 0 <= y <= 1):
                            is_invalid = True
                            error_reason = "coords_out_of_bounds"
                            break
                            
                        if not (0 < w <= 1 and 0 < h <= 1):
                            is_invalid = True
                            error_reason = "dimensions_invalid"
                            break
                            
                        class_distribution[split][cls_id] += 1
                        class_distribution['total'][cls_id] += 1
                        split_instances += 1
                        
                    except ValueError:
                        is_invalid = True
                        error_reason = "non_numeric_values"
                        break
                        
            if is_invalid:
                split_invalid += 1
                invalid_files.append({"file": f_path.name, "split": split, "error": error_reason, "action": "EXCLUDE"})
                
        print(f"Images: {len(images)}")
        print(f"Labels: {len(labels)}")
        print(f"Paired: {len(paired)}")
        print(f"Orphan Images: {len(orphan_images)}")
        print(f"Orphan Labels: {len(orphan_labels)}")
        print(f"Empty Labels (Negatives): {split_empty}")
        print(f"Invalid Annotations: {split_invalid}")
        
        stats['total_images'] += len(images)
        stats['total_labels'] += len(labels)
        stats['total_paired'] += len(paired)
        stats['total_orphan_images'] += len(orphan_images)
        stats['total_orphan_labels'] += len(orphan_labels)
        stats['total_empty_labels'] += split_empty
        stats['total_invalid_annotations'] += split_invalid
        stats['total_instances'] += split_instances
        
        if len(orphan_images) > 0 or len(orphan_labels) > 0:
            overall_status = "NOT_SAFE_FOR_TRAINING"

    print("\n--- Summary Statistics ---")
    for k, v in stats.items():
        print(f"{k}: {v}")
        
    print(f"\nFinal Readiness Decision: {overall_status}")
    
    if invalid_files:
        print("\nInvalid Annotation Policy:")
        for inv in invalid_files:
            print(f"- {inv['split']}/{inv['file']}: {inv['error']} -> Action: {inv['action']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True, help="Path to dataset directory")
    args = parser.parse_args()
    validate(args.dataset)
