# ActiveMQ

[TOC]

## 1. 拉取镜像

```sh
docker pull rmohr/activemq
```

## 2. 创建并运行容器

```sh
docker run --name activemq -dp 61616:61616 -p 8161:8161 --restart always rmohr/activemq
```

## 端口映射

| 端口  | 说明                                  |
| :---- | ------------------------------------- |
| 61616 | JMS                                   |
| 8161  | UI                                    |
| 5672  | AMQP  (since `rmohr/activemq:5.12.1`) |
| 61613 | STOMP (since `rmohr/activemq:5.12.1`) |
| 1883  | MQTT  (since `rmohr/activemq:5.12.1`) |
| 61614 | WS    (since `rmohr/activemq:5.12.1`) |
