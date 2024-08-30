# Kafka

[TOC]

## 1. 单机

```sh
mkdir -p ~/opt/kafka
vi ~/opt/kafka/stack.yml
```

```yaml{.line-numbers}
services:
  kafka:
    image: bitnami/kafka:3.8
    hostname: kafka
    container_name: kafka
    ports:
      - 9092:9092
    environment:
      - KAFKA_CFG_NODE_ID=0
      - KAFKA_CFG_PROCESS_ROLES=controller,broker
      - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
      - KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka:9093
      - KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
    restart: always
```

```sh
docker compose -f ~/opt/kafka/stack.yml up -d
```

## 2. Swarm

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
