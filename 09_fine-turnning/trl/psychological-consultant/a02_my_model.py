import torch
from a00_constant import *
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, TextStreamer

class MyModel():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        # self.EOF_TOKEN = self.tokenizer.eof
        self.model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            device_map = "auto",
            torch_dtype = torch.bfloat16,
        )
        self.streamer = TextStreamer(self.tokenizer)
        self.pipeline = pipeline(
            "text-generation",
            model = self.model,
            tokenizer = self.tokenizer,
        )
    
    def generate(self, message):
        input = prompt_style.format(message, "")
        response = self.pipeline(
            input, 
            max_new_tokens = 1200,
            use_cache = True,
            # generation_kwargs = dict(streamer = self.streamer),
            streamer = self.streamer
        )
        # return response
        # print(response)
        # return response[0]["generated_text"]
    
if __name__ == "__main__":
    my_model = MyModel()
    question = "最近我感到非常抑郁，不知道该怎么办。"
    my_model.generate(question)