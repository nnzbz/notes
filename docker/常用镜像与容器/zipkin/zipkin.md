# zipkin

[TOC]

## 1. 单机

- Zipkin

```sh
docker run --name zipkin --restart=always -dp 9411:9411 openzipkin/zipkin
```

- Zipkin Slim

只支持in-memory与Elasticsearch的精简版

```sh
docker run -dp 9411:9411 --name zipkin --restart=always openzipkin/zipkin-slim
```

## 2. Swarm 部署

1. Docker Compose

```sh
mkdir -p /usr/local/zipkin
vi /usr/local/zipkin/stack.yml
```

```yml{.line-numbers}
version: "3.9"
services:
  zipkin:
    image: openzipkin/zipkin
    hostname: zipkin
    ports:
      - 9411:9411
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    logging:
      options:
        max-size: 50m
networks:
  default:
    external: true
    name: rebue
```

2. 部署

```sh
docker stack deploy -c /usr/local/zipkin/stack.yml zipkin
```

## 3. 浏览

<http://127.0.0.1:9411/zipkin>
