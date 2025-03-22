## VLLM
用VLLM加载各种模型
### 安装
```
conda create -n vllm python=3.10
conda activate vllm

# Install the latest code using pip
pip install vllm --pre --extra-index-url https://wheels.vllm.ai/nightly

pip install -r 16_vllm/requirements.txt

git clone https://github.com/vllm-project/vllm.git
cd vllm
VLLM_USE_PRECOMPILED=1 pip install --editable .

pip install git+https://github.com/huggingface/transformers@v4.49.0-Gemma-3
```