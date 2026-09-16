import os
import glob
import hashlib
import json
import csv
import cv2
import numpy as np

dataset_path = 'Dataset/ChemEq25_training'
splits = ['train', 'valid', 'test']

records = []
stats = {
    'total_images': 0, 'total_labels': 0,
    'missing_labels': 0, 'empty_labels': 0, 'bad_bboxes': 0,
    'duplicates': 0, 'quarantined': 0, 'review_required': 0,
    'class_counts': {}, 'wrong_images_flagged': 0, 'semantic_errors': 0
}

hashes = {}
class_names = {
    0: 'Beaker', 1: 'Buchner_Funnel', 2: 'Burette_Stands', 3: 'Calorimeter',
    4: 'Conical_Flask', 5: 'Funnel', 6: 'Glass_Rod', 7: 'Measuring_Cylinder',
    8: 'Mechanical_Balance_Scale', 9: 'Nessler_Reagent_Bottle', 10: 'Pipette',
    11: 'Porcelain_Mortar_Pestle', 12: 'Precision_Weight_Scale', 13: 'Reagent_Bottle',
    14: 'Round_Bottom_Flask_Borosilicate_Glass_1_Neck', 15: 'Round_Bottom_Flask_Borosilicate_Glass_2_Neck',
    16: 'Round_Bottom_Flask_Borosilicate_Glass_3_Neck', 17: 'Separating_Funnel', 18: 'Spirit_Lamp',
    19: 'TestTube_Holder', 20: 'Test_Tube', 21: 'Volumetric_Flask', 22: 'Volumetric_Pipet',
    23: 'Wash_Bottle', 24: 'Weighing_Bottle'
}

for c in class_names.values():
    stats['class_counts'][c] = 0

os.makedirs('outputs/dataset_audit/montages', exist_ok=True)
montage_samples = {c: [] for c in class_names.values()}

def get_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

for split in splits:
    images = glob.glob(f"{dataset_path}/{split}/images/*.jpg")
    for img_path in images:
        stats['total_images'] += 1
        base = os.path.basename(img_path).rsplit('.', 1)[0]
        # case insensitive extension search for label
        lbl_dir = f"{dataset_path}/{split}/labels"
        lbl_path = os.path.join(lbl_dir, base + ".txt")
        if not os.path.exists(lbl_path):
            lbl_path = os.path.join(lbl_dir, base + ".TXT")
            
        status = 'VERIFIED'
        reason = 'Passed'
        
        img_hash = get_hash(img_path)
        if img_hash in hashes:
            status = 'QUARANTINE'
            reason = f"Duplicate of {hashes[img_hash]}"
            stats['duplicates'] += 1
        else:
            hashes[img_hash] = img_path
        
        if not os.path.exists(lbl_path):
            if status == 'VERIFIED':
                status = 'QUARANTINE'
                reason = "Missing label"
            stats['missing_labels'] += 1
        else:
            with open(lbl_path, 'r') as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
            
            if len(lines) == 0:
                if status == 'VERIFIED':
                    status = 'REVIEW_REQUIRED'
                    reason = "Empty label"
                stats['empty_labels'] += 1
            else:
                stats['total_labels'] += len(lines)
                boxes = []
                for i, line in enumerate(lines):
                    parts = line.split()
                    if len(parts) != 5:
                        status = 'QUARANTINE'
                        reason = f"Malformed label on line {i}"
                        stats['bad_bboxes'] += 1
                        break
                    
                    c, x, y, w, h = map(float, parts)
                    c = int(c)
                    if c not in class_names:
                        status = 'QUARANTINE'
                        reason = f"Invalid class ID {c}"
                        break
                    
                    if not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
                        status = 'QUARANTINE'
                        reason = f"OOB coordinates {x},{y},{w},{h}"
                        stats['bad_bboxes'] += 1
                        break
                        
                    c_name = class_names[c]
                    stats['class_counts'][c_name] += 1
                    
                    area = w * h
                    aspect_ratio = w / h if h > 0 else 0
                    
                    # Heuristics for Semantic/Wrong-Image Review
                    if area < 0.001:
                        if status == 'VERIFIED':
                            status = 'REVIEW_REQUIRED'
                            reason = f"Tiny bbox area: {area:.4f}"
                    elif area > 0.95:
                        if status == 'VERIFIED':
                            status = 'REVIEW_REQUIRED'
                            reason = f"Huge bbox area: {area:.4f}"
                    elif c_name == 'Volumetric_Pipet' and aspect_ratio > 2.0:
                        if status == 'VERIFIED':
                            status = 'REVIEW_REQUIRED'
                            reason = f"Suspicious aspect ratio for Pipet: {aspect_ratio:.2f}"
                    elif c_name == 'Beaker' and aspect_ratio < 0.3:
                        if status == 'VERIFIED':
                            status = 'REVIEW_REQUIRED'
                            reason = f"Suspicious aspect ratio for Beaker: {aspect_ratio:.2f}"
                            
                    boxes.append((c_name, x, y, w, h))

                # Collect samples for montage
                if len(boxes) > 0 and status == 'VERIFIED':
                    for c_name, x, y, w, h in boxes:
                        if len(montage_samples[c_name]) < 5:
                            montage_samples[c_name].append((img_path, x, y, w, h))
                        
        if status == 'QUARANTINE':
            stats['quarantined'] += 1
        elif status == 'REVIEW_REQUIRED':
            stats['review_required'] += 1
            stats['wrong_images_flagged'] += 1
            
        records.append({
            'image': img_path,
            'split': split,
            'status': status,
            'reason': reason
        })

# Generate montages
for c_name, samples in montage_samples.items():
    if not samples:
        continue
    montage_imgs = []
    for img_path, x, y, w, h in samples:
        img = cv2.imread(img_path)
        if img is not None:
            H, W = img.shape[:2]
            x1, y1 = int((x - w/2) * W), int((y - h/2) * H)
            x2, y2 = int((x + w/2) * W), int((y + h/2) * H)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, c_name, (x1, max(y1-10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            img = cv2.resize(img, (300, 300))
            montage_imgs.append(img)
    if montage_imgs:
        montage = np.hstack(montage_imgs)
        cv2.imwrite(f'outputs/dataset_audit/montages/{c_name}.jpg', montage)

with open('outputs/dataset_audit/audit_manifest.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['image', 'split', 'status', 'reason'])
    writer.writeheader()
    writer.writerows(records)

with open('outputs/dataset_audit/stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("Audit complete.")
print(json.dumps(stats, indent=2))
