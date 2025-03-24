BIN_PATH=$(cd `dirname $0`; pwd)
cd $BIN_PATH

export deepspeed_config_file="deepspeed/zero3.json"

# 替换环境变量生成最终配置
envsubst < deepspeed/deepspeed_zero_config_template.yaml > deepspeed/deepspeed_zero_config.yaml

accelerate launch --config_file deepspeed/deepspeed_zero_config.yaml a03_my_trainer.py
# accelerate launch a03_my_trainer.py
# deepspeed --num_gpus=2 a03_my_trainer.py