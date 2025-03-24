BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH

# accelerate launch --config_file deepspeed/default_config.yaml a03_my_trainer.py
accelerate launch a03_my_trainer.py
# deepspeed a03_my_trainer.py
# deepspeed a05_test_distributed.py