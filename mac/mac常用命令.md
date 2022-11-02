# 1. Mac常用命令

[TOC]

## 1. 环境变量PATH

Mac系统的环境变量，加载顺序为：

1. /etc/profile         (系统级)
2. /etc/paths           (系统级)
3. ~/.bash_profile      (当前用户级)
4. ~/.bash_login        (当前用户级)
5. ~/.profile           (当前用户级)
6. ~/.bashrc            (当前用户级)

PATH的语法为如下

```ini
#中间用冒号隔开
export PATH=$PATH:<PATH 1>:<PATH 2>:<PATH 3>:------:<PATH N>
```

## 2. 查看本机IP地址

```sh
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## 3. 查看所有端口号

```sh
lsof -n -P -i TCP -s TCP:LISTEN
```

## 4. 将iso转换成dmg 转iso 用

UDRW 替换为 UDTO

```sh
sudo hdiutil convert -format UDRW -o /linux.dmg kali.iso

 Password:
 正在读取Master Boot Record（MBR：0）…
 正在读取Kali Live （Apple_ISO：1）…
 正在读取（Windows_NTFS_Hidden：2）…
 ............................................................................
 正在读取（DOS_FAT_12：3）…
 ..............................................................................
 已耗时：10.178s
 速度：288.3M 字节/秒
 节省：0.0%
 created: /linux.dmg
```

## 5. 格式化

```sh
# 格式化(注意usb_name命名不能用小写，要大写)
sudo diskutil eraseDisk exFAT usb_name MBRFormat /dev/disk[n]
```

exFAT可为MS-DOS或FAT32

## 6. 刻录ISO到U盘

```sh
# 找出U盘挂载路径
diskutil list
# 取消挂载U盘
diskutil umountDisk /dev/disk[n]
# 刻录U盘
dd if=***.iso of=/dev/disk[n] bs=4m; sync
# 加入r让写入速度加快
#dd if=***.iso of=/dev/rdisk[n] bs=4m; sync
# 用iostat命令查看磁盘写入状态
iostat -w 2
# 将U盘弹出
diskutil eject /dev/disk[n]
```
