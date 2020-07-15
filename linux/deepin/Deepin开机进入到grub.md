# Deepin开机进入到grub

1. 检查 `/boot/efi/EFI/ubuntu` 目录下的grub文件有没问题
2. 将 `/boot/efi/EFI/deepin` 目录下的文件复制到 `/boot/efi/EFI/ubuntu` 目录下
3. 原因: Deepin系统的grub启动是通过 `/boot/efi/EFI/ubuntu` 目录下的**efi**文件来调用 `/boot/efi/EFI/deepin` 目录下的**efi**文件来启动系统的，不知什么原因调用失败了(我这里可能是安装VirtualBox时破坏了这个文件)，干脆直接复制过来就好了