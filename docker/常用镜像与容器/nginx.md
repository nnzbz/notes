# 在Docker中使用nginx

[TOC]

## 1. 单机

### 1.1. 创建目录

```sh
mkdir -p /usr/local/nginx/{html,conf,logs}
```

### 1.2. 创建并运行容器

```yaml{.line-numbers}
version: "3.9"
services:
  nginx:
    image: nginx
    container_name: nginx
    ports:
      - 80:80
      # - 443:443
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      # 配置文件，在 1.27.0 版本中不能 mount 成功，只能采用手动复制的方式
      #- /usr/local/nginx/conf:/etc/nginx/conf.d:z
      # 日志目录
      - /usr/local/nginx/logs:/var/log/nginx:z
      # 网页存放目录，在 1.27.0 版本中不能 mount 成功，只能采用手动复制的方式
      #- /usr/local/nginx/html:/usr/share/nginx/html:z
    restart: always
```

- p: 如果要建立自定义的端口号，请修改“:”前面的80
- 手动复制文件到容器中

  ```sh
  docker cp /usr/local/nginx/conf/default.conf nginx:/etc/nginx/conf.d/
  docker cp /usr/local/nginx/html/ nginx:/usr/share/nginx/
  ```

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

```yaml{.line-numbers}
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
      - /usr/local/nginx/conf/:/etc/nginx/conf.d/:z
      # 数字证书目录
      - /usr/local/nginx/cert/:/etc/nginx/cert/:z
      # 网页存放目录
      - /usr/local/nginx/html:/usr/share/nginx/html:z
    deploy:
      replicas: 1

networks:
  default:
    external: true
    name: rebue
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
# 负载均衡
upstream nacos {
    server nacos1:8848;
    server nacos2:8848;
    server nacos3:8848;
}

# 如果未通过指定的IP或域名访问，返回403
server {
    listen 80 default;
    server_name _;
    return 403;
}

server {
    listen       80;
    listen  [::]:80;
    listen       443 ssl;
    listen  [::]:443;
    server_name 域名1 域名2 域名3;

    # 数字证书
    # 注意文件位置，是从/etc/nginx/下开始算起的
    # 注意文件名不要用通配符，要将具体数字证书的名字写下来
    ssl_certificate cert/**.*.pem;
    ssl_certificate_key cert/**.*.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;

    # 对于只支持HTTP协议里的GET和POST请求，不支持PUT/DELETE请求的
    # 所有的PUT请求，要携带Header：X-HTTP-Method-Override: PUT　　
    # 所有的DELETE请求，要携带Header：X-HTTP-Method-Override: DELETE
    # 可以在nginx层修改和转发
    set $method $request_method;
    if ($http_X_HTTP_Method_Override ~* 'PUT|DELETE') {
        set $method $http_X_HTTP_Method_Override;
    }
    proxy_method $method;

    # http://xxx.xxx.xxx.xxx:xxxx/rabbitmq/ (不能省略后面的“/”)
    location /rabbitmq/ {
        proxy_pass http://rabbitmq:15672/;
    }

    # http://xxx.xxx.xxx.xxx:xxxx/phpmyadmin/ (不能省略后面的“/”)
    # 注意还要在phpMyAdmin的部署文档上配置PMA_ABSOLUTE_URI参数
    location /phpmyadmin/ {
        proxy_pass http://phpmyadmin/;
    }

    # http://xxx.xxx.xxx.xxx:xxxx/alibaba-sentinel-dashboard/ (不能省略后面的“/”)
    location /alibaba-sentinel-dashboard/ {
        proxy_pass http://alibaba-sentinel-dashboard:8080/;
    }

    # http://xxx.xxx.xxx.xxx:xxxx/zipkin/ (不能省略后面的“/”)
    location /zipkin/ {
        # 注意后面不能带有“/”
        proxy_pass http://zipkin:9411;
    }

    # http://xxx.xxx.xxx.xxx:xxxx/nacos/ (不能省略后面的“/”)
    location /nacos/ {
        # 注意后面不能带有“/”
        proxy_pass http://nacos;
    }

    # http://xxx.xxx.xxx.xxx:xxxx/minio/ (不能省略后面的“/”)
    location /minio/ {
        proxy_pass http://minio:9001/;
        sub_filter '"/login"'         '"/minio/login"';
        sub_filter 'href="/'          'href="/minio/';
        # 匹配任意文件，默认只是 text/html
        sub_filter_types *;
        # 可反复匹配替换
        sub_filter_once off;
        # sub_filter无法处理压缩内容，可以使用如下语句禁用压缩
        proxy_set_header Accept-Encoding '';
    }

    location /admin-web {
        root /usr/share/nginx/html;
        index           index.html;
        try_files       $uri $uri/ /admin-web/index.html;
    }

    location = / {
       rewrite ^/(.*) admin-web/platform-admin-web/ redirect;
    }

}
```

- 注意
  - 很常见的一个问题就是 `sub_filter` 无效。因为浏览器都是允许压缩的，所以请求头都是带 `Accept-Encoding: gzip` 的。而 `Nginx` 的 `sub_filter` 无法处理压缩过的请求， `Nginx` 自身也不会解压。事实上，要想写一个解压的插件也是不可能的，因为 Nginx 目前并没有 `input filtering` 相关的接口。一般网上的解决办法都是 `proxy_set_header Accept-Encoding “”;`禁用上游的压缩，对客户端的压缩不受影响。
