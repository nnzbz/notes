# 记录一次升级CentOS7导致ssh连接不上的问题

[TOC]

## 1. 出现问题

在一次升级CentOS版本由7.3=5通过update升级到7.9后，在没重启前ssh还能连接，在重启之前ssh不能连接

## 2. 分析现象

在第一台出了问题后，在其它机器升级未升级之前，特意查看了 `/etc/ssh/sshd_config` 的配置，如下

```sh
vi /etc/ssh/sshd_config
```

```ini
....
PasswordAuthentication yes
....
```

发现并没有问题，然后重启，还是连接不上

## 3. 解决问题

只好通知网管，网管从后台登录进去，发现 `PasswordAuthentication` 被改掉了，如下

```ini
....
PasswordAuthentication no
....
```

将其改为 `yes` 就可以连接了

此坑未弄清楚什么原因，下次要注意
