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
    environment:
      - PMA_ARBITRARY=1
      - PMA_ABSOLUTE_URI=http://xxx.xxx.xxx.xxx:xxxx/phpmyadmin/
networks:
  default:
    external: true
    name: rebue
```

```sh
docker stack deploy -c /usr/local/mysql/phpmyadmin-stack.yml phpmyadmin
```

## nginx映射

```json
server {
    ....

    location /phpmyadmin {
        proxy_pass http://phpmyadmin/;
    }
}
```

## 访问

<http://xxx.xxx.xxx.xxx:xxxx/phpmyadmin/>

- 注意：不能省略后面的 `/`
