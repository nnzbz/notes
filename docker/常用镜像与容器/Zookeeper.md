# ActiveMQ

[TOC]

## 1. 创建并运行容器

```sh
docker run --name zookeeper -dp2181:2181 -p2888:2888 -p3888:3888 -p12080:8080 --restart always zookeeper
```

## 2. 端口映射

| 端口 | 说明             |
| :--- | ---------------- |
| 2181 | client port      |
| 2888 | follower port    |
| 3888 | election port    |
| 8080 | AdminServer port |

## 3. AdminServer

New in 3.5.0: The AdminServer is an embedded Jetty server that provides an HTTP interface to the four letter word commands. By default, the server is started on port 8080, and commands are issued by going to the URL "/commands/[command name]", e.g., http://localhost:8080/commands/stat.