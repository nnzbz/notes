# Linux常用命令

[TOC]

## 1. 软件操作

### 1.1. 修改UTF-8

- CentOS7

```sh
vi /etc/locale.conf
```

```ini
LANG="en_US.UTF-8"
```

```sh
. /etc/locale.conf
```

### 1.2. 修改hostname

- CentOS7

```sh
# 查看
hostname
# 修改
hostnamectl set-hostname www.xxx.com
# 再次查看
hostname

# 在/etc/hosts文件的127.0.0.1的末尾添加hostname
vi /etc/hosts
# 省略
```

### 1.3. 查看版本

```sh
cat /etc/*-release
```

### 1.4. 查看软件安装到了哪些地方

- ubuntu

```sh
dpkg -L lantern
```

## 2. 时间

### 2.1. 查看当前时间

```sh
date
```

### 2.2. 修改年月日时分秒

```sh
date -s "2017-10-11 21:56:00"
```

### 2.3. 将系统时间写入到BIOS

上面修改完时间后，不要忘记同步写入到BIOS的时间，否则重启后，时间又会变回来

```sh
clock -w
```

## 3. 历史

- 查看历史

```sh
history
```

- 清除所有历史

```sh
history -c
```

- 查看及编辑历史的存储文件

```sh
vi ~/.bash_history
```

- 重新加载修改历史存储文件后的文件内容

```sh
history -r
```

## 4. 文件/目录操作

### 4.1. 当前目录

```sh
pwd
```

### 4.2. 添加一行到文件末尾

```sh
# 追加
echo abcdefg >> a.txt
# 覆盖
echo abcbedf > a.txt
```

### 4.3. 复制当前目录下所有文件和目录到另一个目录

```sh
cp -r src/main/resources/. /usr/local/luban-captcha-svr/9101
```

### 4.4. 远程复制

从远程往本地复制文件或目录(如果是反向复制，把目录和源的位置反过来就可以了)

```sh
scp -P 2222 -r root@www.vpser.net:/root/lnmp0.4/ /home/lnmp0.4/
```

> **注意: 路径最后必须是一个“/”表示是一个目录，而且target的目录要预先创建好**

- -P 2222
 表示更改SSH端口后的端口，如果没有更改SSH端口可以不用。
- -r
 参数表示递归复制（即复制该目录下面的文件和目录）。
- -v
 和大多数 linux 命令中的-v意思一样，用来显示进度。可以用来查看连接，认证，或是配置错误。

> **注意：如果路径中有特殊字符，用双引号把路径括起来，并且在特殊字符前加上 ```\\``` 。**

### 4.5. 查找文件及内容

#### 4.5.1. 查找文件

```sh
find / -name filename
```

- -type d/f
  查找的类型是目录/文件

#### 4.5.2. 查找内容

```sh
grep -rl "keyword" ./
```

### 4.6. 批量重命名

批量重命名多个目录下文件名

- centos

```sh
for i in `find . -name logo.png`; do mv $i `echo $i | sed 's/logo.png$/logo3.png/'`; done
```

- ubuntu

```sh
find . -name "zboss*" -exec rename 's/zboss/rebue/' {} \;
```

- mac

与 ubuntu 一样，但需要先安装 rename

```sh
# 修改目录权限
sudo chown -R $(whoami) /usr/local/sbin /usr/local/share/man/man7
# 安装rename
brew install rename
# 将目录权限改回来
sudo chown -R root /usr/local/sbin /usr/local/share/man/man7
```

> **注意:{}与\之间一定要留有空格**

### 4.7. 批量修改文件内容

```sh
sed -i "s/原字符串/新字符串/g" `grep 原字符串 -rl 所在目录`
```

- 例如：把mahuinan替换 为huinanma

```sh
sed -i "s/mahuinan/huinanma/g" 'grep mahuinan -rl /www'
```

### 4.8. 批量删除

- 方法1
批量删除目录下级的多个目录或文件

```sh
find 查找目录 -type f -name ".class" -exec rm -rf {} \;
```

- ```查找目录```：待查找的开始目录，搜索其下的子目录

- ```-type f```：文件类型为普通文件   若查找的目标文件是目录，则用 -type d

- ```-name ".class"```：表示文件名与"*.class"匹配，双引号不能少！

- ```rm -f {}``` : 删除时，不提示，{}表示查找到的文件

- 方法2

```sh
find . -name "*.png" | xargs rm -rf
```

## 5. 后台执行程序

### 5.1. 后台执行命令

```sh
nohup <command> >> /usr/local/output.log 2>&1 &
```

- 执行命令后会输出程序后台运行的PID

### 5.2. 查看命令运行情况

执行命令后可以用 ```jobs -l``` 查看后台运行情况，但是退出当前命令窗口即失效，这时可用 ```ps``` 查看，本文下面有详解

### 5.3. 停止后台执行程序

用 ```kill -9 <PID>```

## 6. 进程操作

### 6.1. 查看进程PID（过滤掉本身grep的进程）

```sh
ps aux|grep java|grep -v grep
```

### 6.2. 查看端口号的进程

```sh
# linux
netstat -anp|grep 8080
# Mac
lsof -i:8080
```

## 7. 定时自动关机

### 7.1. 编辑任务命令

```sh
crontab -e -u root
```

- **-u \<user>**
 设定指定 user 的时程表，这个前提是你必须要有其权限(比如说是 root)才能够指定他人的时程表。如果不使用 ```-u user``` 的话，就是表示设定自己的时程表

### 7.2. 编辑任务内容

格式

```text
t1 t2 t3 t4 t5 program
```

其中 t1 是表示分钟，t2 表示小时，t3 表示一个月份中的第几日，t4 表示月份，t5 表示一个星期中的第几天。program 表示要执行的程式。

例如每天的19点关机

```text
30 18 * * * /usr/sbin/shutdown -h 30
```

### 7.3. 查看任务

```sh
crontab -l
```

### 7.4. 删除当前用户的任务

```sh
crontab -r
```

### 7.5. 查看执行任务是否出错

cron的日志存放在 `/var/log/cron`，默认邮件日志存放在 `/var/spool/mail/root` (root账户)

## 8. 创建软硬链接

- 链接分为有软链接(symbolic link)和硬链接(hard link)
- 软连接又叫符号连接，相当于Windows下的快捷方式
- 硬链接就像一个文件有多个文件名，源文件名和链接文件名都指向相同的物理地址
- 不可以对 **文件夹** 建立硬连接

```sh
ln    source dist     # 建立硬链接
ln -s source dist     # 建立软链接
```

## 9. 挂/卸载U盘

### 9.1. mount挂载

以root用户登录

先加载USB模块

```sh
modprobe usb-storage
```

用 ```fdisk -l``` 看看U盘的设备，假如U盘是sdb

确定在 目录 ```/mnt``` 下建立了 文件夹 ```/usb``` ，如果未建立可键入一下命令：```mkdir /mnt/usb_disk``` ，成功后进行下一步。

载入 u 盘，需键入以下命令：

```sh
mount /dev/sda /mnt/usb_disk
```

成功后，即可使用 u 盘了, 文件就在目录 ```/mnt/usb_disk``` 下。

### 9.2. umount卸载

卸载u盘：在使用完u盘后，在拔出前需要先键入卸载U盘命令

```sh
umount /mnt/usb_disk
```

## 10. 自动挂载

- 查看磁盘分区的UUID

  ```sh
  sudo blkid
  ```

- 配置开机自动挂载

  ```sh
  sudo vi /etc/fstab
  ```

  - 第1列是设备名或者卷标
  - 第2列是挂载点（也就是挂载目录）
  - 第3列是所要挂载设备的文件系统或者文件系统类型
  - 第4列是挂载选项，通常使用defaults就可以
  - 第5列设置是否使用dump备份，置0为不备份，置1，2为备份，但2的备份重要性比1小
  - 第6列设置是否开机的时候使用fsck检验所挂载的磁盘，置0为不检验，置1，2为检验，但置2盘比置1的盘晚检验。

- 检验

  ```sh
  mount -a
  df -h
  ```

## 11. 将iso文件刻录到u盘

### 11.1. 确认U盘路径

```sh
# Ubuntu
sudo fdisk -l
# Mac
diskutil list
```

Mac返回如下：

```cmd
/dev/disk4 (internal, physical):
        #:                  TYPE NAME      SIZE IDENTIFIER
        0:     Apple_partition_scheme   *2.0 GB disk4
        1:        Apple_partition_map    4.1 KB disk4s1
        2:                  Apple_HFS    2.4 MB disk4s2
```

说明U盘是disk4，不需要加后面的s1或s2

### 11.2. dd命令

格式如下

```sh
sudo dd if=xxx.iso of=/dev/sdb bs=200m
```

- xxx.iso
 你的ISO镜像文件的路径，
- of=/dev/sdb
 后面是你的U盘路径，Ubuntu一般就是/dev/sdb或者/dev/sdc（后面不要带1或者2的数字），Mac如上面就是/dev/disk4（后面不要带s1或者s2）。
- bs=xxxm
 一次读取到缓冲的字节