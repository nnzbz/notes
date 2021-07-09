# Docker创建虚拟网络

1. Overlay网络是建立在已有物理网络上的虚拟网络，在Swarm中用于连接不同机器上的docker容器，允许不同机器上的容器相互通信
2. 情况下使用 `docker network create -d overlay <网络名称>` 创建的网络只能被 `swarm service` 使用，如果需要被独立的容器使用，需要添加 `--attachable` 选项

    ```sh
    docker network create -d overlay --attachable <网络名称>
    ```

3. 在用 `docker run ....` 或 `docker service create ...` 创建容器时，使用 `--network <网络名称>` 参数
4. 在 `Docker-Compose` 默认使用已存在的网络如下配置:

   ```yaml
   networks:
     default:
       external:
         name: <网络名称>
   ```
