# 离线安装nfs

1. 下载安装包

```sh
yum -y install nfs-utils --downloadonly --downloaddir /tmp/nfs
```

其它依赖的包

<http://mirror.centos.org/centos/7/os/x86_64/Packages/libtirpc-0.2.4-0.16.el7.x86_64.rpm>
<http://mirror.centos.org/centos/7/os/x86_64/Packages/libevent-2.0.21-4.el7.x86_64.rpm>

2. 安装

```sh
rpm -ivh *.rpm
```

3. 