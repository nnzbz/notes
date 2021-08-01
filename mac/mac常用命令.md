# 1. Mac常用命令

[TOC]

## 1. 查看本机IP地址

```sh
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## 2. 查看所有端口号

```sh
lsof -n -P -i TCP -s TCP:LISTEN
```

## 3. 将iso转换成dmg 转iso 用

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

## 4. 格式化

```sh
# 格式化(注意usb_name命名不能用小写，要大写)
sudo diskutil eraseDisk exFAT usb_name MBRFormat /dev/disk[n]
```

exFAT可为MS-DOS或FAT32

## 5. 刻录ISO到U盘

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
