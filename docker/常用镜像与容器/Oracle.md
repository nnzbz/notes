# Oracle

[TOC]

## 克隆制作镜像的源码

```sh
git clone https://github.com/oracle/docker-images.git
```

## 下载oracle的压缩包

<https://www.oracle.com/database/technologies/oracle-database-software-downloads.html>

## 将下载的文件移动到制作镜像的目录中去

```sh
mv <下载的压缩文件> <git clone创建的目录>/OracleDatabase/SingleInstance/dockerfiles/<Oracle的版本>/
```

## 制作镜像

```sh
cd <git clone创建的目录>/OracleDatabase/SingleInstance/dockerfiles/
./buildDockerImage.sh -v <Oracle的版本> -e
```

## 创建并运行容器

```sh
mkdir /usr/local/oradata
docker run --name oracle19c \
-p 1521:1521 \
-p 5500:5500 \
-v /usr/local/oradata:/opt/oracle/oradata \
oracle/database:19.3.0-ee 
```

- 注意第一行日志
  `ORACLE PASSWORD FOR SYS, SYSTEM AND PDBADMIN: iV86pmS7ZxI=1`
  后面 `iV86pmS7ZxI=1` 是密码

- 完整的运行指南可以在git下来的官方dockerfile目录中找到。
  `docker-images/OracleDatabase/SingleInstance/README.md`
  或直接访问
  <https://github.com/oracle/docker-images/blob/main/OracleDatabase/SingleInstance/README.md>

## 访问

<https://localhost:5500/em>
