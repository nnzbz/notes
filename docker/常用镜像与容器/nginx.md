# 在Docker中使用nginx

[TOC]

## 1. 创建目录

```sh
mkdir ~/nginx
mkdir ~/nginx/mynginx
mkdir ~/nginx/mynginx/conf
mkdir ~/nginx/mynginx/logs
```

## 2. 创建配置文件nginx.conf

```sh
vi ~/nginx/mynginx/conf/nginx.conf
```

```text
user  nginx;
worker_processes 1;

error_log  /var/log/nginx/error.log warn;
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

## 3. 创建并运行容器

```sh
docker run -p80:80 --name mynginx -v ~/nginx/mynginx/html:/usr/share/nginx/html:ro -v ~/nginx/mynginx/conf/nginx.conf:/etc/nginx/nginx.conf:ro -v ~/nginx/mynginx/logs:/var/log/nginx -d nginx
```

- p
  如果要建立自定义的端口号，请修改“:”前面的80
- :ro
  在容器内只读
