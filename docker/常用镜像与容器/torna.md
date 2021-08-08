# torna

[TOC]

## 1. 创建 `torna` 数据库

<https://gitee.com/durcframework/torna/blob/master/mysql.sql>
如果上面的地址失效，可以使用下面的地址
<https://github.com/rebue/archetype/blob/1.2.3/src/main/resources/archetype-resources/doc/torna使用指南/torna.sql>

## 2. 准备配置文件

**注意:** torna配置文件必须是 `application.properties` 而非 `application.yml`，否则识别不了**

```sh
mkdir -p /usr/local/torna/config
vi /usr/local/torna/config/application.properties
```

参考 [server/boot/src/main/resources/application.properties](https://gitee.com/durcframework/torna/blob/master/server/boot/src/main/resources/application.properties) 文件到 `/usr/local/torna/config` 目录下，修改数据库连接配置，其内容如下

```ini
# Server port
server.port=7700

# MySQL
mysql.host=127.0.0.1:3306
mysql.schema=torna
mysql.username=torna
mysql.password=********
```

## 3. 单机

**注意:** 注意设置host和password

### 3.1. 创建并运行 `norta` 容器

```sh
docker run --name torna -dp 7700:7700 -v /usr/local/torna/config:/torna/config --restart=always tanghc2020/torna
```

## 4. Swarm

### 4.1. `Docker Compose`

```sh
vi /usr/local/torna/stack.yml
```

```yml{.line-numbers}
version: "3.9"
services:
  torna:
    image: tanghc2020/torna
    ports:
      - 7700:7700
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    configs:
      - source: application.properties
        target: /torna/config/application.properties
configs:
  application.properties:
    file: /usr/local/torna/config/application.properties
```

### 4.2. 部署

```sh
docker stack deploy -c /usr/local/torna/stack.yml torna
```

## 5. 浏览器访问

<http://127.0.0.1:7700>

**注意:** 如果是部署到了其它服务器上，请将 `127.0.0.1` 改为相应的服务器地址
