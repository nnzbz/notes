# Deepin安装常用软件

[TOC]

## 1. Git

```sh
# 不用每次 `push` 都要输入用户名和密码
git config --global credential.helper store
```

## 2. Chrome

在标题栏右键，去掉选择“Use system title bar and borders”。

## 3. 坚果云

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

## 4. VsCode

- 先在Deepin的应用市场中安装，然后检查更新，安装最新的版本
- 安装完后打开资源管理器默认就被vscode替换了，运行下面的指令

```sh
xdg-mime default dde-file-manager.desktop inode/directory
```

- 使用自定义标题栏
File-Preference-Settings-Window-Title Bar Style > “custom”

## 5. VirtualBox

```sh
sudo vi /etc/apt/sources.list

# 在文末加入下面这行
...
deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian apricot contrib
...

wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -

sudo apt-get update
sudo apt-get install virtualbox-6.1
```

## 6. electerm

Terminal/ssh/sftp client(linux, mac, win) based on electron/ssh2/node-pty/xterm/antd/subx and other libs.

不要从 Deepin 的 `App Store` 中安装，直接从下面的网址下载安装 <https://github.com/electerm/electerm/releases>

## 7. Remmina

从 Deepin 的 `App Store` 中安装，然后再更新

## 8. dbeaver

Deepin中的MySQL Workbench使用有问题，可以用这个软件代替

```sh
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
sudo apt-get update && sudo apt-get install dbeaver-ce
```
