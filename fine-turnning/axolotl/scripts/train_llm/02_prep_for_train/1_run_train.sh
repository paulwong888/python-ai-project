BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH/../../
pwd

# accelerate launch -m axolotl.cli.train configs/bassic_train.yml
docker compose exec axolotl axolotl train /app/configs/advance_train.yml
# docker compose exec axolotl bash
#accelerate launch -m axolotl.cli.train configs/official_train.yml