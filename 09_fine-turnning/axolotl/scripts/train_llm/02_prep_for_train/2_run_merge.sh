BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH/../../
pwd

# accelerate launch -m axolotl.cli.train configs/bassic_train.yml
docker compose exec axolotl axolotl merge_lora /app/configs/advance_train.yml
#accelerate launch -m axolotl.cli.train configs/official_train.yml