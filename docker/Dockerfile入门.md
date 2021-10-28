# Dockerfile

[TOC]

## 1. 构建

进入Dockerfile的目录，然后执行下面的命令

```sh
docker build -t <镜像名称>:<镜像版本> .
# 例如
docker build -t centos-jdk:1.0.0 .
```

## 2. ENV

用于在容器build和run时给环境变量赋值

### 2.1. 格式

```Dockerfile
ENV key value
```

### 2.2. 如何传参

可以在 ```docker run``` 命令中通过 ```-e``` 标记来传递

```sh
docker run -i -t -e "TEST=hello" ubuntu /bin/bash
```

### 2.3. 使用

```Dockerfile
${A_KEY}
$ANOTHER_KEY
```

### 2.4. 注意事项

- 通过ENV定义的环境变量，如果使用 `RUN` 指令，那么在创建容器的启动容器的命令中，`docker run ....`，设置 `-e XXX=xxx` 将不会生效，要想生效，须放在 `CMD` 或 `ENTRYPOINT` 指令中执行
- 通过ENV定义的环境变量，在 `CMD` 指令中不能用 `CMD [xxx xxx]` 的方式，而要用 `CMD xxx xxx` 的方式

## 3. ARG

用以在容器build时定义需要的参数

### 3.1. 格式

```Dockerfile
# 定义参数
ARG A_NAME
# 定义参数（如果没有传入参数时，使用默认值）
ARG A_NOTHER_NAME=a_default_value
```

### 3.2. 如何传参

- 在pom.xml文件中的buildArgs节点下定义实参)
- 在docker build命令中以--build-arg A_NAME=a_value形式赋值

### 3.3. 使用

```Dockerfile
${A_NAME}
$A_NOTHER_NAME
```

### 3.4. 自带的ARG参数(只是不需要定义)

- HTTP_PROXY
- HTTPS_PROXY
- FTP_PROXY
- NO_PROXY

### 3.5. 注意事项

- ARG与ENV不同，只能在build时有效，而在run时无效
- 如果docker build命令传递的参数，在Dockerfile中没有对应的参数，将抛出如下警告 ```[Warning] One or more build-args [foo] were not consumed.```
- 不要与ENV同名，否则会被覆盖
- 如果在Dockerfile中，ARG指令定义参数之前，就有其他指令引用了参数，则参数值为空字符串

#### 3.5.1. 上节第2点的例题

```Dockerfile
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER v1.0.0
RUN echo $CONT_IMG_VER
```

#### 3.5.2. 上节第3点的例题

下面第2和第4行的USER的值分别是什么？

```Dockerfile
FROM busybox
USER ${user:-some_user}
ARG user
USER $user
```

第2行的USER的值为some_user，因为user变量在第3行才定义。第4行的USER值为what_user，因为user变量在它之前定义了并且在命令行给user变量赋值为what_user。
