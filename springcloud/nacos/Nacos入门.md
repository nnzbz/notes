# Nacos入门

## 创建并启动docker容器

```sh
docker run --name nacos-standalone -e MODE=standalone -p 8848:8848 -d nacos/nacos-server:latest
```
