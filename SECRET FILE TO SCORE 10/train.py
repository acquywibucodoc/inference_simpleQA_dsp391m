# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer, setup_chat_format
import torch
import wandb
import os
import numpy as np

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)

# Load the model and tokenizer
model_path = "./checkpoint-116000"
model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=model_path
).to(device)
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_path, model_max_length=2048)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {"accuracy": np.mean(predictions == labels)}

# set the wandb project where this run will be logged
os.environ["WANDB_PROJECT"]="legalQwen2.5_SFT_SimpleQA"

os.environ["WANDB_ENTITY"] = "anhthse180039-fpt-university"

# Load and Train SimpleQA
def load_json_dataset(train_path, val_path):
    dataset = load_dataset('json', data_files={
        'train': train_path,
        'validation': val_path,
    })
    return dataset['train'], dataset['validation']

train_path = r"data\VNLcombined_train.json"
val_path = r"data\VNLcombined_val.json"

# Load datasets
train_dataset, val_dataset = load_json_dataset(train_path, val_path)

print(f"Train dataset size: {len(train_dataset)}")
print(f"Validation dataset size: {len(val_dataset)}")

def formatting_prompt_func(example):
    return (
        "<Instruct>Bạn là một trợ lí tư vấn các vấn đề liên quan đến pháp luật. Hãy trả lời như một luật sư chuyên nghiệp.</Instruct>\n"
        "<Format>Định dạng: Hỏi - Đáp</Format>\n"
        f"<Question>{example['question']}</Question>\n"
        f"<Answer>{example['answer']}</Answer>"
    )

training_args = SFTConfig(
    output_dir="./sft_output_10diemQA",
    report_to="wandb",
    eval_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    lr_scheduler_type="cosine",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=32,
    num_train_epochs=10,
    learning_rate=2e-5,
    weight_decay=0.01,
    bf16=True,  
    #load_best_model_at_end=True,
    #push_to_hub=False,  
)

# Initialize the SFTTrainer
trainer = SFTTrainer(
    model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    #compute_metrics=compute_metrics,  # Commented out as it may not work well with SFT
    formatting_func=formatting_prompt_func,
    )
    
torch.cuda.empty_cache()
trainer.train()

# [optional] finish the wandb run, necessary in notebooks
wandb.finish()
wandb.init()

metrics = trainer.evaluate()

print(metrics)