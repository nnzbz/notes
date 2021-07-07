# 制作和使用nexus的docker容器

[TOC]

## 1. 利用官方Docker镜像

> **注意：第1节用的是官方的镜像，而之后的章节是自己制作的方法**

### 1.1. 创建并运行nexus的容器

- 存放数据在宿主机
  先查看宿主机有没有UID为200的用户
  
  ```sh
  cat /etc/passwd | grep 200
  ```

  - 如果宿主机没有UID为200的用户

    ```sh
    # 添加nexus用户并指定uid为200
    useradd nexus -u 200 --no-create-home
    mkdir /var/lib/nexus
    chown -R nexus:nexus /var/lib/nexus
    docker run -dp 8081:8081 --name nexus -v /var/lib/nexus:/nexus-data --restart=always sonatype/nexus3
    ```

  - 宿主机已经有UID为200的用户
    200的用户是容器中使用的nexus用户，如果在宿主机中添加200的UID会有冲突，可添加另一个没有冲突的，然后在创建容器时使用 `--user` 参数

    ```sh
    # 添加nexus用户并未指定uid为200
    adduser nexus
    cat /etc/passwd|grep nexus # 例如我这里看到UID是1001
    mkdir /var/lib/nexus && chown -R nexus:nexus /var/lib/nexus
    docker run -dp 8081:8081 --name nexus -v /var/lib/nexus:/nexus-data --user 1001:1001 --restart=always sonatype/nexus3
    ```

  - 按上面的方式，Nexus映射到了 `/var/lib/nexus`，但是此路径一般没有分配太大的空间，所以需要更换到有足够容量的空间

    ```sh
    # 首先保证docker没有启动
    sudo service docker stop
    # 然后移动整个/var/lib/mysql目录到目的路径
    sudo mv /var/lib/nexus /usr/local/lib/nexus
    # 添加软链
    sudo ln -s /usr/local/lib/nexus /var/lib/nexus
    ```


- ~~存放数据在数据卷~~(推荐使用上面宿主机的方式)

  ```sh
  docker run --name nexus-data sonatype/nexus3 echo "data-only container for Nexus"
  docker run -dp8081:8081 -p8082:8082 --restart=always --name nexus --volumes-from nexus-data sonatype/nexus3
  ```

- 在Swarm中
  
  ```sh
  docker service create \
        --name nexus \
        -p 8081:8081  \
        --mount type=volume,source=nexusdata,destination=/nexus-data \
        sonatype/nexus3
  ```

### 1.2. 浏览器访问

<http://127.0.0.1:8081>

### 1.3. 查看初始密码

查看初始密码，需查看下面文件的内容

`admin.password`

- 如果目录影射到宿主机
  
  ```sh
  cat /var/lib/nexus/admin.password
  ```

- 如果目录没有影射到宿主机，需进入容器

  ```sh
  docker exec -it nexus /bin/bash
  cat /nexus-data/admin.password
  ```

## 2. 自己制作镜像文件

### 2.1. 准备文件

> **注意:如果要ADD本地文件，则本地文件必须在 docker build \<PATH> ，指定的 \<PATH> 目录下**

#### 2.1.1. 准备jdk源文件

- 官网

<http://www.oracle.com/technetwork/java/javase/downloads/index.html>

<http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html>

- 下载

```sh
wget http://download.oracle.com/otn-pub/java/jdk/8u152-b16/aa0333dd3019491ca4f6ddbe78cdb6d0/jdk-8u152-linux-x64.tar.gz?AuthParam=1508393760_8581e1ef388abd3122635312265a1aa1 -O ~/docker-images/nexus/jdk-8u152-linux-x64.tar.gz
```

#### 2.1.2. 准备nexus源文件

- 官网

http://www.sonatype.com/nexus-repository-oss

https://www.sonatype.com/oss-thank-you-tar.gz

- 下载

```sh
wget https://sonatype-download.global.ssl.fastly.net/nexus/3/nexus-3.6.0-02-unix.tar.gz -O ~/docker-images/nexus/nexus-3.6.0-02-unix.tar.gz
```

### 2.2. 制作Dockerfile文件

```sh
mkdir ~/docker-images/nexus
vi ~/docker-images/nexus/Dockerfile
```

```docker
# 选择一个已有的os镜像作为基础
FROM centos

# 镜像的作者
MAINTAINER zbz "nnzbz@163.com"

# 复制jdk
# RUN mkdir /usr/local/jvm
ADD jdk-8u152-linux-x64.tar.gz /usr/local/jvm

# 复制nexus
# RUN mkdir /usr/local/maven
ADD nexus-3.6.0-02-unix.tar.gz /usr/local/maven

# 配置nexus的jre的路径
ENV INSTALL4J_JAVA_HOME_OVERRIDE /usr/local/jvm/jdk1.8.0_152
# RUN sed -i "@# INSTALL4J_JAVA_HOME_OVERRIDE=@aINSTALL4J_JAVA_HOME_OVERRIDE=/usr/local/jvm/jdk1.8.0_152@" /usr/local/maven/nexus-3.6.0-02/bin/nexus

# EXPOSE 22

CMD ["/usr/local/maven/nexus-3.6.0-02/bin/nexus", "run"]
```

### 2.3. 编译

编译Dockerfile文件，生成新的镜像

> **注意，如果用非root用户编译，先将用户加入到docker组中**

```sh
sudo usermod -a -G docker zbz
# 刷新刚添加用户的组的信息
newgrp - docker
# 重启docker
systemctl restart docker
```

进入Dockerfile文件的目录，运行docker编译

```sh
docker build -t zboss/nexus:v1.0.0 .
```

### 2.4. 创建nexus容器并运行

```sh
docker run -dp8081:8081 --name nexus --restart=always zboss/nexus:v1.0.0
```
