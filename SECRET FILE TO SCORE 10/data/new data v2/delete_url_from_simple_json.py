import json
import os
import glob

# Set the directory containing the JSON files
DATA_DIR = os.path.dirname(os.path.abspath(__file__))  # Default: script's directory
# To use a custom directory, set DATA_DIR = r"E:/path/to/your/data"

def process_simple_json_files():
    """
    Process simple JSON files (VNLs1mpleQA_*.json files):
    1. Delete the 'URL' item
    2. Rename 'Heading' to 'question'
    3. Rename 'Content' to 'answer'
    Simple JSON files contain objects with 'URL', 'Heading', and 'Content' fields.
    """
    
    # Find all simple JSON files in DATA_DIR
    simple_json_files = glob.glob(os.path.join(DATA_DIR, "VNLs1mpleQA_*.json"))
    
    if not simple_json_files:
        print(f"No simple JSON files (VNLs1mpleQA_*.json) found in directory: {DATA_DIR}")
        return
    
    print(f"Found {len(simple_json_files)} simple JSON file(s) in {DATA_DIR}:")
    for file in simple_json_files:
        print(f"  - {os.path.basename(file)}")
    
    # Process each file
    for file_path in simple_json_files:
        print(f"\nProcessing: {os.path.basename(file_path)}")
        
        try:
            # Read the JSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if it's a list of objects
            if not isinstance(data, list):
                print(f"  Warning: {os.path.basename(file_path)} does not contain a list. Skipping...")
                continue
            
            # Count items before processing
            total_items = len(data)
            items_with_url = 0
            items_with_heading = 0
            items_with_content = 0
            items_processed = 0
            
            # Process each object in the list
            for item in data:
                if isinstance(item, dict):
                    # Delete any key that matches 'URL' after stripping whitespace and invisible characters
                    keys_to_remove = [k for k in item.keys() if k.strip().replace('\ufeff', '') == 'URL']
                    for k in keys_to_remove:
                        items_with_url += 1
                        del item[k]
                    
                    # Rename Heading to question if it exists
                    if 'Heading' in item:
                        items_with_heading += 1
                        item['question'] = item.pop('Heading')
                    
                    # Rename Content to answer if it exists
                    if 'Content' in item:
                        items_with_content += 1
                        item['answer'] = item.pop('Content')
                    
                    items_processed += 1
            
            # Write the modified data back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"  Successfully processed {items_processed} items")
            print(f"  Deleted 'URL' from {items_with_url} items")
            print(f"  Renamed 'Heading' to 'question' in {items_with_heading} items")
            print(f"  Renamed 'Content' to 'answer' in {items_with_content} items")
            print(f"  Total items in file: {total_items}")
            
        except json.JSONDecodeError as e:
            print(f"  Error: Invalid JSON format in {os.path.basename(file_path)}: {e}")
        except Exception as e:
            print(f"  Error processing {os.path.basename(file_path)}: {e}")
    
    print("\nFile processing completed!")

def verify_simple_json_structure(file_path):
    """
    Verify the structure of a simple JSON file to ensure it has the expected format.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            return False, "Data is not a list"
        
        if len(data) == 0:
            return True, "Empty list"
        
        # Check the first few items to verify structure
        sample_items = data[:3]
        for i, item in enumerate(sample_items):
            if not isinstance(item, dict):
                return False, f"Item {i} is not a dictionary"
            
            # Check if it has the expected fields for simple JSON
            if 'Heading' in item and 'Content' in item:
                return True, "Simple JSON structure confirmed"
        
        return False, "Items don't have expected 'Heading' and 'Content' fields"
        
    except Exception as e:
        return False, f"Error reading file: {e}"

if __name__ == "__main__":
    print("Simple JSON Files Processing Tool")
    print("=" * 50)
    print(f"This tool will process files in: {DATA_DIR}")
    print("1. Delete the 'URL' field")
    print("2. Rename 'Heading' to 'question'")
    print("3. Rename 'Content' to 'answer'")
    print("=" * 50)
    
    # Verify we're working with simple JSON files
    simple_files = glob.glob(os.path.join(DATA_DIR, "VNLs1mpleQA_*.json"))
    
    if simple_files:
        print("Verifying file structures...")
        for file in simple_files:
            is_valid, message = verify_simple_json_structure(file)
            print(f"  {os.path.basename(file)}: {message}")
        
        print("\nStarting file processing...")
        process_simple_json_files()
    else:
        print(f"No simple JSON files (VNLs1mpleQA_*.json) found in directory: {DATA_DIR}")
        print("Please ensure you're running this script in the directory containing the JSON files or set DATA_DIR appropriately.") 