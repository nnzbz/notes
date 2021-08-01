# 三种方式配置Mac OS X的启动项

[TOC]

收集来源
https://blog.csdn.net/abby_sheen/article/details/7817198

## 1. Login Items

打开System Preferences，选择System -> Accounts，选择Login Items选项卡，将/Applications目录下的.app直接拖进右边的列表中。重启电脑之后就会发现列表中的程序在开机之后就自动启动了。

## 2. StartupItems

StartupItems，顾名思义，就是在系统启动过程中运行的程序，它们可以是运行完就立即终止的程序（比如，开机清空废纸篓），也可以是一直持续在系统运行周期的后台进程。

StartupItems一般存放在以下两个路径下：

1）/System/Library/StartupItems

2）/Library/StartupItems

## 3. Launchd Daemon

launchd是Mac OS下用于初始化系统环境的关键进程，它是内核装载成功之后在OS环境下启动的第一个进程。

采用这种方式来配置自启动项很简单，只需要一个plist文件，通常（同时也是系统推荐）是将plist放在~/Library/LaunchAgents路径下。

