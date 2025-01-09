![GitHub clones](https://img.shields.io/badge/dynamic/json?label=Clones&query=$.count&url=https://api.github.com/repos/coloraven/fuzi.mingcha/traffic/clones&color=blue)

## 本项目在源项目基础上优化之处
1. 添加了多卡运行的支持
2. 全文检索由`es`或`PyLucene`改为`meilisearch`极大减少内存占用、极大简化部署流程
3. 支持`WEB`服务，在保留`cli_demo.py`主体逻辑的基础上，由`cli`方式改为`web`方式
4. 增加容错检索容错机制（官方`cli_demo.py`检索法条或案例时，如果检索不到会直接报错退出）
5. 增加数据快速、强制更新
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
    -e FORCEUPDATE=1 \ # [可选]每次重启容器会强制更新数据
    -p 7860:7860 \
    -v /fuzi.mingcha/src:/fuzi-mingcha/src \ # [可选]用于存放自定义法条、案例数据
    -v /fuzi.mingcha/SDUIRLab/fuzi-mingcha-v1_0:/fuzi-mingcha/SDUIRLab/fuzi-mingcha-v1_0 \
    fuzimingcha:latest
```
### 原版部署方案
[原版README](https://github.com/irlab-sdu/fuzi.mingcha/blob/main/README.md)
[原版部署方案](https://github.com/irlab-sdu/fuzi.mingcha/tree/main/src)
## FAQ
容器内使用`GPU`需要按照`nvidia-container-toolkit`，具体参考[https://blog.csdn.net/qq_40938444/article/details/144763695](https://blog.csdn.net/qq_40938444/article/details/144763695)




