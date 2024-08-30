# 离线安装docker compose

[TOC]

## 1. 查找下载的包

<https://github.com/docker/compose/releases>

- 如果是下载linux的x86_64，链接地址如下

<https://github.com/docker/compose/releases/download/v2.6.1/docker compose-linux-x86_64>

## 2. 直接在服务器下载并安装

```sh
wget https://github.com/docker/compose/releases/download/v2.6.1/docker compose-linux-x86_64
# 改名
mv docker compose-linux-x86_64 docker compose
# 移动到系统路径
mv docker compose /usr/local/bin/
# 可执行
chmod +x /usr/local/bin/docker compose
```
