# 安装常用Linux发行版

[TOC]

## 1. CentOS7

### 1.1. U盘安装

#### 1.1.1. 下载ISO文件

#### 1.1.2. 刻录ISO到U盘

用win32 disk imager软件刻录ISO文件到U盘

#### 1.1.3. U盘启动

### 1.2. 网络配置

#### 1.2.1. IP

编辑网卡的配置文件

```sh
vi /etc/sysconfig/network-scripts/ifcfg-eth0
```

修改

```text
……
DEVICE=eth0
BOOTPROTO=static
IPADDR=192.168.1.223
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
ONBOOT=yes
……
```

重启网络生效

```sh
service network restart
```

#### 1.2.2. DNS

显示当前网络连接

```sh
nmcli connection show
```

显示

```text
NAME UUID                                 TYPE           DEVICE
eno1 5fb06bd0-0bb0-7ffb-45f1-d6edd65f3e03 802-3-ethernet eno1
```

修改当前网络连接对应的DNS服务器，这里的网络连接可以用名称或者UUID来标识

```sh
nmcli con mod eno1 ipv4.dns "114.114.114.114 8.8.8.8"
```

将dns配置生效

```sh
nmcli con up eno1
```

### 1.3. 编码格式

 ```locale``` 或者 ```echo $LANG```

### 1.4. 小版本升级

```sh
# 查看系统版本
cat /etc/redhat-release
# 安装wget
yum install wget -y
# 安装阿里云yum镜像源
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
# 清空yum缓存
yum clean all
# 升级
yum update -y
# 重启系统
reboot
# 查看系统版本
cat /etc/redhat-release
```
