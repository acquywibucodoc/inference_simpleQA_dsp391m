import json
import os
import glob

def convert_to_alpaca_format():
    """
    Convert VNLsimple JSON files to Alpaca format for training with LlamaFactory.
    Alpaca format:
    [
      {
        "instruction": "user instruction (required)",
        "input": "user input (optional)", 
        "output": "model response (required)",
        "system": "system prompt (optional)",
        "history": [
          ["user instruction in the first round (optional)", "model response in the first round (optional)"],
          ["user instruction in the second round (optional)", "model response in the second round (optional)"]
        ]
      }
    ]
    """
    
    print("VNLsimple to Alpaca Format Converter")
    print("=" * 50)
    print("This tool will convert VNLsimple JSON files to Alpaca format")
    print("for training with LlamaFactory.")
    print("=" * 50)
    
    # Find all simple JSON files
    simple_files = glob.glob("VNLs1mpleQA_*.json")
    
    if not simple_files:
        print("No VNLsimple JSON files (VNLs1mpleQA_*.json) found in the current directory.")
        return
    
    print(f"Found {len(simple_files)} VNLsimple JSON file(s):")
    for file in simple_files:
        print(f"  - {file}")
    
    # Ensure the output directory exists
    output_dir = "alpaca"
    os.makedirs(output_dir, exist_ok=True)
    
    # System prompt for Vietnamese legal Q&A
    system_prompt = "Bạn là một trợ lý AI chuyên về pháp luật Việt Nam. Hãy trả lời các câu hỏi pháp lý một cách chính xác, đầy đủ và dễ hiểu dựa trên các quy định pháp luật hiện hành."
    
    # Process each file
    for file_path in simple_files:
        print(f"\nProcessing: {file_path}")
        
        try:
            # Read the original file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert to Alpaca format
            alpaca_data = []
            
            for item in data:
                # Check if the item has the expected structure
                if 'question' in item and 'answer' in item:
                    alpaca_item = {
                        "instruction": item['question'],
                        "input": "",  # No additional input needed for simple Q&A
                        "output": item['answer'],
                        "system": system_prompt,
                        "history": []  # No conversation history for simple Q&A
                    }
                    alpaca_data.append(alpaca_item)
                else:
                    print(f"Warning: Skipping item without 'question' or 'answer' field: {item}")
            
            # Create output filename in the alpaca directory
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_filename = os.path.join(output_dir, f"{base_name}_alpaca.json")
            
            # Write the converted data
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(alpaca_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully converted {len(alpaca_data)} items")
            print(f"📁 Output saved to: {output_filename}")
            
            # Show sample of converted data
            if alpaca_data:
                print(f"\n📋 Sample converted item:")
                print(json.dumps(alpaca_data[0], ensure_ascii=False, indent=2))
            
        except json.JSONDecodeError as e:
            print(f"❌ Error reading JSON file {file_path}: {e}")
        except Exception as e:
            print(f"❌ Error processing file {file_path}: {e}")
    
    print(f"\n🎉 Conversion completed!")
    print("The converted files are ready for training with LlamaFactory.")
    print("\nNote: You may want to customize the system prompt based on your specific training needs.")

if __name__ == "__main__":
    convert_to_alpaca_format() 