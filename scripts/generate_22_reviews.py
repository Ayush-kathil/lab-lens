import cv2, os, csv, numpy as np

os.makedirs('outputs/dataset_audit/final_human_review/bbox', exist_ok=True)
os.makedirs('outputs/dataset_audit/final_human_review/empty_labels', exist_ok=True)

# Generate BBOX review images
with open('outputs/dataset_audit/suspicious_bbox_review.csv', 'r') as f:
    for i, r in enumerate(csv.DictReader(f)):
        img_path = r['image']
        img = cv2.imread(img_path)
        if img is not None:
            h, w = img.shape[:2]
            parts = r['bbox'].strip().split()
            if len(parts) >= 4:
                cx, cy, bw, bh = map(float, parts[:4])
                x1 = int((cx - bw/2) * w)
                y1 = int((cy - bh/2) * h)
                x2 = int((cx + bw/2) * w)
                y2 = int((cy + bh/2) * h)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            panel = np.zeros((200, w, 3), dtype=np.uint8)
            lines = [
                f"ID: BBOX-{i+1:03d} | Human Verdict: {r['human_verdict']}",
                f"File: {os.path.basename(img_path)} [{r['split']}]",
                f"Class: {r['class_name']} ({r['class_id']})",
                f"BBox: {r['bbox']}",
                f"Reason: {r['reason']}"
            ]
            y = 30
            for line in lines:
                cv2.putText(panel, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y += 30
                
            montage = np.vstack([img, panel])
            cv2.imwrite(f'outputs/dataset_audit/final_human_review/bbox/BBOX-{i+1:03d}.jpg', montage)

# Generate Empty Label review images
with open('outputs/dataset_audit/empty_label_review.csv', 'r') as f:
    for i, r in enumerate(csv.DictReader(f)):
        img_path = r['image']
        img = cv2.imread(img_path)
        if img is not None:
            h, w = img.shape[:2]
            
            panel = np.zeros((150, w, 3), dtype=np.uint8)
            lines = [
                f"ID: EMPTY-{i+1:03d} | Human Verdict: {r['human_verdict']}",
                f"File: {os.path.basename(img_path)} [{r['split']}]",
                f"EMPTY LABEL"
            ]
            y = 30
            for line in lines:
                cv2.putText(panel, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                y += 40
                
            montage = np.vstack([img, panel])
            cv2.imwrite(f'outputs/dataset_audit/final_human_review/empty_labels/EMPTY-{i+1:03d}.jpg', montage)

print('Final 22-case review package generated.')
