# wine入门

[TOC]

## 1. 安装与配置

### 1.1. 前提

- Homebrew

### 1.2. 安装

用brew安装

```sh
brew install wine --devel
brew install winetricks
```

- devel参数
 安装最新的开发版，如果没有此参数，则安装最新的稳定版，而由于Wine的开发版也比较稳定，所以一般加上此参数
- 安装winetricks
 winetricks安装不是必须的，但它可以帮助我们更加方便的安装一些windows的程序

### 1.3. 配置

在终端运行

```sh
winecfg
```

## 2. 运行

```sh
wine program.exe
```
