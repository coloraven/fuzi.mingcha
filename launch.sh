#!/bin/bash
# 后台运行meilisearch
nohup meilisearch &
# 等待 MeiliSearch 启动完成
echo "等待 MeiliSearch 启动..."
until curl -sf http://127.0.0.1:7700/health > /dev/null; do
    sleep 1
done

echo "MeiliSearch 已启动，开始执行数据导入..."
# 建库
python3 data_to_db.py
# 开启服务
python3 web_demo.py