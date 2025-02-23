from a00_constant import *
from a01_my_model import MyModel
from unsloth import FastLanguageModel
from transformers import LlamaForCausalLM

"""
{
  "answer": [
    "# 18",
    "# 3"
  ],
  "prompt": [
    [
      {
        "content": "\nRespond in the following format:\n<reasoning>\n...\n</reasoning>\n<answer>\n...\n</answer>\n",
        "role": "system"
      },
      {
        "content": "Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?",
        "role": "user"
      }
    ],
    [
      {
        "content": "\nRespond in the following format:\n<reasoning>\n...\n</reasoning>\n<answer>\n...\n</answer>\n",
        "role": "system"
      },
      {
        "content": "A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?",
        "role": "user"
      }
    ]
  ]
}
"""
class MyMerge(MyModel):
    def __init__(self):
        self.model: LlamaForCausalLM
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name = model_name,
        )
        self.model.load_adapter(adapter_path)

if __name__ == "__main__":
    my_merge = MyMerge()
    # question = "下列是与蛋白质、核酸相关的一些描述，其中正确的是  （    ） A. 核酸均可携带遗传信息，但只有DNA是生物的遗传物质 B. 核酸中的N存在于碱基中，蛋白质中的N主要存在于氨基中 C. 氨基酸分子互相结合的方式与mRNA中碱基排列顺序无关 D. 磷酸和五碳糖的连接方式在单链RNA和双链DNA的一条链中是不同的"
    question = "A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?"
    my_merge.generate(question)
