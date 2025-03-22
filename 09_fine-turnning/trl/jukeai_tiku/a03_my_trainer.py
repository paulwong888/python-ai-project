import torch
from a00_constant import *
from a01_my_dataset import MyDataset
from a02_my_model import MyModel
from trl import SFTConfig, SFTTrainer
from peft import LoraConfig

class MyTrainer():
    def __init__(self):
        my_dataset = MyDataset()
        my_model = MyModel()
        sft_config = SFTConfig(
            output_dir = output_dir,
            num_train_epochs = 10,
            per_device_train_batch_size = 2,
            gradient_checkpointing = True,
            gradient_accumulation_steps = 1,
            learning_rate = 2e-5,
            fp16 = True,
            fp16_full_eval=False,  # ✅ 禁用评估 FP16
            optim="adamw_torch_fused",  # ✅ 使用融合优化器
            # optim = "adamw_8bit",
            logging_steps=1,
        )
        peft_config = LoraConfig(
            r = 32,
            lora_alpha = 64,
            lora_dropout = 0.1,
            bias = "lora_only",
            task_type = "CAUSAL_LM",
            # target_modules=["q_proj", "v_proj"]  # 精简目标模块
        )
        self.my_trainer: SFTTrainer = SFTTrainer(
            model = my_model.model,
            args = sft_config,
            peft_config = peft_config,
            train_dataset = my_dataset.train_dataset,
            eval_dataset = my_dataset.test_dataset,
            formatting_func = lambda x: my_dataset.format_prompt(x),
            data_collator = my_dataset.data_collator,
            # max_seq_length = 1024,
        )

    def train(self):
        self.my_trainer.train()
        self.my_trainer.save_model(adapter_dir)

if __name__ == "__main__":
    my_trainer = MyTrainer()
    my_trainer.train()