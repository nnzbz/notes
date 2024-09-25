# Linux防火墙

[TOC]

## 1. 运行、停止firewalld

### 1.1. 启动

```sh
systemctl start firewalld
```

### 1.2. 停止

```sh
systemctl stop firewalld
```

## 2. 启用firewalld

### 2.1. 启用

```sh
systemctl enable firewalld
```

### 2.2. 禁用

```sh
systemctl disable firewalld
```


## 3. 检查防火墙版本

```sh
firewall-cmd --version
```

## 4. 检查防火墙状态

```sh
systemctl status firewalld
```

或者

```sh
firewall-cmd --state
```

## 5. 更新防火墙规则

```sh
firewall-cmd --reload
firewall-cmd --complete-reload
```

两者的区别就是第一个无需断开连接，就是firewalld特性之一动态添加规则，第二个需要断开连接，类似重启服务

## 6. 防区（zone）管理

### 6.1. 防区（zone）的概念

硬件防火墙默认一般有三个区，firewalld引入这一概念系统默认存在以下区域（根据文档自己理解，如果有误请指正）：

- drop：默认丢弃所有包
- block：拒绝所有外部连接，允许内部发起的连接
- public：指定外部连接可以进入
- external：这个不太明白，功能上和上面相同，允许指定的外部连接
- dmz：和硬件防火墙一样，受限制的公共连接可以进入
- work：工作区，概念和workgoup一样，也是指定的外部连接允许
- home：类似家庭组
- internal：信任所有连接

对防火墙不算太熟悉，还没想明白public、external、dmz、work、home从功能上都需要自定义允许连接，具体使用上的区别还需高人指点

另一篇解释

- drop（丢弃)
任何接收的网络数据包都被丢弃，没有任何回复。仅能有发送出去的网络连接。
- block（阻塞）
任何进入的网络连接都被拒绝，并返回 IPv4 的 icmp-host-prohibited 报文或者 IPv6 的 icmp6-adm-prohibited 报文。只允许由该系统初始化的网络连接。
- public（公开）
用以可以公开的部分。你认为网络中其他的计算机不可信并且可能伤害你的计算机。只允许选中的连接接入。
- external（外部）
用在路由器等启用伪装的外部网络。你认为网络中其他的计算机不可信并且可能伤害你的计算机。只允许选中的连接接入。
- dmz（隔离区）
用以允许隔离区（dmz）中的电脑有限地被外界网络访问。只接受被选中的连接。
- work（工作）
用于工作网络。您可以基本相信网络内的其他电脑不会危害您的电脑。仅仅接收经过选择的连接。
- home（家庭）
用于家庭网络。您可以基本信任网络内的其他计算机不会危害您的计算机。仅仅接收经过选择的连接。
- internal（内部）
用于内部网络。您可以基本上信任网络内的其他计算机不会威胁您的计算机。仅仅接受经过选择的连接。
- trusted（信任）
可接受所有的网络连接。

### 6.2. 查看防区

#### 6.2.1. 列出所有防区

```sh
firewall-cmd --get-zones
```

#### 6.2.2. 查看当前活动的防区

```sh
firewall-cmd --get-active-zones
```

#### 6.2.3. 查看网卡的所属防区

```sh
firewall-cmd --get-zone-of-interface=eth0
```


### 6.3. 将网卡添加到指定防区

```sh
firewall-cmd --zone=dmz --permanent --add-interface=eth0
```

--permanent 永久生效

配置完后reload防火墙

### 6.4. 设置网卡默认的防区

网卡默认会使用public的防区

```sh
firewall-cmd --set-default-zone=dmz
```

立即生效无需重启

## 7. ipset

### 7.1. ipset的存储路径

`/etc/firewalld/ipsets/`

### 7.2. 常用命令

```sh
# 获取指定ipset信息
firewall-cmd --info-ipset=[ipset_name]

# 增加ipset
firewall-cmd --permanent --new-ipset=[ipset_name] --type=[type] --option
#其中option可不填，eg：–option=family=inet6指定该ipset使用IPV6地址。

# 删除指定ipset
firewall-cmd --permanent --delete-ipset=[ipset_name]
# 删除后，在ipset目录下会有一个备份文件，例如：原来的ipset为test_set.xml，则删除后会生成一个test_set.xml.old.

# 指定ipset中增加entry
firewall-cmd --permanent --ipset=[ipset_name] --add-entry=[xx.xx.xx.xx]

# 指定ipset中删除entry
firewall-cmd --permanent --ipset=[ipset_name] --remove-entry=[xx.xx.xx.xx]
```

### 7.3. ipset类型的区别

- hash:ip
- hash:ip,mark
- hash:ip,port
- hash:ip,port,ip
- hash:ip,port,net
- hash:mac
- hash:net
- hash:net,iface
- hash:net,net
- hash:net,port
- hash:net,port,net

## 8. 加入信任域

```sh
# IP
firewall-cmd --zone=trusted --add-source=192.168.1.100 --permanent
# 或网段
firewall-cmd --zone=trusted --add-source=192.168.1.0/24 --permanent
```

## 9. 打开端口

### 9.1. 查看所有打开的端口

```sh
firewall-cmd --zone=dmz --list-ports
```

### 9.2. 打开端口

#### 9.2.1. 对指定的防区打开端口

```sh
firewall-cmd --zone=dmz --permanent --add-port=8080/tcp
firewall-cmd --reload
```

- --permanent 永久生效

### 9.3. 移除端口

```sh
firewall-cmd --zone=dmz --permanent --remove-port=8080/tcp
firewall-cmd --reload
```

- --permanent 永久生效

#### 9.3.1. 允许指定IP访问端口

```sh
# 允许指定IP访问端口
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.0.200" port protocol="tcp" port="1-65535" accept'
# 或者
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source ipset=whitelist-app port protocol="tcp" port="1-65535" accept'

# 重新加载防火墙
firewall-cmd --reload
# 查看已经设置的规则
firewall-cmd --zone=public --list-rich-rules
```

- 也可直接编辑规则文件

```sh
vi /etc/firewalld/zones/public.xml
```

### 9.4. 打开服务

打开一个服务，类似于将端口可视化，服务需要在配置文件中添加，/etc/firewalld 目录下有services文件夹，这个不详细说了，详情参考文档

```sh
firewall-cmd --zone=dmz --permanent --add-service=smtp
```

- 移除服务

```sh
firewall-cmd --zone=dmz --permanent --remove-service=smtp
```
