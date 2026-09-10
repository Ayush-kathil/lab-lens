import argparse
import os
import ctypes
from ctypes import wintypes
from pathlib import Path
import json

def get_long_path_name(path_str):
    try:
        buffer = ctypes.create_unicode_buffer(500)
        ctypes.windll.kernel32.GetLongPathNameW(path_str, buffer, 500)
        long_path = buffer.value
        return long_path if long_path else path_str
    except Exception:
        return path_str

def audit_dataset_pairs(dataset_dir):
    dataset_path = Path(dataset_dir).resolve()
    splits = ['train', 'valid', 'test']
    
    report = {
        'splits': {}
    }

    for split in splits:
        split_path = dataset_path / split
        img_dir = split_path / 'images'
        lbl_dir = split_path / 'labels'
        
        if not img_dir.exists() or not lbl_dir.exists():
            report['splits'][split] = {'error': 'Missing images or labels directory'}
            continue
            
        images = list(img_dir.iterdir())
        labels = list(lbl_dir.iterdir())
        
        # 1. Check direct stem matches
        img_stems_direct = {f.stem for f in images}
        lbl_stems_direct = {f.stem for f in labels}
        
        direct_paired = img_stems_direct.intersection(lbl_stems_direct)
        
        # 2. Check long path matches if direct match is low
        img_stems_long = {Path(get_long_path_name(str(f))).stem for f in images}
        lbl_stems_long = {Path(get_long_path_name(str(f))).stem for f in labels}
        
        long_paired = img_stems_long.intersection(lbl_stems_long)
        
        # 3. Check stripped _jpg.rf hashes
        def strip_rf(s):
            return s.split("_jpg.rf")[0] if "_jpg.rf" in s else s
        
        img_stems_stripped = {strip_rf(s) for s in img_stems_long}
        lbl_stems_stripped = {strip_rf(s) for s in lbl_stems_long}
        
        stripped_paired = img_stems_stripped.intersection(lbl_stems_stripped)
        
        report['splits'][split] = {
            'images_count': len(images),
            'labels_count': len(labels),
            'direct_paired': len(direct_paired),
            'long_path_paired': len(long_paired),
            'stripped_paired': len(stripped_paired),
            'unmatched_images': len(images) - len(stripped_paired),
            'unmatched_labels': len(labels) - len(stripped_paired),
            'recommendation': 'SAFE' if len(stripped_paired) >= min(len(images), len(labels)) * 0.99 else 'UNSAFE'
        }
        
    return report

def run_audit(dataset_dir, output_file=None):
    report = audit_dataset_pairs(dataset_dir)
    print("DATASET PAIRING AUDIT")
    print("=====================")
    for split, data in report['splits'].items():
        print(f"\nSplit: {split}")
        for k, v in data.items():
            print(f"  {k}: {v}")
            
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--output', default=None)
    args = parser.parse_args()
    run_audit(args.dataset, args.output)
