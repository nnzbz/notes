# 记录一次容器内访问不了MySQL的问题

[TOC]

## 1. 问题描述

我在创建xxl-job-admin容器时，使用如下命令

```sh
docker run --name xxl-job-admin -e PARAMS="--spring.datasource.url=jdbc:mysql://10.10.205.54:3306/xxl_job?Unicode=true&characterEncoding=UTF-8 --spring.datasource.username=xxl_job --spring.datasource.password=xxxxxxx" -dp 11080:8080 -v /var/log/xxl-job:/data/applogs --restart=always xuxueli/xxl-job-admin:2.2.0
```

`10.10.205.54`是MySQL容器的宿主机的局域网IP地址，其实与xxl-job-admin容器在同一台机上，但是这不是问题

查看日志，可以看到

```ini
....

The last packet sent successfully to the server was 0 milliseconds ago. The driver has not received any packets from the server.
	at sun.reflect.GeneratedConstructorAccessor43.newInstance(Unknown Source)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
	at com.mysql.cj.exceptions.ExceptionFactory.createException(ExceptionFactory.java:61)
	at com.mysql.cj.exceptions.ExceptionFactory.createException(ExceptionFactory.java:105)
	at com.mysql.cj.exceptions.ExceptionFactory.createException(ExceptionFactory.java:151)
	at com.mysql.cj.exceptions.ExceptionFactory.createCommunicationsException(ExceptionFactory.java:167)
	at com.mysql.cj.protocol.a.NativeSocketConnection.connect(NativeSocketConnection.java:91)
	at com.mysql.cj.NativeSession.connect(NativeSession.java:144)
	at com.mysql.cj.jdbc.ConnectionImpl.connectOneTryOnly(ConnectionImpl.java:956)
	at com.mysql.cj.jdbc.ConnectionImpl.createNewIO(ConnectionImpl.java:826)
	... 12 common frames omitted
Caused by: java.net.NoRouteToHostException: No route to host (Host unreachable)
	at java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.net.Socket.connect(Socket.java:607)
	at com.mysql.cj.protocol.StandardSocketFactory.connect(StandardSocketFactory.java:155)
	at com.mysql.cj.protocol.a.NativeSocketConnection.connect(NativeSocketConnection.java:65)
	... 15 common frames omitted

....
```

## 2. 判断问题

我估计可能是防火墙挡住了，于是将防火墙停掉，果然就没有问题了。

## 3. 解决问题

先查出docker0的ip

```sh
ifconifg
```

我查到是 `172.17.0.1`，这说明docker将容器的IP分配在 `172.17.0.0/16` 范围内

将  `172.17.0.0/16` 加入我之前配置的白名单内

```sh
ipset add whitelist 172.17.0.0/16
```

但是报 `Hash is full, cannot add more elements` 的错误，原来是之前建立 whitelist 时用的是 `hash:ip` 类型，此类型不能用范围段，只好将其改为 `hash:net`，再运行上面的命令

这回没有报错了，可是用下面的命令一查，却不起效

```sh
firewall-cmd --info-ipset=whitelist
```

于是只好硬加入

```sh
vi /etc/firewalld/ipsets/whitelist.xml
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<ipset type="hash:net">
  <entry>172.17.0.0/16</entry>
  <entry>xxx.xxx.xxx.xxx</entry>
  <entry>xxx.xxx.xxx.xxx</entry>
</ipset>
```

重启防火墙

```sh
firewall-cmd --reload
```

这回成功了，再一看xxl-job-admin日志也没有问题了
