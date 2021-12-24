# 记录一次DNS重启后失效的问题

[TOC]

## 1. 出现问题

DNS失效，ping不通外网域名

按规范流程设置了DNS

```sh
vi /etc/sysconfig/network-scripts/ifcfg-eth0
```

添加如下内容

```ini
PEERDNS="no"
```

```sh
vi /etc/resolv.conf
```

添加如下内容

```ini
nameserver 114.114.114.114
```

重启网络

```sh
service network restart
```

成功ping通外网域名

但是重启操作系统后，又恢复如故

## 2. 分析现象

查看网上配置文件

```sh
cat /etc/sysconfig/network-scripts/ifcfg-eth0
```

发现首行如下内容

```ini
# Created by cloud-init on instance boot automatically, do not edit.
#
```

原来每次重启，都会被云服务重置此配置文件~~~

## 3. 解决问题

按之前的再做一遍，但是ping通后先不要重启，运行下面的命令

```sh
# 不得任意更动此文件，如果以后想去掉限制，把 +i 改为 -i 再执行一下就可以了
chattr +i /etc/resolv.conf
```

重启，成功
