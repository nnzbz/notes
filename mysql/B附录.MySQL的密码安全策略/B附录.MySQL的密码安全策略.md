# MySQL的密码安全策略

[TOC]

## 1. 获取安装时的临时密码

```sh
grep 'temporary password' /var/log/mysqld.log
```

> **注意：日志文件是在前面启动mysql后生成的**

## 2. 修改密码

```sh
mysql -uroot -p
...
mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpass');
```

## 3. 设置可使用简单密码

```sh
mysql -uroot -p
```

validate_password_policy有以下取值：
| Policy      | Tests Performed                                                               |
| ----------- | ----------------------------------------------------------------------------- |
| 0 or LOW    | Length                                                                        |
| 1 or MEDIUM | Length; numeric, lowercase/uppercase, and special characters                  |
| 2 or STRONG | Length; numeric, lowercase/uppercase, and special characters; dictionary file |

默认是1，即MEDIUM，所以刚开始设置的密码必须符合长度，且必须含有数字，小写或大写字母，特殊字符。  
要想设置简单的密码，必须修改两个全局参数：

```sh
mysql> set global validate_password_policy=0;
```

这样，判断密码的标准就基于密码的长度了。  
这个由validate_password_length参数来决定。  
而validate_password_length可设置的最小值又由下面3个参数决定。

| 参数                                 | 说明                 | 默认值 |
| ------------------------------------ | -------------------- | ------ |
| validate_password_number_count       | 密码中数字的长度     | 1      |
| validate_password_special_char_count | 密码中特殊字符的长度 | 1      |
| validate_password_mixed_case_count   | 密码中大小字母的长度 | 1      |

> validate_password_length可设置的最小值 =  
    validate_password_number_count  
    + validate_password_special_char_count  
    + 2 * validate_password_mixed_case_count

所以默认validate_password_length可设置的最小值是4

```sh
mysql> set global validate_password_length=4;
```

## 4. 设置安全选项

```sh
mysql_secure_installation
```

## 5. 密码策略

查看密码策略的相关信息

```sh
mysql> show variables like '%password%';
```

修改密码策略

在/etc/my.cnf文件添加validate_password_policy配置，指定密码策略

```text
validate_password_policy=0
```

如果不需要密码策略，添加my.cnf文件中添加如下配置禁用即可：

```text
validate_password = off
```

重新启动mysql服务使配置生效：

```sh
systemctl restart mysqld
```
