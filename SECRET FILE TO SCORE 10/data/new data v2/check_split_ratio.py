import json
import os

# Filenames
files = [
    "VNLs1mpleQA_train (v2).json",
    "VNLs1mpleQA_val (v2).json",
    "VNLs1mpleQA_test (v2).json"
]

labels = ["train", "val", "test"]
all_data = []

total = 0
for fname in files:
    if not os.path.exists(fname):
        print(f"❌ File not found: {fname}")
        all_data.append([])
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            n = len(data) if isinstance(data, list) else 0
            total += n
            all_data.append(data)
        except Exception as e:
            print(f"❌ Error reading {fname}: {e}")
            all_data.append([])

# Combine all data in original order
combined = []
for d in all_data:
    combined.extend(d)

print("Dataset Splitter (Perfect 80-10-10, no shuffle, overwrite)")
print("=" * 50)
print(f"Total items: {len(combined)}")

if len(combined) == 0:
    print("No data to split.")
    exit(1)

# Calculate mathematically perfect split sizes
n_total = len(combined)
raw_train = n_total * 0.8
raw_val = n_total * 0.1
raw_test = n_total * 0.1

n_train = int(round(raw_train))
n_val = int(round(raw_val))
n_test = int(round(raw_test))

# Adjust for rounding error to ensure sum == n_total
while n_train + n_val + n_test > n_total:
    n_train -= 1
while n_train + n_val + n_test < n_total:
    n_train += 1  # Assign remainder to train first

splits = [
    combined[:n_train],
    combined[n_train:n_train + n_val],
    combined[n_train + n_val:]
]

for fname, split, label in zip(files, splits, labels):
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(split, f, ensure_ascii=False, indent=2)
    print(f"{label.title():<6}: {len(split)} items written to {fname}")

print("-" * 50)
print(f"Train: {len(splits[0])} ({len(splits[0])/n_total*100:.2f}%)")
print(f"Val  : {len(splits[1])} ({len(splits[1])/n_total*100:.2f}%)")
print(f"Test : {len(splits[2])} ({len(splits[2])/n_total*100:.2f}%)")
print("\n✅ Mathematically perfect 80-10-10 split complete. Files overwritten.") 