# Pulsar

## 单机

```sh
docker run -it -p 6650:6650  -p 8080:8080 --mount source=pulsardata,target=/pulsar/data --mount source=pulsarconf,target=/pulsar/conf apachepulsar/pulsar:2.10.1 bin/pulsar standalone
```

## Swarm

```sh
mkdir -p /usr/local/pulsar
vi /usr/local/pulsar/stack.yml
```

```ini
version: '3.9'
services:
  svr:
    image: apachepulsar/pulsar:2.10.1
#    ports:
#      - 6650:6650
#      - 8080:8080
    volumes:
#      - /usr/local/pulsar/conf:/pulsar/conf:z
      - pulsardata:/pulsar/data:z
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    command: bin/pulsar standalone
    deploy:
      placement:
        constraints:
          # 部署的节点指定是app角色的
          - node.labels.role==app
          #- node.hostname == app01
    logging:
      options:
        max-size: 50m

volumes:
  pulsardata:

networks:
  default:
    external: true
    name: rebue
```

```sh
docker stack deploy -c /usr/local/pulsar/stack.yml pulsar
```
