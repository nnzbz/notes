# tcpdump监听http

[TOC]

## 1. http过滤

过滤命令：

```sh
tcpdump -i ens33 -A -v -s 0 'tcp port 8000 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

过滤说明：
（1）ens33是网卡号，一般是eth0，可以通过 `tcpdump -D` 查看
（2）8000是监听的端口号
（3）接受和回复的http报文的header和body可以以ascii 显示，非常直观
（4）区分每一次连接看端口号，端口号不变时，说明是一次长连接还没结束，端口号变化时，说明连接重新建立
（5）在端口号port前加上src或者des时，只会打印接受或回复的http报文内容
（6）tcpdump通过这种方式抓捕http报文非常方便，可视化，再结合打印时间，可更好定位分析某个时段的http报文数据，可以不需要再借助wireshark去解析

## 2. 文件分析

可通过文件的形式把抓到的报文数据保存在文件中，在通过过滤方式读取文件内容

(1) 将之指定的接口和端口号输入到文件中保存起来

```sh
tcpdump -i ens33 port 8000 -w 1.pcap
```

(2) 读取pcap文件

```sh
tcpdump -nAr 1.pcap
```

## 3. tcpdump一些参数说明

-A ascii 显示
只使用 ascii 打印报文的全部数据

-X hex/ascii 显示
同时用 hex 和 ascii 显示报文的内容

-s 报文字节数
tcpdump 默认只会截取前 96 字节的内容，要想截取所有的报文内容，可以使用 -s number， number 就是你要截取的报文字节数，如果是 0 的话，表示截取报文全部内容。

-i interface 接口
-i any 监听所有的网卡

-v / -vv / -vvv verbose
显示更多的详细信息

host
过滤某个主机的数据报文
tcpdump host 1.2.3.4

src/dst
过滤源地址和目的地址
tcpdump src 2.3.4.5
tcpdump dst 3.4.5.6
