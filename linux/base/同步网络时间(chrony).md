# 同步网络时间(chrony)

[TOC]

## 简介

`chrony` 是一个多功能的 `NTP (Network Time Protocol)` 实现，类 `Unix` 系统上 `NTP` 客户端和服务器的替代品。它可以通过 `NTP` 服务或者类似 `GPS` 时钟接收器的硬件级参考时钟来同步系统时钟，具有更好的时钟准确度，并且对于那些间歇性互联网连接的系统很有帮助

`Centos 7.x` 开始的最小发行版中都已经预装并开启了 `chrony`

## 配置 `chrony`

```sh
vi /etc/chrony.conf
```

```ini
....

# 配置要同步的 NTP 服务器
server <ntp服务器1> iburst [minpoll x] [maxpoll x]
server <ntp服务器2> iburst [minpoll x] [maxpoll x]

....

# 根据实际时间计算的修正值，将补偿参数记录在该文件
driftfile /var/lib/chrony/drift

....

# 如果偏移值大于 1.0 秒，在头 3 次更新时允许步进式调整系统时间
makestep 1.0 3

....

# 启用内核时间与 RTC 时间同步 (自动写回硬件)
rtcsync

....
```

server参数详解

- minpoll x(可选)
  最小间隔，默认值是 `6`，代表 `64s`
- maxpoll x(可选)
  最大间隔，默认值是 `9`，代表 `512s`
- iburst
  在头四次 NTP 请求以 2s 或者更短的间隔，而不是以 minpoll x 指定的最小间隔
  
## 启用 `chrony`

```sh
# 检查状态
systemctl status chronyd
# 启动
systemctl start chronyd
# 设置开机启动
systemctl enable chronyd
```

## 使用 `chrony` 作为 `NTP` 服务器

```sh
vi /etc/chrony.conf
```

```ini
# 对于安全要求比较高的，这里可以限制谁能访问本机提供的 NTP 服务
allow 192.168.1.0/24

# (可选)设置 chronyd 监听在哪个网络接口
bindcmdaddress 0.0.0.0

# (可选)这个地方很重要，如果服务器本身也不能同步时间，那么就用本地时间替代，层级为 10
local stratum 10
```

```sh
# 重新启动服务
systemctl restart chronyd
```

## 查看

```sh
# 查看 Chrony 服务的日志
journalctl -u chronyd

# 显示所有 NTP 源服务器的信息
chronyc sources -v

# 显示所有 NTP 源服务器的状态
chronyc sourcestats -v

# 查看 NTP 服务器的在线和离线状态
chronyc activity

# 检查 NTP 服务是否允许指定主机访问
chronyc accheck <IP地址>

# 显示所有访问本服务的客户端
chronyc clients
```
