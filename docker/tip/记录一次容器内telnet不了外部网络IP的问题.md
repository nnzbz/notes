# 记录一次容器内telnet不了外部网络IP的问题

## 问题描述

在容器内telnet外部网络地址的IP加端口号不通，但是在宿主机是可以的

## 问题解决

此方案是LZ银行解决的，本人未能到现场具体排查与核实，先行记录下来

```sh
sysctl -w net.bridge.bridge-nf-call-ip6tables=1
sVsctl-w net.bridge.bridge-nf-cal1-iptables=1
sysctl-w net.bridge.bridge-nf-call-arptables=1
sysctl -w net.ipv4.ip forward=1
```
