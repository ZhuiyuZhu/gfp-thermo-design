# Dockerfile for GFP Design Pipeline
# 提供可复现的计算环境

FROM python:3.9-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    wget \
    build-essential \
    pandoc \
    texlive-xetex \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装ESM-2
RUN pip install fair-esm

# 复制项目代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app
ENV TORCH_HOME=/app/.cache/torch

# 默认命令
CMD ["bash", "run_pipeline.sh"]
