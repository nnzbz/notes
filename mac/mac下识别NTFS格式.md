# ~~mac下识别NTFS格式~~

[TOC]

## 1. 查看磁盘名称

```sh
diskutil list
```

## 2. 配置

```sh
sudo vi /etc/fstab
```

输入

```ini
LABEL=<磁盘名称> none ntfs rw,auto,nobrowse
```

## 3. 重启系统

如果是 MAC 本身分区后的硬盘（譬如windows系统盘），则需要重启电脑才会生效。

## 4. 创建快捷方式

```sh
sudo ln -s /Volumes/<磁盘名称> ~/Desktop/<自定义名称>
```
