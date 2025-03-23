import torch
import pandas as pd
from a00_constant import *
from a02_my_model import MyModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, TextStreamer

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
        tokenizer = AutoTokenizer.from_pretrained(adapter_dir)
        model: AutoModelForCausalLM = AutoModelForCausalLM.from_pretrained(
            model_name,
            # torch_dtype = torch.float16,
            device_map = "auto"
        )
        model.load_adapter(adapter_dir)
        return model, tokenizer
    
    # def generate(self, message):
    #     return self.pipeline(message)
    
"""
下列关于细胞呼吸在生产生活中应用的叙述，错误的是  （    ） A. 给含有酵母菌的发酵液连续通气可以提高产酒量 B. 适当降低温度和氧浓度有利于果蔬储藏 C. 利用乳酸细菌制作酸奶过程中需密闭隔绝空气 D. 黑暗条件下绿豆萌发成豆芽的过程中有机物总量不断减少
"""
if __name__ == "__main__":
    df_train = pd.read_json(dataset_dir + "/train.json")
    df_test = pd.read_json(dataset_dir + "/test.json")
    df_train
    df_test
    question1 = "红蟋蟀、滨州蟋蟀和富尔顿蟋蟀形态相同，鸣声的强弱和频率不同，交配只在发生同一鸣声的种内进行。下列叙述正确的是  （    ） A. 蟋蟀之间的鸣声属于物理信息，物理信息只能来自生物 B. 红蟋蟀中出现了新基因，则该种群发生了进化 C. 红蟋蟀、滨州蟋蟀和富尔顿蟋蟀属于同一物种 D. 若滨州蟋蟀和富尔顿蟋蟀之间形成杂交种，则一定是可育后代." 
    # B /n【解析】生态系统中的信息分为物理信息如光、声等，化学信息如生物碱、有机酸等物质，行为信息如动物的行为，生态系统中的信息既可来来自于各种生物，也可来源于无机环境；现代生物进化理论认为，生物进化的基本单位是种群，生物进化的实质就是种群基因频率发生定向改变；不同物种之间一般是不能相互交配的，即使交配成功，也不能产生可育的后代，即存在生殖隔离，生殖隔离可分为：生态隔离、季节隔离、性别隔离、行为隔离、杂种不育等。 【详解】A. 生态系统中物理信息的来源可以来自无机环境或生物，A错误；B. 红蟋蟀中出现了新基因，则种群基因频率发生了改变，该种群发生了进化，B正确；C. 红蟋蟀、滨州蟋蟀和富尔顿蟋蟀鸣声的强弱和频率不同，交配只在发生同一鸣声的种内进行，说明它们之间不能交配，存在生殖隔离，因此它们属于不同的物种，C错误；D. 滨州蟋蟀和富尔顿蟋蟀之间存在生殖隔离，它们形成的杂交种是不育的，D错误。 2020年高考生物选择题专项训练（02）
    question2 = "下列关于细胞呼吸在生产生活中应用的叙述，错误的是  （    ） A. 给含有酵母菌的发酵液连续通气可以提高产酒量 B. 适当降低温度和氧浓度有利于果蔬储藏 C. 利用乳酸细菌制作酸奶过程中需密闭隔绝空气 D. 黑暗条件下绿豆萌发成豆芽的过程中有机物总量不断减少"
    # A /n【解析】呼吸作用的影响因素有：氧气、温度等。 【详解】酵母菌是兼性厌氧型生物，发酵初期需要氧气进行增殖，后期需要在无氧条件下进行酒精发酵，A错误；果蔬储藏时应该降低呼吸作用消耗，应该在低温和低氧条件下进行，B正确；乳酸菌是厌氧型生物，乳酸发酵时需要处于无氧环境中，C正确；黑暗下，豆芽只能进行呼吸作用，不能进行光合作用，故有机物总量会下降，D正确。故选A。
    question3 = "下列关于生命系统中的信息传递的叙述，正确的是  （    ） A. 细胞内的遗传信息传递方式:DNARNA蛋白质（性状） B. 细胞间通过激素、神经递质实现其全部信息传递 C. 在兔→狐过程中，物质、能量从兔到狐单向传递，而信息却是双向传递的 D. 生态系统中信息传递发生在同种生物或不同种生物之间，并能调节种间关系"
    # C /n【解析】分析：细胞生物中遗传信息可以从DNA流向DNA，也可以从DNA流向RNA，进而流向蛋白质，在某些病毒中遗传信息可以从RNA流向RNA以及从RNA流向DNA。细胞间的信息交流主要有三种方式：①通过化学物质来传递信息，如激素；②通过细胞膜直接接触传递信息，如精卵识别；③通过细胞通道来传递信息，如高等植物细胞之间通过胞间连丝相互连接。生态系统中信息的类型包括物理信息、化学信息、行为信息，信息传递在生态系统中的作用主要体现在以下三方面：生态系统中生命活动的正常进行，离不开信息的作用；生物种群的繁衍，也离不开信息的传递；信息还能够调节生物的种间关系，维持生态系统稳定。 详解：A. 生物体细胞中，传递遗传信息传递途径有DNA→DNA即DNA的复制，也有DNA→RNA→蛋白质即转录和翻译，A错误；B. 细胞间的信息传递，除了通过激素，神经递质外，还可通过细胞膜上的糖蛋白传递信息，植物细胞间还可以形成胞间连丝实现信息传递，B错误； C. 物质和能量沿食物链单向传递，捕食过程中捕食者和被捕食者之间的信息传递是双向的，如狼可根据兔子留下的气味捕食后者，兔子同样也能依据狼的气味或行为特征躲避捕食，C正确；D. 信息传递既可以发生在生物与生物之间，也可以发生在生物与环境之间，如植物开花需要光信息和日照时间达到一定长度，这些物理信息即来自无机环境，D错误。 点睛：本题考查中心法则及其发展、细胞膜的功能、生态系统中的信息传递，要求考生识记中心法则的主要内容及后人对其进行的补充和完善；同时识记细胞膜的信息交流功能；掌握生态系统中信息传递在生产实践中的应用，能应用所学的知识准确判断各选项。
    my_merge = MyMerge()
    my_merge.generate(question1)
    print("--" * 10)
    my_merge.generate(question2)
    print("--" * 10)
    my_merge.generate(question3)