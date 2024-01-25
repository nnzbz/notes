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

## 4. 使用代理

- 每次新的终端都设置一次

```sh
export ALL_PROXY=socks5://127.0.0.1:1086
```

## 5. 镜像更换为阿里云的源

<https://developer.aliyun.com/mirror/homebrew>
<https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/>

## 6. 使用brew

### 6.1. 安装软件

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

### 6.2. 搜索软件

```sh
brew search /wge*/
```

**注意：/wge\*/是个正则表达式**

### 6.3. 其它常用命令

|    命令     |            说明            |
| :---------- | -------------------------- |
| brew list   | 列出已安装的软件           |
| brew update | 更新brew                   |
| brew home   | 用浏览器打开brew的官方网站 |
| brew info   | 显示软件信息               |
| brew deps   | 显示包依赖                 |

### 6.4. 卸载软件

```sh
brew uninstall wget
```

### 6.5. 安装常用软件

```sh
brew install caskroom/cask/meld
```

### 6.6. 文件下载的目录

如果 brew install 工具时下载错误，可以直接从浏览器下载，然后放到下面的目录就可以了。

```sh
/Users/XXXX/Library/Caches/Homebrew
```