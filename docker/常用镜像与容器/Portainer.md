# Portainer

## 参考

<https://docs.portainer.io/>

## Swarm

- 参考链接
<https://docs.portainer.io/v/ce-2.9/start/install/server/swarm/linux>

- 下载

```sh
mkdir -p /usr/local/portainer
curl -L https://downloads.portainer.io/portainer-agent-stack.yml \
    -o /usr/local/portainer/portainer-agent-stack.yml
```

- 修改 `/usr/local/portainer/portainer-agent-stack.yml`
  - 首行 `version` 改为 `3.9`
  - ~~在每个镜像版本最后加上 `-alpine`~~ 目前2.9.2版本不能加 `alpine`，否则点击 `primary` 进不去
  - 删除每个服务的 `network`
  - 末尾添加 `networks`

    ```yaml
    networks:
      default:
        external: true
        name: rebue
    ```

  - 最终示例如下
  
```yaml
version: '3.9'

services:
  agent:
    image: portainer/agent:2.9.2
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /var/lib/docker/volumes:/var/lib/docker/volumes
    deploy:
      mode: global
      placement:
        constraints: [node.platform.os == linux]

  portainer:
    image: portainer/portainer-ce:2.9.2
    command: -H tcp://tasks.agent:9001 --tlsskipverify
    ports:
      - "9443:9443"
      - "9000:9000"
      - "8000:8000"
    volumes:
      - portainer_data:/data
    deploy:
      mode: replicated
      replicas: 1
      placement:
        constraints: [node.role == manager]

volumes:
  portainer_data:

networks:
  default:
    external: true
    name: rebue
```

- 部署

```sh
docker stack deploy -c /usr/local/portainer/portainer-agent-stack.yml portainer
```
