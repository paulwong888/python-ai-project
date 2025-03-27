## 使用trl库做微调
这个所做的任务是做LoRA微调, 经发现比全参数微调效果要好
### 安装
```
conda create -n axolotl python=3.10
conda activate axolotl

pip install -r 09_fine-turnning/axolotl/01_psychological-consultant/requirements.txt
```
### 基座模型
```
modelscope download deepseek-ai/DeepSeek-R1-Distill-Llama-8B --local_dir=. --max-workers=1
```
### 数据集
指令微调原本的数据集格式为: 问题、答案两列, 必须要转为单列, 列名为“text”, 里面的数据含system信息, 上下文和答案

指令微调只需两个参数: “prompt”和"completion", 这种数据集格式由于没有system信息, 角色设定等, 效果不好
```
modelscope download --repo-type dataset Kedreamix/psychology-10k-Deepseek-R1-zh --local_dir=. --max-workers=1
```

### 参考
trl的 [SFT](https://huggingface.co/docs/trl/sft_trainer#best-practices)

[配置文件](https://huggingface.co/allura-org/Teleut-7b)

[配置文件UI编辑器](https://axolotl-ui.vercel.app)
