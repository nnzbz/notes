# 离线安装docker

1. 下载安装包

<https://download.docker.com/linux/static/stable/x86_64/>

2. 上传并解压安装包

```sh
tar xzvf /path/to/<FILE>.tar.gz
```

3. 复制到 /usr/bin 目录

```sh
cp docker/* /usr/bin/
```

4. 准备服务配置文件

```sh
vi /etc/systemd/system/docker.service
```

```ini
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
# Uncomment TasksMax if your systemd version supports it.
# Only systemd 226 and above support this version.
#TasksMax=infinity
TimeoutStartSec=0
# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
# kill only the docker process, not all processes in the cgroup
KillMode=process
# restart the docker process if it exits prematurely
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
```

```sh
chmod +x /etc/systemd/system/docker.service
systemctl daemon-reload
```

5. 配置开机启动与启动

```sh
systemctl enable docker
systemctl start docker
```
