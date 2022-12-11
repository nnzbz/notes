# 记录一次容器内telnet不了外部网络IP的问题

## 问题描述

在容器内telnet外部网络地址的IP加端口号不通，但是在宿主机是可以的

## 问题解决

此方案是LZ银行解决的，本人未能到现场具体排查与核实，先行记录下来

- 临时配置

```sh
sysctl -w net.bridge.bridge-nf-call-ip6tables=1
sysctl -w net.bridge.bridge-nf-call-iptables=1
sysctl -w net.bridge.bridge-nf-call-arptables=1
sysctl -w net.ipv4.ip_forward=1
```

- 永久配置

```sh
vi /etc/sysctl.conf
```

```ini
....
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-arptables = 1
....
```

```sh
# 加载并查看是否设置成功
sysctl -p
```
