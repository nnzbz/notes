# Deepin安装常用软件

[TOC]

## 1. Git

```sh
sudo apt install git
# 不用每次 `push` 都要输入用户名和密码
git config --global credential.helper store
```

## 2. Chrome

在标题栏右键，去掉选择“Use system title bar and borders”。

如果右键没有，`[Settings]` -> `[Appearance]` -> 去掉选择“Use system title bar and borders”。

## 3. 坚果云

- 下载
  <https://www.jianguoyun.com/s/downloads/linux>
- 安装
  参考 `How to install Nutstore for KDE/XFCE`
- 如果安装后启动没反应

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

### 5.1. 下载deb文件安装

- 下载debian 10的版本
   <https://www.virtualbox.org/wiki/Linux_Downloads>
- **注意: 一定要用root账户安装**

  ```sh
  sudo -i
  apt install virtualbox-6.1_X.X.XX-XXXXXX_Debian_buster_amd64.deb
  ```

### 5.2. ~~通过apt安装~~(有问题)

**此方法安装后，会发现重启系统启动不成功，报错找不到模块`vs_???`**

```sh
sudo vi /etc/apt/sources.list

# 在文末加入下面这行
...
deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian buster contrib
...

wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -

sudo apt-get update
sudo apt-get install virtualbox-6.1
```

### 5.3. 记录一次安装VirtualBox后重启进不了系统的问题

- 安装VirtualBox后重启进不了系统，提示
  
  ```sh
  FAT-fs(...): IO charset ascii not found
  ....
  Give root password for maintenance
  (or press Control-D to continue):
  ```

- 原因
  deepinV20用的5.3.0-3内核，安装VirtualBox6.1时居然自动安装了5.3.0-42内核

- 解决方法
  删除42内核即可
- 步骤
  
  ```sh
  # 先输入密码登录进来
  ....
  # 查询内核安装情况
  dpkg --get-selections | grep linux
  # 删除多余内核(两个42内核都要删)
  apt-get remove linux-image-usigned-5.3.0-42-generic
  apt-get remove linux-modules-5.3.0-42-greneric
  # 重启系统
  reboot
  ```

## 6. mysql-workbench

```sh
sudo apt install com.mysql.workvbench
```

## 7. snap

包管理器(安装postman需要使用)

```sh
sudo apt install snapd
```

## 8. postman

```sh
# 需安装snap
snap install postman
```

## 9. XMind

1. 官网
   https://www.xmind.cn/download/
2. 下载deb的版本(不要用 **snap** 来安装，否则保存窗口会乱码)
   https://www.xmind.cn/xmind/downloads/XMind-2020-for-Linux-amd-64bit-10.2.1-202008051959.deb
3. 双击运行下载的文件进行安装



## 10. PyCharm

```sh
# 需安装snap
snap install pycharm-community --classic
```

## 11. electerm

Terminal/ssh/sftp client(linux, mac, win) based on electron/ssh2/node-pty/xterm/antd/subx and other libs.

不要从 Deepin 的 `App Store` 中安装，直接从下面的网址下载安装 <https://github.com/electerm/electerm/releases>

## 12. Remmina

从 Deepin 的 `App Store` 中安装，然后再更新

## 13. dbeaver

Deepin中的MySQL Workbench使用有问题，可以用这个软件代替

```sh
wget -O - https://dbeaver.io/debs/dbeaver.gpg.key | sudo apt-key add -
echo "deb https://dbeaver.io/debs/dbeaver-ce /" | sudo tee /etc/apt/sources.list.d/dbeaver.list
sudo apt-get update && sudo apt-get install dbeaver-ce
```
