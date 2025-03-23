import pandas as pd
from a00_constant import *
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer


"""
input:
我晚上难以入睡，我认为这是因为我对工作感到压力	

reasoning_content:
嗯，用户说他晚上难以入睡，认为是因为工作压力。首先，我需要确认他的情况是否常见，以及可能的解决方法。工作压力导致的失眠确实很普遍，但每个人的具体情况可能不同。我需要考虑他的工作环境、压力源是什么，比如工作量、人际关系还是职业发展。然后，可能涉及到他的睡前习惯，是否有使用电子设备、咖啡因摄入等影响睡眠的因素。此外，心理健康方面，比如焦虑或抑郁情绪也可能加剧失眠。我需要建议他调整作息，比如建立规律的睡眠时间，避免咖啡因和蓝光。放松技巧如冥想、深呼吸可能会有帮助。如果自我调节无效，可能需要建议他寻求专业帮助，比如心理咨询师或医生。同时，时间管理技巧可能减轻工作压力，比如任务优先级划分，适当授权任务。还要注意他的支持系统，比如家人朋友的支持。需要提醒他如果症状持续，可能有更严重的健康问题，应该及时就医。最后，要确保建议具体可行，并且语气要 empathetic，让他感受到被理解和支持。

content:
你的情况是很多职场人都会遇到的困扰，工作压力导致的失眠往往是一个恶性循环：压力影响睡眠质量，睡眠不足又导致次日工作效率降低，进一步加重压力。以下是一些针对性建议，希望能帮助你逐步打破这个循环：
**第一步：建立压力档案（当晚即可操作）**
1. 准备笔记本记录：
- 具体压力事件（如"明早要向董事会汇报"）
- 伴随的生理反应（手心出汗/心跳加速）
- 脑海中的具体担忧（"忘词怎么办？数据记错怎么办？"）
- 实际发生概率（用百分比标注，如"忘词概率约20%"）

**第二步：90分钟睡眠周期调整法（3天内见效）**
- 计算就寝时间：设定起床时间后倒推1.5小时的整数倍
- 例：若需7点起床，可尝试11:30或1:00入睡
- 使用SleepCycle等APP监测睡眠质量

**第三歩：办公室微放松（工作中随时可用）**
- 4-7-8呼吸法：吸气4秒→屏息7秒→呼气8秒（
- 桌面减压神器：备握力球/指尖陀螺，在接电话时使用
- 视觉放松：将电脑桌面换成动态自然景观（推荐Rainy Mood网站）

**进阶方案：压力转化训练（需1-2周练习）**
1. 压力具象化练习：
- 每天花5分钟将压力想象成具体物体（如不断膨胀的气球）
- 在脑海中为这个"压力球"设置安全阀，想象缓慢释放过程

2. 焦虑时段专用笔记本：
- 设定"焦虑时间"（如晚8-8:30）
- 其他时间出现担忧时快速记录关键词，留到专用时段处理

**重要提醒：**
若出现以下情况建议立即就医：
- 连续3天睡眠不足4小时
- 出现心悸/手抖等躯体症状
- 对原本爱好完全失去兴趣

建议从今晚开始尝试"压力档案"记录，很多时候当我们把模糊的焦虑具体化后，它的压迫感就会明显减弱。这个过程可能需要持续记录3-5天才能看到明显效果，请给自己足够的耐心。记住，你不需要完美解决所有压力源，重点在于重建对压力的掌控感。	
"""

class MyDataset():
    def __init__(self):
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.EOS_TOKEN = tokenizer.eos_token

        dataset = load_dataset(dataset_dir, split="train")

        train_dataset, val_dataset, test_dataset = self.train_test_spit(dataset)

        self.train_dataset = self.pre_processing(train_dataset)
        self.val_dataset = self.pre_processing(val_dataset)
        self.test_dataset = self.pre_processing(test_dataset)

    def train_test_spit(self, dataset: Dataset):
        train_test_dataset = self.split_dataset(dataset)
        test_dataset = train_test_dataset["test"]

        train_val_dataset = self.split_dataset(train_test_dataset["train"])
        train_dataset = train_val_dataset["train"]
        val_dataset = train_val_dataset["test"]

        return train_dataset, val_dataset, test_dataset


    def split_dataset(self, dataset: Dataset):
        return dataset.train_test_split(0.2, shuffle=True, seed=42)
    
    def format_input(self, samples):
        inputs = samples["input"]
        contents = samples["content"]
        reasoning_contents = samples["reasoning_content"]
        texts = []
        for input, content, reasoning_content in zip(inputs, contents, reasoning_contents):
            text = train_prompt_style.format(input, reasoning_content, content)
            texts.append(text)
        return dict(text = texts)

    def pre_processing(self, dataset: Dataset):
        return dataset.map(
            lambda x: self.format_input(x),
            batched = True,
            remove_columns = ["input", "content", "reasoning_content"]
        )

if __name__ == "__main__":
    df = pd.read_json(
        dataset_dir + "/distill_psychology-10k-r1.json",
        lines = True,
        # chunksize = 20,
    )
    df
    my_dataset = MyDataset()
    my_dataset.train_dataset.to_pandas()
    my_dataset.val_dataset.to_pandas()
    my_dataset.test_dataset.to_pandas()
    