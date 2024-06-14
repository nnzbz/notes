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
      # 节点ID
      - KAFKA_CFG_NODE_ID=0
      # KRAFT模式设置集群ID
      - KAFKA_KRAFT_CLUSTER_ID=abc
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka1:9093,1@kafka2:9093,2@kafka3:9093
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
  kafka2:
    image: 'bitnami/kafka:latest'
    hostname: kafka2
    environment:
      # 节点ID
      - KAFKA_CFG_NODE_ID=1
      # KRAFT模式设置集群ID
      - KAFKA_KRAFT_CLUSTER_ID=abc
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka1:9093,1@kafka2:9093,2@kafka3:9093
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
  kafka3:
    image: 'bitnami/kafka:latest'
    hostname: kafka3
    environment:
      # 节点ID
      - KAFKA_CFG_NODE_ID=2
      # KRAFT模式设置集群ID
      - KAFKA_KRAFT_CLUSTER_ID=abc
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka1:9093,1@kafka2:9093,2@kafka3:9093
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER

networks:
  default:
    external: true
    name: rebue
```

- 部署

```sh
docker stack deploy -c /usr/local/kafka/stack.yml kafka
```
