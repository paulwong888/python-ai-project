import torch
from a00_constant import *
from a02_my_model import MyModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class MyMerge():
    def __init__(self):
        model, tokenizer = self.load_model_tokenizer()
        self.pipeline = pipeline(
            task = "text-generation",
            model = model,
            tokenizer = tokenizer,
            device_map = "auto"
        )

    def load_model_tokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model: AutoModelForCausalLM = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype = torch.float16,
            device_map = "auto"
        )
        model.load_adapter(adapter_dir)
        return model, tokenizer
    
    def generate(self, message):
        return self.pipeline(test_prompt_style.format(message))
    
if __name__ == "__main__":
    question = "物质输入和输出细胞都需要经过细胞膜。下列有关人体内物质跨膜运输的叙述，正确的是（）A.乙醇是有机物，不能通过自由扩散方式跨膜进入细胞 B.血浆中的K＋进入红细胞时需要载体蛋白并消耗ATP C.抗体在浆细胞内合成时消耗能量，其分泌过程不耗能 D.葡萄糖可通过主动运输但不能通过协助扩散进入细胞"
    my_merge = MyMerge()
    print(my_merge.generate(question))