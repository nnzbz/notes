# MongoDB

[TOC]

## 1. Docker Compose

```sh
mkdir -p /usr/local/mongo
vi /usr/local/mongo/stack.yml
```

```yaml
version: '3.9'

services:

  db:
    image: mongo
    hostname: mongo
    container_name: mongo
    ports:
      - 27017:27017
    volumes:
      - mongodata:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    restart: always

  express:
    image: mongo-express
    hostname: mongo-express
    container_name: mongo-express
    ports:
      - 27081:8081
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: example
      ME_CONFIG_MONGODB_URL: mongodb://root:example@mongo:27017/
    restart: always

volumes:
  mongodata:

networks:
  default:
    external: true
    name: rebue
```

## 2. 环境变量说明

Name                            | Default         | Description
--------------------------------|-----------------|------------
ME_CONFIG_BASICAUTH_USERNAME    | ''              | mongo-express web username
ME_CONFIG_BASICAUTH_PASSWORD    | ''              | mongo-express web password
ME_CONFIG_MONGODB_ENABLE_ADMIN  | 'true'          | Enable admin access to all databases. Send strings: `"true"` or `"false"`
ME_CONFIG_MONGODB_ADMINUSERNAME | ''              | MongoDB admin username
ME_CONFIG_MONGODB_ADMINPASSWORD | ''              | MongoDB admin password
ME_CONFIG_MONGODB_PORT          | 27017           | MongoDB port
ME_CONFIG_MONGODB_SERVER        | 'mongo'         | MongoDB container name. Use comma delimited list of host names for replica sets.
ME_CONFIG_OPTIONS_EDITORTHEME   | 'default'       | mongo-express editor color theme, [more here](http://codemirror.net/demo/theme.html)
ME_CONFIG_REQUEST_SIZE          | '100kb'         | Maximum payload size. CRUD operations above this size will fail in [body-parser](https://www.npmjs.com/package/body-parser).
ME_CONFIG_SITE_BASEURL          | '/'             | Set the baseUrl to ease mounting at a subdirectory. Remember to include a leading and trailing slash.
ME_CONFIG_SITE_COOKIESECRET     | 'cookiesecret'  | String used by [cookie-parser middleware](https://www.npmjs.com/package/cookie-parser) to sign cookies.
ME_CONFIG_SITE_SESSIONSECRET    | 'sessionsecret' | String used to sign the session ID cookie by [express-session middleware](https://www.npmjs.com/package/express-session).
ME_CONFIG_SITE_SSL_ENABLED      | 'false'         | Enable SSL.
ME_CONFIG_SITE_SSL_CRT_PATH     | ''              | SSL certificate file.
ME_CONFIG_SITE_SSL_KEY_PATH     | ''              | SSL key file.

如果 `ME_CONFIG_MONGODB_ENABLE_ADMIN` 设为 `false` ， 只需要设置下面几项

Name                            | Default         | Description
--------------------------------|-----------------|------------
ME_CONFIG_MONGODB_AUTH_DATABASE | 'db'            | Database name
ME_CONFIG_MONGODB_AUTH_USERNAME | 'admin'         | Database username
ME_CONFIG_MONGODB_AUTH_PASSWORD | 'pass'          | Database password

## 3. 创建并运行容器

- 单机

```sh
docker-compose -f /usr/local/mongo/stack.yml up -d
```

- Swarm

```sh
docker stack deploy -c /usr/local/mongo/stack.yml mongo
```

## 4. 管理链接

<http://mongo-express:27081>

- 用户名: `admin`
- 密码: `pass`
- 默认建立的数据库是 `admin`

## 为单个数据库创建用户

```sh
mongosh
```

```mongo
use admin
db.auth("root","example")
use Employee
db.createUser({
  user: "Employeeadmin",
  pwd: "password",
  roles:[{
    role: "readWrite" , db:"Employee"
  }]
})
```

