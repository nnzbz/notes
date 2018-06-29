# Docker入门

[TOC]

## 1. 安装

- CentOS

https://docs.docker.com/install/linux/docker-ce/centos/

- Ubuntu

https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce

- mac

https://docs.docker.com/docker-for-mac/install/#what-to-know-before-you-install

## 2. 配置

如果还没有 docker group 就添加一个

```sh
sudo groupadd docker
```

将当前用户加入Docker组

```sh
sudo gpasswd -a ${USER} docker
```

设置开机启动

```sh
systemctl enable docker
```

启动

```sh
systemctl start docker
```

## 3. 镜像

### 3.1. 搜索仓库的镜像

例如，搜索基于Ubuntu 操作系统的容器

```sh
docker search ubuntu
```

官网

https://hub.docker.com/

### 3.2. 国内镜像

#### 3.2.1. 设置默认从国内镜像拉取

- ubuntu

```sh
vi /etc/docker/daemon.json
```

添加"registry-mirrors"节点

```json
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
```

 **注意重启docker才能生效**

```sh
systemctl restart docker
```

- mac

 选择 ```Preferences``` -> ```Daemon``` –> ```Basic``` –> ```Registry mirrors``` ，添加如下内容：

```text
https://registry.docker-cn.com
```

#### 3.2.2. 拉取时指定镜像

```sh
docker pull registry.docker-cn.com/myname/myrepo:mytag
```

例如

```sh
docker pull registry.docker-cn.com/library/ubuntu:16.04
```

### 3.3. 查看本地所有镜像

```sh
docker images
```

### 3.4. 拉取镜像到本地

```sh
docker pull centos
```

确认CentOS 镜像已经被获取

```sh
docker images centos
```

### 3.5. 导出/导入镜像

```sh
# 导出镜像
docker export cbe3cb7799ed > update.tar
# 导入镜像
docker import - update < update.tar
```

### 3.6. 删除镜像

> **注意:删除镜像前要先删除它的容器**

```sh
docker rmi redis
```

## 4. 容器常用操作

### 4.1. 创建并运行容器

```sh
docker run -d -p 7000:6379 --name redis1 --restart=always redis
```

注意顺序，```redis``` 放在最后面

- -d
 后台运行
- -p
 端口映射，7000代表容器外面的端口号，6379是里面的端口号
- --name \<string>
 启动的容器名称
- --restart=always
 重启docker时启动容器(开机启动)
- -i
 捕获标准输入输出
- -t
 分配一个终端或控制台

运行后可以看到指令前缀变成了下面这样

```text
[root@02bb74d47dfd /]#
```

#### 4.1.1. IPv4 forwarding is disabled

WARNING IPv4 forwarding is disabled. Networking will not work

解决办法：

```sh
vi /etc/sysctl.conf
```

或者

```sh
vi /usr/lib/sysctl.d/00-system.conf
```

添加如下代码：

```text
net.ipv4.ip_forward=1
```

重启network服务

```sh
systemctl restart network
```

查看是否修改成功

```sh
sysctl net.ipv4.ip_forward
```

如果返回为“net.ipv4.ip_forward = 1”则表示成功了

#### 4.1.2. 创建并运行完退出

```sh
docker run --name redis-temp redis echo "no run"
```

该命令在创建容器后，运行 ```echo``` 然后退出，通常用于数据卷容器

### 4.2. 启动/停止/重启/删除容器

- start/stop/restart/rm

```sh
docker start redis1
docker stop redis1
docker restart redis1
# 注意：正在运行的容器要先停止后才能删除
docker rm redis1
# 启动所有容器
docker start $(docker ps -a | awk '{ print $1}' | tail -n +2)
# 停止所有容器
docker stop $(docker ps -q)
# 删除所有未运行容器
docker rm $(docker ps -a -q)
# 一句话停止并删除所有容器
docker stop $(docker ps -q) & docker rm $(docker ps -aq)
```

### 4.3. 连接/断开容器

- 连接已启动的容器

```sh
docker exec -it redis1 /bin/bash
```

- 断开与容器的连接
 在容器内的命令行运行 ```exit```的指令或 ```ctrl+d``` 即可断开与容器的连接

### 4.4. 查看所有容器

```sh
docker ps -a
```

- -a
 显示所有状态容器，否则只显示当前运行的容器

### 4.5. 查看变化的文件和文件夹

列出容器内与镜像不同的文件和文件夹

```sh
docker diff redis-temp
```

### 4.6. 生成新镜像

提交容器内修改的内容生成新镜像

```sh
docker commit -m "redis cluster node" -a "zbz" redis-temp zboss/redis-cluster-node:v1.0.0
```

### 4.7. 在容器外编辑容器内的文件

```sh
docker exec -it gitlab vi /etc/gitlab/gitlab.rb
```

### 4.8. 主机与容器间复制文件

- 从主机往容器内复制文件

```sh
docker cp /host/path/target <containerId>:/file/path/within/container
```

- 从容器内往主机复制文件

```sh
docker cp <containerId>:/file/path/within/container /host/path/target
```

### 4.9. 修改容器时区和主机一致

```sh
docker cp /etc/localtime [容器ID或者NAME]:/etc/localtime
```

### 4.10. 修改容器的运行参数(手动修改配置文件)

> **注意：修改参数的时候要将docker停掉**

在创建容器后修改容器的运行参数

在容器的 hostconfig.json 文件中，可以进行修改

默认路径在 ```/var/lib/docker/containers/{容器id}/hostconfig.json```

### 4.11. 修改容器的运行参数(update)

```sh
docker update --restart=always redis1
```

### 4.12. 查看容器的IP地址

查看容器内部的IP地址

```sh
docker inspect node1 | grep IPA
```

### 4.13. 清空容器日志

```sh
docker inspect 【container name】| grep LogPath | cut -d ':' -f 2 | cut -d ',' -f 1 | xargs echo | xargs truncate -s 0
```