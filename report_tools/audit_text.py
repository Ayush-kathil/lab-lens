import re

with open('docs/PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Evidence Language Audit
old_phrase = "No fabricated screenshots or synthesized results were used"
new_phrase = "No fabricated experimental results were used. Figures were generated from verified repository data, model inference, pipeline outputs, and test execution traces."

if old_phrase in text or "fabricated screenshots" in text:
    text = text.replace(old_phrase, new_phrase)
    text = text.replace("fabricated screenshots", "fabricated experimental results")
    with open('docs/PROJECT_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated evidence language.")

# Fact Check
facts = {
    "Train 2891": "2891",
    "Valid 878": "878",
    "Test 455": "455",
    "Total 4224": "4224",
    "Instances 6377": "6377",
    "validation mAP50": "0.897",
    "validation mAP50-95": "0.612",
    "test mAP50": "0.881",
    "test mAP50-95": "0.596",
    "External candidates 10": "10 candidates",
    "tests = 100 passed": "100 tests passed"
}

for desc, val in facts.items():
    if val in text:
        print(f"[PASS] {desc} found.")
    else:
        print(f"[FAIL] {desc} missing.")

bad_terms = ["100% accuracy", "perfect detection", "perfect Canny", "learned setup correctness", "learned experiment recognition", "setup classifier", "setup detection", "external generalization proven", "human verified silver labels", "external benchmark completed"]
for t in bad_terms:
    if t.lower() in text.lower():
        print(f"[WARN] Found prohibited term: {t}")

