import torch
from a00_constant import *
from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollator
from transformers import BitsAndBytesConfig

class MyModel():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        bnb_config = BitsAndBytesConfig(
            load_in_4bit = True,
            bnb_4bit_quant_type = "nf4",
            bnb_4bit_compute_dtype = getattr(torch, "float16"),
            bnb_4bit_use_double_quant = False,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map = "auto",
            torch_dtype = torch.float16,
            quantization_config = bnb_config,
            # use_flash_attention_2 = True,
        )

    def generate(self, message):
        input = prompt_style

if __name__ == "__main__":
    my_model = MyModel()