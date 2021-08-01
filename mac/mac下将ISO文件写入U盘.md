# mac下将ISO文件写入U盘

[TOC]

## 1. 卸载U盘

插入U盘，然后将其卸载，有如下两种方式卸载

- 磁盘工具

在磁盘工具里面找到U盘，把它卸载。

注意在这里看到设备是 ```disk2s4```

- 或者在终端里面使用命令:

```sh
diskutil unmount /Volumes/usb
```

## 2. 使用 dd 命令

```sh
sudo dd if=~/Downloads/VM/Win10_1803_English_x64.iso  of=/dev/disk2 bs=10m
```

- 参数if
 输入文件名，就是iso的文件名
- 参数of
 输出文件名

## 3. 等待

dd 命令将会执行很长的时间，等待就好了