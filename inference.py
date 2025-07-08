from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.streamers import TextStreamer
import torch
import io

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps" if torch.backends.mps.is_available() else "cpu"
)

model_path = r"./checkpoint-15300" # Input your checkpoint path here
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path, model_max_length=2048)

prompt_template = """ Bạn là một trợ lí tư vấn các vấn đề liên quan đến pháp luật. Hãy trả lời như một luật sư chuyên nghiệp. \n\n### Instruction:\n{}\n\n### Response"\n"""

def get_answer(question):
    formatted_input = prompt_template.format(question)
    inputs = tokenizer([formatted_input], return_tensors="pt").to(device)
    output = model.generate(
        **inputs,
        streamer=TextStreamer(tokenizer),
        max_new_tokens=1024,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        early_stopping=True,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
        repetition_penalty=1.2,
    )
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    if formatted_input in generated_text:
        answer = generated_text.split(formatted_input, 1)[-1].strip()
    else:
        answer = generated_text
    # Remove stop tokens if present
    for stop_token in ["<|im_end|>", "<|endoftext|>"]:
        if stop_token in answer:
            answer = answer.split(stop_token)[0]
    return answer.strip()
