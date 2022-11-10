# Postgre入门

[TOC]

## 创建用户和数据库并授权

```sql
# 创建用户
CREATE USER dbuser WITH PASSWORD '********';

# 创建数据库
CREATE DATABASE exampledb OWNER dbuser;

# 将 exampledb 数据库的搜索权限都赋予给 dbuser
GRANT ALL PRIVILEGES ON DATABASE exampledb TO dbuser;
# 将public下所有表的操作权限都赋予给 dbuser
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dbuser;
```
