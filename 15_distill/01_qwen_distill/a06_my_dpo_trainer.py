from a01_contant import *
from transformers import AutoTokenizer

class MyDPOTrainer():
    def __init__(self):
        pass

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    message = [{"role": "system", "content": "You are a helpful assistaint."}]
    message = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=True)
    print(message)