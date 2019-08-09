# Mac下清空Docker容器的日志

## 1. 查看docker日志

```sh
docker inspect container_id
```

找到 `LogPath` 节点内容

```text
....
"LogPath": "/var/lib/docker/containers/ea3efd64c5c3d600df0a446d098f55d2f44b8a2644ba3d3a24a863610c4b7d45/ea3efd64c5c3d600df0a446d098f55d2f44b8a2644ba3d3a24a863610c4b7d45-json.log",
....
```

## 2. 进入Docker for Mac VM

```sh
screen ~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/tty
```

## 3. 清除日志

```sh
true > /var/lib/docker/containers/ea3efd64c5c3d600df0a446d098f55d2f44b8a2644ba3d3a24a863610c4b7d45/ea3efd64c5c3d600df0a446d098f55d2f44b8a2644ba3d3a24a863610c4b7d45-json.log
```
