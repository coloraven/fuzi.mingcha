## 本项目在源项目基础上优化之处
1. 添加了多卡运行的支持
2. 极大简化部署流程
3. 全文检索由`es`改为`meilisearch`，极大减少内存占用
4. 全文检索由`PyLucene`改为`meilisearch`，极大简化部署流程
5. 由`cli`方式改为`web`方式，方便使用。
## 部署
### 克隆本项目
```bash
git clone --depth 1 https://gh-proxy.com/github.com/coloraven/fuzi.mingcha /fuzi.mingcha
cd /fuzi.mingcha
```
### 下载大模型
自行准备好，或者使用下面推荐的方式下载
```bash
pip install modelscope
modelscope download --model furyton/fuzi-mingcha-v1_0 --local_dir /fuzi.mingcha/SDUIRLab/fuzi-mingcha-v1_0
```
### 构建镜像

```bash
docker build -t fuzimingcha:latest .
```
### 运行
```bash
docker run -itd --name fuzimingcha \
    --gpus all \
    -p 7860:7860 \
    -v /fuzi.mingcha/SDUIRLab/fuzi-mingcha-v1_0:/fuzi-mingcha/SDUIRLab/fuzi-mingcha-v1_0 \
    fuzimingcha:latest
```
### FAQ
容器内使用`GPU`需要按照`nvidia-container-toolkit`，具体参考[https://blog.csdn.net/qq_40938444/article/details/144763695](https://blog.csdn.net/qq_40938444/article/details/144763695)




