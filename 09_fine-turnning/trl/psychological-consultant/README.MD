## 使用trl库做微调
这个所做的任务是做LoRA微调, 经发现比全参数微调效果要好
### 安装
```
conda create -n distill-data python=3.10
conda activate distill-data

pip install -r 15_distill/01_qwen_distill/requirements.txt
```
### 基座模型
```
Qwen/Qwen2.5-1.5B-Instruct
```
### 数据集
指令微调原本的数据集格式为: 问题、答案两列, 必须要转为单列, 列名为“text”, 里面的数据含system信息, 上下文和答案

指令微调只需两个参数: “prompt”和"completion", 这种数据集格式由于没有system信息, 角色设定等, 效果不好

### 参考
trl的 [SFT](https://huggingface.co/docs/trl/sft_trainer#best-practices)