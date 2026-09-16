import csv, os

def get_counts(csv_path):
    if not os.path.exists(csv_path): return 0, 0, 0, 0, 0, 0, 0, 0
    with open(csv_path, 'r') as f:
        rows = list(csv.DictReader(f))
    total = len(rows)
    reviewed = sum(1 for r in rows if r['human_verdict'] != 'PENDING')
    pending = sum(1 for r in rows if r['human_verdict'] == 'PENDING')
    nd = sum(1 for r in rows if r['human_verdict'] == 'NOT_DUPLICATE')
    ls = sum(1 for r in rows if r['human_verdict'] == 'LIKELY_SIMILAR')
    cnd = sum(1 for r in rows if r['human_verdict'] == 'CONFIRMED_NEAR_DUPLICATE')
    cl = sum(1 for r in rows if r['human_verdict'] == 'CONFIRMED_LEAKAGE')
    amb = sum(1 for r in rows if r['human_verdict'] == 'AMBIGUOUS')
    return total, reviewed, pending, nd, ls, cnd, cl, amb

csv_nd = 'outputs/dataset_audit/near_duplicate_human_review.csv'
total_nd, reviewed_nd, pending_nd, nd, ls, cnd, cl, amb = get_counts(csv_nd)

tt_count = 0
if os.path.exists(csv_nd):
    with open(csv_nd, 'r') as f:
        tt_count = sum(1 for r in csv.DictReader(f) if {r['split_a'], r['split_b']} == {'train', 'test'})

html_nd = f'''<html><head><title>Near-Duplicate Review Index</title>
<style>body {{font-family: sans-serif; margin: 20px;}} table {{border-collapse: collapse; width: 100%;}} th, td {{border: 1px solid #ddd; padding: 8px; text-align: left;}} img {{max-width: 400px; height: auto;}} .priority {{color: red; font-weight: bold; font-size: 1.2em;}}</style>
</head><body>
<h1>Near-Duplicate Candidates - Human Review Dashboard</h1>
<p class="priority">HIGHEST PRIORITY: TRAIN &harr; TEST ({tt_count} pending candidates)</p>
<h3>Review Counters</h3>
<ul>
<li>Total: {total_nd}</li>
<li>Reviewed: {reviewed_nd}</li>
<li>Pending: {pending_nd}</li>
<li>Not Duplicate: {nd}</li>
<li>Likely Similar: {ls}</li>
<li>Confirmed Near Duplicate: {cnd}</li>
<li>Confirmed Leakage: {cl}</li>
<li>Ambiguous: {amb}</li>
</ul>
<h3>Verdicts Reference</h3>
<ul>
<li><b>NOT_DUPLICATE</b>: Clearly different images/scenes.</li>
<li><b>LIKELY_SIMILAR</b>: Similar visual content but insufficient evidence of duplication.</li>
<li><b>CONFIRMED_NEAR_DUPLICATE</b>: Same visual sample, resized/recompressed/cropped, or effectively identical scene.</li>
<li><b>CONFIRMED_LEAKAGE</b>: Confirmed near-duplicate crossing a protected split boundary in a way that compromises dataset independence.</li>
<li><b>AMBIGUOUS</b>: Cannot determine confidently.</li>
</ul>
<p><i>Note: The authoritative review record must remain the CSV file. This HTML is only a viewing tool.</i></p>
'''

groups = {'train_test': [], 'train_valid': [], 'valid_test': []}
if os.path.exists(csv_nd):
    with open(csv_nd, 'r') as f:
        for r in csv.DictReader(f):
            splits = {r['split_a'], r['split_b']}
            if splits == {'train', 'test'}: groups['train_test'].append(r)
            elif splits == {'train', 'valid'}: groups['train_valid'].append(r)
            elif splits == {'valid', 'test'}: groups['valid_test'].append(r)

for k in ['train_test', 'train_valid', 'valid_test']:
    html_nd += f"<h2>{k.replace('_', ' &harr; ').upper()}</h2><table><tr><th>ID & Status</th><th>Image A</th><th>Image B</th></tr>\n"
    for r in groups[k]:
        html_nd += f"<tr><td><b>ID:</b> {r['candidate_id']}<br><b>dHash Dist:</b> {r['dhash_distance']}<br><b>SSIM:</b> {r['ssim']}<br><b>Auto Status:</b> {r['automated_status']}<br><b>Human Verdict:</b> {r['human_verdict']}</td><td><img src=\"../../{r['image_a']}\"><br>{r['image_a']} [{r['split_a']}]</td><td><img src=\"../../{r['image_b']}\"><br>{r['image_b']} [{r['split_b']}]</td></tr>\n"
    html_nd += "</table>\n"
html_nd += "</body></html>"

with open('outputs/dataset_audit/HUMAN_REVIEW_INDEX.html', 'w') as f: 
    f.write(html_nd)

html_bbox = '''<html><head><title>BBox Review Index</title><style>body {font-family: sans-serif; margin: 20px;} table {border-collapse: collapse; width: 100%;} th, td {border: 1px solid #ddd; padding: 8px; text-align: left;} img {max-width: 400px; height: auto;}</style></head><body><h1>BBox Anomalies Review</h1><table><tr><th>Image</th><th>Details</th><th>Verdict</th></tr>'''
if os.path.exists('outputs/dataset_audit/suspicious_bbox_review.csv'):
    with open('outputs/dataset_audit/suspicious_bbox_review.csv', 'r') as f:
        for i, r in enumerate(csv.DictReader(f)):
            html_bbox += f"<tr><td><img src=\"montages/suspicious_bboxes/suspicious_{i+1}.jpg\"><br>{r['image']}</td><td><b>Split:</b> {r['split']}<br><b>Class:</b> {r['class_name']} ({r['class_id']})<br><b>BBox:</b> {r['bbox']}<br><b>Reason:</b> {r['reason']}</td><td>{r['human_verdict']}</td></tr>\n"
html_bbox += "</table></body></html>"
with open('outputs/dataset_audit/BBOX_REVIEW_INDEX.html', 'w') as f: 
    f.write(html_bbox)

html_empty = '''<html><head><title>Empty Label Review Index</title><style>body {font-family: sans-serif; margin: 20px;} table {border-collapse: collapse; width: 100%;} th, td {border: 1px solid #ddd; padding: 8px; text-align: left;} img {max-width: 400px; height: auto;}</style></head><body><h1>Empty Label Review</h1><table><tr><th>Image</th><th>Split</th><th>Verdict</th></tr>'''
if os.path.exists('outputs/dataset_audit/empty_label_review.csv'):
    with open('outputs/dataset_audit/empty_label_review.csv', 'r') as f:
        for r in csv.DictReader(f):
            bname = os.path.basename(r['image'])
            html_empty += f"<tr><td><img src=\"montages/empty_labels/{bname}\"><br>{r['image']}</td><td>{r['split']}</td><td>{r['human_verdict']}</td></tr>\n"
html_empty += "</table></body></html>"
with open('outputs/dataset_audit/EMPTY_LABEL_REVIEW_INDEX.html', 'w') as f: 
    f.write(html_empty)

print('Dashboards generated!')
