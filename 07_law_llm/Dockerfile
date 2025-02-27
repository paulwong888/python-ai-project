# 使用官方 Python 运行时作为父镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到位于 /app 的容器中
COPY a00_constant.py a02_law_llama3_runner.py app.py requirements.txt /app/

# 安装所需的包
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 使端口 7860 可供此容器外的世界访问
EXPOSE 7860

# 在容器启动时运行 app.py
CMD ["python", "app.py"]