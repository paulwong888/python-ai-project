BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH

accelerate launch -m axolotl.cli.merge_lora configs/deepspeed_train.yml
# accelerate launch -m axolotl.cli.train configs/fsdp_train.yml
#accelerate launch -m axolotl.cli.train configs/official_train.yml