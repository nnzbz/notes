# 在Docker中使用nginx

[TOC]

## 1. 准备nginx的配置文件

```sh
mkdir /usr/local/nginx
vi /usr/local/nginx/nginx.conf
```

内容如下(从容器中/etc/nginx/nginx.conf复制出来):

```js
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
```

## 2. 单机

### 2.1. 创建目录

```sh
mkdir -p /usr/local/nginx/conf
mkdir -p /usr/local/nginx/logs
```

### 2.2. 创建并运行容器

```sh
docker run -p80:80 --name nginx -v /usr/local/nginx/html:/usr/share/nginx/html:ro -v /usr/local/nginx/conf/nginx.conf:/etc/nginx/nginx.conf:ro -v /usr/local/nginx/logs:/var/log/nginx -d nginx
```

- p
  如果要建立自定义的端口号，请修改“:”前面的80
- :ro
  在容器内只读

## 3. Swarm

### 3.1. 创建docker config

```sh
docker config create nginx-proxy.conf /usr/local/nginx/proxy.conf
```

### 3.2. 命令行方式

```sh
docker service create \
    --name nginx \
    --replicas 3 \
    -p 80:80 \
    --config source=nginx-proxy.conf,target=/etc/nginx/conf.d/proxy.conf \
    nginx
```

- `-p`
  如果要建立自定义的端口号，请修改 `:` 前面的80

### 3.3. Docker Compose 方式

- yaml

```sh
vi /usr/local/nginx/stack.yml
```

如果要建立自定义的端口号，请修改 `ports` 部分 `:` 前面的80

```yaml
version: "3.9"
services:
  nginx:
    image: nginx
    ports:
      - 80:80
    deploy:
      replicas: 3
    configs:
      - source: nginx-proxy.conf
        target: /etc/nginx/conf.d/proxy.conf
configs:
  nginx-proxy.conf:
    file: /usr/local/nginx/proxy.conf
```

- 部署

```sh
docker stack deploy -c /usr/local/zookeeper/stack.yml zookeeper
```
