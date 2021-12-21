# 记录一次inode满引发的问题

[TOC]

## 出现问题

在一次重新部署 `swarm` 服务的时候报 `No space left on device`

## 分析现象

出现这个错误第一反应是空间满了，分为3种情况

- inode满了
- block满了
- 特殊原因，如文件一直被占用，没有被彻底清除

## 解决问题

```sh
# 查看block是否满了
df -h
# 查看inode是否满了
df -i
```

结果发现 `/dev/sda1` 的inode满了

```sh
Filesystem       Inodes   IUsed    IFree IUse% Mounted on
/dev/sda1       3276800 3276800        0  100% /
devtmpfs        2030966     397  2030569    1% /dev
tmpfs           2033349       1  2033348    1% /dev/shm
tmpfs           2033349     719  2032630    1% /run
tmpfs           2033349      16  2033333    1% /sys/fs/cgroup
/dev/sdb1      19660800    7143 19653657    1% /usr/local
/dev/sdb2      47448064  109602 47338462    1% /var/lib/docker
tmpfs           2033349       1  2033348    1% /run/user/0
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/b0db4ebc4d91cb9793a06b21d80665361b12ec36b3682b3b2d3b823d3cf87a38/merged
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/1d8e01c2aed1bb35cd05380b1f4a685fad97fa079977d90cc67a7f16a1a02e70/merged
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/48db73ebdb51400a3d8340065f287e446492f33e3902e73ba9c6aab0a53316a9/merged
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/e11432d2296ebedd11824674798ddd2e576d9d9afb3237a9cd2ab090923e9dfb/merged
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/776ea82e054c7b89cb684bda8d6fb423be84c267c27bf9bb8e7c1c9ef2534e64/merged
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/4b476389c034820b1b726ac6164b429690f2e987d567fd1ba03bb07264d874c4/merged
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/41b88172cd4f4925c5165721d37537e736d3a208dcb20810a9b2992f855ba3b4/merged
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/a27b1175e4ea60f7712ecf91ca54f3dc89412b5c0aef9e9dd1e6186b610063b8/merged
overlay        47448064  109602 47338462    1% /var/lib/docker/overlay2/e83b0d1b604090f0448c6a30f1a20613f1e733cf1b3fe26e76ec95803f2d4b47/merged
```

尝试删除临时文件

查看临时文件目录

```sh
ls -it /tmp | wc -l
```

结果过了很久才反应，不停打印出临时文件，果断暂停并删除

```sh
find /tmp -type f -size 0c -exec rm {} \;
```

定时删除文件

```sh
echo 'find /tmp -type f -size 0c -exec rm {} \;' > /usr/local/tmpclean.sh
crontab -e
```

添加一行，每5分钟执行一次清理

```ini
*/5 * * * * /bin/bash /usr/local/tmpclean.sh
```

## 补充解释

- inode在格式化创建文件系统的时候诞生，用来存放文件的属性信息，存放着block的位置，没有文件名，创建一个非空文件占用一个inode和至少1个block
- block是实际存放数据的位置，block大小 1k 4k 8k centos 6.x(分区大于500M 默认是4k)，文件很大的话占用多个block, 文件非常小的时候1k block剩余的空间不能继续使用，所以系统中block消耗更快