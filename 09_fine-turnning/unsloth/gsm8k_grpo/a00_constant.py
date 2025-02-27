import torch, os
from unsloth import is_bfloat16_supported
from dotenv import load_dotenv

load_dotenv("/home/paul/paulwong/work/config")
wandb_key=os.getenv("wandb_key")

# model_name: str="/home/paul/.cache/huggingface/hub/models--unsloth--Meta-Llama-3.1-8B-Instruct/snapshots/da09a334d51a646967eec17cb412575702b3d767"
model_name: str="/home/paul/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/bb46c15ee4bb56c5b63245ef50fd7637234d6f75"
dataset_dir: str = "/home/paul/.cache/huggingface/hub/datasets--openai--gsm8k/socratic"
adapter_path: str = "/home/paul/paulwong/work/workspaces/python-ai-project/fine-turnning/unsloth/gsm8k_grpo/outputs/checkpoint-350"
max_seq_length: int = 512
dtype: str=None
load_in_4bit: bool=True
fast_inference=True
max_lora_rank=32
# gpu_memory_utilization = 0.8 #training for 2080
gpu_memory_utilization = 0.95 #training for 2080
use_gradient_checkpointing = "unsloth"
random_state = 3407
device: str = "cuda" if torch.cuda.is_available() else "cpu"

per_device_train_batch_size: int=2
gradient_accumulation_steps: int=4
warmup_steps: int=5
max_steps: int=350
learning_rate=2e-4
fp16=not is_bfloat16_supported()
bf16=is_bfloat16_supported()
logging_steps: int=1
optim: str ="adamw_8bit"
weight_decay: float=0.01
lr_scheduler_type: str="linear"
seed: int=3407
output_dir: str="fine-turnning/unsloth/gsm8k_grpo/outputs"
report_to = "wandb"

# Load and prep dataset
SYSTEM_PROMPT = """
Respond in the following format:
<reasoning>
...
</reasoning>
<answer>
...
</answer>
"""

XML_COT_FORMAT = """\
<reasoning>
{reasoning}
</reasoning>
<answer>
{answer}
</answer>
"""