# 建立SSH互信

[TOC]

## 1. 建立A登录B的信任通道

### 1.1. 在A主机中生成RSA密钥

```sh
$ ssh-keygen -t rsa
Enter file in which to save the key (/Users/mac/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /Users/mac/.ssh/id_rsa.
Your public key has been saved in /Users/mac/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:nBFO0s1HDwkFSGGBIbHWH4XFNpkNamT68RTQFaQg+PE mac@macdeMacBook-Pro.local
The key's randomart image is:
+---[RSA 2048]----+
|    oo+=%%B%Bo   |
|    .+oX+=Xo+o   |
|    o.ooB.oo  .  |
|   .  .=EB       |
|        S .      |
|                 |
|                 |
|                 |
|                 |
+----[SHA256]-----+
```

注意上面有三处需要输入信息，分别是：

- 存储公私钥的文件夹位置，如果不输入，则默认为 ```~/.ssh/``` ，文件名则默认是 ```id_rsa``` 和 ```id_rsa.pub```
- 使用该公私钥时是否需要密码，如果不输入则表示不需要密码
- 再次确认是否需要密码

### 1.2. 将A主机生成的公钥复制到B主机

将刚才创建的 ```~/.ssh/id_rsa.pub``` 文件中的内容拷贝添加到B主机上的 ```~/.ssh/authorized_keys``` 文件中(如果没有则创建一个)，这个时候就建立了一条A登录B的信任通道。

```sh
scp ~/.ssh/id_rsa.pub root@主机IP:/root/.ssh/authorized_keys
```

注意这个信任通道是有方向性的，如果要建立从B登录A的信任通道，则操作步骤和上面的类似，只不过要反过来。

## 2. 建立B登录A的信任通道(略)

按上面的步骤反着来就可以。

## 3. 当重装一端的系统后

在未重装的一端运行

```sh
vim ~/.ssh/known_hosts
```

删除另一端的授信，否则连接报错
