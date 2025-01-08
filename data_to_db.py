# -*- coding: utf-8 -*-
import csv

from meilisearch import Client
from tqdm import trange

# MeiliSearch 配置
ms_host = "http://127.0.0.1:7700"
ms_master_key = "MASTER_KEY"
client = Client(ms_host, ms_master_key)

# 文件路径与索引名
file_fatiao = "src/data_task1.csv"
index_fatiao = "fatiao"

file_anli = "src/data_task2.csv"
index_anli = "anli"


def load_data(file_path):
    """加载 CSV 数据"""
    data = []
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            if len(row) > 0:
                content = ""
                for i in range(len(headers)):
                    content += row[i]
                data.append({"id": len(data), "content": content})
    return data


def build_index(index_name, data):
    """检查索引是否存在，若不存在则创建并导入数据"""
    try:
        r = client.get_index(index_name)
        if r:
            print(f"索引 {index_name} 已存在，跳过创建和导入。")
            return
    except:
        print(f"索引 {index_name} 不存在，准备导入。")
    print(f"导入数据到索引: {index_name}")
    # 创建索引并配置
    index = client.index(index_name)
    index.update_settings(
        {"searchableAttributes": ["content"], "filterableAttributes": ["id"]}
    )

    # 批量插入数据
    data_size_one_time = 1000
    for begin_index in trange(0, len(data), data_size_one_time):
        batch = data[begin_index : min(len(data), begin_index + data_size_one_time)]
        index.add_documents(batch)


if __name__ == "__main__":
    # 任务1数据导入

    data_task1 = load_data(file_fatiao)
    build_index(index_fatiao, data_task1)

    # 任务2数据导入
    data_task2 = load_data(file_anli)
    build_index(index_anli, data_task2)

    print("所有数据导入完成！")
