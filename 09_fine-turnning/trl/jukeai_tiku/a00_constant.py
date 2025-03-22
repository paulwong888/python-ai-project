
env_file_path = "/home/paul/paulwong/work/config"
model_name = "/home/paul/.cache/huggingface/models/models--Qwen--Qwen2.5-1.5B-Instruct"
dataset_dir = "/home/paul/.cache/huggingface/hub/datasets--juke-ai--tiku"
output_dir = "09_fine-turnning/trl/jukeai_tiku/output/"
adapter_dir = output_dir + "fine_tuned_model"

prompt_style = """以下是一个描述任务的指令，配有提供进一步背景的输入。请写出一个适当完成请求的回答。

### Instruction:
您是一位专业的高考老师，擅长分析和解答各类高考试卷问题，包括选择题、填空题、解答题和作文题。
请根据以下高考试卷问题，提供准确、清晰的解答，并说明解题思路。

### Question:
{}

### Response:
{}"""

response_template = "### Response"