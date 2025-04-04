# MySQL

[TOC]

## 1. Dockerfile

<https://github.com/DockerfileX/mysql>

## 2. 创建并运行MySQL容器

### 2.1. 单机

```sh
mkdir -p ~/opt/mysql/data
vi ~/opt/mysql/stack.yml
```

```yml
services:
  mysql:
    image: mysql:5.7
    container_name: mysql
    ports:
      - "3306:3306"
      - "33060:33060"
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - TZ=CST-8
    command:
      --default-time-zone='+8:00'
      --character-set-client-handshake=FALSE
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_general_ci
      --max_connections=5000
      --skip-name-resolve
    volumes:
      - mysqldata:/var/lib/mysql
    restart: always

  mysql8:
    image: mysql:8
    container_name: mysql8
    ports:
      - "3386:3306"
      - "33860:33060"
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - TZ=CST-8
    command:
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --default-time-zone='+8:00'
      --max_connections=5000
      --skip-name-resolve
    volumes:
      - mysql8data:/var/lib/mysql
    restart: always

  mysql9:
    image: mysql:9
    container_name: mysql9
    ports:
      - "3396:3306"
      - "33960:33060"
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - TZ=CST-8
    command:
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
      --default-time-zone='+8:00'
      --max_connections=5000
      --skip-name-resolve
    volumes:
      - mysql9data:/var/lib/mysql
    restart: always

volumes:
  mysqldata:
  mysql8data:
  mysql9data:
```

- MYSQL_ROOT_PASSWORD: 初始化root账户访问的密码
- max_connections: 设置最大连接数，默认151太小
- skip-name-resolve:
  服务器是否执行客户端主机名解析，是则跳过对连接客户端的主机名解析，直接使用IP地址进行连接。这可以提高连接速度。但是某些情况下无法使用主机名进行连接，例如在授权表中使用主机名进行授权时

```sh
docker compose -f ~/opt/mysql/stack.yml up -d
```

### 2.2. 将数据映射到宿主机路径中保存

#### 2.2.1. 宿主机没有UID为999的用户

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

#### 2.2.2. 宿主机已经有UID为999的用户

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

#### 2.2.3. 改变MySQL在宿主机中的路径

按上面的方式，MySQL映射到了 `/var/lib/mysql`，但是此路径一般没有分配太大的空间，所以需要更换到有足够容量的空间

```sh
# 首先保证docker没有启动
service docker stop
# 然后移动整个/var/lib/mysql目录到目的路径
sudo mv /var/lib/mysql ~/opt/lib/mysql
# 添加软链
sudo ln -s ~/opt/lib/mysql /var/lib/mysql
```

### 2.3. ~~将数据映射到数据卷中保存~~(推荐使用上面映射到宿主机中的方式)

```sh
# 创建MySQL的数据卷
docker run --name mysql-data nnzbz/mysql echo "data-only container for MySQL"
# 创建并运行MySQL的容器
docker run -dp3306:3306 --restart=always --name mysql -e MYSQL_ROOT_PASSWORD=root --volumes-from mysql-data nnzbz/mysql
```

### 2.4. Swarm单机

#### 2.4.1. 创建 secret

```sh
# 两种方式
# 创建 secret(20位随机密码)
openssl rand -base64 20 | docker secret create mysql_root_password -
# 创建 secret(自定义密码)
echo "xxxxxxxx" | docker secret create mysql_root_password -
```

#### 2.4.2. 准备 `my.cnf` 文件

```sh
mkdir -p ~/opt/mysql
vi ~/opt/mysql/mysql-my.cnf
```

```ini
[mysqld]
# 为服务器分配id，可以自定义，不区分大小，起标识作用。不同数据库节点分配不同的id
server_id=1
# 打开Mysql 日志，日志格式为二进制
log-bin=mysql-bin
# 每1次在事务提交前会将二进制日志同步到磁盘上，保证在服务器崩溃时不会丢失事件
# 默认是0，为性能考虑，也可以改为100
sync_binlog=1
```

#### 2.4.3. `Docker Compose`

```sh
vi ~/opt/mysql/stack.yml
```

```yaml{.line-numbers}
services:
  mysql:
    image: mysql:5.7
    # 注意: 如果是arm架构服务器，请用下面这个镜像
    # image: biarms/mysql:5
    hostname: mysql
    ports:
      - 3306:3306
      - 33060:33060
    secrets:
      - mysql_root_password
    volumes:
      - ~/opt/mysql/mysql-my.cnf:/etc/mysql/my.cnf
      - mysqldata:/var/lib/mysql
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
      - MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql_root_password
    # max_connections设置最大连接数，默认151太小
    # skip-name-resolve为了加快连接速度，禁用反向域名解析，这样授权表中的host字段就不能用IP
    command: --default-time-zone='+8:00'
            --character-set-client-handshake=FALSE
            --character-set-server=utf8mb4
            --collation-server=utf8mb4_general_ci
            --max_connections=5000
            --skip-name-resolve
    # deploy:
    #   placement:
    #     constraints:
    #       #该hostname为指定容器在哪个主机启动
    #       - node.hostname == db1
    logging:
      options:
        max-size: 8m


secrets:
  mysql_root_password:
    external: true
volumes:
  mysqldata:

networks:
  default:
    external: true
    name: rebue
```

#### 2.4.4. 部署

```sh
docker stack deploy -c ~/opt/mysql/stack.yml mysql
```

### 2.5. Swarm集群

#### 2.5.1. ~~创建 secret~~

```sh
# 两种方式
# 创建 secret(20位随机密码)
openssl rand -base64 20 | docker secret create mysql_root_password -
# 创建 secret(自定义密码)
echo "xxxxxxxx" | docker secret create mysql_root_password -
```

- 查看密钥(在创建容器后)

```sh
# 进入容器
docker exec -it <容器id> /bin/sh
# 在容器中查看密钥
cat /run/secrets/mysql_root_password
```

#### 2.5.2. 准备 `my.cnf` 文件

- mysql00的 `my.cnf`

```sh
mkdir -p ~/opt/mysql
vi ~/opt/mysql/mysql00-my.cnf
```

```ini
[mysqld]
# 为服务器分配id，可以自定义，不区分大小，起标识作用。不同数据库节点分配不同的id
server_id=10
# 打开Mysql 日志，日志格式为二进制
log-bin=mysql-bin
# 每1次在事务提交前会将二进制日志同步到磁盘上，保证在服务器崩溃时不会丢失事件
# 默认是0，为性能考虑，也可以改为100
sync_binlog=1
# 当启用时，服务器通过只允许执行可以使用GTID安全地记录的语句来强制GTID一致性。
enforce-gtid-consistency=on
# 启用基于GTID的复制，启用之前必须保证enforce-gtid-consistency=true
gtid_mode=on
# 默认为mixed混合模式，为了数据一致性，可以更改成row，但是效率和空间消耗会较大(debezium 需要设置为 row)
binlog_format=mixed

#replicate-ignore-db=mysql
#replicate-ignore-db=sys
#replicate-ignore-db=information_schema
#replicate-ignore-db=performance_schema
```

- mysql01的 `my.cnf`

```sh
vi ~/opt/mysql/mysql01-my.cnf
```

```ini
[mysqld]
#为服务器分配id，可以自定义，不区分大小，起标识作用。不同数据库节点分配不同的id
server_id=20
# 打开Mysql 日志，日志格式为二进制
log-bin=mysql-bin
# 当启用时，服务器通过只允许执行可以使用GTID安全地记录的语句来强制GTID一致性。
enforce-gtid-consistency=on
# 启用基于GTID的复制，启用之前必须保证enforce-gtid-consistency=true
gtid_mode=on
# 默认为mixed混合模式，为了数据一致性，可以更改成row，但是效率和空间消耗会较大
binlog_format=mixed

# Slave的binlog默认不写入来自于Master的更新，这样如果此Slave还有Slave就无法同步Master的更新
# 开启 log-slave-updates 选项，Slave将来自Master更新写入到binlog中
# 一台服务器即做主库又做从库必须开启，例如 A -> B -> C 中的B，或者双主中的主，都需要开启
log-slave-updates=on
# 避免启动后还是使用老的复制协议
skip_slave_start=on
# 即使开启了skip_slave_start，从库仍然可能在崩溃后被中断
# 因为master.info和中级日志文件都不是崩溃安全的，所以建议开启以下3个选项：
#sync_master_info=on
#sync_relay_log=on
#sync_relay_log_info=on

# 不能执行写操作(root用户依旧可以)
read_only=on
# root用户也不能执行写操作
#super_read_only=on

#replicate-ignore-db=mysql
#replicate-ignore-db=sys
#replicate-ignore-db=information_schema
#replicate-ignore-db=performance_schema
```

#### 2.5.4. `Docker Compose`

```sh
vi ~/opt/mysql/stack.yml
```

```yaml{.line-numbers}
services:
  mysql00:
    image: mysql:5.7
    # 注意: 如果是arm架构服务器，请用下面这个镜像
    # image: biarms/mysql:5.7
    hostname: mysql00
    ports:
      - 3306:3306
      - 33060:33060
    # secrets:
    #   - mysql_root_password
    volumes:
      - ~/opt/mysql/mysql00-my.cnf:/etc/mysql/my.cnf:z
      - mysql00data:/var/lib/mysql:z
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
      # 允许空密码
      - MYSQL_ALLOW_EMPTY_PASSWORD=true
      #- MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql_root_password
    # max_connections设置最大连接数，默认151太小
    # skip-name-resolve为了加快连接速度，禁用反向域名解析，这样授权表中的host字段就不能用IP
    # skip-grant-tables首次进入容器不用密码登录
    command: --default-time-zone='+8:00'
            --character-set-client-handshake=FALSE
            --character-set-server=utf8mb4
            --collation-server=utf8mb4_general_ci
            --max_connections=5000
            --skip-name-resolve
            --skip-grant-tables
    # deploy:
    #   placement:
    #     constraints:
    #       #该hostname为指定容器在哪个主机启动
    #       - node.hostname == mysql00
    logging:
      options:
        max-size: 8m
  mysql01:
    image: mysql:5.7
    # 注意: 如果是arm架构服务器，请用下面这个镜像
    # image: biarms/mysql:5.7
    hostname: mysql01
    ports:
      - 3316:3306
      - 33160:33060
    depends_on:
      - mysql00
    volumes:
      - ~/opt/mysql/mysql01-my.cnf:/etc/mysql/my.cnf:z
      - mysql01data:/var/lib/mysql:z
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
      # 允许空密码
      - MYSQL_ALLOW_EMPTY_PASSWORD=true
      #- MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql_root_password
    # max_connections设置最大连接数，默认151太小
    # skip-name-resolve为了加快连接速度，禁用反向域名解析，这样授权表中的host字段就不能用IP
    # skip-grant-tables首次进入容器不用密码登录
    command: --default-time-zone='+8:00'
            --character-set-client-handshake=FALSE
            --character-set-server=utf8mb4
            --collation-server=utf8mb4_general_ci
            --max_connections=5000
            --skip-name-resolve
            # 首次进入容器不用密码登录
            --skip-grant-tables
    # deploy:
    #   placement:
    #     constraints:
    #       #该hostname为指定容器在哪个主机启动
    #       - node.hostname == mysql01
    logging:
      options:
        max-size: 8m

volumes:
  mysql00data:
  mysql01data:

networks:
  default:
    external: true
    name: rebue
```

#### 2.5.5. 部署

```sh
docker stack deploy -c ~/opt/mysql/stack.yml mysql
```

#### 2.5.6. 开启主从同步

1. 分别对 mysql00 和 mysql01 执行下面命令

```sh
# 查看mysql的容器id
docker ps | grep mysql
# 进入mysql容器
docker exec -it <容器id> bash
# 进入 mysql
mysql -uroot
```

```mysql
# 设置xxxxxxxx为密码，注意不能超过32位
update mysql.user set authentication_string=password('xxxxxxxx') where user='root';

# 开放 root 用户给所有地址访问
# 检查 root 用户的 Host 配置
SELECT User, Host FROM mysql.user WHERE User = 'root';
# 如果 root 的 Host 属性是 localhost，需要更新为 %
UPDATE mysql.user SET Host = '%' WHERE User = 'root' AND Host = 'localhost';

flush privileges;
```

2. 在 mysql00 中执行下面的命令

```sh
# 创建用户并授权
GRANT REPLICATION SLAVE ON *.* to 'slave'@'%' identified by '密码';
```

3. 在 mysql01 中执行下面的命令

**注意：** 如果是重新部署的，需要先执行这个命令 `reset slave;`

```sh
# 开启IO线程监听mysql-1的binlog文件
change master to master_host='mysql00',master_user='slave',master_password='密码',master_port=3306,MASTER_AUTO_POSITION=1;
# 开启同步
start slave;
# 查看是否开启成功
show slave status\G;
```

- 如果开启成功，返回结果如下图:

![主从开启成功](主从开启成功.png)

4. 创建账户、数据库并授权

分别对 mysql00 执行下面命令

```sh
# 查看mysql的容器id
docker ps | grep mysql
# 进入mysql容器
docker exec -it <容器id> /bin/sh
# 进入 mysql
mysql -u root -p
# 创建用户并授权(xxx是账户名)
GRANT ALL ON xxx.* to 'xxx'@'%' identified by '密码';
```



#### 2.5.7. ~~开启主主同步~~

1. 分别对 mysql00 和 mysql01 执行下面命令

```sh
# 查看mysql的容器id
docker ps | grep mysql
# 进入mysql容器
docker exec -it <容器id> /bin/sh
# 查看密码
cat /run/secrets/mysql_root_password
# 进入 mysql
mysql -u root -p
# 创建用户并授权
GRANT REPLICATION SLAVE ON *.* to 'slave'@'%' identified by '密码';
```

2. 在 mysql01 中执行下面的命令

**注意：** 如果是重新部署的，需要先执行这个命令 `reset slave;`

```sh
# 开启IO线程监听mysql-1的binlog文件
change master to master_host='mysql00',master_user='slave',master_password='密码',master_port=3306,MASTER_AUTO_POSITION=1;
# 开启同步
start slave;
```

3. 在 mysql00 中执行下面的命令

```sh
# 开启IO线程监听mysql-1的binlog文件
change master to master_host='mysql01',master_user='slave',master_password='密码',master_port=3306,MASTER_AUTO_POSITION=1;
# 开启同步
start slave;
```

4. 分别在 mysql00 和 mysql01 中执行下面命令查看是否开启成功

```sh
show slave status\G;
```

- 如果开启成功，返回结果如下图:

![主从开启成功](主从开启成功.png)

#### 2.5.8. ~~在主主环境中创建账户并授权~~

分别对 mysql00 和 mysql01 执行下面命令

```sh
# 查看mysql的容器id
docker ps | grep mysql
# 进入mysql容器
docker exec -it <容器id> /bin/sh
# 查看密码
cat /run/secrets/mysql_root_password
# 进入 mysql
mysql -u root -p
# 创建用户并授权(xxx是账户名)
GRANT ALL ON xxx.* to 'xxx'@'%' identified by '密码';
```

#### 2.5.9. ~~在主主环境中修改账户密码~~

分别对 mysql00 和 mysql01 执行下面命令

```sh
# 查看mysql的容器id
docker ps | grep mysql
# 进入mysql容器
docker exec -it <容器id> /bin/sh
# 查看密码
cat /run/secrets/mysql_root_password
# 进入 mysql
mysql -u root -p
# 选择数据库
use mysql;
# 查看账户密码(密码是经过杂凑算法显示出来的)
select host,user,authentication_string from user;
# 修改账户密码(xxx是账户名)
update user set authentication_string=password('密码') where user='xxx' and host='%';
# 刷新缓存
FLUSH PRIVILEGES;
```

## 3. 其它容器连接MySQL容器

```sh
docker run --name some-app --link some-mysql:mysql -d application-that-uses-mysql
```
