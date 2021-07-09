# Zookeeper

[TOC]

## 1. 单机

### 1.1. 创建并运行容器

```sh
docker run --name zookeeper -dp2181:2181 -p2888:2888 -p3888:3888 -p12080:8080 --restart always zookeeper
```

### 1.2. 端口映射

| 端口 | 说明             |
| :--- | ---------------- |
| 2181 | client port      |
| 2888 | follower port    |
| 3888 | election port    |
| 8080 | AdminServer port |

### 1.3. AdminServer

New in 3.5.0: The AdminServer is an embedded Jetty server that provides an HTTP interface to the four letter word commands. By default, the server is started on port 8080, and commands are issued by going to the URL "/commands/[command name]", e.g., <http://localhost:8080/commands/stat>.

## 2. Swarm

### 2.1. 准备部署文件

```sh
mkdir /usr/local/zookeeper/
vi /usr/local/zookeeper/stack.yml
```

```sh
version: '3.9'

services:
  zoo1:
    image: zookeeper
    restart: always
    hostname: zoo1
    ports:
      - 2181:2181
    environment:
      ZOO_MY_ID: 1
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181

  zoo2:
    image: zookeeper
    restart: always
    hostname: zoo2
    ports:
      - 2182:2181
    environment:
      ZOO_MY_ID: 2
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181

  zoo3:
    image: zookeeper
    restart: always
    hostname: zoo3
    ports:
      - 2183:2181
    environment:
      ZOO_MY_ID: 3
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181
```

### 2.2. 部署

```sh
docker stack deploy -c /usr/local/zookeeper/stack.yml zookeeper
```
