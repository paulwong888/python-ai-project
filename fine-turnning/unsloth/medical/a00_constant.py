import torch, os
from unsloth import is_bfloat16_supported
from dotenv import load_dotenv

load_dotenv("/home/paul/paulwong/work/config")
wandb_key=os.getenv("wandb_key")

model_name: str="/home/paul/.cache/huggingface/models/unsloth--DeepSeek-R1-Distill-Llama-8B"
dataset_name: str = "/home/paul/.cache/huggingface/hub/datasets--FreedomIntelligence--medical-o1-reasoning-SFT"
max_seq_length: int = 2048
dtype: str=None
load_in_4bit: bool=True
dataset_num_proc: int=2
device: str = "cuda" if torch.cuda.is_available() else "cpu"

per_device_train_batch_size: int=2
gradient_accumulation_steps: int=4
warmup_steps: int=5
max_steps: int=200
learning_rate=2e-4
fp16=not is_bfloat16_supported()
bf16=is_bfloat16_supported()
logging_steps: int=1
optim: str ="adamw_8bit"
weight_decay: float=0.01
lr_scheduler_type: str="linear"
seed: int=3407
output_dir: str="outputs"

prompt_style = """Below is an instruction that describes a task, paired with an input that provides further context. 
Write a response that appropriately completes the request. 
Before answering, think carefully about the question and create a step-by-step chain of thoughts to ensure a logical and accurate response.

### Instruction:
You are a medical expert with advanced knowledge in clinical reasoning, diagnostics, and treatment planning. 
Please answer the following medical question. 

### Question:
{}

### Response:
<think>{}"""

train_prompt_style = """Below is an instruction that describes a task, paired with an input that provides further context. 
Write a response that appropriately completes the request. 
Before answering, think carefully about the question and create a step-by-step chain of thoughts to ensure a logical and accurate response.

### Instruction:
You are a medical expert with advanced knowledge in clinical reasoning, diagnostics, and treatment planning. 
Please answer the following medical question. 

### Question:
{}

### Response:
<think>
{}
</think>
{}"""