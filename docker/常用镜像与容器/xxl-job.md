# xxl-job

[TOC]

## 1. docker仓库的地址

<https://hub.docker.com/r/xuxueli/xxl-job-admin/>

## 2. 根据SQL脚本创建数据库

SQL脚本在github项目中的位置为:

`/xxl-job/doc/db/tables_xxl_job.sql`

也可直接打开链接

<https://github.com/xuxueli/xxl-job/blob/master/doc/db/tables_xxl_job.sql>

## 3. 创建并运行容器

```sh
docker run --name xxl-job-admin -e PARAMS="--spring.datasource.url=jdbc:mysql://db:3306/xxl_job?Unicode=true&characterEncoding=UTF-8 --spring.datasource.username=xxl_job --spring.datasource.password=xxl_job" -dp <主机端口号>:8080 -v /var/log/xxl-job:/data/applogs --link mysql:db --restart=always xuxueli/xxl-job-admin:<版本号>
```

- --spring.datasource.username 和 --spring.datasource.password
  可根据实际xxl_job数据库设置的用户名和密码设置
- -v
  将容器中/data/applogs目录中的日志输出到主机/var/log/xxl-job目录下，输出目录可根据自己的需要调整
- <主机端口号>
  暴露出来可供网页访问的端口
- <版本号>
  必须填，因为目前 xxl_job 没有 latest 的 tag
- JAVA_OPTS
  如需自定义 JVM内存参数 等配置，可通过 "-e JAVA_OPTS" 指定，参数格式 JAVA_OPTS="-Xmx512m"

## 4. 网页管理地址

`http://<IP>:<port>/xxl-job-admin`

- IP
  docker宿主机的IP
- port
  docker容器暴露出来的端口
- 默认的登录名称和密码
  admin 123456
