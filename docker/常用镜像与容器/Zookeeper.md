# Zookeeper

[TOC]

## 1. 单机

### 1.1. 创建并运行容器

```sh
docker run --name zoo \
    --network rebue \
    -h zoo \
    -dp2181:2181 -p2888:2888 -p3888:3888 \
    -e ZOO_ADMINSERVER_ENABLED=false \
    -e ZOO_4LW_COMMANDS_WHITELIST=* \
    --restart always zookeeper
```

- `-e ZOO_4LW_COMMANDS_WHITELIST=*`
  开放监控客户端的白名单(EFAK监控需要打开)

### 1.2. 端口映射

| 端口 | 说明             |
| :--- | ---------------- |
| 2181 | client port      |
| 2888 | follower port    |
| 3888 | election port    |

## 2. Swarm

### 2.1. 准备部署文件

```sh
mkdir /usr/local/zookeeper/
vi /usr/local/zookeeper/stack.yml
```

```sh{.line-numbers}
version: '3.9'

services:
  zoo1:
    image: zookeeper
    hostname: zoo1
    #ports:
    #  - 2181:2181
    environment:
      - ZOO_MY_ID=1
      - ZOO_SERVERS=server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181
      # 嵌入的Admin服务器，默认为true
      - ZOO_ADMINSERVER_ENABLED=false
      # 开放监控客户端的白名单(EFAK监控需要打开)
      - ZOO_4LW_COMMANDS_WHITELIST=*
      - TZ=CST-8
    volumes:
      - zoo1data:/data
      - zoo1datalog:/datalog
  zoo2:
    image: zookeeper
    hostname: zoo2
    #ports:
    #  - 2182:2181
    environment:
      - ZOO_MY_ID=2
      - ZOO_SERVERS=server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181
      # 嵌入的Admin服务器，默认为true
      - ZOO_ADMINSERVER_ENABLED=false
      # 开放监控客户端的白名单(EFAK监控需要打开)
      - ZOO_4LW_COMMANDS_WHITELIST=*
      - TZ=CST-8
    volumes:
      - zoo2data:/data
      - zoo2datalog:/datalog
  zoo3:
    image: zookeeper
    hostname: zoo3
    #ports:
    #  - 2183:2181
    environment:
      - ZOO_MY_ID=3
      - ZOO_SERVERS=server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181
      # 嵌入的Admin服务器，默认为true
      - ZOO_ADMINSERVER_ENABLED=false
      # 开放监控客户端的白名单(EFAK监控需要打开)
      - ZOO_4LW_COMMANDS_WHITELIST=*
      - TZ=CST-8
    volumes:
      - zoo3data:/data
      - zoo3datalog:/datalog
  # web-ui:
  #   image: tobilg/zookeeper-webui
  #   environment:
  #     ZK_DEFAULT_NODE: zoo1:2181/,zoo2:2181,zoo3:2181
  #     TZ: CST-8

volumes:
  zoo1data:
  zoo1datalog:
  zoo2data:
  zoo2datalog:
  zoo3data:
  zoo3datalog:

networks:
  default:
    external: true
    name: rebue
```

### 2.2. 部署

```sh
docker stack deploy -c /usr/local/zookeeper/stack.yml zookeeper
```

## 3. Web UI

- 开发环境

```sh
docker run -dp 12080:12080 \
    -e HTTP_PORT=12080 \
    -e ZK_DEFAULT_NODE=172.17.0.1:2181 \
    -e USER=admin \
    -e PASSWORD=xxxxxxxx \
    --name zk-web \
    tobilg/zookeeper-webui
```

- Swarm环境

```sh
docker run --rm -t --network rebue \
    -p 12080:8080 \
    -e ZK_DEFAULT_NODE=zoo1:2181/,zoo2:2181/,zoo3:2181/ \
    -e USER=admin \
    -e PASSWORD=xxxxxxxx \
    --name zk-web \
    tobilg/zookeeper-webui
```

- ZK_DEFAULT_NODE
  连接ZooKeeper的地址
- HTTP_PORT
  Web网站监听的端口号，默认为8080
- USER
  登录Web网站的用户名
- PASSWORD
  登录Web网站的密码
