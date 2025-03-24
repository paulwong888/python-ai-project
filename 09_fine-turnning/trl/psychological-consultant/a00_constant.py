
env_file_path = "/home/paul/paulwong/work/config"
model_dir = "/home/paul/.cache/huggingface/hub/models--deepseek-ai--DeepSeek-R1-Distill-Llama-8B"
dataset_dir = "/home/paul/.cache/huggingface/hub/datasets--Kedreamix--psychology-10k-Deepseek-R1-zh"
project_home = "/home/paul/paulwong/work/workspaces/python-ai-project/"
output_dir = project_home + "09_fine-turnning/trl/psychological-consultant/output/"
adapter_dir = output_dir + "fine_tuned_model"
best_adapter_dir = output_dir + "checkpoint-910"
# output_dir = "/home/paul/paulwong/work/workspaces/python-ai-project/09_fine-turnning/trl/jukeai_tiku/output/checkpoint-910/"

zero1_path = project_home + "09_fine-turnning/trl/psychological-consultant/deepspeed/zero1.json"
zero2_path = project_home + "09_fine-turnning/trl/psychological-consultant/deepspeed/zero2.json"
zero2_2_path = project_home + "09_fine-turnning/trl/psychological-consultant/deepspeed/zero2-2.json"
zero3_path = project_home + "09_fine-turnning/trl/psychological-consultant/deepspeed/zero3.json"

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