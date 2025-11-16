# 忘记MySQL的密码

[TOC]

## 1. 修改配置文件my.cnf

```sh
vi /etc/my.cnf
```

找到[mysqld]节点下添加

```text
skip-grant-tables
```

保存退出

## 2. 重启mysqld

```sh
systemctl restart mysqld
```

## 3. 登录MySQL并修改密码

### 3.1. 登录MySQL而不需要密码

```sh
mysql -u root
```

### 3.2. 修改密码

```sh
mysql> update mysql.user set authentication_string=password('root') where user='root';
mysql> flush privileges;
```

### 3.3. 退出MySQL

```sh
mysql> quit
```

## 4. 恢复需要密码登录

```sh
vi /etc/my.cnf
```

找到[mysqld]节点下之前添加的

```text
skip-grant-tables
```

删除并保存退出

## 5. 重启mysqld

```sh
systemctl restart mysqld
```