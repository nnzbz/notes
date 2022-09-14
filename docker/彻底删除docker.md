# 彻底删除docker

## 1. 停止运行docker

```sh
systemctl stop docker
systemctl stop docker.socket
```

## 2. 删除旧版本的docker

```sh
yum remove -y docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```

## 3. 删除新版本的docker

```sh
yum remove -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
yum autoremove -y
```

## 4. 删除docker目录

```sh
rm -rf /var/lib/docker
rm -rf /var/lib/containerd
rm -rf /etc/systemd/system/docker.service.d
rm -rf /etc/systemd/system/docker.service
rm -rf /var/lib/docker
rm -rf /var/run/docker
rm -rf /usr/local/docker
rm -rf /etc/docker
rm -rf /usr/bin/docker* /usr/bin/containerd* /usr/bin/runc /usr/bin/ctr
```

## 5. 删除docker创建的网卡

```sh
yum -y install bridge-utils
ifconfig docker0 down
brctl delbr docker0

ifconfig docker_gwbridge down
brctl delbr docker_gwbridge
```

