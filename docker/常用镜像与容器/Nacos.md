# Nacos

[TOC]

## 1. 简单创建并运行

本方案适合初次尝试，数据库是内置的derby。为方便管理，推荐第二节中的 MySQL 方式

```sh
docker run --name nacos-standalone -e MODE=standalone -dp 8848:8848 --restart=always nacos/nacos-server:latest
```

## 2. 利用官方 `docker-compose`

### 2.1. 从github下载nacos示例

```sh
git clone --depth 1 https://github.com/nacos-group/nacos-docker.git
cd nacos-docker
```

### 2.2. 各种部署方式

- 单机derby

  ```sh
  # 编辑docker-compose文件
  vi example/standalone-derby.yaml
  # 每个容器下都设置 `restart: always`
  ....

  # 创建并运行容器

  docker-compose -f example/standalone-derby.yaml up -d
  ```

- 单机mysql
  - 创建数据库
    数据库名称/用户名/密码分别是nacos/nacos/nacos(这个可以根据需要改动，但注意后面要对应 `env/nacos-standlone-mysql.env` 文件里的参数)
  - 创建数据库表及索引结构的脚本
    执行 [nacos-mysql.sql](https://github.com/alibaba/nacos/blob/master/distribution/conf/nacos-mysql.sql) 里面的内容
  - 修改 yaml 文件内容
    - 取消示例 yaml 中关联mysql容器的地方
      因为示例中是要关联一个自己定义的mysql容器，一般开发环境都会有mysql，不用再独立弄一个出来，所以要取消掉，然后关联自己的mysql即可

      ```sh
      # 删除容器依赖而改为直接访问本地数据库的mysql
      vi example/standalone-mysql-5.7.yaml

      
      # 1. 删除 mysql 节点
      ....
      # 2. 删除 nacos 节点下的 depenOn 节点
      ....
      ```

    - 修改示例 yaml 中映射卷的地方
      - `- ./standalone-logs/:/home/nacos/logs` 中的后面的路径改为 `/var/log/nacos`，并且创建此路径
      - 删除 `- ./init.d/custom.properties:/home/nacos/init.d/custom.properties` 行(因为目前没什么要自定义的)  
    - 删除示例 yaml 中 `prometheus` 与 `grafana` 的节点(可选)
    - 修改 yaml 中 `restart` 的值为 `always`
    - 最终结果如下:

      ```ini
      version: "2"
      services:
        nacos:
          image: nacos/nacos-server:${NACOS_VERSION}
          container_name: nacos-standalone-mysql
          env_file:
            - ../env/nacos-standlone-mysql.env
          volumes:
            - ./standalone-logs/:/var/log/nacos
      #      - ./init.d/custom.properties:/home/nacos/init.d/custom.properties
          ports:
            - "8848:8848"
            - "9848:9848"
            - "9555:9555"
      #    depends_on:
      #      - mysql
      #    restart: on-failure
          restart: always
      #  mysql:
      #    container_name: mysql
      #    image: nacos/nacos-mysql:5.7
      #    env_file:
      #      - ../env/mysql.env
      #    volumes:
      #      - ./mysql:/var/lib/mysql
      #    ports:
      #      - "3306:3306"
      #  prometheus:
      #    container_name: prometheus
      #    image: prom/prometheus:latest
      #    volumes:
      #      - ./prometheus/prometheus-standalone.yaml:/etc/prometheus/prometheus.yml
      #    ports:
      #      - "9090:9090"
      #    depends_on:
      #      - nacos
      #    restart: on-failure
      #  grafana:
      #    container_name: grafana
      #    image: grafana/grafana:latest
      #    ports:
      #      - 3000:3000
      #    restart: on-failure
      ```

  - 配置数据库连接参数(与上面创建数据库时的参数要一致)

    ```sh
    # 配置mysql参数
    vi env/nacos-standlone-mysql.env

    修改下列参数
      MYSQL_SERVICE_DB_NAME=nacos(数据库名称)
      MYSQL_SERVICE_PORT=3306
      MYSQL_SERVICE_USER=nacos(用户名)
      MYSQL_SERVICE_PASSWORD=nacos(密码)
    ....
    ```

    **注意**，如果是容器内要连接宿主机上的MySQL，查询docker0的IP是什么(我这里是172.17.0.1)，然后修改 `MYSQL_SERVICE_HOST` 项的值
  - 创建并运行容器
  
    ```sh
    docker-compose -f example/standalone-mysql-5.7.yaml up -d
    ```

## 3. Swarm

### 3.1. 创建数据库

数据库名称/用户名/密码分别是nacos/nacos/nacos(这个可以根据需要改动，但注意后面要对应 `env/nacos-hostname.env` 文件里的参数)

### 3.2. 创建数据库表及索引结构的脚本

执行 [nacos-mysql.sql](https://github.com/alibaba/nacos/blob/master/distribution/conf/nacos-mysql.sql) 里面的内容

### 3.3. 修改 yaml 文件内容

```sh
# 删除容器依赖而改为直接访问本地数据库的mysql
vi /usr/local/nacos-docker/example/cluster-hostname.yaml
```

- `version` 改为 `"3.9"`
- 删除 `hostname` 和 `container_name` 节点
- 删除 `image` 的 `:${NACOS_VERSION}`
- 删除 `mysql` 节点
- 删除 `depenOn` 节点
- 删除 `volumes` 节点
- 删除 `restart: always`
- 每个服务添加
  
  ```yml
  environment:
    # 最好使用此设定时区，其它镜像也可以使用
    - TZ=CST-8
  ```

- 最终结果如下:

```ini
version: "3.9"
services:
  nacos1:
    image: nacos/nacos-server
    ports:
      - "8848:8848"
      - "9848:9848"
      - "9555:9555"
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    env_file:
      - ../env/nacos-hostname.env
  nacos2:
    image: nacos/nacos-server
    ports:
      - "8849:8848"
      - "9849:9848"
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    env_file:
      - ../env/nacos-hostname.env
  nacos3:
    image: nacos/nacos-server
    ports:
      - "8850:8848"
      - "9850:9848"
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    env_file:
      - ../env/nacos-hostname.env
```

### 3.4. 配置数据库连接参数(与上面创建数据库时的参数要一致)

```sh
# 配置mysql参数
vi /usr/local/nacos-docker/env/nacos-hostname.env
```

修改下列参数:

- NACOS_SERVERS=nacos_nacos1:8848 nacos_nacos2:8848 nacos_nacos3:8848
- MYSQL_SERVICE_HOST=mysql_nginx
- MYSQL_SERVICE_DB_NAME=nacos
- MYSQL_SERVICE_PORT=80
- MYSQL_SERVICE_USER=nacos
- MYSQL_SERVICE_PASSWORD=nacos


### 3.5. 部署

```sh
cd /usr/local/nacos-docker/
docker-compose -f example/standalone-mysql-5.7.yaml up -d
```

## 4. Nacos 控制台

link：<http://127.0.0.1:8848/nacos/>

默认用户名/密码为： `nacos/nacos`
