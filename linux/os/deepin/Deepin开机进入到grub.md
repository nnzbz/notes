# Deepin开机进入到grub

## 新

1. 在grub下检查 `/efi/EFI/UOS` 目录下的grub文件有没问题
2. 查找启动分区

   ```sh
   # 逐个查看是否是Deepin的启动分区
   ls (hd0,gpt0)/grub/
   # 如果有内容，则应该是Deepin启动分区
   ```

3. 输入如下命令启动，即可进入系统

   ```sh
   set root=(hd1,gpt2)
   set prefix=(hd1,gpt2)/grub/
   normal
   ```

4. 进入系统后将 `/boot/efi/EFI/deepin` 目录下的文件复制到 `/boot/efi/EFI/UOS` 目录下

   ```sh
   cp -r /boot/efi/EFI/deepin/* /boot/efi/EFI/UOS/
   ```

5. 原因: Deepin系统新版本的grub启动是通过 `/boot/efi/EFI/UOS` 目录下的**efi**文件来调用 `/boot/efi/EFI/deepin` 目录下的**efi**文件来启动系统的
6. 最后发现是 `/boot/efi/EFI/UOS/grub.cfg` 这个文件不见了，还缺少其它几个文件。。。。

## 旧

1. 检查 `/boot/efi/EFI/ubuntu` 目录下的grub文件有没问题
2. 将 `/boot/efi/EFI/deepin` 目录下的文件复制到 `/boot/efi/EFI/ubuntu` 目录下
3. 原因: Deepin系统的grub启动是通过 `/boot/efi/EFI/ubuntu` 目录下的**efi**文件来调用 `/boot/efi/EFI/deepin` 目录下的**efi**文件来启动系统的，不知什么原因调用失败了(我这里可能是安装VirtualBox时破坏了这个文件)，干脆直接复制过来就好了
4. 最后发现是 `/boot/efi/EFI/ubuntu/grub.cfg` 这个文件的第二行，在 VirtualBox设置物理磁盘启动时改变错了路径。。。。

