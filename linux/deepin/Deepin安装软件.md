# Deepin安装常用软件

[TOC]

## 1. Git

```sh
# 不用每次 `push` 都要输入用户名和密码
git config --global credential.helper store
```

## 2. 坚果云

如果安装后启动没反应

```sh
vi ~/.nutstore/dist/bin/nutstore-pydaemon.py
```

将 50 行注释即可

```py
    ....
    # gi.require_version('Notify', '0.7')
    ....
```

## 3. VisualStudioCode

1. 先在Deepin的应用市场中安装，然后检查更新，安装最新的版本
2. 安装完后打开资源管理器默认就被vscode替换了，运行下面的指令

```sh
xdg-mime default dde-file-manager.desktop inode/directory
```

## 4. VirtualBox

```sh
sudo apt-get install virtualbox-6.1
```
