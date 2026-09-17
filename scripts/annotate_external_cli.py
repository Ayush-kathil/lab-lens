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
    print("  y - Mark as POSITIVE (Requires BBox annotation)")
    print("  n - Mark as NEGATIVE (Empty label file)")
    print("  o - Mark as OUT_OF_TAXONOMY")
    print("  a - Mark as AMBIGUOUS")
    print("  r - Mark as REJECT")
    print("  q - Quit")

    for row in records:
        if row['ground_truth_status'] != 'PENDING':
            continue

        img_path = os.path.join('Dataset/ExternalLabBench/images', row['filename'])
        if not os.path.exists(img_path):
            continue

        img = cv2.imread(img_path)
        if img is None:
            continue

        # Display image
        cv2.imshow('Annotation CLI', img)
        print(f"\nImage: {row['filename']}")
        
        while True:
            key = cv2.waitKey(0) & 0xFF
            if key == ord('y'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'POSITIVE'
                # Placeholder for actual bounding box UI
                print("Marked POSITIVE. Bounding box drawing would trigger here.")
                break
            elif key == ord('n'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'NEGATIVE'
                
                # Create empty label file
                label_name = os.path.splitext(row['filename'])[0] + '.txt'
                label_path = os.path.join('Dataset/ExternalLabBench/labels', label_name)
                open(label_path, 'w').close()
                print("Marked NEGATIVE. Created empty label file.")
                break
            elif key == ord('o'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'OUT_OF_TAXONOMY'
                print("Marked OUT_OF_TAXONOMY.")
                break
            elif key == ord('a'):
                row['annotation_status'] = 'HUMAN_VERIFIED'
                row['ground_truth_status'] = 'AMBIGUOUS'
                print("Marked AMBIGUOUS.")
                break
            elif key == ord('r'):
                row['annotation_status'] = 'REJECTED'
                row['ground_truth_status'] = 'REJECT'
                print("Marked REJECT.")
                break
            elif key == ord('q'):
                print("Quitting...")
                cv2.destroyAllWindows()
                
                # Save progress
                with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=records[0].keys())
                    writer.writeheader()
                    writer.writerows(records)
                return

    cv2.destroyAllWindows()
    
    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print("Done reviewing.")

if __name__ == '__main__':
    main()
