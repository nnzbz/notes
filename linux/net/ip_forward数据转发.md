# ip_forward数据转发

[TOC]

## 1. 简介

所谓转发即当主机拥有多于一块的网卡时，其中一块收到数据包，根据数据包的目的ip地址将数据包发往本机另一块网卡，该网卡根据路由表继续发送数据包。这通常是路由器所要实现的功能，在docker中容器访问外部网络需要开启。

## 2. ip_forward的值

- 0 未开启
- 1 已开启

## 3. 检查

- 查看是否配置开启

```sh
sysctl net.ipv4.ip_forward
```

- 查看当前实时是否已开启

```sh
cat /proc/sys/net/ipv4/ip_forward
```

## 4. 配置

- 临时开启

```sh
sysctl -w net.ipv4.ip_forward=1
```

- 配置永久开启

```sh
vi /etc/sysctl.conf
```

```ini
....
net.ipv4.ip_forward = 1
....
```

```sh
# 加载并查看是否配置成功
sysctl -p
```

- 最后记得用上一节的命令查看当前实时是否已开启

```sh
cat /proc/sys/net/ipv4/ip_forward
```

## 5. 防火墙开启masquerade

防火墙的masquerade功能进行地址伪装（类似NAT），私网访问公网或公网访问私网都需要开启此功能来进行地址转换，否则无法正常互访

- 开启

```sh
firewall-cmd --add-masquerade
firewall-cmd --add-masquerade --permanent
```

开启后 `net.ipv4.ip_forward` 的值自动会被设置为 `1`，因为不开启就相当于只有本机的数据能进出网络接口，那么 `NAT` 就没有意义了
