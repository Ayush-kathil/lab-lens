import os
import yaml
import json
from pathlib import Path
import argparse

def validate_roboflow(dataset_dir, output_md, output_json):
    base_path = Path(dataset_dir)
    if not base_path.exists():
        return generate_missing_report(base_path, output_md, output_json)
        
    data_yaml_path = base_path / 'data.yaml'
    if not data_yaml_path.exists():
        return generate_error_report(base_path, "data.yaml missing", output_md, output_json)
        
    with open(data_yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        
    splits = ['train', 'valid', 'test']
    
    report = {
        'source': data.get('roboflow', {}).get('url', 'Unknown'),
        'version': data.get('roboflow', {}).get('version', 'Unknown'),
        'classes': data.get('names', []),
        'splits': {},
        'total_images': 0,
        'total_labels': 0,
        'total_invalid': 0,
        'total_empty': 0,
        'total_orphan_images': 0,
        'total_orphan_labels': 0
    }
    
    for split in splits:
        # Determine actual split path from data.yaml, fallback to split name
        split_rel = data.get(split if split != 'valid' else 'val', split)
        # Handle cases where split_rel is a string like "../train/images"
        if isinstance(split_rel, str) and 'images' in split_rel:
            split_dir = base_path / split_rel.split('images')[0].strip('/').strip('.')
        else:
            split_dir = base_path / split
            
        img_dir = split_dir / 'images'
        lbl_dir = split_dir / 'labels'
        
        if not img_dir.exists() or not lbl_dir.exists():
            report['splits'][split] = {'error': 'missing directories'}
            continue
            
        images = {f.stem for f in img_dir.iterdir() if f.is_file()}
        labels = {f.stem for f in lbl_dir.iterdir() if f.is_file()}
        
        paired = images.intersection(labels)
        orphan_img = images - labels
        orphan_lbl = labels - images
        
        invalid_count = 0
        empty_count = 0
        
        for lbl in lbl_dir.iterdir():
            if lbl.stat().st_size == 0:
                empty_count += 1
                continue
            try:
                with open(lbl, 'r') as f:
                    for line in f:
                        parts = line.strip().split()
                        if not parts: continue
                        if len(parts) != 5:
                            invalid_count += 1
                            break
                        try:
                            cls_id = int(parts[0])
                            coords = [float(p) for p in parts[1:]]
                            if not (0 <= cls_id < len(report['classes'])):
                                invalid_count += 1
                                break
                            if not all(0 <= c <= 1 for c in coords):
                                invalid_count += 1
                                break
                            if coords[2] <= 0 or coords[3] <= 0:
                                invalid_count += 1
                                break
                        except ValueError:
                            invalid_count += 1
                            break
            except Exception:
                invalid_count += 1
                
        report['splits'][split] = {
            'images': len(images),
            'labels': len(labels),
            'paired': len(paired),
            'orphan_images': len(orphan_img),
            'orphan_labels': len(orphan_lbl),
            'invalid': invalid_count,
            'empty': empty_count
        }
        
        report['total_images'] += len(images)
        report['total_labels'] += len(labels)
        report['total_orphan_images'] += len(orphan_img)
        report['total_orphan_labels'] += len(orphan_lbl)
        report['total_invalid'] += invalid_count
        report['total_empty'] += empty_count
        
    is_safe = (report['total_orphan_images'] == 0 and 
               report['total_orphan_labels'] == 0 and 
               report['total_invalid'] == 0 and
               report['total_images'] > 0)
               
    report['status'] = "SAFE_FOR_TRAINING" if is_safe else "NOT_SAFE_FOR_TRAINING"
    
    write_reports(report, output_md, output_json if is_safe else None)
    return report

def generate_missing_report(base_path, md_path, json_path):
    rep = {'status': 'NOT_SAFE_FOR_TRAINING', 'error': f'Directory {base_path} not found.'}
    write_reports(rep, md_path, None)
    return rep

def generate_error_report(base_path, msg, md_path, json_path):
    rep = {'status': 'NOT_SAFE_FOR_TRAINING', 'error': msg}
    write_reports(rep, md_path, None)
    return rep

def write_reports(report, md_path, json_path):
    with open(md_path, 'w') as f:
        f.write("# Roboflow Dataset Validation\n\n")
        f.write(f"**Status:** {report.get('status')}\n\n")
        if 'error' in report:
            f.write(f"**Error:** {report['error']}\n")
            return
            
        f.write(f"- Source: {report['source']}\n")
        f.write(f"- Version: {report['version']}\n")
        f.write(f"- Classes ({len(report['classes'])}): {', '.join(report['classes'])}\n")
        f.write(f"- Total Images: {report['total_images']}\n")
        f.write(f"- Total Labels: {report['total_labels']}\n")
        f.write(f"- Invalid Annotations: {report['total_invalid']}\n")
        f.write(f"- Empty Labels: {report['total_empty']}\n")
        f.write(f"- Orphan Images: {report['total_orphan_images']}\n")
        f.write(f"- Orphan Labels: {report['total_orphan_labels']}\n\n")
        
        for s, d in report['splits'].items():
            f.write(f"### Split: {s}\n")
            if 'error' in d:
                f.write(f"Error: {d['error']}\n")
            else:
                for k,v in d.items():
                    f.write(f"- {k}: {v}\n")
                    
    if json_path:
        with open(json_path, 'w') as f:
            json.dump(report, f, indent=2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--md', required=True)
    parser.add_argument('--json', required=True)
    args = parser.parse_args()
    rep = validate_roboflow(args.dataset, args.md, args.json)
    print(json.dumps(rep, indent=2))
