FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

# 设置环境变量
ENV MEILI_HTTP_ADDR=0.0.0.0:7700
ENV MEILI_MASTER_KEY=MASTER_KEY
RUN sed -i.bak -E 's|http://(.*\.)?archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g; s|http://(.*\.)?security.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list
# 更新包并安装 PPA 管理工具
RUN apt update && apt install -y software-properties-common
# 添加 deadsnakes PPA 源
RUN add-apt-repository -y ppa:deadsnakes/ppa && apt update
# 安装指定版本 Python 和常用工具
RUN DEBIAN_FRONTEND=noninteractive apt install -y wget curl python3.9 python3.9-venv python3.9-dev python3-pip \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*
# 下载 MeiliSearch 二进制文件并设置执行权限
RUN wget https://gh-proxy.com/github.com/meilisearch/meilisearch/releases/download/v1.12.1/meilisearch-linux-amd64 \
    -O /usr/bin/meilisearch && chmod +x /usr/bin/meilisearch
WORKDIR /fuzi-mingcha
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

COPY . .
# 设置 launch.sh 为可执行
RUN chmod +x launch.sh
ENTRYPOINT ["./launch.sh"]