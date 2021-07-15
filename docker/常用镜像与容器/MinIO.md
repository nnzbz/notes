# MinIO

[TOC]

## 1. 单机

```sh
docker run --name minio -d -p9000:9000 -p9001:9001 --restart=always minio/minio server /data --console-address ":9001"
```

- 访问
  - 地址
    <http://127.0.0.1:9001>
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
      - 9000:9000
      - 9001:9001
    secrets:
      - source: minio_access_key
        target: access_key
      - source: minio_secret_key
        target: secret_key
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    command: server /data
            --console-address ":9001"
secrets:
  minio_access_key:
    external: true
  minio_secret_key:
    external: true
```

4. 部署

```sh
docker stack deploy -c /usr/local/minio/stack.yml minio
```


  ```sh
  docker service create --name="minio-service" -p 9000:9000 --secret="access_key" --secret="secret_key" minio/minio server /data
  ```

- 访问
  - 地址
    <http://xxxx:9001>
  - Access Key
    AKIAIOSFODNN7EXAMPLE
  - Secret Key
    wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
