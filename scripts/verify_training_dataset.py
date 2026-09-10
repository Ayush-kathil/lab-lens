import argparse
import hashlib
from pathlib import Path

def hash_file(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def verify_dataset(dataset_dir):
    dataset_root = Path(dataset_dir).resolve()
    splits = ['train', 'valid', 'test']
    
    split_hashes = {s: set() for s in splits}
    
    errors = []
    
    for split in splits:
        img_dir = dataset_root / split / 'images'
        lbl_dir = dataset_root / split / 'labels'
        
        if not img_dir.exists() or not lbl_dir.exists():
            continue
            
        images = {f.stem: f for f in img_dir.iterdir() if f.is_file()}
        labels = {f.stem: f for f in lbl_dir.iterdir() if f.is_file()}
        
        # E. No orphan images
        orphan_img = set(images.keys()) - set(labels.keys())
        if orphan_img:
            errors.append(f"{split} has orphan images: {len(orphan_img)}")
            
        # F. No orphan labels
        orphan_lbl = set(labels.keys()) - set(images.keys())
        if orphan_lbl:
            errors.append(f"{split} has orphan labels: {len(orphan_lbl)}")
            
        for img in images.values():
            h = hash_file(img)
            # Check within-split uniqueness
            if h in split_hashes[split]:
                errors.append(f"Within-split duplicate found in {split}: {img.name}")
            split_hashes[split].add(h)
            
    # A. No exact image hash occurs in both TRAIN and VALID
    train_valid = split_hashes['train'].intersection(split_hashes['valid'])
    if train_valid:
        errors.append(f"TRAIN and VALID share {len(train_valid)} hashes")
        
    # B. No exact image hash occurs in both TRAIN and TEST
    train_test = split_hashes['train'].intersection(split_hashes['test'])
    if train_test:
        errors.append(f"TRAIN and TEST share {len(train_test)} hashes")
        
    # C. No exact image hash occurs in both VALID and TEST
    valid_test = split_hashes['valid'].intersection(split_hashes['test'])
    if valid_test:
        errors.append(f"VALID and TEST share {len(valid_test)} hashes")
        
    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        exit(1)
    else:
        print("Dataset verification passed! No cross-split leakage or within-split duplicates found.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    args = parser.parse_args()
    verify_dataset(args.dataset)
