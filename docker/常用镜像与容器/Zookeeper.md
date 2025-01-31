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
    --restart always zookeeper:3.9
```

- `-e ZOO_4LW_COMMANDS_WHITELIST=*`
  开放监控客户端的白名单(EFAK监控需要打开)

### 1.2. 端口映射

| 端口 | 说明             |
| :--- | ---------------- |
| 2181 | client port      |
| 2888 | follower port    |
| 3888 | election port    |


## 2. Swarm 单机

### 2.1. 准备部署文件

```sh
mkdir ~/opt/zookeeper/
vi ~/opt/zookeeper/stack.yml
```

```sh{.line-numbers}
services:
  zoo:
    image: zookeeper:3.9
    hostname: zoo
    #ports:
    #  - 2181:2181
    environment:
      # 嵌入的Admin服务器，默认为true
      - ZOO_ADMINSERVER_ENABLED=false
      # 开放监控客户端的白名单(EFAK监控需要打开)
      - ZOO_4LW_COMMANDS_WHITELIST=*
      - TZ=CST-8
    volumes:
      - zoodata:/data:z
      - zoodatalog:/datalog:z
    deploy:
      endpoint_mode: dnsrr
      placement:
        constraints:
          - node.labels.role==zookeeper
    logging:
      options:
        max-size: 8m

volumes:
  zoodata:
  zoodatalog:

networks:
  default:
    external: true
    name: rebue
```

### 2.2. 部署

```sh
docker stack deploy -c ~/opt/zookeeper/stack.yml zookeeper
```

## 3. Swarm集群

### 3.1. 准备部署文件

```sh
mkdir ~/opt/zookeeper/
vi ~/opt/zookeeper/stack.yml
```

```yml{.line-numbers}
version: '3.9'

services:
  zoo1:
    image: zookeeper:3.9
    # hostname: zoo1
    #ports:
    #  - 2181:2181
    environment:
      - ZOO_MY_ID=1
      - ZOO_SERVERS=server.1=zookeeper_zoo1:2888:3888;2181 server.2=zookeeper_zoo2:2888:3888;2181 server.3=zookeeper_zoo3:2888:3888;2181
      # 嵌入的Admin服务器，默认为true
      - ZOO_ADMINSERVER_ENABLED=false
      # 开放监控客户端的白名单(EFAK监控需要打开)
      - ZOO_4LW_COMMANDS_WHITELIST=*
      - TZ=CST-8
    # volumes:
    #   - zoo1data:/data:z
    #   - zoo1datalog:/datalog:z
    logging:
      options:
        max-size: 8m
    deploy:
      endpoint_mode: dnsrr
  zoo2:
    image: zookeeper:3.9
    # hostname: zoo2
    #ports:
    #  - 2182:2181
    environment:
      - ZOO_MY_ID=2
      - ZOO_SERVERS=server.1=zookeeper_zoo1:2888:3888;2181 server.2=zookeeper_zoo2:2888:3888;2181 server.3=zookeeper_zoo3:2888:3888;2181
      # 嵌入的Admin服务器，默认为true
      - ZOO_ADMINSERVER_ENABLED=false
      # 开放监控客户端的白名单(EFAK监控需要打开)
      - ZOO_4LW_COMMANDS_WHITELIST=*
      - TZ=CST-8
    # volumes:
    #   - zoo2data:/data:z
    #   - zoo2datalog:/datalog:z
    logging:
      options:
        max-size: 8m
    deploy:
      endpoint_mode: dnsrr
  zoo3:
    image: zookeeper:3.9
    # hostname: zoo3
    #ports:
    #  - 2183:2181
    environment:
      - ZOO_MY_ID=3
      - ZOO_SERVERS=server.1=zookeeper_zoo1:2888:3888;2181 server.2=zookeeper_zoo2:2888:3888;2181 server.3=zookeeper_zoo3:2888:3888;2181
      # 嵌入的Admin服务器，默认为true
      - ZOO_ADMINSERVER_ENABLED=false
      # 开放监控客户端的白名单(EFAK监控需要打开)
      - ZOO_4LW_COMMANDS_WHITELIST=*
      - TZ=CST-8
    # volumes:
    #   - zoo3data:/data:z
    #   - zoo3datalog:/datalog:z
    logging:
      options:
        max-size: 8m
    deploy:
      endpoint_mode: dnsrr

# volumes:
#   zoo1data:
#   zoo1datalog:
#   zoo2data:
#   zoo2datalog:
#   zoo3data:
#   zoo3datalog:

networks:
  default:
    external: true
    name: rebue
```

### 3.2. 部署

```sh
docker stack deploy -c ~/opt/zookeeper/stack.yml zookeeper
```

## 4. Zoo Navigator

```sh
mkdir -p ~/opt/zookeeper/navigator/
vi ~/opt/zookeeper/navigator/stack.yml
```

```yml{.line-numbers}
version: '3.9'

services:
  navigator:
    image: elkozmon/zoonavigator:1.1.2
    ports:
     - 12080:12080
    environment:
      - HTTP_PORT=12080
    logging:
      options:
        max-size: 8m
    deploy:
      endpoint_mode: dnsrr

networks:
  default:
    external: true
    name: rebue
```

```sh
docker stack deploy -c ~/opt/zookeeper/navigator/stack.yml zookeeper
```

## 5. ~~Web UI~~

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
