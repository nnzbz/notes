# 附录A.CentOS7安装MySQL

[TOC]

## 1. 安装YUM Repo

YUM Repo官方网址

> https://dev.mysql.com/downloads/repo/yum/

下载rpm

```sh
wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
```

检测下md5是否与页面上的一致：

```sh
md5sum mysql57-community-release-el7-10.noarch.rpm
安装rpm
```

安装rpm

```sh
yum install mysql57-community-release-el7-11.noarch.rpm
```

## 2. 安装MySQL

```sh
yum install -y mysql-server
```

## 3. MySQL的启动配置

```sh
systemctl start mysqld #启动MySQL
systemctl stop mysqld #关闭MySQL
systemctl restart mysqld #重启MySQL
systemctl status mysqld #查看MySQL运行状态
systemctl enable mysqld #设置开机启动
systemctl disable mysqld #关闭开机启动
```

## 4. 配置MySQL

### 4.1. 默认配置文件路径

配置文件：/etc/my.cnf  
日志文件：/var/log//var/log/mysqld.log  
服务启动脚本：/usr/lib/systemd/system/mysqld.service  
socket文件：/var/run/mysqld/mysqld.pid

### 4.2. 修改root的密码

较新版本的MySQL会在新安装好后第一次启动时给root用户生成一个随机的密码，这里就需要我们修改。

可按忘记密码或修改安全策略来进行，这里略。


### 4.3. 添加远程登录用户

默认只允许root帐户在本地登录，如果要在其它机器上连接mysql，必须修改root允许远程连接，或者添加一个允许远程连接的帐户，为了安全起见，最好添加一个新的帐户：

```sh
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;
mysql> flush privileges;
```

### 4.4. 配置默认编码为utf8mb4

检查编码配置

```sh
mysql> show variables like 'character%';
```

修改/etc/my.cnf配置文件，在[mysqld]下添加编码配置:

```ini
[client]
default-character-set=utf8mb4

# 对其他远程连接的mysql客户端的配置
[mysql]
default-character-set=utf8mb4

# 本地mysql服务的配置
[mysqld]
character-set-client-handshake=FALSE
character-set-server=utf8mb4
collation-server=utf8mb4_general_ci
```

重新启动mysql服务，查看数据库默认编码已全改为utf8
+--------------------------+----------------------------+
| Variable_name            | Value                      |
+--------------------------+----------------------------+
| character_set_client     | utf8mb4                    |
| character_set_connection | utf8mb4                    |
| character_set_database   | utf8mb4                    |
| character_set_filesystem | binary                     |
| character_set_results    | utf8mb4                    |
| character_set_server     | utf8mb4                    |
| character_set_system     | utf8                       |
| character_sets_dir       | /usr/share/mysql/charsets/ |
+--------------------------+----------------------------+

### 4.5. 修改database默认的字符集

ALTER DATABASE database_name CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

## 5. 打开防火墙

### 5.1. 查看防火墙的当前防区

```sh
firewall-cmd --get-active-zones
```

### 5.2. 打开端口

假设当前防区是dmz，mysql的端口号是3306

```sh
firewall-cmd --zone=dmz --add-port=3306/tcp --permanent
```

### 5.3. 重新加载

```sh
firewall-cmd --reload
```
