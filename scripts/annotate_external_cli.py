import cv2
import csv
import os
import json
from datetime import datetime

def main():
    manifest_path = 'outputs/external_evaluation/external_manifest.csv'
    jsonl_path = 'outputs/external_evaluation/external_annotations.jsonl'
    if not os.path.exists(manifest_path):
        print("Manifest not found.")
        return

    records = []
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    print("=== ExternalLabBench Human Annotation CLI ===")
    print("Controls:")
    print("  y - Mark as POSITIVE (Opens ROI selector)")
    print("  n - Mark as NEGATIVE (Empty label)")
    print("  o - Mark as OUT_OF_TAXONOMY")
    print("  a - Mark as AMBIGUOUS")
    print("  r - Mark as REJECT")
    print("  q - Quit")

    reviewer_name = input("Enter reviewer name: ").strip() or "Unknown"

    for row in records:
        if row['ground_truth_status'] != 'PENDING':
            continue

        img_path = os.path.join('Dataset/ExternalLabBench/images', row['filename'])
        if not os.path.exists(img_path):
            continue

        img = cv2.imread(img_path)
        if img is None:
            continue

        cv2.imshow('Annotation CLI', img)
        print(f"\nImage: {row['filename']}")
        
        while True:
            key = cv2.waitKey(0) & 0xFF
            if key == ord('y'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'POSITIVE'
                row['annotator'] = reviewer_name
                row['annotation_timestamp'] = datetime.utcnow().isoformat() + 'Z'
                
                print("Select ROI for POSITIVE object. Press SPACE or ENTER to finish selection, c to cancel.")
                objects = []
                while True:
                    bbox = cv2.selectROI('Annotation CLI', img, fromCenter=False, showCrosshair=True)
                    if bbox != (0,0,0,0):
                        cls_id = input("Enter ChemEq25 class ID (0-24): ").strip()
                        notes = input("Annotation notes: ").strip()
                        
                        x, y, bw, bh = bbox
                        objects.append({
                            'class_name': f"class_{cls_id}",
                            'class_id': int(cls_id) if cls_id.isdigit() else -1,
                            'x_min': int(x),
                            'y_min': int(y),
                            'x_max': int(x + bw),
                            'y_max': int(y + bh),
                            'annotation_notes': notes
                        })
                        
                        cont = input("Add another box? (y/n): ")
                        if cont.lower() != 'y':
                            break
                    else:
                        break
                
                save_jsonl(jsonl_path, {
                    'image_id': row['image_id'],
                    'filename': row['filename'],
                    'image_status': 'HUMAN_VERIFIED',
                    'reviewer': reviewer_name,
                    'review_timestamp': row['annotation_timestamp'],
                    'ground_truth_status': 'POSITIVE',
                    'objects': objects
                })
                print("Saved POSITIVE annotation.")
                break
            elif key == ord('n'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'NEGATIVE'
                row['annotator'] = reviewer_name
                row['annotation_timestamp'] = datetime.utcnow().isoformat() + 'Z'
                
                save_jsonl(jsonl_path, {
                    'image_id': row['image_id'],
                    'filename': row['filename'],
                    'image_status': 'HUMAN_VERIFIED',
                    'reviewer': reviewer_name,
                    'review_timestamp': row['annotation_timestamp'],
                    'ground_truth_status': 'NEGATIVE',
                    'objects': []
                })
                print("Marked NEGATIVE. Saved empty object array.")
                break
            elif key == ord('o'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'OUT_OF_TAXONOMY'
                row['annotator'] = reviewer_name
                row['annotation_timestamp'] = datetime.utcnow().isoformat() + 'Z'
                save_jsonl(jsonl_path, {
                    'image_id': row['image_id'],
                    'filename': row['filename'],
                    'image_status': 'HUMAN_VERIFIED',
                    'reviewer': reviewer_name,
                    'review_timestamp': row['annotation_timestamp'],
                    'ground_truth_status': 'OUT_OF_TAXONOMY',
                    'objects': []
                })
                break
            elif key == ord('a'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'AMBIGUOUS'
                row['annotator'] = reviewer_name
                row['annotation_timestamp'] = datetime.utcnow().isoformat() + 'Z'
                save_jsonl(jsonl_path, {
                    'image_id': row['image_id'],
                    'filename': row['filename'],
                    'image_status': 'HUMAN_VERIFIED',
                    'reviewer': reviewer_name,
                    'review_timestamp': row['annotation_timestamp'],
                    'ground_truth_status': 'AMBIGUOUS',
                    'objects': []
                })
                break
            elif key == ord('r'):
                row['annotation_status'] = 'REJECTED'
                row['ground_truth_status'] = 'REJECT'
                row['annotator'] = reviewer_name
                row['annotation_timestamp'] = datetime.utcnow().isoformat() + 'Z'
                save_jsonl(jsonl_path, {
                    'image_id': row['image_id'],
                    'filename': row['filename'],
                    'image_status': 'REJECTED',
                    'reviewer': reviewer_name,
                    'review_timestamp': row['annotation_timestamp'],
                    'ground_truth_status': 'REJECT',
                    'objects': []
                })
                break
            elif key == ord('q'):
                print("Quitting...")
                cv2.destroyAllWindows()
                save_manifest(manifest_path, records)
                return

    cv2.destroyAllWindows()
    save_manifest(manifest_path, records)
    print("Done reviewing.")

def save_jsonl(path, data):
    # Validate schema loosely
    if data['ground_truth_status'] in ['NEGATIVE', 'OUT_OF_TAXONOMY', 'AMBIGUOUS', 'REJECT']:
        assert len(data['objects']) == 0
    
    for obj in data['objects']:
        assert obj['x_min'] < obj['x_max']
        assert obj['y_min'] < obj['y_max']
        assert 0 <= obj['class_id'] <= 24
        
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data) + '\n')

def save_manifest(path, records):
    if not records: return
    # Add new fieldnames if they don't exist
    fieldnames = list(records[0].keys())
    for new_field in ['annotator', 'annotation_timestamp']:
        if new_field not in fieldnames:
            fieldnames.append(new_field)
            for r in records: r[new_field] = r.get(new_field, '')
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

if __name__ == '__main__':
    main()
