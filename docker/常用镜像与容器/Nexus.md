# 制作和使用nexus的docker容器

[TOC]

> **注意：第1节用的是官方的镜像，而之后的章节是自己制作的方法**

## 1. 创建并运行nexus的容器和容器卷

```sh
docker run --name nexus-data sonatype/nexus3 echo "data-only container for Nexus"
docker run -dp8081:8081 -dp8082:8082 --restart=always --name nexus --volumes-from nexus-data sonatype/nexus3
```

> **注意：下面是自己制作的方法**

## 2. 准备文件

> **注意:如果要ADD本地文件，则本地文件必须在 docker build \<PATH> ，指定的 \<PATH> 目录下**

### 2.1. 准备jdk源文件

- 官网

http://www.oracle.com/technetwork/java/javase/downloads/index.html

http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

- 下载

```sh
wget http://download.oracle.com/otn-pub/java/jdk/8u152-b16/aa0333dd3019491ca4f6ddbe78cdb6d0/jdk-8u152-linux-x64.tar.gz?AuthParam=1508393760_8581e1ef388abd3122635312265a1aa1 -O ~/docker-images/nexus/jdk-8u152-linux-x64.tar.gz
```

### 2.2. 准备nexus源文件

- 官网

http://www.sonatype.com/nexus-repository-oss

https://www.sonatype.com/oss-thank-you-tar.gz

- 下载

```sh
wget https://sonatype-download.global.ssl.fastly.net/nexus/3/nexus-3.6.0-02-unix.tar.gz -O ~/docker-images/nexus/nexus-3.6.0-02-unix.tar.gz
```

## 3. 制作Dockerfile文件

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

## 4. 编译

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

## 5. 创建nexus容器并运行

```sh
docker run -dp8081:8081 --name nexus --restart=always zboss/nexus:v1.0.0
```