# Debezium

## 前置条件

- Zookeeper
  <https://github.com/nnzbz/notes/blob/master/docker/%E5%B8%B8%E7%94%A8%E9%95%9C%E5%83%8F%E4%B8%8E%E5%AE%B9%E5%99%A8/Zookeeper.md>
- Kafka
  <https://github.com/nnzbz/notes/blob/master/docker/%E5%B8%B8%E7%94%A8%E9%95%9C%E5%83%8F%E4%B8%8E%E5%AE%B9%E5%99%A8/Kafka.md>

## Kafka Connect

### 单机

```sh
docker run -d --name debezium-connect \
    --net bridge \
    -p 10083:8083 \
    -e GROUP_ID=1 \
    -e CONFIG_STORAGE_TOPIC=my_connect_configs \
    -e OFFSET_STORAGE_TOPIC=my_connect_offsets \
    -e STATUS_STORAGE_TOPIC=my_connect_statuses \
    --link zookeeper:zookeeper \
    --link kafka:kafka \
    --link mysql:mysql \
    --restart=always \
    debezium/connect
```

### Swarm

```sh
mkdir /usr/local/debezium
vi /usr/local/debezium/stack.yml
```

```yaml
version: "3.9"
services:
  connect:
    image: 'debezium/connect'
    hostname: debezium-connect
    ports:
      - 10083:8083
    environment:
      # REST服务对外暴露的端口
      - ADVERTISED_PORT=10083
      # REST服务监听网卡的IP地址
      - REST_HOST_NAME=0.0.0.0
      # kafka服务器地址
      - BOOTSTRAP_SERVERS=kafka1:9092,kafka2:9092,kafka3:9092
      # 分组
      - GROUP_ID=debezium-test
      # TOPIC
      - CONFIG_STORAGE_TOPIC=my_connect_configs
      - OFFSET_STORAGE_TOPIC=my_connect_offsets
      - STATUS_STORAGE_TOPIC=my_connect_statuses
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8

networks:
  default:
    external: true
    name: rebue
```

- 部署

```sh
docker stack deploy -c /usr/local/debezium/stack.yml debezium
```

- 监听事件

```sh
docker run -it --rm --name watcher \
      --link zookeeper:zookeeper \
      --link kafka:kafka \
      debezium/kafka:1.6 \
      watch-topic -a -k mytest1.rac.RAC_ACCOUNT
```
