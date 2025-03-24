import torch
from a00_constant import *
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, TextStreamer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

class MyModel():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        # self.EOF_TOKEN = self.tokenizer.eof
        bnb_config_4bit = BitsAndBytesConfig(
            load_in_4bit = True,
            bnb_4bit_quant_type = "nf4",
            bnb_4bit_compute_dtype = getattr(torch, "float16"),
            bnb_4bit_use_double_quant = False,
        )
        bnb_config_8bit = BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_threshold=6.0
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_dir,
            # device_map = "auto",
            torch_dtype = torch.bfloat16,
            quantization_config = bnb_config_8bit,
            # quantization_config = bnb_config_4bit,
        )
        self.model = prepare_model_for_kbit_training(self.model)
        self.streamer = TextStreamer(self.tokenizer)
        self.pipeline = pipeline(
            "text-generation",
            model = self.model,
            tokenizer = self.tokenizer,
        )

    def get_my_peft_model(self):
        peft_config = LoraConfig(
            r = 32,
            lora_alpha = 64,
            lora_dropout = 0.1,
            bias = "lora_only",
            task_type = "CAUSAL_LM",
            target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",]  # 精简目标模块
        )
        return get_peft_model(self.model, peft_config)
    
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
    peft_model = my_model.get_my_peft_model()
    trainable_params = [p for p in peft_model.parameters() if p.requires_grad]
    print(f"Trainable params: {len(trainable_params)}")
    print(trainable_params)
    
    question = "最近我感到非常抑郁，不知道该怎么办。"
    # my_model.generate(question)