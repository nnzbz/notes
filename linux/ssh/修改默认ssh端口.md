# 修改默认SSH端口

## 1. 先用防火墙打开端口

* CentOS

```sh
firewall-cmd --permanent --zone=public --add-port=xxxxx/tcp
firewall-cmd --reload
```

* Ubuntu

```sh
sudo ufw allow xxxxx/tcp
sudo ufw reload
```

## 2. 修改SELinux

- 查看当前SElinux 允许的ssh端口：

```sh
semanage port -l | grep ssh
```

> 解决 linux 下 semanage command not found 的问题
执行 ：yum provides /usr/sbin/semanage 或者 yum whatprovides /usr/sbin/semanage
然后 yum -y install policycoreutils-python

- 查看SELinux状态

```sh
#
/usr/sbin/sestatus -v      # 如果SELinux status参数为enabled即为开启状态
SELinux status:                enabled
....
```

如果SELinux未开启则先开启

- 开启SELinux
修改/etc/selinux/config 文件
将SELINUX=disabled改为SELINUX=enforcing
重启机器即可

- 添加 xxxxx 端口到 SELinux

```sh
semanage port -a -t ssh_port_t -p tcp xxxxx
```

然后确认一下是否添加进去

```sh
semanage port -l | grep ssh
```

如果成功会输出

```sh
ssh_port_t                    tcp    xxxxx, 22
```

## 3. 修改默认端口

编辑ssh的配置文件

```sh
vi /etc/ssh/sshd_config
```

文本内容如下:

```ini
....
# Port 22
....
```

修改如下:

```ini
....
Port 22         # 这行去掉#号，防止配置不好以后不能远程登录，还得去机房修改，等修改以后的端口能使用以后在注释掉
Port xxxxx      # xxxxx为要修改的端口号
```

## 4. 重启ssh生效

* CentOS

```sh
systemctl restart sshd
```

* Ubuntu

```sh
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```