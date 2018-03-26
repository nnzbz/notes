# 制作MySQL镜像

[TOC]

## 1. Dockerfile

```Dockerfile
# 选择一个已有的os镜像作为基础
FROM mysql
# 镜像的作者和邮箱
MAINTAINER zbz "nnzbz@163.com"

# 时区修改为上海
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 让系统支持统一的编码格式
RUN apt-get update && \
    apt-get install -y locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8 && \
    apt-get remove -y locales
# 设置utf-8，统一编码格式
ENV LANG C.UTF-8

# 修改my.cnf文件支持utf-8
RUN mv /etc/mysql/my.cnf /etc/mysql/my.cnf.bak
RUN echo "[client]" >>/etc/mysql/my.cnf
RUN echo "default-character-set=utf8mb4" >>/etc/mysql/my.cnf

RUN echo "[mysql]" >>/etc/mysql/my.cnf
RUN echo "default-character-set=utf8mb4" >>/etc/mysql/my.cnf

RUN echo "[mysqld]" >>/etc/mysql/my.cnf
RUN echo "character-set-client-handshake=FALSE" >>/etc/mysql/my.cnf
RUN echo "character-set-server=utf8mb4" >>/etc/mysql/my.cnf
RUN echo "collation-server=utf8mb4_general_ci" >>/etc/mysql/my.cnf
```

## 2. 编译与上传

```sh
docker build -t nnzbz/mysql:5 .
docker tag nnzbz/mysql:5 nnzbz/mysql:latest
docker push nnzbz/mysql:5
docker push nnzbz/mysql:latest
```

## 3. 创建并运行MySQL容器

```sh
# 创建MySQL的数据卷
docker run --name mysql-data nnzbz/mysql echo "data-only container for MySQL"
# 创建并运行MySQL的容器
docker run -dp3306:3306 --restart=always --name mysql -e MYSQL_ROOT_PASSWORD=root --volumes-from mysql-data nnzbz/mysql
```

## 4. 其它容器连接MySQL容器

```sh
docker run --name some-app --link some-mysql:mysql -d application-that-uses-mysql
```