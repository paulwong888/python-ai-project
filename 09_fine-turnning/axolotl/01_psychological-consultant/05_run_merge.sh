BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH
pwd

axolotl merge-lora configs/03_llama3_deepspeed.yml \
    --lora-model-dir="models/Llama3_Storyteller_deepspeed/llama3-checkpoint-4800"