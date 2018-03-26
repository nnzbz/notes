# 制作RabbitMQ的Docker容器

[TOC]

## 创建并运行容器

```sh
docker run -d --name rabbitmq -p5671:5671 -p5672:5672 -p4369:4369 -p25672:25672 -p15671:15671 -p15672:15672 --restart=always rabbitmq:management
```

## 使用

容器启动之后就可以访问web 管理端了 http://127.0.0.1:15672 ，默认创建了一个 guest 用户，密码也是 guest。