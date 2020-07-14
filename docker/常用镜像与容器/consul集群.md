# 在docker中搭建consul集群

[TOC]

## 1. 创建并运行容器

### 1.1. 格式

```sh
docker run -d --net=host -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' consul agent -server -bind=<external ip> -retry-join=<root agent ip> -bootstrap-expect=<number of server agents>
```

部分参数说明

- –net=host
 使得docker容器越过了net namespace的隔离，免去手动指定端口映射的步骤
- -server
 consul支持以server或client的模式运行, server是服务发现模块的核心, client主要用于转发请求
- -advertise
 将本机私有IP传递到consul
- -bootstrap-expect
 指定consul将等待几个节点连通，成为一个完整的集群
- -retry-join
 指定要加入的consul节点地址，失败会重试, 可多次指定不同的地址

### 1.2. sample

```sh
# leader
docker run -d --net=host -e 'CONSUL_LOCAL_CONFIG={"skip_leave_on_interrupt": true}' consul agent -server -bind=192.168.1.201 -node=server1 -bootstrap-expect 1 -client 0.0.0.0 -ui
# node
docker run -d --net=host consul agent -bind=192.168.1.202 -node=client1 -retry-join=192.168.1.201
```