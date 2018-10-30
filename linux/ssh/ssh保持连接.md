# ssh保持连接

[TOC]

## 1. 优雅退出

敲下按键 ```~.```

## 2. 在客户端配置

```sh
vim ~/.ssh/config
```

（注意不是/etc/ssh/sshd_config文件）

后面添加

```text
Host *
  ServerAliveInterval 30
```

这表示要让所有的ssh连接自动加上此属性

- ServerAliveInterval 30
  指定向服务端请求消息的时间间隔，单位是秒

如果要指定服务端，如下：

```sh
# 使用-o的参数ServerAliveInterval来设置一个防止超时的时间
ssh -o ServerAliveInterval=30 IP地址
```

## 3. 在服务端配置

　　基于安全的理由，如果用户连线到 SSH Server 后闲置，SSH Server 会在超过特定时间后自动终止 SSH 连线。以下是设定终止连线时间的方法:

```sh
vim /etc/ssh/sshd_config
```

```text
TCPKeepAlive yes
。。。。
ClientAliveInterval 60
ClientAliveCountMax 60
```

如果每条最前面有#号，将那个#号删除，并修改想要的参数。

- TCPKeepAlive yes
  表示TCP保持连接不断开
- ClientAliveInterval 60
  指定服务端向客户端请求消息的时间间隔，单位是秒，默认是0，不发送。
- ClientAliveCountMax 60
  指服务端发出请求后客户端无响应则自动断开的最大次数。使用默认给的3其实也可以了。

修改后保存并关闭文件，重新启动 sshd:

```sh
systemctl restart sshd
```

另：

```sh
vim .bash_profile
```

编辑

```text
export TMOUT=1000000
```

```sh
. .bash_profile
```

## 4. 坑不停

上面基本就把现象，原因，处理方法都说得差不多了，不过，这里还要多说两句。

一般来说，不建议修改服务端。会涉及到权限问题，以及安全问题。还是比较推荐修改客服端或工具等的方法。查的过程有看到过说关于抓包看到服务器发包时握手问题的，具体原因……

还有，TCPKeepAlive，其实还有更深一层的意思和相关作用。但这里涉及的TCP心跳包，保活，探测报文等等……

与上面搭配的还有系统变量echo $TMOUT……