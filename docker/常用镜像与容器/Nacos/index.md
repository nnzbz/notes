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
  - 配置数据库连接参数(与上面创建数据库时的参数要一致)

    ```sh
    # 配置mysql参数
    vi env/nacos-standlone-mysql.env
    ....
    ```

    **注意**，如果是容器内要连接宿主机上的MySQL，查询docker0的IP是什么(我这里是172.17.0.1)，然后修改 `MYSQL_SERVICE_HOST` 项的值
  - 创建并运行容器
  
    ```sh
    docker-compose -f example/standalone-mysql-5.7.yaml up -d
    ```

## 3. Nacos 控制台

link：<http://127.0.0.1:8848/nacos/>

默认用户名/密码为： `nacos/nacos`
