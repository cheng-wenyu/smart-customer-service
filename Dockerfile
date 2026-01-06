FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 设置环境变量（使用国内镜像源）
ENV HF_ENDPOINT=https://hf-mirror.com
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖（使用国内源）
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p logs/monitoring data/models
# 
# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "run.py"]
