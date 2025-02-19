from a00_constant import *
from a01_my_model import MyModel
from a02_my_dataset import MyDataset
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported
import wandb

class MyTrainer:
    # PeftModelForCausallm
    def __init__(self):
        wandb.login(key="aa9241b28fbdbef0477258f0d8a4f8d0f43df80a")
        run = wandb.init(
            project='Fine-tune-DeepSeek-R1-Distill-Llama-8B on Medical COT Dataset', 
            job_type="training", 
            anonymous="allow"
        )
        my_model=MyModel()
        my_dataset = MyDataset()
        self.trainer = SFTTrainer(
            model = my_model.get_peft_model(),
            tokenizer = my_model.tokenizer,
            train_dataset = my_dataset.dataset,
            dataset_text_field = "text",
            max_seq_length = max_seq_length,
            dataset_num_proc = dataset_num_proc,
            args = TrainingArguments(
                per_device_train_batch_size=per_device_train_batch_size,
                gradient_accumulation_steps=gradient_accumulation_steps,
                warmup_steps=warmup_steps,
                max_steps=max_steps,
                learning_rate=learning_rate,
                fp16=fp16,
                bf16=bf16,
                logging_steps=logging_steps,
                optim=optim,
                weight_decay=weight_decay,
                lr_scheduler_type=lr_scheduler_type,
                seed=seed,
                output_dir=output_dir,
                report_to="wandb"
            )
        )

    def train(self):
        self.trainer.train()

if __name__ == "__main__":
    my_trainer = MyTrainer()
    my_trainer.train()