# 制作redis的Docker容器

[TOC]

## 1. 制作单机版redis

### 1.1. 拉取redis镜像

```sh
docker pull redis
```

### 1.2. 创建容器并运行redis

- 无密码（不推荐）

```sh
docker run -dp6379:6379 --name redis --restart=always redis
```

- 配置密码

```sh
# 准备配置文件
echo requirepass b4903e4939f55c329abeb0861a107ecb327fa2baace95b489bf94b36f0c501f71e07e93d22b25f17bd63abb5c69b1a6318cf834f0ec4511595deaa6d52986288 >> /usr/local/etc/redis.conf
# 创建并运行容器
docker run -dp6379:6379 --privileged=true -v /usr/local/etc/redis.conf:/data/redis.conf --name redis --restart=always redis redis.conf
```

## 2. 安装redis5集群

### 2.1. 拉取redis镜像(同上)

### 2.2. 准备redis源文件

从官网下载redis软件包

<http://download.redis.io/releases/redis-5.0.5.tar.gz>

**具体下载文件的版本号部分请以网站上最新版本为准**

软件包里面需要用到下面这个配置文件

- 配置文件 ```redis.conf```

在宿主机中，解压软件包并将配置文件复制到指定目录中

```sh
cd /tmp
wget http://download.redis.io/releases/redis-5.0.5.tar.gz
tar vxf /tmp/redis-5.0.5.tar.gz
mkdir -p /usr/local/redis-cluster/conf
cp /tmp/redis-5.0.5/redis.conf /usr/local/redis-cluster/conf
```

### 2.3. 修改配置文件

```sh
sed -i 's/^bind 127.0.0.1$/bind 0.0.0.0/' /usr/local/redis-cluster/conf/redis.conf
sed -i '/# cluster-enabled yes/acluster-enabled yes' /usr/local/redis-cluster/conf/redis.conf
```

### 2.4. 准备集群中每个节点的配置文件

```sh
cd /usr/local/redis-cluster/conf/
mkdir 7000
mkdir 7001
mkdir 7002
mkdir 7100
mkdir 7101
mkdir 7102
cp ./redis.conf 7000
cp ./redis.conf 7001
cp ./redis.conf 7002
cp ./redis.conf 7100
cp ./redis.conf 7101
cp ./redis.conf 7102
sed -i 's/^port 6379$/port 7000/' 7000/redis.conf
sed -i 's/^port 6379$/port 7001/' 7001/redis.conf
sed -i 's/^port 6379$/port 7002/' 7002/redis.conf
sed -i 's/^port 6379$/port 7100/' 7100/redis.conf
sed -i 's/^port 6379$/port 7101/' 7101/redis.conf
sed -i 's/^port 6379$/port 7102/' 7102/redis.conf
```

### 2.5. 创建并运行容器

**注：目前latest的版本是5.0.5**

```sh
# master
docker run -d --net=host --name redis-a --restart=always -v /usr/local/redis-cluster/conf/7000:/usr/local/etc/redis redis redis-server /usr/local/etc/redis/redis.conf
docker run -d --net=host --name redis-b --restart=always -v /usr/local/redis-cluster/conf/7001:/usr/local/etc/redis redis redis-server /usr/local/etc/redis/redis.conf
docker run -d --net=host --name redis-c --restart=always -v /usr/local/redis-cluster/conf/7002:/usr/local/etc/redis redis redis-server /usr/local/etc/redis/redis.conf

# slaver
docker run -d --net=host --name redis-a1 --restart=always -v /usr/local/redis-cluster/conf/7100:/usr/local/etc/redis redis redis-server /usr/local/etc/redis/redis.conf
docker run -d --net=host --name redis-b1 --restart=always -v /usr/local/redis-cluster/conf/7101:/usr/local/etc/redis redis redis-server /usr/local/etc/redis/redis.conf
docker run -d --net=host --name redis-c1 --restart=always -v /usr/local/redis-cluster/conf/7102:/usr/local/etc/redis redis redis-server /usr/local/etc/redis/redis.conf
```

### 2.6. 打开防火墙端口

```sh
firewall-cmd --zone=dmz --permanent --add-port=7000/tcp
firewall-cmd --zone=dmz --permanent --add-port=7001/tcp
firewall-cmd --zone=dmz --permanent --add-port=7002/tcp
firewall-cmd --zone=dmz --permanent --add-port=7100/tcp
firewall-cmd --zone=dmz --permanent --add-port=7101/tcp
firewall-cmd --zone=dmz --permanent --add-port=7102/tcp
```

### 2.7. 创建集群

- 进入任一个容器

```sh
docker exec -it redis-a /bin/bash
```

```sh
redis-cli --cluster create --cluster-replicas 1 192.168.1.201:7000 192.168.1.201:7001 192.168.1.201:7002 192.168.1.201:7100 192.168.1.201:7101 192.168.1.201:7102
```

> replicas的参数 ```1``` ，表示每个master就有一个从节点
> **注意:这里IP不能是 ```127.0.0.1``` ，而是局域网所能访问的IP**

### 2.8. 检查集群是否安装成功

在宿主机上执行如下：

```sh
$ ps aux|grep redis-server
polkitd  28130  0.1  0.0  49396 12536 ?        Ssl  16:02   0:01 redis-server 0.0.0.0:7000 [cluster]
polkitd  28244  0.1  0.0  43252 10376 ?        Ssl  16:02   0:01 redis-server 0.0.0.0:7001 [cluster]
polkitd  28356  0.1  0.0  43252 10532 ?        Ssl  16:02   0:01 redis-server 0.0.0.0:7002 [cluster]
polkitd  28468  0.1  0.0  43252 12420 ?        Ssl  16:02   0:01 redis-server 0.0.0.0:7100 [cluster]
polkitd  28578  0.1  0.0  43252 10372 ?        Ssl  16:02   0:01 redis-server 0.0.0.0:7101 [cluster]
polkitd  28704  0.1  0.0  43252 10368 ?        Ssl  16:02   0:01 redis-server 0.0.0.0:7102 [cluster]
```

## 3. ~~安装redis4集群~~

### 3.1. ~~拉取redis镜像(同上)~~

### 3.2. ~~准备redis源文件~~

从官网下载redis软件包

<http://download.redis.io/releases/redis-4.0.2.tar.gz>

**具体下载文件的版本号部分请以网站上最新版本为准**

软件包里面取出下面两个文件

- 配置文件 ```redis.conf```
- 集群管理程序 ```src/redis-trib.rb```

在宿主机中，解压软件包并将配置文件复制到指定目录中

```sh
cd /tmp
wget http://download.redis.io/releases/redis-4.0.2.tar.gz
tar vxf redis-4.0.2.tar.gz
mkdir -p /usr/local/redis-cluster/conf
cp /tmp/redis-4.0.2/redis.conf /usr/local/redis-cluster/conf
```

### 3.3. ~~修改配置文件~~

```sh
sed -i 's/^bind 127.0.0.1$/bind 0.0.0.0/' /usr/local/redis-cluster/conf/redis.conf
sed -i '/# cluster-enabled yes/acluster-enabled yes' /usr/local/redis-cluster/conf/redis.conf
```

### 3.4. ~~准备集群中每个节点的配置文件~~

```sh
cd /usr/local/redis-cluster/conf/
mkdir 7000
mkdir 7001
mkdir 7002
mkdir 7100
mkdir 7101
mkdir 7102
cp ./redis.conf 7000
cp ./redis.conf 7001
cp ./redis.conf 7002
cp ./redis.conf 7100
cp ./redis.conf 7101
cp ./redis.conf 7102
sed -i 's/^port 6379$/port 7000/' 7000/redis.conf
sed -i 's/^port 6379$/port 7001/' 7001/redis.conf
sed -i 's/^port 6379$/port 7002/' 7002/redis.conf
sed -i 's/^port 6379$/port 7100/' 7100/redis.conf
sed -i 's/^port 6379$/port 7101/' 7101/redis.conf
sed -i 's/^port 6379$/port 7102/' 7102/redis.conf
```

### 3.5. ~~制作集群管理的镜像~~

> **注意：其实可以不用制作镜像，直接用现成的，用类似下面这条命令**

```sh
docker run -it --rm zvelo/redis-trib create --replicas 1 192.168.1.201:7000 192.168.1.201:7001 192.168.1.201:7002 192.168.1.201:7100 192.168.1.201:7101 192.168.1.201:7102
```

#### 3.5.1. ~~创建集群管理的容器~~

```sh
docker run --net=host -it --name redis-trib centos /bin/bash
```

修改

```sh
yum install ruby rubygems -y
```

更换国内镜像

```sh
gem sources --remove https://rubygems.org/
gem sources --add http://gems.ruby-china.org/
gem sources -l
```

升级ruby

先安装rvm，再把ruby版本提升至2.3.4

安装curl

```sh
yum install curl which -y
```

```sh
gpg2 --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
```

安装RVM

```sh
curl -L get.rvm.io | bash -s stable
```

```sh
. /usr/local/rvm/scripts/rvm
```

查看rvm库中已知的ruby版本

```sh
rvm list known
```

安装一个ruby版本

```sh
rvm install 2.3.4
```

使用一个ruby版本

```sh
rvm use 2.3.4
```

设置默认版本

```sh
rvm use 2.3.4 --default
```

卸载一个已知版本

```sh
rvm remove 2.0.0
```

查看ruby版本

```sh
ruby --version
```

下面这步我也不知道做的是什么

```sh
gem install redis
```

#### 3.5.2. ~~复制redis-trib.rb到容器~~

在主机中将 redis-trib.rb 文件复制到redis-trib容器中的 /usr/local/bin/ 目录下

```sh
docker cp /tmp/redis-4.0.2/src/redis-trib.rb redis-trib:/usr/local/bin/
```

#### 3.5.3. ~~提交修改生成新镜像~~

```sh
docker commit -m "redis trib" -a "zbz" redis-trib zboss/redis-trib:v1.0.0
```

### 3.6. ~~创建并运行容器~~

```sh
# master
docker run -d --net=host --name redis-a --restart=always -v /usr/local/redis-cluster/conf/7000:/usr/local/redis/conf redis /usr/local/redis/conf/redis.conf
docker run -d --net=host --name redis-b --restart=always -v /usr/local/redis-cluster/conf/7001:/usr/local/redis/conf redis /usr/local/redis/conf/redis.conf
docker run -d --net=host --name redis-c --restart=always -v /usr/local/redis-cluster/conf/7002:/usr/local/redis/conf redis /usr/local/redis/conf/redis.conf

# slaver
docker run -d --net=host --name redis-a1 --restart=always -v /usr/local/redis-cluster/conf/7100:/usr/local/redis/conf redis /usr/local/redis/conf/redis.conf
docker run -d --net=host --name redis-b1 --restart=always -v /usr/local/redis-cluster/conf/7101:/usr/local/redis/conf redis /usr/local/redis/conf/redis.conf
docker run -d --net=host --name redis-c1 --restart=always -v /usr/local/redis-cluster/conf/7102:/usr/local/redis/conf redis /usr/local/redis/conf/redis.conf
```

### 3.7. ~~打开防火墙端口~~

```sh
firewall-cmd --zone=dmz --permanent --add-port=7000/tcp
firewall-cmd --zone=dmz --permanent --add-port=7001/tcp
firewall-cmd --zone=dmz --permanent --add-port=7002/tcp
firewall-cmd --zone=dmz --permanent --add-port=7100/tcp
firewall-cmd --zone=dmz --permanent --add-port=7101/tcp
firewall-cmd --zone=dmz --permanent --add-port=7102/tcp
```

### 3.8. ~~创建集群~~

启动redis-trib容器

```sh
docker start redis-trib
docker exec -it redis-trib /bin/bash
```

在容器内创建集群

```sh
redis-trib.rb create --replicas 1 192.168.1.201:7000 192.168.1.201:7001 192.168.1.201:7002 192.168.1.201:7100 192.168.1.201:7101 192.168.1.201:7102
```

> replicas的参数 ```1``` ，表示每个master就有一个从节点
> **注意:这里IP不能是 ```127.0.0.1``` ，而是局域网所能访问的IP**
