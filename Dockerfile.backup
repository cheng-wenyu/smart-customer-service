FROM python:3.9-slim

WORKDIR /app

# 1. 升级pip并设置清华源
RUN python -m pip install --upgrade pip && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 2. 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 3. 下载并安装torch（CPU版本，避免哈希问题）
RUN pip install torch==2.0.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 4. 复制并安装其他依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# +++ 新增的核心步骤：固化模型 +++
# 4.1 安装模型下载工具
RUN pip install --no-cache-dir huggingface-hub
# 4.2 设置环境变量，使用国内镜像源加速下载（对国内服务器至关重要）
ENV HF_ENDPOINT=https://hf-mirror.com
# 4.3 将模型作为镜像的一部分下载到固定目录
RUN python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='BAAI/bge-small-zh', local_dir='/app/models/bge-small-zh', force_download=True)"




# 5. 复制应用代码
COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
