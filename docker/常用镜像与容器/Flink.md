# Flink

[TOC]

## Appclication

```sh
mkdir /usr/local/flink
vi /usr/local/flink/stack.yml
```

```yaml{.line-numbers}
version: "3.9"
services:
  jobmanager:
    image: flink:1.13.2-scala_2.12
    ports:
      - "8091:8081"
    command: standalone-job --job-classname com.job.ClassName [--job-id <job id>] [--fromSavepoint /path/to/savepoint [--allowNonRestoredState]] [job arguments]
    volumes:
      - /host/path/to/job/artifacts:/opt/flink/usrlib
    environment:
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager
        parallelism.default: 2        
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    deploy:
      replicas: 3

  taskmanager:
    image: flink:1.13.2-scala_2.12
    depends_on:
      - jobmanager
    command: taskmanager
    volumes:
      - /host/path/to/job/artifacts:/opt/flink/usrlib
    environment:
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager
        taskmanager.numberOfTaskSlots: 2
        parallelism.default: 2
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    deploy:
      replicas: 2

networks:
  default:
    external: true
    name: rebue
```

## Session

```sh
mkdir /usr/local/flink
vi /usr/local/flink/stack.yml
```

```yaml
version: "3.9"
services:
  jobmanager:
    image: nnzbz/flink-with-connector-jdbc:1.13.3
    ports:
      - "8091:8081"
    command: jobmanager
    environment:
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager

  taskmanager:
    image: flink:1.13.3-scala_2.12
    depends_on:
      - jobmanager
    command: taskmanager
    environment:
      - |
        FLINK_PROPERTIES=
        jobmanager.rpc.address: jobmanager
        taskmanager.numberOfTaskSlots: 2
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    deploy:
      replicas: 2

networks:
  default:
    external: true
    name: rebue
```
