import torch
from a00_constant import *
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers.pipelines import pipeline

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
            # torch_dtype = torch.float16,
            # quantization_config = bnb_config,
            # load_in_8bit = True,
            # use_flash_attention_2 = True,
        )
        self.pipeline = pipeline(
            task = "text-generation",
            model = self.model,
            tokenizer = self.tokenizer,
            device_map = "auto",
            # max_seq_length = "512",
        )

    def generate(self, message):
        input = prompt_style.format(message, "")
        input = message
        return self.pipeline(
            input,
            max_length = 512,
            # truncation = True,
        )[0]["generated_text"]

"""
下列关于细胞呼吸在生产生活中应用的叙述，错误的是  （    ） A. 给含有酵母菌的发酵液连续通气可以提高产酒量 B. 适当降低温度和氧浓度有利于果蔬储藏 C. 利用乳酸细菌制作酸奶过程中需密闭隔绝空气 D. 黑暗条件下绿豆萌发成豆芽的过程中有机物总量不断减少
A /n【解析】呼吸作用的影响因素有：氧气、温度等。 【详解】酵母菌是兼性厌氧型生物，发酵初期需要氧气进行增殖，后期需要在无氧条件下进行酒精发酵，A错误；果蔬储藏时应该降低呼吸作用消耗，应该在低温和低氧条件下进行，B正确；乳酸菌是厌氧型生物，乳酸发酵时需要处于无氧环境中，C正确；黑暗下，豆芽只能进行呼吸作用，不能进行光合作用，故有机物总量会下降，D正确。故选A。
"""
if __name__ == "__main__":
    my_model = MyModel()
    question = "下列关于细胞呼吸在生产生活中应用的叙述，错误的是  （    ） A. 给含有酵母菌的发酵液连续通气可以提高产酒量 B. 适当降低温度和氧浓度有利于果蔬储藏 C. 利用乳酸细菌制作酸奶过程中需密闭隔绝空气 D. 黑暗条件下绿豆萌发成豆芽的过程中有机物总量不断减少" #A
    print(my_model.generate(question))