# xxl-job

[TOC]

## 1. 根据SQL脚本创建数据库

SQL脚本在github项目中的位置为:

`/xxl-job/doc/db/tables_xxl_job.sql`

也可直接打开链接

<https://github.com/xuxueli/xxl-job/blob/master/doc/db/tables_xxl_job.sql>

## 2. 创建并运行容器

```sh
docker run -e PARAMS="--spring.datasource.url=jdbc:mysql://db:3306/xxl_job?Unicode=true&characterEncoding=UTF-8 --spring.datasource.username=xxl_job --spring.datasource.password=xxl_job" -p <主机端口号>:8080 -v /var/log/xxl-job:/data/applogs --link mysql:db --name xxl-job-admin  -d xuxueli/xxl-job-admin:<版本号>
```

- --spring.datasource.username 和 --spring.datasource.password 可根据实际xxl_job数据库设置的用户名和密码设置
- -v 将容器中/data/applogs目录中的日志输出到主机/var/log/xxl-job目录下，输出目录可根据自己的需要调整
