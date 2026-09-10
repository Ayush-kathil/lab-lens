import argparse
import json
from pathlib import Path

def validate_annotations(dataset_dir, output_file):
    dataset_path = Path(dataset_dir).resolve()
    splits = ['train', 'valid', 'test']
    
    report = {
        'total_malformed': 0,
        'categories': {
            'empty_file': 0,
            'wrong_number_of_fields': 0,
            'non_numeric_value': 0,
            'class_id_outside_range': 0,
            'coordinate_outside_bounds': 0,
            'zero_negative_width_height': 0
        },
        'files': []
    }

    for split in splits:
        split_path = dataset_path / split
        lbl_dir = split_path / 'labels'
        
        if not lbl_dir.exists():
            continue
            
        labels = list(lbl_dir.iterdir())
        
        for lbl_file in labels:
            if lbl_file.stat().st_size == 0:
                report['categories']['empty_file'] += 1
                report['total_malformed'] += 1
                report['files'].append({'file': lbl_file.name, 'split': split, 'error': 'empty_file'})
                continue
                
            try:
                with open(lbl_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    has_error = False
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) == 0:
                            continue
                        if len(parts) != 5:
                            report['categories']['wrong_number_of_fields'] += 1
                            report['files'].append({'file': lbl_file.name, 'split': split, 'error': 'wrong_number_of_fields'})
                            has_error = True
                            break
                        
                        try:
                            cls_id = int(parts[0])
                            x, y, w, h = float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])
                        except ValueError:
                            report['categories']['non_numeric_value'] += 1
                            report['files'].append({'file': lbl_file.name, 'split': split, 'error': 'non_numeric_value'})
                            has_error = True
                            break
                            
                        if not (0 <= cls_id <= 24):
                            report['categories']['class_id_outside_range'] += 1
                            report['files'].append({'file': lbl_file.name, 'split': split, 'error': 'class_id_outside_range', 'value': cls_id})
                            has_error = True
                            break
                            
                        if not (0 <= x <= 1 and 0 <= y <= 1):
                            report['categories']['coordinate_outside_bounds'] += 1
                            report['files'].append({'file': lbl_file.name, 'split': split, 'error': 'coordinate_outside_bounds'})
                            has_error = True
                            break
                            
                        if not (0 < w <= 1 and 0 < h <= 1):
                            report['categories']['zero_negative_width_height'] += 1
                            report['files'].append({'file': lbl_file.name, 'split': split, 'error': 'zero_negative_width_height'})
                            has_error = True
                            break
                            
                    if has_error:
                        report['total_malformed'] += 1
                        
            except Exception as e:
                pass
                
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
            
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    validate_annotations(args.dataset, args.output)
