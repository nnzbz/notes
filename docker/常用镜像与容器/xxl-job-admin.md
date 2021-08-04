# xxl-job-admin

[TOC]

## 1. docker仓库的地址

<https://hub.docker.com/r/xuxueli/xxl-job-admin/>

## 2. 根据SQL脚本创建数据库

在数据库中创建名为 `xxl_job` 的schema，账户名称为 xxl_job，密码自定义

SQL脚本在github项目中的位置为:

`/xxl-job/doc/db/tables_xxl_job.sql`

也可直接打开链接

<https://github.com/xuxueli/xxl-job/blob/master/doc/db/tables_xxl_job.sql>


## 3. 准备好配置文件

```sh
mkdir -p /usr/local/xxl-job-admin
vi /usr/local/xxl-job-admin/application.yml
```

```yml
spring:
  # 数据库连接
  datasource:
    # 172.17.0.1是容器内连接其它容器内MySQL数据库所需要设置的docker0的地址，可根据实际调整
    url: jdbc:mysql://172.17.0.1:3306/xxl_job?useUnicode=true&characterEncoding=UTF-8&autoReconnect=true&serverTimezone=Asia/Shanghai
    # 连接数据库的用户，可根据实际情况设置
    username: xxl_job
    # 连接数据库的密码，可根据实际情况设置
    password: xxl_job
  # 报警发件人邮箱
  mail:
    # 发件邮箱服务器，具体可以通过网页登录邮箱查看
    host: smtp.qq.com
    # 发件邮箱服务器端口号，具体可以通过网页登录邮箱查看
    port: 25
    # 发件人邮箱
    username: xxx@qq.com
    # 这里的密码是授权码，可以通过网页登录邮箱设置
    password: xxx
```

其它默认配置在 [application.properties](https://github.com/xuxueli/xxl-job/blob/master/xxl-job-admin/src/main/resources/application.properties)，可参考进行配置

## 4. 单机

```sh
docker run --name xxl-job-admin -dp <宿主机端口号>:8080 -v /usr/local/xxl-job-admin/application.yml:/application.yml -v /var/log/xxl-job:/data/applogs --restart=always xuxueli/xxl-job-admin:<指定版本>
```

Mac用下面的命令（因为Mac下只能映射 `~/` 下的文件）

```sh
docker run --name xxl-job-admin -dp <宿主机端口号>:8080 -v ~/docker/xxl-job-admin/application.yml:/application.yml --restart=always xuxueli/xxl-job-admin:2.3.0
```

- -v
  - 第一个: 将配置文件映射到容器中
  - 第二个: 将容器中/data/applogs目录中的日志输出到主机/var/log/xxl-job目录下，输出目录可根据自己的需要调整
- <宿主机端口号>
  暴露出来可供网页访问的端口，我们默认设置为6060
- <指定版本>
  必须填，因为目前 xxl_job 没有 latest 的 tag，目前最新的版本是 `2.3.0`
- JAVA_OPTS
  如需自定义 JVM内存参数 等配置，可通过 "-e JAVA_OPTS" 指定，参数格式 JAVA_OPTS="-Xmx512m"

## 5. Swarm

### 5.1. `Docker Compose`

```sh
mkdir -p /usr/local/xxl-job-admin
vi /usr/local/xxl-job-admin/stack.yml
```

```yml{.line-numbers}
version: "3.9"
services:
  xxl-job-admin:
    image: xuxueli/xxl-job-admin:2.3.0
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      - /usr/local/xxl-job-admin/application.yml:/application.yml
```

### 5.2. 部署

```sh
docker stack deploy -c /usr/local/xxl-job-admin/stack.yml xxl-job-admin
```

## 6. 网页管理地址

`http://<IP>:<port>/xxl-job-admin`

- IP
  docker宿主机的IP
- port
  docker容器暴露出来的端口
- 默认的登录名称和密码
  admin 123456
