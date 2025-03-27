import torch
import pandas as pd
from a00_constant import *
from a04_01_test_data import *
from a02_my_model import MyModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig
from peft import PeftModel

class MyMerge(MyModel):
    def __init__(self):
        model, tokenizer = self.load_model_tokenizer()
        self.streamer = TextStreamer(tokenizer)
        self.pipeline = pipeline(
            task = "text-generation",
            model = model,
            tokenizer = tokenizer,
            device_map = "auto"
        )

    def load_model_tokenizer(self):
        # tokenizer = AutoTokenizer.from_pretrained(adapter_dir)
        tokenizer = AutoTokenizer.from_pretrained(best_adapter_dir)
        bnb_config_4bit = BitsAndBytesConfig(
            load_in_4bit = True,
            bnb_4bit_quant_type = "nf4",
            bnb_4bit_compute_dtype = getattr(torch, "float16"),
            bnb_4bit_use_double_quant = True,
        )
        model: AutoModelForCausalLM = AutoModelForCausalLM.from_pretrained(
            model_dir,
            # torch_dtype = torch.float16,
            device_map = "auto",
            quantization_config = bnb_config_4bit,
        )
        # model.load_adapter(best_adapter_dir)
        model = PeftModel.from_pretrained(model, best_adapter_dir)
        return model, tokenizer
    
    # def generate(self, message):
    #     return self.pipeline(message)
    

if __name__ == "__main__":
    
    my_merge = MyMerge()
    my_merge.generate(question1)
    print("--" * 10)
    my_merge.generate(question2)
    print("--" * 10)
    my_merge.generate(question3)