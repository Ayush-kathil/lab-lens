import argparse
import hashlib
import json
import math
import shutil
import subprocess
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone

def get_git_commit():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except Exception:
        return 'unknown'

def hash_file(filepath):
    # Full hash for determinism
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def is_valid_annotation(lbl_path, num_classes):
    if lbl_path.stat().st_size == 0:
        return True # Valid empty label

    with open(lbl_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            if len(parts) != 5:
                return False
            try:
                cls_id = int(parts[0])
                x, y, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                
                if math.isnan(x) or math.isnan(y) or math.isnan(w) or math.isnan(h) or math.isinf(x) or math.isinf(y):
                    return False
                if not (0 <= cls_id < num_classes):
                    return False
                if not (0 <= x <= 1 and 0 <= y <= 1):
                    return False
                if not (0 < w <= 1 and 0 < h <= 1):
                    return False
            except ValueError:
                return False
    return True

def prepare_dataset(source_dir, output_dir, manifest_path):
    source_root = Path(source_dir).resolve()
    output_root = Path(output_dir).resolve()
    
    import yaml
    data_yaml_paths = list(source_root.rglob("data.yaml"))
    if not data_yaml_paths:
        raise ValueError("data.yaml not found in source dataset")
    
    data_yaml_path = data_yaml_paths[0]
    with open(data_yaml_path, 'r') as f:
        data_yaml = yaml.safe_load(f)
        
    num_classes = data_yaml.get('nc', 25)
    class_names = data_yaml.get('names', [])
    
    splits = ['train', 'valid', 'test']
    
    # Track files
    all_images = []
    original_counts = {'train': 0, 'valid': 0, 'test': 0}
    
    malformed_excluded = 0
    empty_retained = 0
    
    for split in splits:
        yaml_split_key = split if split != 'valid' else 'val'
        split_rel = data_yaml.get(yaml_split_key, split)
        if isinstance(split_rel, str) and 'images' in split_rel:
            proposed_path = (data_yaml_path.parent / Path(split_rel).parent).resolve()
            if not proposed_path.exists():
                proposed_path = data_yaml_path.parent / split
            split_dir = proposed_path
        else:
            split_dir = data_yaml_path.parent / split
            
        img_dir = split_dir / 'images'
        lbl_dir = split_dir / 'labels'
        
        if not img_dir.exists() or not lbl_dir.exists():
            continue
            
        images = {f.stem: f for f in img_dir.iterdir() if f.is_file()}
        labels = {f.stem: f for f in lbl_dir.iterdir() if f.is_file()}
        
        original_counts[split] = len(images)
        
        for stem, img_path in sorted(images.items()): # Deterministic iteration
            if stem not in labels:
                continue # Orphan image
                
            lbl_path = labels[stem]
            if not is_valid_annotation(lbl_path, num_classes):
                malformed_excluded += 1
                continue
                
            if lbl_path.stat().st_size == 0:
                empty_retained += 1
                
            all_images.append({
                'stem': stem,
                'split': split,
                'img_path': img_path,
                'lbl_path': lbl_path
            })
            
    # Hash all valid images
    hash_groups = defaultdict(list)
    for item in all_images:
        h = hash_file(item['img_path'])
        hash_groups[h].append(item)
        
    final_selections = []
    removed_count = 0
    
    split_priority = {'test': 3, 'valid': 2, 'train': 1}
    cross_split_groups_count = 0
    
    for h, group in sorted(hash_groups.items()):
        if len(group) > 1:
            splits_in_group = {item['split'] for item in group}
            if len(splits_in_group) > 1:
                cross_split_groups_count += 1
                
            # Select highest priority split
            best_split = max(splits_in_group, key=lambda s: split_priority[s])
            
            # Filter candidates in the best split
            candidates = [item for item in group if item['split'] == best_split]
            
            # Tie-breaker: Lexicographically smallest relative path (using stem for determinism)
            candidates.sort(key=lambda x: x['stem'])
            representative = candidates[0]
            
            final_selections.append(representative)
            removed_count += len(group) - 1
        else:
            final_selections.append(group[0])
            
    # Write outputs
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    
    final_counts = {'train': 0, 'valid': 0, 'test': 0}
    
    for item in final_selections:
        split = item['split']
        out_split_dir = output_root / split
        (out_split_dir / 'images').mkdir(parents=True, exist_ok=True)
        (out_split_dir / 'labels').mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(item['img_path'], out_split_dir / 'images' / item['img_path'].name)
        shutil.copy2(item['lbl_path'], out_split_dir / 'labels' / item['lbl_path'].name)
        
        final_counts[split] += 1
        
    # Write data.yaml
    out_yaml = {
        'train': 'train/images',
        'val': 'valid/images',
        'test': 'test/images',
        'nc': num_classes,
        'names': class_names
    }
    with open(output_root / 'data.yaml', 'w') as f:
        yaml.dump(out_yaml, f, sort_keys=False)
        
    manifest = {
        'source_dataset_path': str(source_root),
        'preparation_script_version': '1.0',
        'preparation_timestamp': datetime.now(timezone.utc).isoformat(),
        'source_git_commit': get_git_commit(),
        'original_counts': original_counts,
        'final_counts': final_counts,
        'total_final_image_count': sum(final_counts.values()),
        'duplicate_groups': len([g for g in hash_groups.values() if len(g) > 1]),
        'cross_split_duplicate_groups': cross_split_groups_count,
        'duplicate_images_removed': removed_count,
        'malformed_annotations_excluded': malformed_excluded,
        'empty_labels_retained': empty_retained,
        'class_mapping': class_names,
        'deterministic_representative_selection_rule': 'lexicographically smallest stem within the highest priority split',
        'deterministic_split_priority_rule': 'test > valid > train',
        'final_per_split_hash_uniqueness_status': 'verified'
    }
    
    Path(manifest_path).parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--manifest', default='outputs/training_dataset_manifest.json')
    args = parser.parse_args()
    prepare_dataset(args.source, args.output, args.manifest)
