# 离线安装ntp

1. 下载安装包

RPM下载网站：<https://pkgs.org/download/ntp>（几乎涵盖了所有RPM包）

CentOS7的下载地址:

<http://mirror.centos.org/centos/7/os/x86_64/Packages/ntp-4.2.6p5-29.el7.centos.2.x86_64.rpm>
<http://mirror.centos.org/centos/7/os/x86_64/Packages/ntpdate-4.2.6p5-29.el7.centos.2.x86_64.rpm>
<http://mirror.centos.org/centos/7/os/x86_64/Packages/autogen-libopts-5.18-5.el7.x86_64.rpm>

- ntp-4.2.6p5-29.el7.centos.2.x86_64.rpm: 这个包为NTP服务器的安装包
- 其它: 必须的依赖包

2. 安装NTPDATE、NTP服务

```sh
rpm -ivh ntpdate-4.2.6p5-29.el7.centos.2.x86_64.rpm
rpm -ivh autogen-libopts-5.18-5.el7.x86_64.rpm
rpm -ivh ntp-4.2.6p5-29.el7.centos.2.x86_64.rpm
```
