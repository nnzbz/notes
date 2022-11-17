# phpMyAdmin

## `Docker Compose`

```sh
mkdir -p /usr/local/mysql
vi /usr/local/mysql/phpmyadmin-stack.yml
```

```yaml{.}
version: "3.9"
services:
  web:
    image: phpmyadmin
    hostname: phpmyadmin
    ports:
      - 33068:80
    environment:
      - PMA_ARBITRARY=1
      - PMA_ABSOLUTE_URI=http://xxx.xxx.xxx.xxx:xxxx/phpmyadmin/
    deploy:
      placement:
        constraints:
          # 部署的节点指定是web角色的
          - node.labels.role==web
          #- node.hostname == db01
    logging:
      options:
        max-size: 50m

networks:
  default:
    external: true
    name: rebue
```

```sh
docker stack deploy -c /usr/local/mysql/phpmyadmin-stack.yml phpmyadmin
```
