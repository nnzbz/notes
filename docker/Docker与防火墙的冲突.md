# Docker与防火墙的冲突

## 1. 冲突

docker命令中使用 -p 暴露端口时，实现需要依赖iptables
CentOS 7默认使用的是firewalld，firewalld是在iptables上再做了一层封装

这样两者就可能如下而照成冲突

- docker默认会自动添加iptables的规则
- firewalld在启动时，会重新加载自己的规则，这时就会清空原来docker设置的规则
- 旧版本的docker，这里需要重启，重新往iptables加入规则，这样端口又会重新被打开
- 新版本的docker，firewalld识别不了docker添加的规则，无法阻止端口

## 2. 原则

在服务器的防火墙策略中，关于防火墙的规则应该统一交由firewalld管理，docker不应该擅自打开自己的端口

## 3. 让docker放弃对iptables的修改

```sh
sed -i  's:^ExecStart=/usr/bin/dockerd.*:ExecStart=/usr/bin/dockerd --iptables=false:g' /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 4. 通过防火墙放开限制

- 允许指定IP可访问端口

```sh
# 允许指定IP访问端口
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.0.200" port protocol="tcp" port="1-65535" accept'
# 或者
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source ipset=whitelist-app port protocol="tcp" port="1-65535" accept'

# 重新加载防火墙
firewall-cmd --reload
# 查看已经设置的规则
firewall-cmd --zone=public --list-rich-rules
```

- 也可直接编辑规则文件

```sh
vi /etc/firewalld/zones/public.xml
```

- 允许docker容器访问外网

```sh
# 查看有没有设置启用ip转发功能，即 net.ipv4.ip_forward=1
cat /etc/sysctl.conf|grep 'net.ipv4.ip_forward = 1'
# 如果没有设置，启用ip转发功能
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf
# 加载并查看是否设置成功
sysctl -p
# 开启类似NAT的功能, 让docker容器内部可以访问外网资源
firewall-cmd --permanent --zone=public --add-masquerade

# 重新加载防火墙
firewall-cmd --reload
```
