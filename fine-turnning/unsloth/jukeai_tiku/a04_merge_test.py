from a00_constant import *
from a01_my_model import MyModel
from unsloth import FastLanguageModel
from transformers import Qwen2ForCausalLM

class MyMerge(MyModel):
    def __init__(self):
        self.model: Qwen2ForCausalLM
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name = model_name,
        )
        self.model.load_adapter(adapter_path)

if __name__ == "__main__":
    my_merge = MyMerge()
    """
    C /n【解析】细胞类生物都含有DNA和RNA两种核酸，其遗传物质是DNA。核酸的基本组成单位是核苷酸，1分子核苷酸由1分子磷酸、1分子五碳糖和1分子含氮碱基组成。
    蛋白质的基本组成单位是氨基酸，氨基酸通过脱水缩合反应形成肽键（－CO－NH－），组成蛋白质的氨基酸之间通过肽键连接。 
    【详解】核酸均能携带遗传信息，有细胞结构的生物遗传物质是DNA，某些病毒的遗传物质是RNA，A错误；核酸中的N存在碱基中，蛋白质中的氮主要存在肽键（－CO－NH－）中， B错误；
    氨基酸分子之间以脱水缩合的方式互相结合，与mRNA中碱基排列顺序无关，C正确；磷酸和五碳糖的连接方式在单链RNA和双链DNA的一条链中是相同的，D错误；
    故选C。
    """
    # question = "下列是与蛋白质、核酸相关的一些描述，其中正确的是  （    ） A. 核酸均可携带遗传信息，但只有DNA是生物的遗传物质 B. 核酸中的N存在于碱基中，蛋白质中的N主要存在于氨基中 C. 氨基酸分子互相结合的方式与mRNA中碱基排列顺序无关 D. 磷酸和五碳糖的连接方式在单链RNA和双链DNA的一条链中是不同的"
    question = "物质输入和输出细胞都需要经过细胞膜。下列有关人体内物质跨膜运输的叙述，正确的是（）A.乙醇是有机物，不能通过自由扩散方式跨膜进入细胞 B.血浆中的K＋进入红细胞时需要载体蛋白并消耗ATP C.抗体在浆细胞内合成时消耗能量，其分泌过程不耗能 D.葡萄糖可通过主动运输但不能通过协助扩散进入细胞"
    my_merge.generate(question)
