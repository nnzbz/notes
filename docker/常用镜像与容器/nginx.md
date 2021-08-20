# 在Docker中使用nginx

[TOC]

## 1. 单机

### 1.1. 创建目录

```sh
mkdir -p /usr/local/nginx/{html,conf,logs}
```

### 1.2. 创建并运行容器

```sh
docker run -p80:80 --name nginx -v /usr/local/nginx/html:/usr/share/nginx/html:ro -v /usr/local/nginx/conf:/etc/nginx/nginx.conf:ro -v /usr/local/nginx/logs:/var/log/nginx -d nginx
```

- p
  如果要建立自定义的端口号，请修改“:”前面的80
- :ro
  在容器内只读

## 2. Swarm

### 2.1. 准备配置文件的目录

```sh
mkdir -p /usr/local/nginx/{html,conf,cert}
# 在此目录下放入配置文件，配置文件参考最后一节
```

### 2.2. Docker Compose

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
      - 443:443
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      # 配置文件目录
      - /usr/local/nginx/conf/:/etc/nginx/conf.d/
      # 数字证书目录
      # - /usr/local/nginx/cert/:/etc/nginx/cert/
      # 网页存放目录
      - /usr/local/nginx/html:/usr/share/nginx/html
    deploy:
      replicas: 3
```

- 部署

```sh
docker stack deploy -c /usr/local/nginx/stack.yml nginx
```

## 3. 参考nginx的配置

```sh
vi /usr/local/nginx/conf/default.conf
```

```ini
upstream gateway {
    server gateway-server:80;
    keepalive 2000;
}

server {
    listen       80;
    listen  [::]:80;
    listen       443 ssl;
    server_name 域名;

    # 注意文件位置，是从/etc/nginx/下开始算起的
    ssl_certificate cert/**.*.pem;
    ssl_certificate_key cert/**.*.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;

    location /admin-web/ {
        root /usr/share/nginx/html/;
    }
    location / {
        proxy_pass http://gateway/;
    }
}
```
