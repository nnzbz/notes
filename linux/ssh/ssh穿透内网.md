# SSH穿透内网

[TOC]

## 1. 将域名映射到服务器的公网IP

略

## 2. 服务端的ssh开启网关配置

```sh
vi /etc/ssh/sshd_config
```

```text
GatewayPorts yes
```

重启ssh服务

```sh
systemctl restart sshd
```

## 3. 客户端通过ssh将流量转发到本地

### 3.1. ssh命令

利用 ```ssh``` 的转发功能 ```-R``` 参数。

```sh
#!/bin/bash
while :
do
    ssh user@remotehost -fNR <remote port>:localhost:<local port>
done
```

为了在自动重连时避免每次输入密码，还需要配置 ssh 证书实现免密码登录。

### 3.2. 脚本示例

```sh
#!/bin/bash
# file: ~/sh/sshNAT.sh
# author: zbz
#
# 参数说明
# local-port 本地端口
# remote-host 远程服务器地址
# remote-port 远程服务器的端口
#
# 示例: 将远程服务器120.78.180.227:80端口映射到本地8080端口
# sshNAT.sh --local-port 8080 --remote-host 120.78.180.227 --remote-port 80

# 获取参数数组
args=`getopt -u -o n:h:d: -l local-port-long:,remote-host-long:,remote-port-long: -- $*`
# $?: 上个命令的退出状态，或函数的返回值。
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

# echo $args

# set 会重新排列参数的顺序，也就是改变$1,$2...$n的值，这些值在getopt中重新排列过了
set -- $args

# echo $args

#经过getopt的处理，下面处理具体选项。
while true ; do
    case $1 in
        -p|--local-port-long) LOCAL_PORT=$2 ; shift 2 ;;
        -H|--remote-host-long) REMOTE_HOST=$2 ; shift 2 ;;
        -P|--remote-port-long) REMOTE_PORT=$2 ; shift 2 ;;
        --) shift ; break ;;
        *) echo "Internal error!" ; echo $1 ; exit 1 ;;
    esac
done

echo '穿透内网: localhost:'$LOCAL_PORT' <--------> '$REMOTE_HOST':'$REMOTE_PORT

while :
do
  ssh root@$REMOTE_HOST -fNR $REMOTE_PORT:localhost:$LOCAL_PORT
done
```

运行脚本示例

```sh
~/sh/sshNAT.sh --local-port 8080 --remote-host 120.78.180.227 --remote-port 80
```

## 4. 确认内网穿透是否打通

```sh
curl http://<remote host>:<remote port>
```
