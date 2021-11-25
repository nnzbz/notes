# Gitea

[TOC]

## 1. Swarm

```sh
mkdir /usr/local/gitea
vi /usr/local/gitea/stack.yml
```

```yaml{.line-numbers}
version: "3.9"

services:
  server:
    image: gitea/gitea
    hostname: gitea
    container_name: gitea
    volumes:
      - giteadata:/data
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    ports:
      # Http端口
      - "30000:3000"
      # SSH端口
      - "220:22"

volumes:
  giteadata:

networks:
  default:
    external: true
    name: rebue
```

- 部署

```sh
docker stack deploy -c /usr/local/gitea/stack.yml gitea
```

## 2. 初始化

注意修改下面的选项

- 基础URL
  <http://mykp1:30000/>
