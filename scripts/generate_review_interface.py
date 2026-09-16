import csv, os, cv2, numpy as np

src_csv = 'outputs/dataset_audit/near_duplicate_verification.csv'
dst_csv = 'outputs/dataset_audit/near_duplicate_human_review.csv'

if not os.path.exists(src_csv):
    print('Source CSV not found!')
    exit(1)

records = []
with open(src_csv, 'r') as f:
    for r in csv.DictReader(f):
        if r['final_status'] == 'LIKELY_NEAR_DUPLICATE':
            r['ssim_f'] = float(r['strong_similarity'])
            r['dist_i'] = int(r['hash_distance'])
            records.append(r)

# Sort: SSIM descending, dHash distance ascending
records.sort(key=lambda x: (-x['ssim_f'], x['dist_i']))

train_test, train_valid, valid_test = [], [], []
for r in records:
    splits = {r['split_a'], r['split_b']}
    if splits == {'train', 'test'}:
        train_test.append(r)
    elif splits == {'train', 'valid'}:
        train_valid.append(r)
    elif splits == {'valid', 'test'}:
        valid_test.append(r)

out_dirs = {
    'train_test': 'outputs/dataset_audit/montages/train_test',
    'train_valid': 'outputs/dataset_audit/montages/train_valid',
    'valid_test': 'outputs/dataset_audit/montages/valid_test'
}
for d in out_dirs.values():
    os.makedirs(d, exist_ok=True)

out_records = []
total_sheets = 0

def create_sheets(group, dir_key):
    global total_sheets
    for i, r in enumerate(group):
        imgA = cv2.imread(r['image_a'])
        imgB = cv2.imread(r['image_b'])
        if imgA is not None and imgB is not None:
            imgA = cv2.resize(imgA, (400, 400))
            imgB = cv2.resize(imgB, (400, 400))
            
            # create text panel
            panel = np.zeros((200, 800, 3), dtype=np.uint8)
            lines = [
                f"ID: {r['candidate_id']} | Status: {r['final_status']} | HUMAN VERDICT: PENDING",
                f"Image A: {os.path.basename(r['image_a'])} [{r['split_a']}]",
                f"Image B: {os.path.basename(r['image_b'])} [{r['split_b']}]",
                f"dHash Dist: {r['hash_distance']} | SSIM: {r['strong_similarity']}"
            ]
            y = 40
            for line in lines:
                cv2.putText(panel, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                y += 40
                
            montage = np.vstack([np.hstack([imgA, imgB]), panel])
            out_name = f"{i+1:03d}_{r['candidate_id']}.jpg"
            cv2.imwrite(os.path.join(out_dirs[dir_key], out_name), montage)
            total_sheets += 1
            
        out_records.append({
            'candidate_id': r['candidate_id'],
            'image_a': r['image_a'], 'split_a': r['split_a'],
            'image_b': r['image_b'], 'split_b': r['split_b'],
            'dhash_distance': r['hash_distance'],
            'ssim': r['strong_similarity'],
            'automated_status': r['final_status'],
            'human_verdict': 'PENDING',
            'reviewer_notes': ''
        })

create_sheets(train_test, 'train_test')
create_sheets(train_valid, 'train_valid')
create_sheets(valid_test, 'valid_test')

with open(dst_csv, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=out_records[0].keys())
    writer.writeheader()
    writer.writerows(out_records)

print(f'Train-Test: {len(train_test)}')
print(f'Train-Valid: {len(train_valid)}')
print(f'Valid-Test: {len(valid_test)}')
print(f'Total sheets generated: {total_sheets}')
