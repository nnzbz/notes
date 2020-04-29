# Linux下启动物理盘上已安装的Windows系统

## 1. 准备

1. 创建一个没有硬盘的windows虚拟机，与已安装在物理硬盘上的系统一致。
2. 通过命令行在创建的虚拟机目录下创建一个指向物理硬盘的虚拟硬盘

```sh
# 下面这句注意不要用sudo
VBoxManage internalcommands createrawvmdk -filename /path/to/file.vmdk -rawdisk /dev/sda -partitions 1,2,3,4,5,8 -relative
sudo usermod -a -G disk $USER # 运行完此命令后，需要注销重新进来
```

- `/path/to/file.vmdk` 必须是绝对路径
- `-partitions` 指定了映射的分区，如没有则表示要映射整个磁盘(我的windows直接装在了一个完整的硬盘上，直接省略该选项)。具体可以用 `VBoxManage internalcommands listpartitions -rawdisk /dev/sda` 来查看分区号
- `-relative` 保证了创建出来的虚拟磁盘文件的可移植性，在sda1或者sda5的实际位置和大小变化后也可以用，没有这个参数的话到时候就要重新创建一遍vmdk文件了。
创建好可能会产生多个文件： `xxx.vmdk` 和 `xxx-pt.vmdk` ，实际在虚拟机里使用 `xxx.vmdk` ，`xxx-pt.vmdk` 需要存在。

3. 在创建的虚拟机中加载刚创建的vmdk虚拟硬盘。
4. `Settings` > `System` > `Motherboard` > 选择 `Enable EFI(special OSes only)`
5. 正常启动虚拟机，一切搞定。
6. 当然，要在虚拟机里用得爽，就要把配置搞好，并安装上extension包里的guest additions。

## 2. 翻车现场

我安装启动的时候，碰到运行到grub的命令行下就完了，这时候需要如下设置

- 在宿主机上编辑 `grub.cfg` 文件

```sh
sudo vi /boot/efi/EFI/ubuntu/grub.cfg
```

- 原内容如下

```sh
search.fs_uuid fd768300-aeea-461c-93e8-c8db81eb3fb2 root hd1,gpt1
set prefix=($root)'/boot/grub'
configfile $prefix/grub.cfg
```

- 修改内容如下

```sh
search.fs_uuid fd768300-aeea-461c-93e8-c8db81eb3fb2 root hd1,gpt1
set prefix=($root)'/boot/grub'
if [ -f $prefix/grub.cfg ]
then
    configfile $prefix/grub.cfg
else
    insmod chain
    set root=(hd0,gpt2)
    chainloader /EFI/Microsoft/Boot/bootmgfw.efi
    boot
fi
```
