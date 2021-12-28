# 共享存储NFS

[TOC]

当构建一个有容错机制的应用时，有一些数据或文件需要共享到各个节点服务的容器中，有多种方法可以实现，其中一种就是外部存储系统，比如NFS或者Amazon S3

## 1. 安装

- 所有节点安装

```sh
yum -y install nfs-utils
```

## 2. 启动

- 在manager节点上启动nfs服务端

```sh
systemctl enable nfs
systemctl start nfs
```

- 工作节点上启动nfs客户端

```sh
systemctl enable rpcbind
systemctl start rpcbind
```

## 3. 打开防火墙

```sh
firewall-cmd --zone=public --add-port=111/tcp --permanent
firewall-cmd --zone=public --add-port=111/udp --permanent
firewall-cmd --zone=public --add-port=2049/tcp --permanent
firewall-cmd --zone=public --add-port=2049/udp --permanent
firewall-cmd --reload
```

## 4. 配置

- 在manager节点上配置nfs

```sh
vi /etc/exports
```

```ini
# swarm nfs share volume
/usr/local 172.16.0.0/16(rw,sync,no_root_squash)
```

- 参数说明
  - /usr/local : 共享的目录
  - 172.16.0.0/16 : 可以访问的主机网段
    如果不限制，则设为 `*`
  - rw : 可读写权限
    ro : 只读权限
  - sync : 同步，数据更安全，速度慢
    async : 异步，速度快，效率高，安全性低
  - no_root_squash ：NFS 服务共享的目录的属性, 如果用户是root, 对这个目录就有root的权限

- 重启nfs

```sh
systemctl restart nfs
```

- worker节点挂载nfs共享目录
  
  172.16.0.75 是manager节点的IP地址

```sh
mount -t nfs 172.16.0.75:/usr/local /usr/local
```

- 检查目录是否同步

```sh
ls -al /usr/local
```

- worker节点设置开机自动挂载

```sh
echo 'mount -t nfs 172.16.0.75:/usr/local /usr/local' >> /etc/rc.d/rc.local
```
