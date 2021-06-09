# MinIO

[TOC]

## 开发环境

```sh
docker run --name minio -dp 9000:9000 --restart=always minio/minio server /data
```

- 访问
  - 地址
    <http://127.0.0.1:9000>
  - Access Key
    minioadmin
  - Secret Key
    minioadmin

## 线上单机环境

## 线上SWARM环境

1. 准备好 `docker swarm` 运行环境
2. 用 `docker secrets` 建立密钥

  ```sh
  echo "AKIAIOSFODNN7EXAMPLE" | docker secret create access_key -
  echo "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" | docker secret create secret_key -
  ```

  事后可以通过 `docker secret ls` 来查看密钥

3. 创建并运行容器

  ```sh
  docker service create --name="minio-service" -p 9000:9000 --secret="access_key" --secret="secret_key" minio/minio server /data
  ```

- 访问
  - 地址
    <http://xxxx:9000>
  - Access Key
    AKIAIOSFODNN7EXAMPLE
  - Secret Key
    wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

4. 更换密码

更换密码要先删除服务，然后再执行第2、3步

```sh
docker service rm minio-service
```
