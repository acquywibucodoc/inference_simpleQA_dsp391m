import json
import os
import glob

def combine_json_files():
    """
    Combine simple and complex JSON files' train and test data into a single combined file.
    Both simple and complex files now have 'question' and 'answer' fields.
    """
    
    print("JSON Files Combination Tool")
    print("=" * 50)
    print("This tool will combine:")
    print("1. Simple JSON files (VNLs1mpleQA_*.json)")
    print("2. Complex JSON files (VNLc0mpl3xQA_*.json)")
    print("Train and test data into a single combined file")
    print("=" * 50)
    
    # Find all JSON files
    simple_files = glob.glob("VNLs1mpleQA_*.json")
    complex_files = glob.glob("VNLc0mpl3xQA_*.json")
    
    all_files = simple_files + complex_files
    
    if not all_files:
        print("No JSON files found in the current directory.")
        return
    
    print(f"Found {len(all_files)} JSON file(s):")
    for file in all_files:
        print(f"  - {file}")
    
    # Get train and test files
    train_test_files = [f for f in all_files if "train" in f or "test" in f]
    
    print(f"\nTrain and test files to combine: {len(train_test_files)}")
    for file in train_test_files:
        print(f"  - {file}")
    
    # Combine all train and test files
    if train_test_files:
        print(f"\nCombining train and test files...")
        combined_data = []
        
        for file_path in train_test_files:
            print(f"  Processing: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if isinstance(data, list):
                    combined_data.extend(data)
                    print(f"    Added {len(data)} items")
                else:
                    print(f"    Warning: {file_path} does not contain a list. Skipping...")
                    
            except json.JSONDecodeError as e:
                print(f"    Error: Invalid JSON format in {file_path}: {e}")
            except Exception as e:
                print(f"    Error processing {file_path}: {e}")
        
        # Save combined data
        if combined_data:
            output_file = "VNLcombined_train.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ Combined data saved to: {output_file}")
            print(f"  Total items: {len(combined_data)}")
    
    print("\n" + "=" * 50)
    print("Combination process completed!")
    
    # Show summary
    print("\nSummary of created file:")
    if train_test_files and combined_data:
        print(f"  VNLcombined_train.json: {len(combined_data)} items")

def verify_combined_files():
    """
    Verify the structure of combined files to ensure they have the expected format.
    """
    combined_files = glob.glob("VNLcombined_*.json")
    
    if not combined_files:
        print("No combined files found to verify.")
        return
    
    print("\nVerifying combined files structure...")
    
    for file_path in combined_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print(f"  {file_path}: Data is not a list")
                continue
            
            if len(data) == 0:
                print(f"  {file_path}: Empty list")
                continue
            
            # Check the first few items to verify structure
            sample_items = data[:3]
            valid_structure = True
            
            for i, item in enumerate(sample_items):
                if not isinstance(item, dict):
                    print(f"  {file_path}: Item {i} is not a dictionary")
                    valid_structure = False
                    break
                
                # Check if it has the expected fields
                if 'question' not in item or 'answer' not in item:
                    print(f"  {file_path}: Item {i} missing 'question' or 'answer' fields")
                    valid_structure = False
                    break
            
            if valid_structure:
                print(f"  {file_path}: ✅ Valid structure with {len(data)} items")
            
        except Exception as e:
            print(f"  {file_path}: Error reading file: {e}")

if __name__ == "__main__":
    combine_json_files()
    verify_combined_files() 