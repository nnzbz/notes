# 制作jre的docker镜像

[TOC]

## 1. 下载JRE和JCE

- Server JRE
 http://www.oracle.com/technetwork/java/javase/downloads/server-jre8-downloads-2133154.html
- JCE
 http://www.oracle.com/technetwork/java/javase/downloads/jce8-download-2133166.html

## 2. Dockerfile

### 2.1. centos

```docker
# 选择一个已有的os镜像作为基础
FROM centos

# 镜像的作者和邮箱
MAINTAINER zbz "nnzbz@163.com"

# 时区修改为上海
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 设置utf-8，统一编码格式
ENV LC_ALL en_US.UTF-8

# 加入jre
ADD server-jre-8u172-linux-x64.tar.gz /usr/local/jvm
# 加入JCE
ADD UnlimitedJCEPolicyJDK8/*.jar /usr/local/jvm/jdk1.8.0_172/lib/security

# 设置环境变量
ENV JAVA_HOME /usr/local/jvm/jdk1.8.0_172
ENV PATH $JAVA_HOME/bin:$PATH
```

### 2.2. debian

```Dockerfile
# 选择一个已有的os镜像作为基础
FROM debian

# 镜像的作者和邮箱
MAINTAINER zbz "nnzbz@163.com"

# 时区修改为上海
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 换成网易国内镜像(猜的9的网址)
#RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
#    echo "deb http://mirrors.163.com/debian/ stretch main" >/etc/apt/sources.list && \
#    echo "deb http://mirrors.163.com/debian/ stretch-updates main" >>/etc/apt/sources.list

# 让系统支持统一的编码格式
RUN apt-get update && \
    apt-get install -y locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8 && \
    apt-get remove -y locales
# 设置utf-8，统一编码格式
ENV LANG C.UTF-8

# 复制jre
ADD http://download.oracle.com/otn-pub/java/jdk/8u162-b12/0da788060d494f5095bf8624735fa2f1/server-jre-8u162-linux-x64.tar.gz /usr/local/jvm

# 设置环境变量
ENV JAVA_HOME /usr/local/jvm/jdk1.8.0_162
ENV PATH $JAVA_HOME/bin:$PATH
```

## 3. 编译

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
docker build -t nnzbz/centos-jre:8 .
docker tag nnzbz/centos-jre:8 nnzbz/centos-jre:latest
docker push nnzbz/centos-jre:8
docker push nnzbz/centos-jre:latest
```

## 创建并运行容器

```sh
docker run -it --name centos-jre nnzbz/centos-jre /bin/bash
```
