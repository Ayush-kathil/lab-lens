import cv2
import csv
import os
from datetime import datetime

def main():
    manifest_path = 'outputs/external_evaluation/external_manifest.csv'
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
    print("  n - Mark as NEGATIVE (Empty label file)")
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
                bbox = cv2.selectROI('Annotation CLI', img, fromCenter=False, showCrosshair=True)
                if bbox != (0,0,0,0):
                    cls_id = input("Enter ChemEq25 class ID (0-24): ").strip()
                    notes = input("Annotation notes: ").strip()
                    
                    label_name = os.path.splitext(row['filename'])[0] + '.txt'
                    label_path = os.path.join('Dataset/ExternalLabBench/labels', label_name)
                    
                    # Convert to YOLO format
                    h, w, _ = img.shape
                    x, y, bw, bh = bbox
                    cx = (x + bw/2.0) / w
                    cy = (y + bh/2.0) / h
                    nw = bw / w
                    nh = bh / h
                    
                    with open(label_path, 'a') as lf:
                        lf.write(f"{cls_id} {cx} {cy} {nw} {nh} {notes}\n")
                    print("Saved bounding box.")
                break
            elif key == ord('n'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'NEGATIVE'
                row['annotator'] = reviewer_name
                row['annotation_timestamp'] = datetime.utcnow().isoformat() + 'Z'
                
                label_name = os.path.splitext(row['filename'])[0] + '.txt'
                label_path = os.path.join('Dataset/ExternalLabBench/labels', label_name)
                open(label_path, 'w').close()
                print("Marked NEGATIVE. Created empty label file.")
                break
            elif key == ord('o'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'OUT_OF_TAXONOMY'
                row['annotator'] = reviewer_name
                break
            elif key == ord('a'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'AMBIGUOUS'
                row['annotator'] = reviewer_name
                break
            elif key == ord('r'):
                row['annotation_status'] = 'REJECTED'
                row['ground_truth_status'] = 'REJECT'
                row['annotator'] = reviewer_name
                break
            elif key == ord('q'):
                print("Quitting...")
                cv2.destroyAllWindows()
                save_manifest(manifest_path, records)
                return

    cv2.destroyAllWindows()
    save_manifest(manifest_path, records)
    print("Done reviewing.")

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
