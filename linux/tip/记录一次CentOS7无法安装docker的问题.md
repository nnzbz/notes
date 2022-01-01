# 记录一次DNS重启后失效的问题

[TOC]

## 1. 出现问题

安装docker不成功，提示需要一些包，但是总是有一些包安装时找不到，想升级CentOS居然报找不到

## 2. 分析现象

首先排除了网络问题，解决了域名解析问题，最后发现是yum的仓库文件似乎有问题

## 3. 解决问题

决定重装yum

1. 卸载yum

```sh
# 删除旧仓库文件
rm -f /etc/yum.repos.d/*.*
# 查看yum版本
rpm -qa yum
# 卸载yum安装包(注意这里要相应修改为查看到的版本)
rpm -qa yum yum-3.4.3-168.el7.centos.noarch
# 卸载安装组件
rpm -qa | grep yum | xargs rpm -e --nodeps 
# 再次查看yum版本
rpm -qa yum
```

2. 下载yum相应安装文件

在 <http://mirrors.163.com/centos/7/os/x86_64/Packages/> 目录下找出最新的rpm包，并下载

- yum-最新版.centos.noarch.rpm 
- yum-metadata-parser-最新版.x86_64.rpm
- yum-plugin-fastestmirror-最新版.noarch.rpm
- wget-最新版.x86_64.rpm

3. 安装yum和wget

```sh
rpm -ivh yum-*
rpm -ivh wget-*
```

4. 导入证书

```sh
rpm --import http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-7
```

5. 添加阿里的源

```sh
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```

6. 清除缓存 生成新的缓存

```sh
yum clean all
yum makecache
```

问题解决

## 4. 更简单的解决方案

后来在其它服务器发现只要拿正常的仓库覆盖过来就可以了，正常的仓库文件内容如下:

```sh
cat /etc/yum.repos.d/CentOS-Base.repo
```

```ini
# CentOS-Base.repo
#
# The mirror system uses the connecting IP address of the client and the
# update status of each mirror to pick mirrors that are updated to and
# geographically close to the client.  You should use this for CentOS updates
# unless you are manually picking other mirrors.
#
# If the mirrorlist= does not work for you, as a fall back you can try the 
# remarked out baseurl= line instead.
#
#
 
[base]
name=CentOS-$releasever - Base - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/os/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/os/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/os/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#released updates 
[updates]
name=CentOS-$releasever - Updates - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/updates/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/updates/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/updates/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/extras/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/extras/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/extras/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$releasever - Plus - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/centosplus/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/centosplus/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/centosplus/$basearch/
gpgcheck=1
enabled=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#contrib - packages by Centos Users
[contrib]
name=CentOS-$releasever - Contrib - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/contrib/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/contrib/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/contrib/$basearch/
gpgcheck=1
enabled=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
```
