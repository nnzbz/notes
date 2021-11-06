# 制作RabbitMQ的Docker容器

[TOC]

## 1. 参考

<https://hub.docker.com/_/rabbitmq>
<https://www.rabbitmq.com/clustering.html>
<https://medium.com/hepsiburadatech/implementing-highly-available-rabbitmq-cluster-on-docker-swarm-using-consul-based-discovery-45c4e7919634>

## 2. 单机

- 创建并运行容器

```sh
docker run -d \
  --name rabbitmq \
  -h rabbitmq \
  --network rebue \
  -e TZ=CST-8 \
  -p5671:5671 -p5672:5672 \
  -p4369:4369 -p25672:25672 \
  -p15671:15671 -p15672:15672 \
  --restart=always \
  rabbitmq:management
```

## 3. Swarm

### 3.1. Docker Compose

```sh
mkdir -p /usr/local/rabbitmq
vi /usr/local/rabbitmq/stack.yml
```

```yml{.line-numbers}
version: "3.9"
services:
  rabbitmq:
    image: rabbitmq:3-management
    hostname: rabbitmq
    ports:
      - 5672:5672
      - 15672:15672
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
```

### 3.2. 部署

```sh
docker stack deploy -c /usr/local/rabbitmq/stack.yml rabbitmq
```

## 4. 访问

容器启动之后就可以访问web 管理端了 <http://127.0.0.1:15672> ，默认创建了一个 guest 用户，密码也是 guest。

- 修改密码
  登录后，点击右上角 `guest`，页面下方找到 `Update this user`，填写 `Password` 并 `confirm`，然后 `Update user`

**注意:** 新版本的guest只允许在localhost本地访问，须注册一个新的账户，这里示例添加 `admin` 账户

```sh
# 进入容器
docker exec -it '容器ID' /bin/sh
# 添加admin账户并授权
rabbitmqctl add_user admin '密码'
rabbitmqctl set_user_tags admin administrator
rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
```
