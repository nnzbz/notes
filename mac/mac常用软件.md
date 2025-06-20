# mac常用软件

[TOC]

## 1. Screen Utility

测试屏幕的软件

## 2. iTerm2

比较好用的终端软件

## 3. Amphetamine

防止mac休眠的软件

## 4. meld

跨平台的比较软件，在ubuntu和mac下都可以使用

先安装brew，然后

```sh
brew install Caskroom/cask/xquartz
brew install pygtk
brew cask install caskroom/cask/meld
```

## 5. NTFS

NTFS-X

<https://github.com/Sailiy/ntfsx>

Seagate Paragon Driver（希捷移动硬盘驱动）

<https://www.seagate.com/support/downloads/>

## 6. Xnip

截图、滚动截图、添加注释

## 7. Unarchiver

压缩、解压缩软件

## 8. gnu-getopt

命令行解析参数的工具(系统自带的getopt不支持长参数)

```sh
brew install gnu-getopt
# linked in /usr/local/bin/
brew link --force gnu-getopt
```

## 9. lfs

支持GitHub上传可以超过100M

```sh
brew update
brew install git-lfs
git lfs install
```

## 10. Another Redis Desktop Manager

Redis图形界面客户端

```sh
brew install another-redis-desktop-manager
```

## 11. UNetbootin

记录U盘启动的工具

## 12. mvnd

```sh
brew install mvndaemon/homebrew-mvnd/mvnd
```

## 13. Scroll Reverser

设置鼠标和触摸板滚轮的方向相反

<https://pilotmoon.com/scrollreverser/>

## 14. Typora

**一个仅仅需要修改官方配置文件的方法，非破解版**

1. 去官网下载<https://typoraio.cn/>官方软件
2. command+space，输入 `/Applications/Typora.app/Contents/Resources/TypeMark/` 并打开文件夹
3. 编辑 `/Applications/Typora.app/Contents/Resources/TypeMark/page-dist/static/js/Licenselndex.*.chunk.js` 文件
4. 全文搜索 `e.hasActivated` 找到 `hasActivated="true"==e.hasActivated`
6. 将后面的 `e.hasActivated` 修改为 `"true"`
