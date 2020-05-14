# 修改默认SSH端口

## 1. 先用防火墙打开端口

```sh
firewall-cmd --permanent --zone=public --add-port=xxxxx/tcp

firewall-cmd --reload
```

## 2. 修改默认端口

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

将上而的注释去掉，并将22改为xxxxx(端口号)

```sh
# 重启ssh生效
systemctl restart sshd
```
