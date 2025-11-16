# nginx反向代理

[TOC]

## 1. 常见的反向代理配置

```js
# 负载均衡
upstream my_server {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
}
server {
    # 公网暴露的端口变量
    set $expose_port xxxx;

    # 监听的端口
    listen       80;
    listen       [::]:80; # 支持ipv6
    listen       443 ssl;
    listen       [::]:443 ssl; # 支持ipv6
    # 限制host只能是下面的内容
    server_name  xxx.xxx.xxx.xxx www.abc.com;
    # 限制body的大小
    client_max_body_size 1024M;

    # HTTPS设置，注意文件位置，相对路径是从/etc/nginx/下开始算起的
    ssl_certificate cert/xxxxx.pem;
    ssl_certificate_key cert/xxxxx.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;

    # 处理 http(s)://xxx.xxx.xxx.xxx:80(443)/my 的请求
    location /my/ {
        proxy_pass http://my_server/;
        # 如果nginx前面没有代理，可以使用X-Real-IP获取用户IP
        proxy_set_header X-Real-IP       $remote_addr;
        # 如果 nginx 前面有代理，请使用X-Forwarded-For获取用户IP，因为它是被广泛支持的头部
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host:$expose_port;
#        # 下面这段部分解决一些web网站把路径写成绝对路径，无法代理的情况
#        sub_filter_types *; # 默认是text/html
#        sub_filter_once off;
#        sub_filter 'href="/' 'href="/my/';
#        sub_filter 'src="/' 'src="/my/';
    }
}
```

- 在http节点下，upstream配置服务地址，server的location配置代理映射
- expose_port 因为nginx如果安装在docker容器内部的话，只知道自己内部端口
- proxy_pass
  - 如果末尾有 `/`，请求会被转发到 `my_server` 的服务地址 <http://10.0.0.2:8080/>
  - 如果末尾没有 `/`，则请求会转发到 `my_server` 的 <http://10.0.0.2:8080/my>
