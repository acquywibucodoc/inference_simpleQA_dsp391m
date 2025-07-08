import csv
import json

def csv_to_json(csv_file, json_file):
    # Read the CSV and add data to a list
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    # Write the list of dicts to a JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    csv_file = "VNLs1mpleQA_test (v2).csv"   # Change this to your CSV filename
    json_file = "VNLs1mpleQA_test (v2).json" # Change this to your desired JSON filename
    csv_to_json(csv_file, json_file)
    print(f"Converted {csv_file} to {json_file}")