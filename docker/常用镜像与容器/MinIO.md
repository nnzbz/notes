# MinIO

[TOC]

## 1. 单机

```sh
docker run --name minio -d -p19000:19000 -p19001:9001 --restart=always minio/minio server /data --address "0.0.0.0:19000" --console-address ":9001"
```

- 访问
  - 地址
    <http://127.0.0.1:19001>
  - Access Key
    minioadmin
  - Secret Key
    minioadmin

## 2. Swarm

1. 准备好 `docker swarm` 运行环境
2. 用 `docker secrets` 建立密钥

```sh
# 用明码生成密钥
echo "AKIAIOSFODNN7EXAMPLE" | docker secret create minio_access_key -
echo "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" | docker secret create minio_secret_key -
# 生成随机密钥(20位)
openssl rand -base64 20 | docker secret create minio_access_key -
openssl rand -base64 20 | docker secret create minio_secret_key -
```

- 查看密钥(在创建容器后)

```sh
# 进入容器
docker exec -it <容器id> /bin/sh
# 在容器中查看密钥
cat /run/secrets/access_key
cat /run/secrets/secret_key
```

3. `Docker Compose`

```sh
mkdir -p /usr/local/minio
vi /usr/local/minio/stack.yml
```

```yml{.line-numbers}
version: "3.9"
services:
  minio:
    image: minio/minio
    ports:
      - 19000:19000
      - 19001:9001
    secrets:
      - source: minio_access_key
        target: access_key
      - source: minio_secret_key
        target: secret_key
    volumes:
      - miniodata:/data
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    command: server /data
            --address "0.0.0.0:19000"
            --console-address ":9001"
secrets:
  minio_access_key:
    external: true
  minio_secret_key:
    external: true

volumes:
  miniodata:

networks:
  default:
    external: true
    name: rebue
```

4. 部署

```sh
docker stack deploy -c /usr/local/minio/stack.yml minio
```

- 访问
  - 地址
    <http://xxxx:19001>
  - Access Key
    AKIAIOSFODNN7EXAMPLE
  - Secret Key
    wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
