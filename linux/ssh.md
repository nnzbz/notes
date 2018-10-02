# ssh

一.在Linux server去设置SSH保持连接时间:

　　基于安全的理由，如果用户连线到 SSH Server 后闲置，SSH Server 会在超过特定时间后自动终止 SSH 连线。以下是设定终止连线时间的方法:

　　1、打开 /etc/ssh/sshd_config 文件，找到一个参数为 ClientAliveCountMax，它是设定用户端的 SSH 连线闲置多长时间后自动终止连线的数值，单位为分钟。

　　2、如果这一行最前面有#号，将那个#号删除，并修改想要的时间。

　　3、修改后保存并关闭文件，重新启动 sshd:

　　systemctl restart sshd

　　4. vim .bash_profile

　　export TMOUT=1000000

　　---------

二.保持ssh连接不断开

用ssh连接服务端，一段时间不操作或屏幕没输出（比如复制文件）的时候，会自动断开

解决：（2种办法）
1、在客户端配置
#vi /etc/ssh/ssh_config（注意不是/etc/ssh/sshd_config文件）,后面添加
Host *
ServerAliveInterval 30
这表示要让所有的ssh连接自动加上此属性；如果要指定服务端，如下：
使用-o的参数ServerAliveInterval来设置一个防止超时的时间
ssh -o ServerAliveInterval=30 IP地址

2、在服务端配置
编辑服务器 /etc/ssh/sshd_config，最后增加
ClientAliveInterval 60
ClientAliveCountMax 1
这 样，SSH Server 每 60 秒就会自动发送一个信号给 Client，而等待 Client 回应

　　---------

三.修改server和连接终端

Linux系统server

在linux系统中使用ssh连接远程服务器时，可以使用-o的一个参数ServerAliveInterval来设置防止超时的时间。

比如：ssh -o serveraliveinterval=60 username@hostIP

服务器配置修改

修改ssh配置文件/etc/ssh/sshd_config，添加或者修改ClientAliveInterval为“ClientAliveInterval 60”。这个参数的是意思是每1分钟，服务器向客户端发一个消息，用于保持连接。保存后记得重启ssh服务。

修改过后，上面几个办法都可以让ssh保持连接，一直处于alive状态，不会因为没有操作而被服务器强制断线了。

 

终端：

使用SecureCRT连接远程服务器，在会话选项 -> 终端设置中勾选“发送协议 NO-OP”。

使用putty连接远程服务器，找到Connection -> Seconds between keepalives ( 0 to turn off )， 默认为0，改为60。



 

　　---------

 四.如何退出退出无响应的 SSH 连接

有时候会发现 ssh 挂在那里没有响应了，可能是客户端的问题，也可能是服务器端的问题，也可能是客户端和服务器之间的网络问题；可能是客户端电脑休眠后连接断了、可能是网络断了、可能是 WiFi 信号不好、可能是网络延迟大了、可能是服务器挂了、也可能是服务器上的 sshd 进程挂了，…，可能是技术问题，也可能是非技术问题，可以找出无数可能。

有时我们离开办公桌前忘了退出 ssh 会话，或者工作的时候长时间 ssh 到服务器上忘记断开，之后发现那些没退出的 ssh 会话还挂在那里，无法退出、无法 Ctrl+C、无法做任何操作。通常我们就直接关闭 Terminal 后重新开一个新的；如果用的不是图形系统，没有窗口可以关闭，那还要启用另一个终端找到相关进程后 kill 掉。这里有一个小技巧，在那些没退出的 ssh 会话里用 ~. “优雅” 的断开连接。

可以这样操作：先 按“回车” 换行 再 按“shift + ` ”再按 “. ”

我们man 一下 ssh来看看：



　　其实Linux本身已经提供了很多便利的操作，只是我们需要多学习。

　　---------

 　　附录：附上之前我写的那句简单粗暴的命令，反思一下。

　　kill -9 `ps -ef |grep ssh |grep StrictHostKeyChecking | awk '{print $2}'`