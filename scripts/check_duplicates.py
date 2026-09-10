import hashlib
from pathlib import Path
import argparse
import json

def analyze_duplicates(dataset_dir):
    dataset_root = Path(dataset_dir).resolve()
    images = list(dataset_root.rglob("*.jpg")) + list(dataset_root.rglob("*.png"))
    
    file_hashes = {}
    dup_groups = {}
    
    for img in images:
        split = "unknown"
        if "train" in img.parts: split = "train"
        elif "valid" in img.parts or "val" in img.parts: split = "valid"
        elif "test" in img.parts: split = "test"
            
        with open(img, 'rb') as f:
            h = hashlib.md5(f.read(100000)).hexdigest()
            
        if h not in file_hashes:
            file_hashes[h] = [(str(img.name), split)]
        else:
            file_hashes[h].append((str(img.name), split))
            dup_groups[h] = file_hashes[h]

    total_groups = len(dup_groups)
    cross_split_leakage = False
    leakage_details = []
    
    for h, group in dup_groups.items():
        splits_involved = {item[1] for item in group}
        if len(splits_involved) > 1:
            cross_split_leakage = True
            leakage_details.append(group)
            
    print(f"Total Images Scanned: {len(images)}")
    print(f"Total Duplicate Groups: {total_groups}")
    print(f"Cross-Split Leakage Exists: {cross_split_leakage}")
    if cross_split_leakage:
        print("LEAKAGE FOUND:")
        for g in leakage_details:
            print(f" - {g}")
            
    with open("docs/DATASET_DUPLICATE_ANALYSIS.md", "w") as f:
        f.write("# Dataset Duplicate Analysis\n\n")
        f.write(f"- Total Images Scanned: {len(images)}\n")
        f.write(f"- Total Duplicate Groups: {total_groups}\n")
        f.write(f"- Cross-Split Leakage Exists: {cross_split_leakage}\n\n")
        if cross_split_leakage:
            f.write("## Cross-Split Leakage Details\n")
            for g in leakage_details:
                f.write(f"- {g}\n")
        else:
            f.write("No identical image files exist across train, validation, and test splits.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    args = parser.parse_args()
    analyze_duplicates(args.dataset)
