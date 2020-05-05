# 在Docker中搭建gogs

[TOC]

## 1. 拉取镜像

```sh
docker pull gogs/gogs
```

## 2. 创建并运行容器

```sh
# Create local directory for volume.
$ mkdir -p /var/gogs

# Use `docker run` for the first time.
$ docker run --name=gogs -dp 10022:22 -p 10080:3000 -v /var/gogs:/data --restart always gogs/gogs
```

- 如果指定使用同为docker容器内的mysql数据库，请用link参数

```sh
docker run --name=gogs -dp 10022:22 -p 10080:3000 -v /var/gogs:/data --restart always --link mysql:mysql  gogs/gogs
```

## 3. 打开防火墙端口

```sh
firewall-cmd --zone=dmz --permanent --add-port=10022/tcp
firewall-cmd --zone=dmz --permanent --add-port=10080/tcp
firewall-cmd --reload
```

## 4. 初始化

- 访问 <http://ip:10080>
  注意填写上部分连接mysql的参数，其它默认即可
- 注册新用户
  第一次注册的用户即为管理员

## 5. 克隆项目

```sh
git clone http://zbz@192.168.1.201:10080/wboly/wboly-suc.git
```
