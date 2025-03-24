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
            num_train_epochs = 5,
            per_device_train_batch_size = 6,
            gradient_checkpointing = True,
            logging_steps=1,
        )
        self.my_trainer: SFTTrainer = SFTTrainer(
            model = my_model.model,
            tokenizer = my_model.tokenizer,
            args = sft_config,
            # peft_config = peft_config,
            train_dataset = my_dataset.train_dataset,
            eval_dataset = my_dataset.test_dataset,
            # dataset_text_field = "text",
            # dataset_num_proc = 2,
            # max_seq_length = 512,
        )

    def train(self):
        self.my_trainer.train()
        self.my_trainer.save_model(adapter_dir)

if __name__ == "__main__":
    my_trainer = MyTrainer()
    my_trainer.train()