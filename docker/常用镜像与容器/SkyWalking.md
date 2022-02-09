# SkyWalking

[TOC]

## 1. Swarm

```sh
mkdir /usr/local/skywalking
vi /usr/local/skywalking/stack.yml
```

```yaml{.line-numbers}
version: "3.9"

services:
  oap:
    image: apache/skywalking-oap-server
    hostname: skywalking-oap
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
      - SW_STORAGE=elasticsearch
      - SW_STORAGE_ES_CLUSTER_NODES=es01:9200,es02:9200,es03:9200
      # ElasticSearch启用BASE认证的账户
      - SW_ES_USER=xxxxxxxx
      # ElasticSearch启用BASE认证的账户的密码
      - SW_ES_PASSWORD=xxxxxxxx
    deploy:
      placement:
        constraints:
          - node.labels.role==app

networks:
  default:
    external: true
    name: rebue
```

- 部署

```sh
docker stack deploy -c /usr/local/skywalking/stack.yml skywalking
```

## 2. 浏览

<http://skywalking-ui:8080/>
