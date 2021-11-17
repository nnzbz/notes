# Docker入门

[TOC]

## 参考资料

<https://yeasy.gitbook.io/docker_practice/>

## 1. 安装

- CentOS
  <https://docs.docker.com/engine/install/centos/>

  当服务器连接docker官方网站速度非常缓慢，可以参考以下地址，更换docker-ce.repo为国内源

  https://mirror.tuna.tsinghua.edu.cn/help/docker-ce/

  国内源更换完成后，安装还是使用官网上的命令操作：

  ```
  sudo yum install docker-ce docker-ce-cli containerd.io
  ```

- Ubuntu
  <https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce>

- Mac
  <https://docs.docker.com/docker-for-mac/install/#what-to-know-before-you-install>

- Deepin
  由于 Deepin 是基于 debian 的 unstable 版本开发的，通过 `lsb_release -cs` 获取到的版本信息为 unstable，而 docker 官方源并没支持 debian 的 unstable 版本，因此使用 docker 官方教程是安装不成功的。
  安装请参考官方Debian的方案
  <https://docs.docker.com/engine/install/debian/>
  但是在 `SET UP THE REPOSITORY`的第 `3` 步时注意，修改为下面的命令

```sh
sudo vi /etc/apt/sources.list.d/docker.list
```

```sh
deb [arch=amd64] https://download.docker.com/linux/debian buster stable
```

解释

- 官方文档使用 `$(lsb_release -cs)`，在Deepin中得到 *unstable*， 这里就具体指定debian的版本(在Deepin中查看Debian的版本请用 `cat /etc/debian_version` ，然后查看该版本对应的代号)

## 2. 安装后配置系统

<https://docs.docker.com/engine/install/linux-postinstall/>

- 如果还没有 docker group 就添加一个

```sh
sudo groupadd docker
```

- 将当前用户加入Docker组

```sh
sudo usermod -aG docker $USER
```

- 改变docker安装的路径
  docker一般安装在 `/var/lib/docker`，但是此路径一般没有分配太大的空间，所以需要更换到有足够容量的空间

  ```sh
  # 首先保证docker没有启动
  service docker stop
  # 然后移动整个/var/lib/docker目录到目的路径
  sudo mv /var/lib/docker /usr/local/lib/docker
  # 添加软链
  sudo ln -s /usr/local/lib/docker /var/lib/docker
  ```

- 设置开机启动

```sh
# 设置开机启动
systemctl enable docker
# 启动docker
systemctl start docker
```

## 3. 镜像

### 3.1. 搜索仓库的镜像

例如，搜索基于Ubuntu 操作系统的容器

```sh
docker search ubuntu
```

官网

<https://hub.docker.com/>

### 3.2. 国内镜像

#### 3.2.1. 设置默认从国内镜像拉取

- 查看阿里云镜像加速器地址

<https://cr.console.aliyun.com/cn-shenzhen/instances/mirrors>

- ubuntu/centos

```sh
vi /etc/docker/daemon.json
```

添加"registry-mirrors"节点

```json
{
  "registry-mirrors": ["https://XXXXXXXX.mirror.aliyuncs.com"]
}
```

或

```json
{
  "registry-mirrors": ["https://ustc-edu-cn.mirror.aliyuncs.com"]
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

#### 4.1.1. 创建并运行完退出

```sh
docker run --name redis-temp redis echo "no run"
```

该命令在创建容器后，运行 ```echo``` 然后退出，通常用于数据卷容器

#### 4.1.2. 启动容器不自动退出

两种方法

- 创建并运行容器时，后面用 ```/bin/sh```

```sh
docker run -d -it <容器ID> /bin/sh
```

- 在镜像里面配置启动脚本里面增加一个执行进程

Dockerfile文件

```Dockerfile
RUN touch /var/log/1.txt
CMD "tail" "-f" "/var/log/1.txt"
```

#### 4.1.3. 创建容器后修改参数

如果创建容器后想修改参数，如设置为自动启动，如下：

```sh
docker container update --restart=always 容器名字
```

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

### 4.3. 进入/退出容器

- 进入已启动的容器

  ```sh
  docker exec -it redis1 /bin/bash
  ```

  进入后可以看到指令前缀变成了下面这样

  ```sh
  [root@02bb74d47dfd /]#
  ```

- 退出容器
 在容器内的命令行运行 ```exit```的指令或 ```ctrl+d```

### 4.4. 查看所有容器

```sh
docker ps -a
```

- -a
 显示所有状态容器，否则只显示当前运行的容器

### 4.5. 查看指定端口号的容器是哪个

```sh
# 查找端口号的PID
netstat -nap|grep 8080
# 最后的PID是上面查出来的PID
docker ps -q | xargs docker inspect --format '{{.State.Pid}}, {{.Name}}' | grep "%PID%"
```

### 4.6. 查看变化的文件和文件夹

列出容器内与镜像不同的文件和文件夹

```sh
docker diff redis-temp
```

### 4.7. 生成新镜像

提交容器内修改的内容生成新镜像

```sh
docker commit -m "redis cluster node" -a "zbz" redis-temp zboss/redis-cluster-node:v1.0.0
```

### 4.8. 在容器外编辑容器内的文件

```sh
docker exec -it gitlab vi /etc/gitlab/gitlab.rb
```

### 4.9. 主机与容器间复制文件

- 从主机往容器内复制文件

```sh
docker cp /host/path/target <containerId>:/file/path/within/container
```

- 从容器内往主机复制文件

```sh
docker cp <containerId>:/file/path/within/container /host/path/target
```

### 4.10. 修改容器时区和主机一致

```sh
docker cp /etc/localtime [容器ID或者NAME]:/etc/localtime
```

### 4.11. 修改容器的运行参数(手动修改配置文件)

> **注意：修改参数的时候要将docker停掉**

在创建容器后修改容器的运行参数

在容器的 hostconfig.json 文件中，可以进行修改

默认路径在 ```/var/lib/docker/containers/{容器id}/hostconfig.json```

### 4.12. 修改容器的运行参数(update)

```sh
docker update --restart=always redis1
```

### 4.13. 查看容器的IP地址

查看容器内部的IP地址

```sh
docker inspect node1 | grep IPA
```

### 4.14. 清空容器日志

```sh
docker inspect 【container name】| grep LogPath | cut -d ':' -f 2 | cut -d ',' -f 1 | xargs echo | xargs truncate -s 0
```

### 4.15. 常见报错

- 未启动docker会报错

  当使用 docker ps报错

  ```sh
  Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
  ```

  - service docker start 报错

  ```sh
  Redirecting to /bin/systemctl start docker.service
  ```

  可以设置开机启动  

  ```sh
  systemctl enable docker
  ```

- IPv4 forwarding is disabled

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
