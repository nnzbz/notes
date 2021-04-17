# docker-compose

[TOC]

## 1. 安装

- Deepin/Ubuntu

  ```sh
  apt install docker-compose
  ```

- CentOS
  
  ```sh
  # 安装额外依赖包
  yum install epel-release
  # 安装 python-pip:
  yum install -y python-pip
  # 安装 Docker Compose:
  pip install docker-compose
  # 升级 python 包：
  yum upgrade python*
  # 验证安装：
  docker-compose version
  ```

## 2. `docker-compose.yml`

### 2.1. version

- 目前为止有三个版本分别为 `1`, `2`, `3`
- 版本越高支持越多的指令
- 区分 `1` 和 `2`（Compose 1.6.0+，Docker Engine 1.10.0+）

## 3. 启动应用

进入到 `docker-compose.yml` 文件所在目录，执行下面的命令

```sh
docker-compose up -d
```
