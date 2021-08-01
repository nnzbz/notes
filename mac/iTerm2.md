# iTerm2

[TOC]

## 1. 防止阿里云中断连接（对所有ssh的终端适用）

```sh
vim /etc/ssh/sshd_config
```

找到下面两行

```ini
#ClientAliveInterval 0
#ClientAliveCountMax 3
```

去掉注释，改成

```ini
ClientAliveInterval 30
ClientAliveCountMax 10
```

这两行的意思分别是
1、客户端每隔多少秒向服务发送一个心跳数据
2、客户端多少秒没有相应，服务器自动断掉连接
重启sshd服务

```sh
service sshd restart
```

## 2. ssh登陆Linux是终端提示cannot change locale (UTF-8)

iTerm菜单 > Preferences... > 在右上角查询 set locale variables automatically > 取消选中

## 3. 启用 ```⌥←``` 和 ```⌥→``` 向前或向后跳过一个单词

By default in iTerm 2, it's a pain to skip between words.

Here's how you can configure iTerm 2 on OSX to allow you to use ⌥ ← and ⌥→ to do just that.

First you need to set your left ⌥ key to act as an escape character.

Picture

Second you need to either locate the current shortcut for ⌥ ← or create a new one, in the Profile Shortcut Keys, with the following settings:

Keyboard Shortcut: ⌥←
Action: Send Escape Sequence
Esc+: b
Picture

Third, repeat for the ⌥→ keyboard shortcut with the following settings:

Keyboard Shortcut: ⌥→
Action: Send Escape Sequence
Esc+: f
You're done! Now you can skip entire words on the command line by holding down the left ⌥ key and hitting ← or →

To make this work for the right option key you need to set the key modifier to act as an Escape Sequence, a la the first step.
