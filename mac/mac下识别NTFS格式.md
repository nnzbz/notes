# mac下识别NTFS格式

[TOC]

## 1. 查看磁盘名称

```sh
diskutil list
```

## 2. 配置

```sh
sudo nano /etc/fstab
```

输入

```ini
LABEL=BOOTCAMP none ntfs rw,auto,nobrowse
```

## 3. 重启系统

## 4. 创建快捷方式

```sh
sudo ln -s /Volumes/BOOTCAMP ~/Desktop/BOOTCAMP
```
