# 制作MySQL镜像

[TOC]

## 1. Dockerfile

https://github.com/nnzbz/Dockerfiles/tree/master/mysql

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