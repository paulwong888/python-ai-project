from a00_constant import *
from unsloth import FastLanguageModel

class MyModel:
    def __init__(self):
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name,
        )

    def generate(self, message):
        FastLanguageModel.for_inference(self.model)
        input = self.tokenizer(
            [prompt_style.format(message, "")], return_tensors="pt"
        ).to(device)
        output = self.model.generate(
            **input,
            use_cache = True
        )
        response = self.tokenizer.batch_decode(output)
        print(response[0].split("### Response:")[1])
        return response
    
    def get_peft_model(self):
        return FastLanguageModel.get_peft_model(
            self.model,
        )

if __name__ == "__main__":
    my_model = MyModel()
    question = "下列关于细胞结构和功能的叙述，正确的是（  ） A. 有内质网的细胞不一定是真核细胞 B. 有中心体的细胞一定是动物细胞 C. 有高尔基体的细胞不一定有分泌功能 D. 有核糖体的细胞一定能合成分泌蛋白"
    my_model.generate(question)