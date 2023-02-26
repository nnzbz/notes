# Docker的Volume

[TOC]

## 1. 什么是Volume

Volume就是Docker主机和容器之间共享的文件或文件夹。

## 2. 设置volume

- **-v**
 运行容器时加上-v参数可以设置volume，例如下面是将容器中的 ```/data``` 目录共享出来

```sh
docker run -d -p 7000:6379 -v /data --name redis1 redis
```

- **VOLUME**
 而在Dockerfile文件中也可使用 ```VOLUME```命令达到同样的目的

```text
VOLUME /data
```

- 两者区别

而 ```-v```参数还可以指定主机的目录，而 ```VOLUME```做不到

```sh
docker run -d -p 7000:6379 -v /home/zbz/data:/data --name redis1 redis
```

这里的 ```/home/zbz/data```是指定的主机的目录

> **注意：当使用 ```-v``` 参数时，镜像目录下的任何文件都不会被复制到Volume中**

## 3. 查看Volumes

```sh
docker inspect redis1 | grep Mounts -A 10
```

控制台输出如下，注意 ```Source``` 项，这就是主机对应的目录

```text
"Mounts": [
    {
        "Name": "5452a3f43d2abc3a72275efc15437f4eec6efeaa8e101d2b164076408ebc105b",
        "Source": "/var/lib/docker/volumes/5452a3f43d2abc3a72275efc15437f4eec6efeaa8e101d2b164076408ebc105b/_data",
        "Destination": "/data",
        "Driver": "local",
        "Mode": "",
        "RW": true,
        "Propagation": ""
    }
],
```

## 4. 容器中共享Volume

```sh
docker run -h redis2 --volumes-from redis1 redis
```

值得注意的是，不管redis1是否正在运行，此命令都会起效

### 4.1. 数据卷容器

数据卷容器就是将一个正常的容器作为数据卷，让其他容器通过挂载这个容器实现数据共享。

可是值得注意的是，**数据卷容器会降低I/O性能** 。

创建一个已经在Dockerfile文件中定义了 ```VOLUME``` 的 postgres镜像，运行echo后退出

```sh
docker run --name dbdata postgres echo "Data-only container for postgres"
```

用 ```--volumes-from``` 命令识别其它容器的Volume

```sh
docker run -d --volumes-from dbdata --name db1 postgres
```

#### 4.1.1. 使用注意

> **注意：不要运行数据卷容器，这纯粹是在浪费资源。**

不要为了数据卷容器而使用 **“最小的镜像”** ，只使用数据镜像本身即可。你已经拥有该镜像，所以不会占用额外的空间。

### 4.2. 权限与许可

通常你需要设置Volume的权限或为Volume初始化一些默认配置和配置文件，需要注意的是，Dockerfile文件中，在 ```VOLUME``` 指令之后的任何语句都不能改变该Volume。

## 5. 删除Volume

Volume只有在下列情况下才会被删除

- ```docker rm -v```
- ```docker run --rm```

## 6. 改名

```sh
docker volume create --name <new_volume>
docker run --rm -it -v <old_volume>:/from:ro -v <new_volume>:/to alpine ash -c "cd /from ; cp -av . /to"
```

## 7. 备份

```sh
docker run --rm --volumes-from <数据卷的名称> -v $(pwd):/bak alpine tar cvf /bak/backup.tar <数据卷内要备份的目录>
```
