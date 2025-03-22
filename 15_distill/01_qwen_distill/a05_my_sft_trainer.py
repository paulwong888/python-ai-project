from a01_contant import *
from a02_test_model import MyModel
from a04_my_dataset import MyDataset
from trl import SFTConfig, SFTTrainer

class MySFTTrainer():
    def __init__(self):
        dataset = MyDataset().dataset
        sft_config = SFTConfig(
            output_dir = output_path,
            max_seq_length = 1024,
            per_device_train_batch_size = 2,
            num_train_epochs = 10,
            logging_steps = 1,
        )
        my_model = MyModel()
        train_model = my_model.model
        tokenizer = my_model.tokenizer
        self.trainer = SFTTrainer(
            model = train_model,
            tokenizer = tokenizer,
            train_dataset = dataset,
            args = sft_config, 
            # formatting_func = lambda x: f"### Prompt: {x['prompt']}\n### Response: {x['completion']}",
        )

    def train(self):
        self.trainer.train()

if __name__ == "__main__":
    my_sft_trainer = MySFTTrainer()
    my_sft_trainer.train()