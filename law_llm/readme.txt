conda create -n huggingface python=3.10

conda activate huggingface

pip install -r requirements.txt

pip install torch==2.3.1+cu121 torchvision torchaudio -f https://mirrors.aliyun.com/pytorch-wheels/cu121/
清华源无cuda版本

huggingface-cli download Qwen/Qwen2.5-7B-Instruct --max-workers 1 --local-dir-use-symlinks false --local-dir XXX
huggingface-cli download unsloth/Meta-Llama-3.1-8B-Instruct --max-workers 1 --local-dir-use-symlinks false --local-dir XXX

modelscope download Qwen/Qwen2.5-7B-Instruct --max-workers 1 --local_dir ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/bb46c15ee4bb56c5b63245ef50fd7637234d6f75
modelscope download unsloth/Meta-Llama-3.1-8B-Instruct --max-workers 1 --local_dir ~/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/snapshots/bb46c15ee4bb56c5b63245ef50fd7637234d6f75

法律知识dataset:
huggingface-cli download leo009/lawdata --repo-type dataset

--------------------
export HF_ENDPOINT=https://hf-mirror.com
export HF_HOME=XXX
export MODELSCOPE_CACHE=/path/to/your/directory
--------------------
学术加速
source /etc/network_turbo
取消学术加速，如果不再需要建议关闭学术加速，因为该加速可能对正常网络造成一定影响
unset http_proxy && unset https_proxy
--------------------

某拍卖企业在进行文物拍卖时，有观众提出质疑，认为拍卖师不具备合法资格。请问拍卖师应当具备哪些条件？

#pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
#pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/