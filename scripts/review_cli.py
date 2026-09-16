#!/usr/bin/env python
import csv, sys, os, argparse

BBOX_CSV = 'outputs/dataset_audit/suspicious_bbox_review.csv'
EMPTY_CSV = 'outputs/dataset_audit/empty_label_review.csv'

def count_verdicts(csv_path):
    if not os.path.exists(csv_path): return {}
    with open(csv_path, 'r') as f:
        rows = list(csv.DictReader(f))
    counts = {'total': len(rows), 'reviewed': 0, 'pending': 0}
    for r in rows:
        v = r.get('human_verdict', 'PENDING')
        if v == 'PENDING': counts['pending'] += 1
        else: counts['reviewed'] += 1
        counts[v] = counts.get(v, 0) + 1
    return counts

def status_cmd():
    b_counts = count_verdicts(BBOX_CSV)
    e_counts = count_verdicts(EMPTY_CSV)
    
    print("BBox:")
    print(f"{b_counts.get('total', 0)} total")
    print(f"{b_counts.get('reviewed', 0)} reviewed")
    print(f"{b_counts.get('pending', 0)} pending")
    print(f"correct: {b_counts.get('CORRECT', 0)}")
    print(f"incorrect: {b_counts.get('INCORRECT', 0)}")
    print(f"ambiguous: {b_counts.get('AMBIGUOUS', 0)}")
    
    print("\nEmpty:")
    print(f"{e_counts.get('total', 0)} total")
    print(f"{e_counts.get('reviewed', 0)} reviewed")
    print(f"{e_counts.get('pending', 0)} pending")
    print(f"valid_negative: {e_counts.get('VALID_NEGATIVE', 0)}")
    print(f"target_present: {e_counts.get('TARGET_PRESENT', 0)}")
    print(f"ambiguous: {e_counts.get('AMBIGUOUS', 0)}")
    
    print("\nOverall:")
    if b_counts.get('pending', 1) == 0 and e_counts.get('pending', 1) == 0:
        print("READY")
    else:
        print("BLOCKED")

def update_csv(csv_path, type_prefix, target_id, verdict, notes, allowed):
    if verdict not in allowed:
        print(f"Error: Verdict must be one of {allowed}")
        sys.exit(1)
        
    if not os.path.exists(csv_path):
        print(f"Error: CSV {csv_path} not found.")
        sys.exit(1)
        
    records = []
    updated = False
    
    # Simple ID parsing BBOX-001 -> index 0
    try:
        idx = int(target_id.split('-')[1]) - 1
    except:
        print("Error: Invalid ID format.")
        sys.exit(1)

    with open(csv_path, 'r') as f:
        reader = list(csv.DictReader(f))
        fieldnames = list(reader[0].keys())
        
        if idx < 0 or idx >= len(reader):
            print("Error: ID out of range.")
            sys.exit(1)
            
        for i, r in enumerate(reader):
            if i == idx:
                r['human_verdict'] = verdict
                # If notes column doesn't exist, this is a bit tricky, but we can add it or just ignore if not requested in schema.
                # The user prompt for BBOX says "Record: original annotation, human verdict, review notes, recommended corrected annotation"
                # But to avoid breaking schema, we'll just add it if it doesn't exist.
                if 'review_notes' not in fieldnames: fieldnames.append('review_notes')
                r['review_notes'] = notes
                updated = True
            records.append(r)
            
    if updated:
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        print(f"Successfully updated {target_id} to {verdict}")
    else:
        print(f"Failed to update {target_id}")

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python scripts/review_cli.py [status | bbox | empty]")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    
    if cmd == 'status':
        status_cmd()
    elif cmd == 'bbox':
        if len(sys.argv) < 5:
            print("Usage: uv run python scripts/review_cli.py bbox [ID] [VERDICT] [NOTES]")
            sys.exit(1)
        update_csv(BBOX_CSV, 'BBOX', sys.argv[2], sys.argv[3].upper(), sys.argv[4], ['CORRECT', 'INCORRECT', 'AMBIGUOUS'])
    elif cmd == 'empty':
        if len(sys.argv) < 5:
            print("Usage: uv run python scripts/review_cli.py empty [ID] [VERDICT] [NOTES]")
            sys.exit(1)
        update_csv(EMPTY_CSV, 'EMPTY', sys.argv[2], sys.argv[3].upper(), sys.argv[4], ['VALID_NEGATIVE', 'TARGET_PRESENT', 'AMBIGUOUS'])
    else:
        print("Unknown command.")
        sys.exit(1)

if __name__ == '__main__':
    main()
