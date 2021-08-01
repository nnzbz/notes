# brew

[TOC]

## 1. brew简介

brew 又叫Homebrew，是Mac OSX上的软件包管理工具，能在Mac中方便的安装软件或者卸载软件， 只需要一个命令， 非常方便

brew类似ubuntu系统下的apt-get的功能

## 2. 官网

http://brew.sh/

## 3. 安装brew

```sh
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

## 4. 镜像更换为阿里云的源

<https://developer.aliyun.com/mirror/homebrew>

## 5. 使用brew

### 5.1. 安装软件

```sh
brew install wget
brew install git
```

Homebrew 会将软件包安装到独立目录，并将其文件软链接至 /usr/local

```sh
$ cd /usr/local
$ find Cellar
Cellar/wget/1.16.1
Cellar/wget/1.16.1/bin/wget
Cellar/wget/1.16.1/share/man/man1/wget.1

$ ls -l bin
bin/wget -> ../Cellar/wget/1.16.1/bin/wget
```

默认Homebrew会将软件安装在/usr/local/Cellar目录下，当然你也可以改变这个默认的路径

### 5.2. 搜索软件

```sh
brew search /wge*/
```

**注意：/wge\*/是个正则表达式**

### 5.3. 其它常用命令

|    命令     |            说明            |
| :---------- | -------------------------- |
| brew list   | 列出已安装的软件           |
| brew update | 更新brew                   |
| brew home   | 用浏览器打开brew的官方网站 |
| brew info   | 显示软件信息               |
| brew deps   | 显示包依赖                 |

### 5.4. 卸载软件

```sh
brew uninstall wget
```

### 5.5. 安装常用软件

```sh
brew install caskroom/cask/meld
```