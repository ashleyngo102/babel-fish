import json
import csv
import difflib

# Load signals
with open('google_signal.json', 'r') as f:
    schema = json.load(f)

# Extract all signal names
signal_names = []
for cat, data in schema['Signals'].items():
    if isinstance(data, dict):
        for subcat, signals in data.items():
            signal_names.extend([s['name'] for s in signals])
    elif isinstance(data, list):
        signal_names.extend([s['name'] for s in data])

# Load CSV headers
with open('Translation 2 - sample dataset-v1_generated_200.csv', 'r') as f:
    reader = csv.reader(f)
    headers = [h.strip() for h in next(reader) if h.strip()]

# Find mappings
report = []
report.append("# Mapping Evaluation Report\n")
report.append("| Client Column | Google Signal Matched | Relationship Logic | Required Action |")
report.append("| --- | --- | --- | --- |")

for header in headers:
    # Exact match (case-insensitive)
    matched_exact = [s for s in signal_names if s.lower() == header.lower()]
    if matched_exact:
        report.append(f"| {header} | {matched_exact[0]} | One-to-One | Approve |")
    else:
        # Fuzzy match
        matches = difflib.get_close_matches(header, signal_names, n=1, cutoff=0.8)
        if matches:
            report.append(f"| {header} | {matches[0]} | One-to-One | Approve |")
        else:
            report.append(f"| {header} | None | Undetected | Manual Mapping |")

# Write report
with open('mapping_report.md', 'w') as f:
    f.write('\n'.join(report))

print("Report generated: mapping_report.md")
