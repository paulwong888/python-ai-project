import torch
from a00_constant import *
from a01_test_message import *
from transformers import AutoProcessor, AutoModelForImageTextToText, pipeline, BitsAndBytesConfig

class MyModel:
    def __init__(self):
        model_path = GEMMA_3_12B_IT_4BIT_PATH #GEMMA_3_12B_IT_PATH
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True, 
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        # processor = AutoProcessor.from_pretrained(model_path, use_fast=True)
        # model = AutoModelForImageTextToText.from_pretrained(
        #     model_path,
        #     # quantization_config=bnb_config,
        #     low_cpu_mem_usage=True,
        # )
        self.pipe = pipeline(
            # "image-text-to-text", 
            "text-generation", 
            model=model_path,
            # processor=processor,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
    
    def generate(self, message):
        model_input = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful assistant."}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image", "url": "16_vllm/data/candy.jpg"},
                    {"type": "text", "text": "What animal is on the candy?"}
                ]
            }
        ]
        model_input = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful assistant."}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What animal is on the candy?"}
                ]
            }
        ]
        response = self.pipe(text=model_input, max_new_tokens=200)
        print(response)
        return response[0]["generated_text"][-1]["content"]
    
if __name__ == "__main__":
    my_model = MyModel()
    print(my_model.generate(json_output_message))