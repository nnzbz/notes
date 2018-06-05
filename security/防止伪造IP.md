# 防止伪造IP

[TOC]

## 1. 各个常用请求头

- X-Real-IP
 是Nginx的反向代理标志（只包含真实ip）
- x-forwarded-for
 是Nginx的反向代理标志（包含真实ip和反向代理服务器地址，以“,”隔开，第一个为用户真实ip，后面的是各个层代理服务器ip）
- Proxy-Client-IP
 是Apache的反向代理标志
- WL-Proxy-Client-IP
 是WebLogic的反向代理标志

## 2. 常见伪造请求头方式

- 服务器没有使用反向代理
  - X-Real-IP
  - x-forwarded-for
  - Proxy-Client-IP
  - WL-Proxy-Client-IP
- 服务器使用的是Apache(Proxy-Client-IP请求头)
  - X-Real-IP
  - x-forwarded-for
  - WL-Proxy-Client-IP
- 服务器使用的是WebLogic(WL-Proxy-Client-IP请求头)
  - X-Real-IP
  - x-forwarded-for
  - Proxy-Client-IP
  - WL-Proxy-Client-IP
- 服务器使用的是Nginx（x-forwarded-for请求头）
  - X-Real-IP
  - x-forwarded-for
  - Proxy-Client-IP
  - WL-Proxy-Client-IP

## 3. 解决方法

### 3.1. 配置好Nginx

如果不配置好Nginx，也会获取到伪造的ip。
比如Nginx的配置是

```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

这个配置是对 ```x-forwarded-for``` 请求头进行追加ip。如果用户伪造 ```x-forwarded-for``` 请求头的话，Nginx不会覆盖用户伪造的ip，而是追加到后面，这样获取的也是伪造的ip。

如果Nginx反向代理有多台，那么在最外层的反向代理服务器加上

```nginx
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $remote_addr;
```

内层的反向代理服务器加上(！注意不要加X-Real-IP配置)

```nginx
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

### 3.2. 分不同代理进行严格判断

#### 3.2.1. 没有代理

用request.getRemoteAddr();方法就能获取到用户的ip了。


