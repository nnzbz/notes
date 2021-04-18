# 理解 docker 容器中的 uid 和 gid

[TOC]

## 1. 危险的默认情况

默认情况下，容器中的进程以 root 用户权限运行，并且这个 root 用户和宿主机中的 root 是同一个用户。

**这就意味着一旦容器中的进程有了适当的机会，它就可以控制宿主机上的一切！**

## 2. 先来了解下 uid 和 gid

uid 和 gid 由 Linux 内核负责管理，并通过内核级别的系统调用来决定是否应该为某个请求授予特权。

比如当进程试图写入文件时，内核会检查创建进程的 uid 和 gid，以确定它是否有足够的权限修改文件。

**注意，内核使用的是 uid 和 gid，而不是用户名和组名。**

与虚拟机技术不同，同一主机上运行的所有容器共享同一个内核(主机的内核)。

容器化带来的巨大价值在于所有这些独立的容器(其实是进程)可以共享一个内核。

这意味着即使由成百上千的容器运行在 docker 宿主机上，但内核控制的 uid 和 gid 则仍然只有一套。

所以同一个 uid 在宿主机和容器中代表的是同一个用户(即便在不同的地方显示了不同的用户名)。

**注意，由于普通的用来显示用户名的 Linux 工具并不属于内核(比如 id 等命令)，所以我们可能会看到同一个 uid 在不同的容器中显示为不同的用户名。但是对于相同的 uid 不能有不同的特权，即使在不同的容器中也是如此。**

如果你已经了解了 Linux 的 user namespace 技术，参考《Linux Namespace : User》，你需要注意的是到目前为止，docker 默认并没有启用 user namesapce，这也是本文讨论的情况。笔者会在接下来的文章中介绍如何配置 docker 启用 user namespace。

## 3. 容器中默认使用 root 用户

如果不做相关的设置，容器中的进程默认以 root 用户权限启动。

下面做一下实验:

- 启动并创建ubuntu镜像的容器来运行 sleep 程序

  ```sh
  docker run -d --name sleepme ubuntu sleep infinity
  ```

  **注意，这里并没有用 sudo 升权**

- 查看宿主机的当前uid

  ```sh
  id
  ```

  笔者的uid是501(zbz)

- 在宿主机中查看 sleep 进程的信息
  
  ```sh
  ps aux | grep sleep
  ```

  笔者查看到的是 zbz，也就是当前用户

- 然后进入容器内部看看
  
  ```sh
  # 进入容器
  docker exec -it sleepme bash
  ....
  # 进入容器后执行下面的命令
  ps aux | grep sleep
  ```

  笔者看到的是 root

## 4. 验证权限的实验
  
(先按 Ctrl+D 从上面的容器中退出到宿主机中)

在宿主机上创建一个只有 root 用户可以读写的文件

```sh
sudo mkdir /test/
sudo tee /test/file <<-'EOF'
test file
EOF
```

设置只有root 用户才能读写

```sh
sudo chmod 700 /test/file
```

这里宿主机中的当前用户就没有访问的权限了

```sh
cat /test/file
```

然后挂载到容器中

```sh
# 注意: 在MacOS中要先配置共享 /test 目录
docker run --rm -it -w=/test -v /test:/test ubuntu
```

进入容器后，查看 /test/file 文件

```sh
cat file
```

没有权限访问

从这个实验可以看出，虽然容器内是 root 账号，但是如果运行容器的账户不是 root，是没有权限访问宿主机上 root账户才能访问的文件的

但是如果运行容器的是 root 账户就可以访问了（实验略）

而如果运行容器的是 root 账户，进入容器时指定另一个用户，则仍然不能访问

```sh
docker run --rm -it --user 1001 -w=/test -v /test:/test ubuntu
```

**注意，这里比之前的命令多了 `--user 1001` 指定uid来运行容器**
