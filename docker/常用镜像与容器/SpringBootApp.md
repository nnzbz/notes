# 在Docker中启动SpringBoot的服务

## 1. Dockerfile

```Dockerfile
# 基础镜像
FROM nnzbz/centos-jre
# 作者及邮箱
MAINTAINER zbz <nnzbz@163.com>

# 设置工作目录
WORKDIR /usr/local/myservice

# 运行服务
ENTRYPOINT ["/bin/bash", "-c", "java -Djava.security.egd=file:/dev/./urandom -server -jar myservice.jar"]
```

## 2. 编译

```sh
docker build -t nnzbz/spring-boot-app:1.0.0 .
docker tag nnzbz/spring-boot-app:1.0.0 nnzbz/spring-boot-app:latest
docker push nnzbz/spring-boot-app:1.0.0
docker push nnzbz/spring-boot-app:latest
```

## 3. 准备服务的文件

```sh
mkdir -p /usr/local/luban-captcha-svr/9101
cd ~/workspaces/02/luban/luban-captcha/luban-captcha-svr
cp target/luban-captcha-svr-0.0.1-SNAPSHOT.jar /usr/local/luban-captcha-svr/
cp -r src/main/resources/. /usr/local/luban-captcha-svr/9101
cd /usr/local/luban-captcha-svr/9101/
ln ../luban-captcha-svr-0.0.1-SNAPSHOT.jar myservice.jar
```

## 4. 创建并启动容器

启动时注意映射端口号

```sh
docker run -d --net=host --name luban-captcha-svr-a -e "SERVER_PORT=9101" -v /usr/local/luban-captcha-svr/9101:/usr/local/myservice --restart=always nnzbz/spring-boot-app
```

## 5. 开启防火墙

```sh
firewall-cmd --zone=dmz --permanent --add-port=9101/tcp
firewall-cmd --reload
```
