# Kafka

[TOC]

## 1. 前置条件

- zookeeper
  <https://github.com/nnzbz/notes/blob/master/docker/%E5%B8%B8%E7%94%A8%E9%95%9C%E5%83%8F%E4%B8%8E%E5%AE%B9%E5%99%A8/Zookeeper.md>

## 2. 单机

```sh
docker run -d --name kafka \
    --net host \
    -e KAFKA_BROKER_ID=1 \
    -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092 \
    -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://127.0.0.1:9092 \
    -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181 \
    -e ALLOW_PLAINTEXT_LISTENER=yes \
    --restart=always \
    docker.io/bitnami/kafka:2
```

- Web UI

```sh
docker run -d --name kafka-manager \
     -p 10090:9000  \
     -e ZK_HOSTS="zookeeper:2181" \
     --restart=always \
     hlebalbau/kafka-manager
```

- 注意
  zookeeper改为本机zookeeper相应的地址，如果是容器内访问宿主机，Mac系统为 `docker.for.mac.host.internal`，Linux为 `172.17.0.1`

## 3. Swarm

```sh
mkdir /usr/local/kafka
vi /usr/local/kafka/stack.yml
```

```yaml
version: "3.9"
services:
  kafka1:
    image: 'bitnami/kafka:latest'
    hostname: kafka1
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2181,zoo3:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
    volumes:
      - kafkadata1:/bitnami/kafka
  kafka2:
    image: 'bitnami/kafka:latest'
    hostname: kafka2
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2181,zoo3:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
    volumes:
      - kafkadata2:/bitnami/kafka
  kafka3:
    image: 'bitnami/kafka:latest'
    hostname: kafka3
    environment:
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zoo1:2181,zoo2:2181,zoo3:2181
      - ALLOW_PLAINTEXT_LISTENER=yes
    volumes:
      - kafkadata3:/bitnami/kafka

volumes:
  kafkadata1:
  kafkadata2:
  kafkadata3:

networks:
  default:
    external: true
    name: rebue
```

- 部署

```sh
docker stack deploy -c /usr/local/kafka/stack.yml kafka
```
