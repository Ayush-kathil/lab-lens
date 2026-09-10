import hashlib
from pathlib import Path
import argparse

def check_duplicates(dataset_dir):
    dataset_root = Path(dataset_dir).resolve()
    
    file_names = {}
    file_hashes = {}
    
    dup_names = []
    dup_hashes = []
    
    images = list(dataset_root.rglob("*.jpg")) + list(dataset_root.rglob("*.png"))
    
    for img in images:
        name = img.name
        if name in file_names:
            dup_names.append((str(img), str(file_names[name])))
        else:
            file_names[name] = img
            
        # Lightweight hash (first 100k)
        with open(img, 'rb') as f:
            h = hashlib.md5(f.read(100000)).hexdigest()
        if h in file_hashes:
            dup_hashes.append((str(img), str(file_hashes[h])))
        else:
            file_hashes[h] = img
            
    print(f"Total Images Scanned: {len(images)}")
    print(f"Duplicate Filenames: {len(dup_names)}")
    print(f"Duplicate Hashes (Exact content dupes): {len(dup_hashes)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    args = parser.parse_args()
    check_duplicates(args.dataset)
