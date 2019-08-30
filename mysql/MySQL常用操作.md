# MySQL常用操作

[TOC]

## 1. 执行本地SQL文件

```sh
mysql -u用户名 -p
输入密码
mysql> use 数据库名
mysql> source 本地SQL文件
```

## 2. 查看实时执行的SQL语句

MySQL默认不能实时查看执行的SQL语句，因为这会消耗一定的资源。要开启这个功能，稍微配置一下，打开这个LOG记录就可以了。

### 2.1. 查看是否已经开启日志功能

```sh
mysql -u用户名 -p
输入密码
mysql> use 数据库名
mysql> SHOW VARIABLES LIKE "general_log%";
```

如下general_log值为OFF说明没有开启：

```text
+------------------+----------------------------------+
| Variable_name    | Value                            |
+------------------+----------------------------------+
| general_log      | OFF                              |
| general_log_file | /var/lib/mysql/galley-pc.log |
+------------------+----------------------------------+
2 rows in set (0.00 sec)
```

### 2.2. 开启日志功能

- 临时开启

```sh
mysql> SET GLOBAL general_log = 'ON';
mysql> SET GLOBAL general_log_file = '/var/log/mysql/general_sql.log';
```

**此命令在重启mysql后失效**

- 永久开启

配置 `my.cnf` 文件，加入下面两行：

```sh
general_log = 1
general_log_file = /var/log/mysql/general_sql.log
```

**此配置需要重启MySQL生效**

### 2.3. 实时查看

```sh
tail -f /var/log/mysql/general_sql.log
```

## 3. 备份与恢复

还有个--opt选项要测试

```sh
# 创建密钥
mysql_config_editor set --login-path=密钥名 -h127.0.0.1 -uroot -p
输入密码

# 备份(mysqldump)
mysqlpump --login-path=密钥名 --add-drop-database 数据库名 | gzip > /backup/数据库名_$(date +%Y%m%d_%H%M%S).sql.gz


# 还原(mysql)
gzip -d < /backup/备份文件名.sql.gz | mysql -hhost -u用户名 -p 数据库名
```

- 备份与恢复注意“>”和“<”的区别
- **-h** 参数后面跟远程主机的地址，如果是本地，可不用 **-h**

## 4. 定时自动备份

### 4.1. 添加文件的可执行权限

```sh
chmod u+x bk-数据库名.sh
```

### 4.2. 添加任务

```sh
crontab -e
```

根据不同情况添加以下行：

```text
* 3 * * * /bak/bak.sh
30 3 * * * find /bak -mtime +5 -name 'db*.sql' -exec rm -rf {} \;
*/180 * * * * /home/backup/bkDatabaseName.sh
```

前面几个选项分别是：分 时 日 月 周，星星代表“每”，按:wq保存，这样服务器就会每天自动执行了：
第一行是每天凌晨3点备份数据库，第二行是每天凌晨3点半删除5天以前的旧数据文件，第三行是每3个小时备份一次。

### 4.3. 查看任务执行情况

```sh
tail -f /var/log/cron
```