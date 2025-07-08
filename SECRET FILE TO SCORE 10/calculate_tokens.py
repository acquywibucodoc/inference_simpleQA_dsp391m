import json
import os
from transformers import AutoTokenizer
import numpy as np
from collections import defaultdict
import argparse

def load_tokenizer(model_path):
    """Load tokenizer from the checkpoint directory"""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        return tokenizer
    except Exception as e:
        print(f"Error loading tokenizer from {model_path}: {e}")
        return None

def analyze_json_file(file_path, tokenizer):
    """Analyze a JSON file and calculate token statistics"""
    print(f"Analyzing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total samples: {len(data)}")
    
    # Statistics containers
    question_lengths = []
    answer_lengths = []
    combined_lengths = []
    all_texts = []
    
    # Process each sample
    for i, sample in enumerate(data):
        if i % 1000 == 0:
            print(f"Processing sample {i}/{len(data)}")
        
        question = sample.get('question', '')
        answer = sample.get('answer', '')
        
        # Tokenize individual parts
        question_tokens = tokenizer.encode(question, add_special_tokens=False)
        answer_tokens = tokenizer.encode(answer, add_special_tokens=False)
        
        # Combined text (for SFT format)
        combined_text = f"Question: {question}\nAnswer: {answer}"
        combined_tokens = tokenizer.encode(combined_text, add_special_tokens=True)
        
        question_lengths.append(len(question_tokens))
        answer_lengths.append(len(answer_tokens))
        combined_lengths.append(len(combined_tokens))
        all_texts.append(combined_text)
    
    return {
        'question_lengths': question_lengths,
        'answer_lengths': answer_lengths,
        'combined_lengths': combined_lengths,
        'all_texts': all_texts,
        'total_samples': len(data)
    }

def calculate_statistics(lengths, name):
    """Calculate statistics for a list of lengths"""
    if not lengths:
        return {}
    
    stats = {
        'count': len(lengths),
        'mean': np.mean(lengths),
        'median': np.median(lengths),
        'std': np.std(lengths),
        'min': np.min(lengths),
        'max': np.max(lengths),
        'percentiles': {
            '50%': np.percentile(lengths, 50),
            '75%': np.percentile(lengths, 75),
            '90%': np.percentile(lengths, 90),
            '95%': np.percentile(lengths, 95),
            '99%': np.percentile(lengths, 99),
        }
    }
    
    print(f"\n{name} Token Statistics:")
    print(f"  Count: {stats['count']}")
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  Median: {stats['median']:.2f}")
    print(f"  Std: {stats['std']:.2f}")
    print(f"  Min: {stats['min']}")
    print(f"  Max: {stats['max']}")
    print(f"  Percentiles:")
    for p, v in stats['percentiles'].items():
        print(f"    {p}: {v:.2f}")
    
    return stats

def recommend_max_length(combined_stats, target_coverage=0.95):
    """Recommend max length based on statistics"""
    recommended_length = int(combined_stats['percentiles'][f'{int(target_coverage*100)}%'])
    
    print(f"\nMax Length Recommendations:")
    print(f"  For {target_coverage*100}% coverage: {recommended_length}")
    print(f"  For 99% coverage: {int(combined_stats['percentiles']['99%'])}")
    print(f"  For 90% coverage: {int(combined_stats['percentiles']['90%'])}")
    
    # Round to nearest power of 2 for efficiency
    power_of_2_length = 2 ** int(np.log2(recommended_length))
    print(f"  Recommended (power of 2): {power_of_2_length}")
    
    return recommended_length

def main():
    parser = argparse.ArgumentParser(description='Calculate token statistics for SFT training')
    parser.add_argument('--model_path', default='checkpoint-116000', 
                       help='Path to the model checkpoint directory')
    parser.add_argument('--train_file', default='data/VNLcombined_train.json',
                       help='Path to training JSON file')
    parser.add_argument('--val_file', default='data/VNLcombined_val.json',
                       help='Path to validation JSON file')
    
    args = parser.parse_args()
    
    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = load_tokenizer(args.model_path)
    if tokenizer is None:
        print("Failed to load tokenizer. Exiting.")
        return
    
    print(f"Tokenizer loaded: {tokenizer.__class__.__name__}")
    print(f"Vocab size: {tokenizer.vocab_size}")
    
    # Analyze training data
    if os.path.exists(args.train_file):
        train_stats = analyze_json_file(args.train_file, tokenizer)
        print("\n" + "="*50)
        print("TRAINING DATA STATISTICS")
        print("="*50)
        
        calculate_statistics(train_stats['question_lengths'], "Question")
        calculate_statistics(train_stats['answer_lengths'], "Answer")
        combined_stats = calculate_statistics(train_stats['combined_lengths'], "Combined (SFT format)")
        
        recommend_max_length(combined_stats)
    else:
        print(f"Training file not found: {args.train_file}")
    
    # Analyze validation data
    if os.path.exists(args.val_file):
        print("\n" + "="*50)
        print("VALIDATION DATA STATISTICS")
        print("="*50)
        
        val_stats = analyze_json_file(args.val_file, tokenizer)
        calculate_statistics(val_stats['question_lengths'], "Question")
        calculate_statistics(val_stats['answer_lengths'], "Answer")
        val_combined_stats = calculate_statistics(val_stats['combined_lengths'], "Combined (SFT format)")
        
        recommend_max_length(val_combined_stats)
    else:
        print(f"Validation file not found: {args.val_file}")
    
    print("\n" + "="*50)
    print("SFT TRAINING RECOMMENDATIONS")
    print("="*50)
    print("1. Use the 'Combined' statistics for max_length as it represents the full SFT format")
    print("2. Consider using a power of 2 for max_length for computational efficiency")
    print("3. You may want to truncate very long sequences or split them into multiple examples")
    print("4. Monitor training loss to ensure the chosen max_length is appropriate")

if __name__ == "__main__":
    main() 