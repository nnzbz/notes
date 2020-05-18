# Nacos

[TOC]

## 1. 简单的命令(适合本机开发调试)

```sh
docker run --name nacos-standalone -e MODE=standalone -p 8848:8848 -d nacos/nacos-server:latest
```

## 2. docker-compose

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

- ~~单机mysql~~(sql文件居然是oracle的，我对阿里再次无语了)

  ```sh
  # 删除容器依赖而改为直接访问本地数据库的mysql
  vi example/standalone-mysql-5.7.yaml
  # 1. 删除 mysql 节点
  ....
  # 2. 删除 nacos 节点下的 depenOn 节点
  ....
  # 3. 修改restart的值为always
  ....

  # 配置mysql参数
  vi env/nacos-standlone-mysql.env
  ....

  # 创建并运行容器
  docker-compose -f example/standalone-mysql-5.7.yaml up -d
  ```

## 3. Nacos 控制台

link：<http://127.0.0.1:8848/nacos/>

默认用户名/密码为： `nacos/nacos`
