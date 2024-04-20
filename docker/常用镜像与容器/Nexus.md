# 制作和使用nexus的docker容器

[TOC]

## 1. 单机

- 存放数据在宿主机
  先查看宿主机有没有UID为200的用户

  ```sh
  cat /etc/passwd | grep 200
  ```

  - 如果宿主机没有UID为200的用户

    ```sh
    # 添加nexus用户并指定uid为200
    useradd nexus -u 200 --no-create-home
    mkdir /usr/local/nexus-data && chown -R nexus:nexus /usr/local/nexus-data
    docker run -d -p 8081:8081 --name nexus -v /usr/local/nexus:/nexus-data --restart=always sonatype/nexus3
    ```

  - 宿主机已经有UID为200的用户
    200的用户是容器中使用的nexus用户，如果在宿主机中添加200的UID会有冲突，可添加另一个没有冲突的，然后在创建容器时使用 `--user` 参数

    ```sh
    # 添加nexus用户并未指定uid为200
    adduser nexus
    cat /etc/passwd|grep nexus # 例如我这里看到UID是1001
    mkdir /var/lib/nexus && chown -R nexus:nexus /var/lib/nexus
    docker run -dp 8081:8081 --name nexus -v /var/lib/nexus:/nexus-data --user 1001:1001 --restart=always sonatype/nexus3
    ```

  - 按上面的方式，Nexus映射到了 `/var/lib/nexus`，但是此路径一般没有分配太大的空间，所以需要更换到有足够容量的空间

    ```sh
    # 首先保证docker没有启动
    sudo service docker stop
    # 然后移动整个/var/lib/mysql目录到目的路径
    sudo mv /var/lib/nexus /usr/local/lib/nexus
    # 添加软链
    sudo ln -s /usr/local/lib/nexus /var/lib/nexus
    ```

## 2. Swarm

### 2.1. `Docker Compose`

```sh
mkdir -p /usr/local/nexus
vi /usr/local/nexus/stack.yml
```

```yml{.line-numbers}
version: "3.9"
services:
  nexus:
    image: sonatype/nexus3
    ports:
      - 8081:8081
      # docker私服HTTP的接口
      - 8082:8082
      # docker私服HTTPS的接口
      # - 8083:8083
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      - nexusdata:/nexus-data
volumes:
  nexusdata:
```

### 2.2. 部署

```sh
docker stack deploy -c /usr/local/nexus/stack.yml nexus
```

## 3. 浏览器访问

<http://127.0.0.1:8081>

## 4. 查看初始密码

查看初始密码，需查看下面文件的内容

`admin.password`

- 如果目录影射到宿主机

  ```sh
  cat /var/lib/nexus/admin.password
  ```

- 如果目录没有影射到宿主机，需进入容器

  ```sh
  docker exec -it nexus /bin/bash
  cat /nexus-data/admin.password
  ```

