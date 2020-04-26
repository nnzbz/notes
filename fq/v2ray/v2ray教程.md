# v2ray教程

[TOC]

## 1. 官网教程

<https://www.v2ray.com/>

## 2. 安装

### 2.1. 服务器

- docker

在宿主机编辑配置文件

```sh
mkdir /usr/local/v2ray/
vi /usr/local/v2ray/config.json
```

config.json 内容如下:


```json
{
  "inbounds": [{
    "port": 6668, // 服务器监听端口
    "protocol": "vmess",
    "settings": {
      "clients": [{ "id": "5b778fe6-4a70-4139-9f2d-36ff06a94f3d" }] // 与客户端的配置必须一致
    }
  }],
  "outbounds": [{
    "protocol": "freedom",
    "settings": {}
  }]
}
```

创建容器

```sh
docker run -dp6668:6668 -v /usr/local/v2ray:/etc/v2ray/ --name v2fly --restart=always v2fly/v2fly-core
```

### 2.2. 客户端

<https://www.v2ray.com/awesome/tools.html>

- Windows
  - V2RayW
- Linux
  - Mellow
- Android
  - BifrostV
