# PostgreSQL

## 单机

```sh
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```

## Swarm

```sh
mkdir -p /usr/local/pgsql
vi /usr/local/pgsql/stack.yml
```

```ini
version: '3.9'
services:
  db:
    image: postgres
    ports:
      - 5432:5432
    environment:
      # 用户名
      - POSTGRES_USER=postgres
      # 密码
      - POSTGRES_PASSWORD=xxxxxxxx
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      - pgsqldata:/var/lib/postgresql/data
    deploy:
      placement:
        constraints:
          # 部署的节点指定是db角色的
          - node.labels.role==db
          #- node.hostname == db01
    logging:
      options:
        max-size: 50m
  adminer:
    image: adminer
    ports:
      - 8080:8080
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    deploy:
      placement:
        constraints:
          # 部署的节点指定是db角色的
          - node.labels.role==db
          #- node.hostname == db01
    logging:
      options:
        max-size: 50m
volumes:
  pgsqldata:

networks:
  default:
    external: true
    name: rebue
```

```sh
docker stack deploy -c /usr/local/pgsql/stack.yml pgsql
```
