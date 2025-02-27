README
MIT license
AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration

[Paper][Slides][Video]

Efficient and accurate low-bit weight quantization (INT3/4) for LLMs, supporting instruction-tuned models and multi-modal LMs.

overview

The current release supports:

AWQ search for accurate quantization.
Pre-computed AWQ model zoo for LLMs (Llama-1/2/3, OPT, CodeLlama, StarCoder, Vicuna, VILA, LLaVA; load to generate quantized weights).
Memory-efficient 4-bit Linear in PyTorch.
Efficient CUDA kernel implementation for fast inference (support context and decoding stage).
Examples on 4-bit inference of an instruction-tuned model (Vicuna) and multi-modal LM (VILA).
Chunk prefilling for faster prefilling in multi-round Q&A setting.
State-of-the-art prefilling speed of LLMs/VLMs on edge devices: TinyChat 2.0.
Thanks to AWQ, TinyChat can deliver more efficient responses with LLM/VLM chatbots through 4-bit inference.

TinyChat with LLaMA-3-8b on RTX 4090 (2.7x faster than FP16):
TinyChat with LLaMA-3-8b on RTX 4090: W4A16 is 2.7x faster than FP16

TinyChat with LLaMA-3-8b on Jetson Orin (2.9x faster than FP16):
 

TinyChat also supports inference with vision language models (e.g., VILA, LLaVA). In the following examples, W4A16 quantized models from VILA family are launched with TinyChat.

TinyChat with NVILA-8B on RTX 4090 (single-image inputs):
TinyChat with NVILA on 4090 single image

TinyChat with NVILA-8B on RTX 4090 (multi-image inputs):
TinyChat with NVILA on 4090 multiple images

TinyChat with video reasoning:
 AvVDsFBc6bA.0.mp4 

Prompt: What might be the next step according to the video?

Answer: The next step in the video could be to place the shaped dough onto a baking sheet and let it rise before baking.

Online demo: https://vila.mit.edu

Check out TinyChat, which offers a turn-key solution for on-device inference of LLMs and VLMs on resource-constrained edge platforms. With TinyChat, it is now possible to efficiently run large models on small and low-power devices even without Internet connection!

News

[2024/10] 🔥⚡ Explore advancements in TinyChat 2.0, the latest version with significant advancements in prefilling speed of Edge LLMs and VLMs, 1.5-1.7x faster than the previous version of TinyChat. Please refer to the README and blog for more details.
[2024/05] 🏆 AWQ receives the Best Paper Award at MLSys 2024. 🎉
[2024/05] 🔥 The VILA-1.5 model family which features video understanding is now supported in AWQ and TinyChat. Check out out online demo powered by TinyChat here. Example is here.
[2024/05] 🔥 AMD adopts AWQ to improve LLM serving efficiency.
[2024/04] 🔥 We released AWQ and TinyChat support for The Llama-3 model family! Check out our example here.
[2024/02] 🔥 AWQ has been accepted to MLSys 2024!
[2024/02] 🔥 We supported VILA Vision Languague Models in AWQ & TinyChat! Check our latest demos with multi-image inputs!
[2024/02] 🔥 We released new version of quantized GEMM/GEMV kernels in TinyChat, leading to 38 tokens/second inference speed on NVIDIA Jetson Orin!
[2024/01] 🔥 AWQ has been integrated by Google Vertex AI!
[2023/11] 🔥 AWQ has been integrated by Amazon Sagemaker Containers!
[2023/11] 🔥 We added AWQ support and pre-computed search results for CodeLlama, StarCoder, StableCode models. Checkout our model zoo here!
[2023/11] 🔥 AWQ is now integrated natively in Hugging Face transformers through from_pretrained. You can either load quantized models from the Hub or your own HF quantized models.
[2023/10] AWQ is integrated into NVIDIA TensorRT-LLM
[2023/09] AWQ is integrated into Intel Neural Compressor, FastChat, vLLM, HuggingFace TGI, and LMDeploy.
[2023/09] ⚡ Check out our latest TinyChat, which is ~2x faster than the first release on Orin!
[2023/09] ⚡ Check out AutoAWQ, a third-party implementation to make AWQ easier to expand to new models, improve inference speed, and integrate into Huggingface.
[2023/07] 🔥 We released TinyChat, an efficient and lightweight chatbot interface based on AWQ. TinyChat enables efficient LLM inference on both cloud and edge GPUs. Llama-2-chat models are supported! Check out our implementation here.
[2023/07] 🔥 We added AWQ support and pre-computed search results for Llama-2 models (7B & 13B). Checkout our model zoo here!
[2023/07] We extended the support for more LLM models including MPT, Falcon, and BLOOM.
Contents

AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration
News
Contents
Helpful Links
Install
AWQ Model Zoo
Examples
Usage
Results on Visual Language Models
Reference
Related Projects
Helpful Links

VILA online demo: Visual Language Models efficiently supported by AWQ & TinyChat.
LLM on the Edge: AWQ and TinyChat support edge GPUs such as NVIDIA Jetson Orin.
VLMs on Laptop: Follow the instructions to deploy VLMs on NVIDIA Laptops with TinyChat.
Gradio Server: Try to build your own VLM online demo with AWQ and TinyChat!
QServe: 🔥 [New] Efficient and accurate serving system for large-scale LLM inference.
Install

Clone this repository and navigate to AWQ folder
git clone https://github.com/mit-han-lab/llm-awq
cd llm-awq
Install Package
conda create -n awq python=3.10 -y
conda activate awq
pip install --upgrade pip  # enable PEP 660 support
pip install -e .
For edge devices like Orin, before running the commands above, please:

Modify pyproject.toml by commenting out this line.
Manually install precompiled PyTorch binaries (>=2.0.0) from NVIDIA. You also need to install torchvision from this website when running NVILA.
Set the appropriate Python version for conda environment (e.g., conda create -n awq python=3.8 -y for JetPack 5).
Install efficient W4A16 (4-bit weight, 16-bit activation) CUDA kernel and optimized FP16 kernels (e.g. layernorm, positional encodings).
cd awq/kernels
python setup.py install
In order to run AWQ and TinyChat with NVILA model family, please install VILA:
git clone https://github.com/NVlabs/VILA.git
cd VILA
pip install -e .