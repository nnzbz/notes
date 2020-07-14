# Docker私服

[TOC]

## 1. 搭建nexue(略)

## 2. 创建docker的仓库

- 操作步骤：
  - ```Create repository``` > ```docker(hosted)```
- 填写的主要内容：
  - Name : ```my-docker```
  - HTTP : ```8082```
  - Enable Docker V1 API : 打勾

## 3. 修改本机Docker的连接安全配置（重要）

### 3.1. 方案一

- Mac

 右上角系统任务栏Docker图标 -> Preferences... -> Daemon -> Insecure registries -> + -> hub.docker.com

- Ubuntu

```sh
sudo vi /etc/default/docker
```

```text
....
DOCKER_OPTS="--insecure-registry 192.168.1.201:8082"
....
DOCKER_OPTS="--insecure-registry 127.0.0.1:8082"
....
DOCKER_OPTS="--insecure-registry hub.docker.com"
....
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

- 重启docker

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 3.2. 方案二(未验证)

> 正确的方式在报错信息里已经有提示了：
In the case of HTTPS, if you have access to the registry's CA certificate, no need for the flag; simply place the CA certificate at /etc/docker/certs.d/10.0.1.44:5000/ca.crt

首先，你不要直接使用docker-registry，你在registry前面套一层nginx代理，在nginx里自己签一组证书，把ca.crt拷贝到 /etc/docker/certs.d/10.0.1.44:5000/ca.crt 就可以了。

## 4. 打开防火墙的8082端口(略)

## 5. 创建上传的角色和用户

### 5.1. 创建专门用于上传的角色

- 操作步骤：
  - ```Create role```
- 填写的主要内容：
  - Role ID : ```nx-my-deployment```
  - Role name : ```nx-my-deployment```
  - Role description : ```My releases and snapshots deployment role```
  - Privileges > Given :
    - ```nx-repository-admin-maven2-my-docker-*```
    - ```nx-repository-view-maven2-my-docker-*```

### 5.2. 新建专门用于上传的用户

- 操作步骤：
  - ```Create user```
- 填写的主要内容：
  - ID : ```my-deployment```
  - Password : ```deployment123```
  - Status : ```Active```
  - Roles > Granted : ```nx-my-deployment```


## 6. 上传镜像

### 6.1. 登录私服

```sh
docker login 127.0.0.1:8082 -umy-deployment -pdeployment123
```

> 注意：如果要登录 **docker hub**，请不要输入主机地址

### 6.2. 打标记

格式：

```sh
docker tag <imageId or imageName> <nexus-hostname>:<repository-port>/<image>:<tag>
```

例如：

```sh
docker tag nnzbz/debian-jre:8 192.168.1.201:8082/nnzbz/debian-jre:8
```

### 6.3. 上传镜像

上传镜像：

```sh
docker push 192.168.1.201:8082/nnzbz/debian-jre:8
```

## 7. 拉取镜像

```sh
docker pull 127.0.0.1:8082/nnzbz/debian-jre:8
```
