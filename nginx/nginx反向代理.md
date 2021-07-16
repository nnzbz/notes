# nginx反向代理

[TOC]

## 1. 常见的反向代理配置

```js
upstream my_server {                                                         
    server xxxxx:8080;                                                
    keepalive 2000;
}
server {
    # 公网暴露的端口变量
    set $expose_port xxxx;

    # 监听的端口
    listen       80;                                                         
    listen       443 ssl;
    server_name  127.0.0.1;
    client_max_body_size 1024M;

    # HTTPS设置，注意文件位置，相对路径是从/etc/nginx/下开始算起的
    ssl_certificate cert/xxxxx.pem;
    ssl_certificate_key cert/xxxxx.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;

    location /my/ {
        proxy_pass http://my_server/;
        proxy_set_header Host $host:$expose_port;
        # 下面这段部分解决一些web网站把路径写成绝对路径，无法代理的情况
        sub_filter 'href="/' 'href="/my/';
        sub_filter 'src="/' 'src="/my/';
        sub_filter_types text/html;
        sub_filter_once off;
    }
}
```

- 在http节点下，upstream配置服务地址，server的location配置代理映射
- expose_port 因为nginx如果安装在docker容器内部的话，只知道自己内部端口
- 
