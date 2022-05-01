# Kafka

[TOC]

## 1. 前置条件

- zookeeper
  <https://github.com/nnzbz/notes/blob/master/docker/%E5%B8%B8%E7%94%A8%E9%95%9C%E5%83%8F%E4%B8%8E%E5%AE%B9%E5%99%A8/Zookeeper.md>

## 2. 单机

```sh
docker run -d --name kafka \
    -p 9092:9092 \
    -p 1099:1099 \
    -e JMX_PORT=1099 \
    -e KAFKA_BROKER_ID=1 \
    -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092 \
    -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://172.17.0.1:9092 \
    -e KAFKA_CFG_ZOOKEEPER_CONNECT=172.17.0.1:2181 \
    -e ALLOW_PLAINTEXT_LISTENER=yes \
    -e TZ=CST-8 \
    --restart=always \
    bitnami/kafka:latest
```

- `-e JMX_PORT=1099` 为开启JMX的端口(efak监控需要开启)
- 监控
  <https://github.com/DockerfileX/efak>

## 3. Swarm

```sh
mkdir /usr/local/kafka
vi /usr/local/kafka/stack.yml
```

```yaml{.line-numbers}
version: "3.9"
services:
  kafka1:
    image: 'bitnami/kafka:latest'
    hostname: kafka1
    environment:
      # 为开启JMX的端口(efak监控需要开启)
      - JMX_PORT=1099
      # 默认为-Xmx1024m -Xms1024m
      - KAFKA_HEAP_OPTS=-Xmx256m -Xms256m
      # 给客户端访问的地址
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka1:9092
      # ZooKeeper的连接地址
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2181,zoo3:2181
      # 允许监听器所用明文，只在开发环境中推荐
      - ALLOW_PLAINTEXT_LISTENER=yes
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      - kafka1data:/bitnami/kafka
  kafka2:
    image: 'bitnami/kafka:latest'
    hostname: kafka2
    environment:
      # 为开启JMX的端口(efak监控需要开启)
      - JMX_PORT=1099
      # 默认为-Xmx1024m -Xms1024m
      - KAFKA_HEAP_OPTS=-Xmx256m -Xms256m
      # 给客户端访问的地址
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka2:9092
      # ZooKeeper的连接地址
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2181,zoo3:2181
      # 允许监听器所用明文，只在开发环境中推荐
      - ALLOW_PLAINTEXT_LISTENER=yes
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      - kafka2data:/bitnami/kafka
  kafka3:
    image: 'bitnami/kafka:latest'
    hostname: kafka3
    environment:
      # 为开启JMX的端口(efak监控需要开启)
      - JMX_PORT=1099
      # 默认为-Xmx1024m -Xms1024m
      - KAFKA_HEAP_OPTS=-Xmx256m -Xms256m
      # 给客户端访问的地址
      - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka3:9092
      # ZooKeeper的连接地址
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2181,zoo3:2181
      # 允许监听器所用明文，只在开发环境中推荐
      - ALLOW_PLAINTEXT_LISTENER=yes
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      - kafka3data:/bitnami/kafka
  efak:
    image: nnzbz/efak
    hostname: efak
    ports:
      - 1048:8048
    environment:
      # ZooKeeper的连接地址
      - ZK_HOSTS=zoo1:2181,zoo2:2181,zoo3:2181
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8

volumes:
  kafka1data:
  kafka2data:
  kafka3data:

networks:
  default:
    external: true
    name: rebue
```

- 部署

```sh
docker stack deploy -c /usr/local/kafka/stack.yml kafka
```
