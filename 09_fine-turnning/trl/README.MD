## 使用trl库做微调
这个所做的任务是指令微调, 而且是全参数微调, 不做任何LoRA处理
### 安装
```
conda create -n distill-data python=3.10
conda activate distill-data

pip install -r 15_distill/01_qwen_distill/requirements.txt
```
### 数据集
指令微调只需两个参数: “prompt”和"completion", 无需做任何其他处理, 而且做了反而没效果