# MySQL

[TOC]

## 1. Dockerfile

<https://github.com/DockerfileX/mysql>

## 2. 创建并运行MySQL容器

### 2.1. 将数据映射到宿主机路径中保存

#### 2.1.1. 宿主机没有UID为999的用户

在宿主机中执行以下命令

```sh
# 如果是重新安装，/var/lib/mysql目录已然有数据，那么这一段可不用执行，直接创建并运行容器就可以了，数据不会被覆盖
mkdir /var/lib/mysql
# 添加mysql用户并指定uid为999
useradd mysql -u 999 --no-create-home
chown -R mysql:mysql /var/lib/mysql/
# 或直接
chown -R 999:999 /var/lib/mysql/

# 创建并运行MySQL的容器
docker run --name mysql -dp3306:3306 -p33060:33060 -e MYSQL_ROOT_PASSWORD=root -v /var/lib/mysql:/var/lib/mysql --restart=always nnzbz/mysql
```

- 如果要复制容器内数据库的数据到宿主机中，可使用如下命令

  ```sh
  docker cp mysql:/var/lib/mysql /var/lib
  # 注意执行完后要修改宿主机中目录的权限
  chown -R mysql:mysql /var/lib/mysql/
  ```

- -v 冒号前一个 `/var/lib/mysql` 是宿主机的路径

#### 2.1.2. 宿主机已经有UID为999的用户

999的用户是容器中使用的用户，如果在宿主机中添加999的UID会有冲突，可添加另一个没有冲突的，然后在创建容器时使用 `--user` 参数

  ```sh
  # 如果是重新安装，/var/lib/mysql目录已然有数据，那么这一段可不用执行，直接创建并运行容器就可以了，数据不会被覆盖
  mkdir /var/lib/mysql
  adduser mysql --no-create-home --disabled-password
  cat /etc/passwd|grep mysql # 我这里看到UID是1001
  chown -R mysql:mysql /var/lib/mysql/

  # 创建并运行MySQL的容器，注意1001为之前前一步
  docker run --name mysql -dp3306:3306 -p33060:33060 -e MYSQL_ROOT_PASSWORD=root -v /var/lib/mysql:/var/lib/mysql --user 1001:1001 --restart=always nnzbz/mysql
  ```

#### 2.1.3. 改变MySQL在宿主机中的路径

按上面的方式，MySQL映射到了 `/var/lib/mysql`，但是此路径一般没有分配太大的空间，所以需要更换到有足够容量的空间

  ```sh
  # 首先保证docker没有启动
  service docker stop
  # 然后移动整个/var/lib/mysql目录到目的路径
  sudo mv /var/lib/mysql /usr/local/lib/mysql
  # 添加软链
  sudo ln -s /usr/local/lib/mysql /var/lib/mysql
  ```

### 2.2. ~~将数据映射到数据卷中保存~~(推荐使用上面映射到宿主机中的方式)

  ```sh
  # 创建MySQL的数据卷
  docker run --name mysql-data nnzbz/mysql echo "data-only container for MySQL"
  # 创建并运行MySQL的容器
  docker run -dp3306:3306 --restart=always --name mysql -e MYSQL_ROOT_PASSWORD=root --volumes-from mysql-data nnzbz/mysql
  ```

## 3. 其它容器连接MySQL容器

```sh
docker run --name some-app --link some-mysql:mysql -d application-that-uses-mysql
```
