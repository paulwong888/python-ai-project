BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH

axolotl inference configs/03_llama3_deepspeed.yml \
    --base-model /home/paul/.cache/huggingface/hub/models--deepseek-ai--DeepSeek-R1-Distill-Llama-8B \
    --lora-model-dir="/home/paul/paulwong/work/workspaces/python-ai-project/09_fine-turnning/axolotl/01_psychological-consultant/models/Llama3_Storyteller_deepspeed/llama3-checkpoint-4800" \
    --gradio \
    --gradio-server-name 0.0.0.0 \
    --gradio-server-port 8000