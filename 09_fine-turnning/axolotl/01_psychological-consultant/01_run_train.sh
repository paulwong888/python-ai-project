BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH

# accelerate launch -m axolotl.cli.train configs/deepspeed_train.yml --deepspeed configs/deepspeed/zero3.json
accelerate launch -m axolotl.cli.train configs/03_llama3_deepspeed.yml --use_deepspeed configs/deepspeed/zero3.json
