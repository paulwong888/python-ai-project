import torch, os
# from unsloth import is_bfloat16_supported
# from dotenv import load_dotenv

# load_dotenv("/home/paul/paulwong/work/config")
wandb_key=os.getenv("wandb_key")

model_name: str="/home/paul/.cache/huggingface/models/models--Qwen--Qwen2.5-1.5B-Instruct"
dataset_dir: str = "/home/paul/.cache/huggingface/hub/datasets--juke-ai--tiku"
adapter_path: str = "outputs/checkpoint-1100"
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
num_train_epochs = 50
# fp16=not is_bfloat16_supported()
# bf16=is_bfloat16_supported()
logging_steps: int=1
optim: str ="adamw_8bit"
weight_decay: float=0.01
lr_scheduler_type: str="linear"
seed: int=3407
output_dir: str="outputs"

prompt_style = """以下是一个描述任务的指令，配有提供进一步背景的输入。请写出一个适当完成请求的回答。

### Instruction:
您是一位专业的高考老师，擅长分析和解答各类高考试卷问题，包括选择题、填空题、解答题和作文题。
请根据以下高考试卷问题，提供准确、清晰的解答，并说明解题思路。

### Question:
{}

### Response:
{}"""

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