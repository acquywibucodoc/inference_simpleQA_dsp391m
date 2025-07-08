import os
import csv
import json

# Set the directory containing your CSV files
csv_dir = r"E:\data luatvietnam.vn\DEMO\SECRET FILE TO SCORE 10\data\new data v2"

# List all CSV files in the directory
for filename in os.listdir(csv_dir):
    if filename.endswith(".csv"):
        csv_path = os.path.join(csv_dir, filename)
        json_path = os.path.join(csv_dir, filename.replace(".csv", ".json"))
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
        
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)
        
        print(f"Converted {filename} to {os.path.basename(json_path)}")