# Flink的Tip

[TOC]

## 1. 官方帮助文档

<https://ci.apache.org/projects/flink/flink-docs-release-1.13/zh/>

## 2. 运行

### 2.1. 改变 WebUI 的端口

```sh
cd /usr/local/flink-1.13.2/
vi conf/flink-conf.yaml
```

```ini
....

# rest.port: 8081
rest.port: 8091

....
```

### 2.2. 启动与停止

```sh
cd /usr/local/flink-1.13.2/
# 启动
./bin/start-cluster.sh
# 停止
./bin/stop-cluster.sh
```
