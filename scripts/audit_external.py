import os
import csv
import hashlib
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path

def compute_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

def compute_dhash(filepath, hash_size=8):
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    resized = cv2.resize(img, (hash_size + 1, hash_size))
    diff = resized[:, 1:] > resized[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def get_all_reference_images():
    # Gather images from ChemEq25 verified sets and protected test set
    ref_dirs = [
        'Dataset/ChemEq25_training/images',
        'Dataset/ChemEq25_training_verified_v2/images',
        'Dataset/ChemEq25_training_verified_final/images',
        'Dataset/ChemEq25/images/test'
    ]
    ref_images = []
    for d in ref_dirs:
        p = Path(d)
        if p.exists():
            for img_path in p.glob('*.jpg'):
                ref_images.append(str(img_path))
    return ref_images

def main():
    manifest_path = 'outputs/external_evaluation/external_manifest.csv'
    duplicate_audit_path = 'outputs/external_evaluation/external_duplicate_audit.csv'
    provenance_audit_path = 'outputs/external_evaluation/external_provenance_audit.csv'
    
    if not os.path.exists(manifest_path):
        print("Manifest not found.")
        return

    # 1. Build Reference Hashes
    print("Building reference hashes...")
    ref_images = get_all_reference_images()
    ref_sha256 = {}
    ref_dhash = {}
    for img_p in ref_images:
        sha = compute_sha256(img_p)
        dh = compute_dhash(img_p)
        ref_sha256[sha] = img_p
        if dh is not None:
            ref_dhash[img_p] = dh

    # 2. Load Manifest
    records = []
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    # 3. Audit
    dup_audit_records = []
    prov_audit_records = []
    ext_sha256_seen = {} # for DUPLICATE_OF_EXTERNAL
    
    # Pre-compute external dhashes
    ext_dhashes = {}
    for row in records:
        img_path = os.path.join('Dataset/ExternalLabBench/images', row['filename'])
        if os.path.exists(img_path):
            ext_dhashes[row['image_id']] = compute_dhash(img_path)
            
    for row in records:
        img_path = os.path.join('Dataset/ExternalLabBench/images', row['filename'])
        
        # PROVENANCE AUDIT
        req_fields = ['image_id', 'filename', 'source_page_url', 'direct_image_url', 
                      'creator', 'license', 'license_url', 'retrieval_timestamp', 
                      'width', 'height', 'sha256']
        missing_prov = [f for f in req_fields if not row.get(f) or row.get(f) == 'Unknown']
        
        prov_status = 'PROVENANCE_INCOMPLETE' if missing_prov else 'PROVENANCE_COMPLETE'
        # License specific check
        lic = str(row.get('license', 'Unknown')).strip()
        lic_status = 'LICENSE_INCOMPLETE' if lic in ['', 'Unknown', 'None'] else 'LICENSE_COMPLETE'
        
        prov_audit_records.append({
            'image_id': row['image_id'],
            'provenance_status': prov_status,
            'license_status': lic_status,
            'missing_fields': '|'.join(missing_prov)
        })

        if not os.path.exists(img_path):
            row['duplicate_status'] = 'ERROR'
            row['duplicate_reference'] = 'File Missing'
            continue

        # EXACT DUPLICATE AUDIT
        actual_sha = compute_sha256(img_path)
        # Fix possible mismatched sha256 in manifest
        row['sha256'] = actual_sha
        
        dup_status = 'UNIQUE'
        dup_ref = ''
        if actual_sha in ref_sha256:
            dup_status = 'EXACT_DUPLICATE'
            dup_ref = ref_sha256[actual_sha]
        elif actual_sha in ext_sha256_seen:
            dup_status = 'DUPLICATE_OF_EXTERNAL'
            dup_ref = ext_sha256_seen[actual_sha]
        else:
            ext_sha256_seen[actual_sha] = row['image_id']
            
        row['duplicate_status'] = dup_status
        row['duplicate_reference'] = dup_ref

        # NEAR DUPLICATE AUDIT
        near_dup_status = 'UNIQUE'
        nd_ref = ''
        sim_val = ''
        threshold_used = '5' # Hamming distance threshold for 8x8 dhash
        
        dh = ext_dhashes.get(row['image_id'])
        if dh is not None and dup_status == 'UNIQUE':
            best_dist = 999
            best_ref = None
            
            # Compare vs ref
            for ref_p, r_dh in ref_dhash.items():
                # Hamming distance
                dist = bin(dh ^ r_dh).count('1')
                if dist < best_dist:
                    best_dist = dist
                    best_ref = ref_p
            
            # Compare vs other external
            for ext_id, e_dh in ext_dhashes.items():
                if ext_id != row['image_id'] and e_dh is not None:
                    dist = bin(dh ^ e_dh).count('1')
                    if dist < best_dist:
                        best_dist = dist
                        best_ref = f"External:{ext_id}"
            
            if best_dist <= int(threshold_used):
                near_dup_status = 'NEAR_DUPLICATE_CANDIDATE'
                nd_ref = best_ref
                sim_val = str(best_dist)
        
        dup_audit_records.append({
            'image_id': row['image_id'],
            'exact_duplicate_status': dup_status,
            'near_duplicate_status': near_dup_status,
            'reference_image': dup_ref if dup_status != 'UNIQUE' else nd_ref,
            'similarity_metric': 'dHash_Hamming' if near_dup_status != 'UNIQUE' else '',
            'similarity_value': sim_val,
            'threshold_used': threshold_used
        })

    # Save manifest
    with open(manifest_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    # Save prov audit
    with open(provenance_audit_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['image_id', 'provenance_status', 'license_status', 'missing_fields'])
        writer.writeheader()
        writer.writerows(prov_audit_records)

    # Save dup audit
    with open(duplicate_audit_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['image_id', 'exact_duplicate_status', 'near_duplicate_status', 'reference_image', 'similarity_metric', 'similarity_value', 'threshold_used'])
        writer.writeheader()
        writer.writerows(dup_audit_records)
        
    print(f"Audited {len(records)} external candidates.")

if __name__ == '__main__':
    main()
