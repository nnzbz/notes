# Docker创建虚拟网络

## 1. Overlay 和 Attachable

Overlay网络是建立在已有物理网络上的虚拟网络，在Swarm中用于连接不同机器上的docker容器，允许不同机器上的容器相互通信情况下使用 `docker network create -d overlay <网络名称>` 创建的网络只能被 `swarm service` 使用，如果需要被独立的容器使用，需要添加 `--attachable` 选项

## 2. 命令行创建虚拟网络

```sh
docker network create -d overlay --attachable <网络名称>
```

## 3. 命令行中使用虚拟网络

在用 `docker run ....` 或 `docker service create ...` 创建容器时，使用 `--network <网络名称>` 参数

## 4. 在 `Docker Compose` 中创建和使用虚拟网络

```yaml
version: "3.9"
services:
  app:
    networks:
      - rebue
    # ...
  # ...
networks:
  rebue:
```

## 5. 在 `Docker Compose` 中配置默认使用的虚拟网络

```yaml
networks:
  default:
    rebue:
```

## 6. 在 `Docker compose` 中配置默认使用已存在的网络

```yaml
networks:
  default:
    external: true
    name: <网络名称>
```
