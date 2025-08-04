import csv

with open('courses.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    expected_cols = len(header)
    for i, row in enumerate(reader, start=2):
        if len(row) != expected_cols:
            print(f"❌ Row {i} has {len(row)} columns, expected {expected_cols}: {row}")
        else:
            print(f"✅ Row {i} OK")
