# Nacos

[TOC]

## 1. 简单创建并运行

本方案适合初次尝试，数据库是内置的derby

```sh
docker run --name nacos-standalone -e MODE=standalone -dp 8848:8848 --restart=always nacos/nacos-server:latest
```

## 2. 利用官方 `docker-compose`

- 从github下载nacos示例

```sh
cd /usr/local/
# git clone --depth 1 https://github.com/nacos-group/nacos-docker.git
# 国内镜像
git clone --depth 1 https://gitee.com/nnzbz/nacos-docker.git
cd nacos-docker
```

## 3. 部署单机derby

```sh
# 编辑docker-compose文件
vi example/standalone-derby.yaml
# 每个容器下都设置 `restart: always`
....

# 创建并运行容器

docker-compose -f example/standalone-derby.yaml up -d
```

## 4. Swarm单机

- 创建数据库
  数据库名称/用户名/密码分别是nacos/nacos/nacos(这个可以根据需要改动，但注意后面要对应 `env/nacos-standlone-mysql.env` 文件里的参数)
- 创建数据库表及索引结构的脚本
  执行 [nacos-mysql.sql](https://github.com/alibaba/nacos/blob/master/distribution/conf/nacos-mysql.sql) 里面的内容
- 修改 yaml 文件内容
  - `version` 改为 `"3.9"`
  - 修改镜像为 `nnzbz/nacos`
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
    删除 `nacos` 下的 `volumes` 节点
  - 删除示例 yaml 中 `prometheus` 与 `grafana` 的节点
  - 删除 yaml 中 `restart` 节点
  - 添加 `networks`

    ```yaml
    networks:
      default:
        external: true
        name: rebue
    ```

  - 最终结果如下:

    ```yaml
    version: "3.9"
    services:
      nacos:
        image: nnzbz/nacos
        hostname: nacos
        container_name: nacos-standalone-mysql
        env_file:
          - ../env/nacos-standlone-mysql.env
        ports:
          - "8848:8848"
          - "9848:9848"
          - "9555:9555"
    networks:
      default:
        external: true
        name: rebue
    ```

- 配置数据库连接参数(与上面创建数据库时的参数要一致)

  ```sh
  # 配置mysql参数
  vi env/nacos-standlone-mysql.env

  修改下列参数
    MYSQL_SERVICE_HOST=mysql(MySQL主机名)
    MYSQL_SERVICE_PORT=3306
    MYSQL_SERVICE_DB_NAME=nacos(数据库名称)
    MYSQL_SERVICE_USER=nacos(用户名)
    MYSQL_SERVICE_PASSWORD=nacos(密码)
  ....
  ```

- 创建并运行容器

  ```sh
  docker stack deploy -c /usr/local/nacos-docker/example/standalone-mysql-5.7.yaml nacos
  ```

## 5. 部署Swarm

### 5.1. 创建数据库

数据库名称/用户名/密码分别是nacos/nacos/nacos(这个可以根据需要改动，但注意后面要对应 `env/nacos-hostname.env` 文件里的参数)

### 5.2. 创建数据库表及索引结构的脚本

执行 `nacos-mysql.sql`

- github
  <https://github.com/alibaba/nacos/blob/master/distribution/conf/nacos-mysql.sql> 
- 国内镜像
  <https://gitee.com/mirrors/Nacos/blob/develop/distribution/conf/nacos-mysql.sql>


### 5.3. 修改 yaml 文件内容

```sh
# 删除容器依赖而改为直接访问本地数据库的mysql
vi /usr/local/nacos-docker/example/cluster-hostname.yaml
```

- `version` 改为 `"3.9"`
- 修改镜像为 `nnzbz/nacos`
- 删除 nacos1/nacos2/nacos3 下 `image` 的 `:${NACOS_VERSION}`
- 删除 nacos1/nacos2/nacos3 下 `depenOn` 节点
- 删除 `mysql` 节点
- 删除 `volumes` 节点
- 删除 `restart: always`
- 每个服务添加
  
  ```yml
  ....
      environment:
      # 最好使用此设定时区，其它镜像也可以使用
        - TZ=CST-8
  ....
  ```

- 添加 `networks` 节点
  
  ```sh
  networks:
    default:
      external: true
      name: rebue
  ```

- 最终结果如下:

```yml
version: "3.9"
services:
  nacos1:
    image: nnzbz/nacos
    hostname: nacos1
    container_name: nacos1
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
    image: nnzbz/nacos
    hostname: nacos2
    container_name: nacos2
    ports:
      - "8849:8848"
      - "9849:9848"
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    env_file:
      - ../env/nacos-hostname.env
  nacos3:
    image: nnzbz/nacos
    hostname: nacos3
    container_name: nacos3
    ports:
      - "8850:8848"
      - "9850:9848"
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    env_file:
      - ../env/nacos-hostname.env
networks:
  default:
    external: true
    name: rebue
```

### 5.4. 配置数据库连接参数(与上面创建数据库时的参数要一致)

```sh
# 配置mysql参数
vi /usr/local/nacos-docker/env/nacos-hostname.env
```

修改下列参数:

- MYSQL_SERVICE_HOST=mysql
- MYSQL_SERVICE_DB_NAME=nacos
- MYSQL_SERVICE_PORT=3306
- MYSQL_SERVICE_USER=nacos
- MYSQL_SERVICE_PASSWORD=********

**注意上面的密码改为实际的密码**

### 5.5. 部署

```sh
docker stack deploy -c /usr/local/nacos-docker/example/cluster-hostname.yaml nacos
```

## 6. Nacos 控制台

link：<http://127.0.0.1:8848/nacos/>

默认用户名/密码为： `nacos/nacos`
