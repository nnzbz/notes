# docker-compose

[TOC]

## 1. 安装

<https://docs.docker.com/compose/install/>

- Deepin/Ubuntu

  ```sh
  apt install docker-compose
  ```

- Linux
  
  ```sh
  # 安装 Docker Compose:
  curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  # 添加执行的权限
  chmod +x /usr/local/bin/docker-compose
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
