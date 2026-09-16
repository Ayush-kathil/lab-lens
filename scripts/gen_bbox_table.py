import csv
with open('docs/BBOX_EMPTY_LABEL_REVIEW.md', 'w') as out:
    out.write('# Remaining Dataset Anomaly Reviews\n\n')
    out.write('## Suspicious Bounding-Box Cases (16)\n')
    out.write('| ID | Image | Split | Class | BBox | Reason | Human Verdict |\n')
    out.write('|---|---|---|---|---|---|---|\n')
    for i, r in enumerate(csv.DictReader(open('outputs/dataset_audit/suspicious_bbox_review.csv'))):
        out.write(f"| BBOX-{i+1:03d} | {r['image']} | {r['split']} | {r['class_name']} | {r['bbox']} | {r['reason']} | PENDING |\n")
    
    out.write('\n## Empty-Label Cases (6)\n')
    out.write('| ID | Image | Split | Verdict |\n')
    out.write('|---|---|---|---|\n')
    for i, r in enumerate(csv.DictReader(open('outputs/dataset_audit/empty_label_review.csv'))):
        out.write(f"| EMPTY-{i+1:03d} | {r['image']} | {r['split']} | PENDING |\n")
