from meilisearch import Client


def search(index_name, query_str, top_k):
    # MeiliSearch 配置
    ms_host = "http://127.0.0.1:7700"
    ms_master_key = "MASTER_KEY"
    client = Client(ms_host, ms_master_key)
    index = client.index(index_name)
    results = index.search(query_str, {"limit": top_k})
    docs = [hit["content"] for hit in results["hits"]]
    return docs


if __name__ == "__main__":
    index_name = "fatiao"
    query_str = "网络安全法"
    top_k = 10
    docs = search(index_name, query_str, top_k)
    print(docs)
