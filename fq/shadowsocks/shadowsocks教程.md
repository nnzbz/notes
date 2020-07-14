# shadowsocks教程

[TOC]

## 1. 使用

<https://github.com/shadowsocks/shadowsocks/wiki/Shadowsocks-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E>

## 2. 服务端

### 2.1. 安装

<https://shadowsocks.org/en/download/servers.html>

- python

```sh
$ python --version
Python 2.6.8

$ pip install shadowsocks
```

- docker

```sh
docker pull shadowsocks/shadowsocks-libev
docker run -e PASSWORD=<password> -p<server-port>:8388 -p<server-port>:8388/udp -d shadowsocks/shadowsocks-libev
```

### 2.2. 配置

修改配置文件/etc/shadowsocks.json，如果没有则新建。

```json
{
    "server": "0.0.0.0",
    "server_port": 8388,
    "password": "mypassword",
    "fast_open": false
}
```

或（多个SS账号）

```json
{
    "server": "0.0.0.0",
    "server_port": 8388,
    "port_password": {
        "8381": "xxxxxxx",
        "8382": "xxxxxxx",
        "8383": "xxxxxxx",
        "8384": "xxxxxxx"
    },
    "fast_open": false
}
```

配置说明：

| 字段          | 说明                            |
| :------------ | ------------------------------- |
| server        | ss服务监听地址                  |
| server_port   | ss服务监听端口                  |
| local_address | 本地的监听地址                  |
| local_port    | 本地的监听端口                  |
| password      | 密码                            |
| timeout       | 超时时间，单位秒                |
| method        | 加密方法，默认是aes-256-cfb     |
| fast_open     | 使用TCP_FASTOPEN, true / false  |
| workers       | workers数，只支持Unix/Linux系统 |

### 2.3. 运行

- 后台运行

```sh
ssserver -c /etc/shadowsocks.json -d start
```

- 停止运行

```sh
ssserver -c /etc/shadowsocks.json -d stop
```

- 如需开机启动
  修改/etc/rc.local，加入以下内容

```sh
ssserver -c /etc/shadowsocks.json -d start
```

- 检查日志

```sh
sudo less /var/log/shadowsocks.log
```

## 3. 客户端

### 3.1. 下载地址

- Windows
<https://github.com/shadowsocks/shadowsocks-windows/releases>
  
- Mac OS X
<https://github.com/shadowsocks/ShadowsocksX-NG/releases>

- Linux
<https://github.com/shadowsocks/shadowsocks-qt5/wiki/Installation>
<https://github.com/shadowsocks/shadowsocks-qt5/releases>

- IOS
<https://itunes.apple.com/app/apple-store/id1070901416?pt=2305194&ct=shadowsocks.org&mt=8>
<https://github.com/shadowsocks/shadowsocks-iOS/releases>

- Android
<https://play.google.com/store/apps/details?id=com.github.shadowsocks>
<https://github.com/shadowsocks/shadowsocks-android/releases>
