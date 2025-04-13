## Football Predict
体育赛事预测
### 安装
```
conda create -n football-predict python=3.10
conda activate football-predict

pip install -r 17_football_predict/requirements.txt


```
### 验证numpy的cuda版本是否安装正确
```
import cupy as cp
print(cp.cuda.runtime.getDeviceCount())  # 输出可用GPU数量
```