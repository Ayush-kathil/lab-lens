import argparse
import json
from pathlib import Path

def clean_stem(filename: str) -> str:
    """
    Cleans the stem to handle Roboflow formats or 8.3 short names if possible.
    Actually, to avoid guessing Windows 8.3 mismatches, we use a basic prefix match or just return the stem.
    Given the constraints, we strip out extensions and normalize to upper case.
    We also remove '_jpg.rf.*' hashes to match original names.
    """
    stem = Path(filename).stem.upper()
    if "_JPG.RF" in stem:
        stem = stem.split("_JPG.RF")[0]
    return stem

def validate(dataset_dir: str):
    dataset_path = Path(dataset_dir)
    if not dataset_path.exists():
        print(f"Error: Dataset path {dataset_path} does not exist.")
        return

    splits = ['train', 'valid', 'test']
    
    overall_status = "PASS"
    total_imgs = 0
    total_lbls = 0
    class_distribution = {}

    for split in splits:
        print(f"\nSplit:\n{split}")
        split_path = dataset_path / split
        img_dir = split_path / 'images'
        lbl_dir = split_path / 'labels'
        
        if not img_dir.exists() or not lbl_dir.exists():
            print(f"  Missing images or labels directory.")
            overall_status = "FAIL"
            continue
            
        images = list(img_dir.iterdir())
        labels = list(lbl_dir.iterdir())
        
        print(f"images: {len(images)}")
        print(f"labels: {len(labels)}")
        
        total_imgs += len(images)
        total_lbls += len(labels)
        
        # Simple count mismatch logic
        # Due to 8.3 filename truncation on some filesystems, exact string matching might fail.
        # We will report orphan counts based on the exact numbers if we can't reliably map them.
        # But we must find the exact orphan if there's exactly 1.
        
        img_stems = {clean_stem(f.name): f for f in images}
        lbl_stems = {clean_stem(f.name): f for f in labels}
        
        orphan_images = set(img_stems.keys()) - set(lbl_stems.keys())
        orphan_labels = set(lbl_stems.keys()) - set(img_stems.keys())
        
        # If the number of stems matches the number of files minus the exact discrepancy,
        # we try to report the raw discrepancy.
        orphan_img_files = [img_stems[s].name for s in orphan_images]
        orphan_lbl_files = [lbl_stems[s].name for s in orphan_labels]
        
        invalid_annotations = 0
        
        for lbl_file in labels:
            if lbl_file.stat().st_size == 0:
                invalid_annotations += 1
                continue
                
            try:
                with open(lbl_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) != 5:
                            invalid_annotations += 1
                            break
                        cls_id, x, y, w, h = parts
                        cls_id = int(cls_id)
                        x, y, w, h = float(x), float(y), float(w), float(h)
                        
                        if not (0 <= cls_id <= 24):
                            invalid_annotations += 1
                            break
                        if not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
                            invalid_annotations += 1
                            break
                        
                        class_distribution[cls_id] = class_distribution.get(cls_id, 0) + 1
            except Exception:
                invalid_annotations += 1

        print(f"orphan images: {len(orphan_images)}")
        print(f"orphan labels: {len(orphan_labels)}")
        print(f"invalid annotations: {invalid_annotations}")
        
        if len(orphan_images) > 0 or len(orphan_labels) > 0:
            if overall_status == "PASS":
                overall_status = "WARN"
                
        if invalid_annotations > 0:
            overall_status = "FAIL"

    print("\nOVERALL DATASET STATUS:")
    print(overall_status)
    
    print("\nClass Distribution (Instances):")
    for k in sorted(class_distribution.keys()):
        print(f"Class {k}: {class_distribution[k]}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True, help="Path to dataset directory")
    args = parser.parse_args()
    validate(args.dataset)
