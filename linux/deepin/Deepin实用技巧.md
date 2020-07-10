# Deepin实用技巧

[TOC]

## 1. 加入staff组

因为一般要将软件安装在 `/usr/local` 下并运行，所以要先将当前用户加入 `staff` 组。

```sh
sudo usermod -a -G staff `whoami`
```

## 2. 自动登录

`Control Center` > `Accounts` > 点击账户右边的 `>` > 打开 `Auto Login` 开关

## 3. 使用左手鼠标

1. `Control Center` > `Mouse` > 打开 `Left Hand`
2. 下载左手光标
   <https://www.gnome-look.org/content/show.php/Obsidian+(left+handed+version)?content=121197>
   或
   <https://raw.githubusercontent.com/nnzbz/notes/master/linux/deepin/121197-Obsidian_L.tar.gz>(需要翻墙)
3. 解压目录到 `~/.icons` 或 `/usr/share/icons/`
4. 在Deepin的外观设置界面看到这个光标主题，切换过去
   `Control Center` > `Personalization` > `Theme` > 选择 `Obsidian`

## 4. 安装五笔输入法

- 删除 `fcitx-table-wbpy` 的简繁转换快捷键
  `Fcitx Configuration` > 选择 `Addon` Tab页 > 双击 `Simplified Chiness To Tradiional Chinese` > 清空快捷键

- ~~安装 `ibus-wubi` (不稳定)~~

```sh
# 删除当前系统所有fcitx包
sudo apt remove fcitx* -y
# 自动清理所有孤立的包
sudo apt autoremove
# sudo apt install fcitx fcitx-table-wbpy fcitx-config-gtk fcitx-frontend-all  fcitx-ui-classic fcitx-tools fcitx-ui-kimpanel
sudo apt-get install ibus ibus-table ibus-table-wubi
# 这一步不做似乎也可以
echo -e "\n# 支持ibus启动\nexport GTK_IM_MODULE=ibus\nexport XMODIFIERS=@im=ibus\nexport QT_IM_MODULE=ibus" >> ~/.bashrc
# 清理一下冗余文件(这一步关键，否则下面im-config设置识别不了ibus)
sudo rm -f /usr/share/im-config/data/23_ibus.*
# 设定默认的输入法为ibus
im-config
....
```

如果安装命令出现提示没有依赖的错误，请运行下面的指令

```sh
sudo apt --fix-broken install -f
```

最后注销再重新进来，配置输入法(`Fcitx Configuration`)即可

## 5. 在文件管理器中修改后缀名

菜单 -> Settings -> Basic -> Open behavior -> 不要勾选 "Hide file extension when rename"

设置如下图

![修改后缀名](修改后缀名.png)

## 6. 让文件管理器有以管理员身份打开的功能

下载 admin-file-manager.zip
<https://bbs.deepin.org/forum.php?mod=attachment&aid=ODk2Njl8ZTU5NDkzNjd8MTU5NDM2NTUxMnwwfDE5MjA3MQ%3D%3D>

将压缩包中的文件解压到 /usr/share/deepin/dde-file-manager/oem-menuextensions 目录下，重新打开文件管理器即可

## 7. 解决deepin中vim无法复制文本到系统剪切板的问题

```sh
sudo apt-get install vim-gtk
```

然后使用 `"+y` 三个键就可以复制了

## 8. 添加ll命令

```sh
sudo vim ~/.bashrc
```

打开下面三行的注释

```txt
....
#alias ll='ls -l'
#alias la='ls -A'
#alias l='ls -CF'
....
```

执行

```sh
. ~/.bashrc
```

## 9. 字体

### 9.1. 更纱字体

<https://github.com/be5invis/Sarasa-Gothic/releases>

### 9.2. Deepin中使用Windows字体

- 只需要把Windows下 `/Windows/Fonts` 文件夹复制到 Deepin下 `/usr/share/fonts/`，再把Fonts改名为winfonts 即可
- 可以使用 `Gnome Tweak Tool` 来设置默认字体

## 10. 利用Deepin Terminal上传下载服务器的文件

- 服务器端安装rz和lz
  - CentOS

    ```sh
    yum -y install lrzsz
    ```

- 客户端配置 > Deepin Terminal > 右键 > `Remote management` > ....

- 上传与下载
  - 通过 `Remote management` 连接上服务器
  - 右键菜单: `上传文件` 、 `下载文件`

## 11. 跳板配置

配置 `~/.ssh/config` 文件

```ini
Host Relay
  hostname 跳板机地址
  user 跳板机用户
  port 跳板机端口

Host host-1-behind-Replay
  hostname 跳板机能访问的 host-1 的地址或者内网别名
  user 目标机器 host-1 的用户名
  port 目标机器 host-1 的 ssh 端口
  proxyjump Relay #使用的跳板机名称 这里就是上面配置的 Relay
  identityfile ~/.ssh/私钥
```

连接的时候 只要 `ssh host-1` 按 tab 自动补全 回车自动从 Relay 登录目标机器

如果临时要登录某机器 但是没配置 proxyjump 可以用 -J 参数临时指定
比如上面的配置 移除 proxyjump 配置后
`ssh host-1-behind-Replay -J Relay`
是等效的。
其他可以看 ssh config 的文档 还有很多高级用法，比如用 ssh-agent 或这个 gpg 管理秘钥等

## 12. 添加快捷方式

```sh
sudo vi /usr/share/applications/{文件名}.desktop
```

添加如下内容

```txt
[Desktop Entry]
Encoding=UTF-8
Name=eclipse  
Comment=Eclipse IDE  
Exec=/opt/eclipse/eclipse  
Icon=/opt/eclipse/icon.xpm  
Terminal=false  
StartupNotify=true  
Type=Application  
Categories=Application;Development;
```

- Exec
  代表应用程序的位置(如果要加参数要在前后空格再加)
- Icon
  代表应用程序图标的位置
- Terminal
  为false表示启动时不启动命令行窗口，值为true表示启动命令行窗口（建议false）
- Categories
  决定创建出的起动器在应用程序菜单中的位置

## 13. 微信不能打开

```sh
rm -rf ~/.deepinwine/Deepin-WeChat/*
```
