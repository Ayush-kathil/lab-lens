#!/usr/bin/env python
import csv, sys, os

CSV_PATH = 'outputs/dataset_audit/near_duplicate_human_review.csv'

def main():
    if not os.path.exists(CSV_PATH):
        print("Review CSV not found.")
        sys.exit(1)
        
    records = []
    with open(CSV_PATH, 'r') as f:
        reader = list(csv.DictReader(f))
        fieldnames = list(reader[0].keys())
        records = reader

    print("--- Local Python Review CLI ---")
    cand_id = input("Enter Candidate ID (or 'q' to quit): ").strip()
    if cand_id.lower() == 'q':
        sys.exit(0)
        
    target = next((r for r in records if r['candidate_id'] == cand_id), None)
    if not target:
        print("Candidate not found.")
        sys.exit(1)
        
    print(f"Current Verdict: {target['human_verdict']}")
    print("Options: 1=NOT_DUPLICATE, 2=LIKELY_SIMILAR, 3=CONFIRMED_NEAR_DUPLICATE, 4=CONFIRMED_LEAKAGE, 5=AMBIGUOUS")
    choice = input("Enter choice (1-5): ").strip()
    
    mapping = {
        '1': 'NOT_DUPLICATE',
        '2': 'LIKELY_SIMILAR',
        '3': 'CONFIRMED_NEAR_DUPLICATE',
        '4': 'CONFIRMED_LEAKAGE',
        '5': 'AMBIGUOUS'
    }
    
    if choice in mapping:
        target['human_verdict'] = mapping[choice]
        notes = input("Enter reviewer notes (optional): ").strip()
        if notes:
            target['reviewer_notes'] = notes
            
        with open(CSV_PATH, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
            
        print("Saved successfully to authoritative CSV.")
    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main()
