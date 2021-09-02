# Docker私服

[TOC]

## 1. 搭建nexue(略)

## 2. 创建docker的仓库

1. `Create repository` -> `docker(hosted)`
2. 填写的主要内容，并保存

- Name : `my-docker`
- HTTP : `8082`
- ~~HTTPS : `8083`~~
- 打勾 `Allow anonymous docker pull ( Docker Bearer Token Realm required )`

## 3. 添加 `Docker Bearer Token Realm`

`Security` -> `Realms` -> 双击 `Docker Bearer Token Realm` -> `save`

## 4. 禁用 `Outreach: Management`

`System` -> `Capabilities` -> 选择 `Outreach: Management` -> `Disable`

- 不禁用在上传的时候会报错 `Could not download page bundle` `Connection reset`

## 5. 修改本机(客户端)Docker的连接安全配置（使用HTTP而非HTTPS）

### 5.1. 方案一

- Mac

 右上角系统任务栏Docker图标 -> Preferences... -> Daemon -> Insecure registries -> + -> hub.docker.com

- Deepin/Ubuntu

```sh
sudo vi /etc/docker/daemon.json
```

```json
{
  "registry-mirrors": ["https://xxxxxxxx.mirror.aliyuncs.com"],
  "insecure-registries": ["xx.xx.xx.xx:8082"]   // 新增
}
```

- CentOS

```sh
vi /usr/lib/systemd/system/docker.service
```

```text
....
ExecStart=/usr/bin/dockerd-current \
          --insecure-registry 127.0.0.1:8082 \
          ....
....
```

如果上述操作无效，使用下面的配置（同Deepin/Ubuntu系统的配置）

```
vi /etc/docker/daemon.json
```

写入以下配置

```
{
    "insecure-registries":["172.20.14.237:8082"]
}
```

- 重启docker

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 5.2. 方案二(未验证)

> 正确的方式在报错信息里已经有提示了：
In the case of HTTPS, if you have access to the registry's CA certificate, no need for the flag; simply place the CA certificate at /etc/docker/certs.d/10.0.1.44:5000/ca.crt

首先，你不要直接使用docker-registry，你在registry前面套一层nginx代理，在nginx里自己签一组证书，把ca.crt拷贝到 /etc/docker/certs.d/10.0.1.44:5000/ca.crt 就可以了。

## 6. 打开防火墙的8082/8083端口(略)

## 7. 创建上传及下载的角色和用户

### 7.1. 创建专门用于上传的角色

- 操作步骤：
  - ```Create role```
- 填写的主要内容：
  - Role ID : ```nx-my-deployment```
  - Role name : ```nx-my-deployment```
  - Role description : ```My releases and snapshots deployment role```
  - Privileges > Given :
    - ```nx-repository-admin-maven2-my-docker-*```
    - ```nx-repository-view-maven2-my-docker-*```

### 7.2. 新建专门用于上传的用户

- 操作步骤：
  - ```Create user```
- 填写的主要内容：
  - ID : ```my-deployment```
  - Password : ```deployment123```
  - Status : ```Active```
  - Roles > Granted : ```nx-my-deployment```


## 8. 上传镜像

### 8.1. 登录私服

```sh
docker login 127.0.0.1:8082 -umy-deployment -pdeployment123
```

> 注意：如果要登录 **docker hub**，请不要输入主机地址

### 8.2. 打标记

格式：

```sh
docker tag <imageId or imageName> <nexus-hostname>:<repository-port>/<image>:<tag>
```

例如：

```sh
docker tag nnzbz/debian-jre:8 192.168.1.201:8082/nnzbz/debian-jre:8
```

### 8.3. 上传镜像

上传镜像：

```sh
docker push 192.168.1.201:8082/nnzbz/debian-jre:8
```

## 9. 拉取镜像

```sh
docker pull 127.0.0.1:8082/nnzbz/debian-jre:8
```
