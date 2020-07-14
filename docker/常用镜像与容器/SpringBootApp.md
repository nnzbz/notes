# 在Docker中启动SpringBoot的服务

## 1. 准备服务的文件

```sh
mkdir -p /usr/local/luban-captcha-svr/9101
cd ~/workspaces/02/luban/luban-captcha/luban-captcha-svr
cp target/luban-captcha-svr-0.0.1-SNAPSHOT.jar /usr/local/luban-captcha-svr/
cp -r src/main/resources/. /usr/local/luban-captcha-svr/9101
cd /usr/local/luban-captcha-svr/9101/
ln ../luban-captcha-svr-0.0.1-SNAPSHOT.jar myservice.jar
```

## 2. 创建并启动容器

启动时注意映射端口号

```sh
docker run -d --net=host --name luban-captcha-svr-a -e "SERVER_PORT=9101" -v /usr/local/luban-captcha-svr/9101:/usr/local/myservice --restart=always nnzbz/spring-boot-app
```

- JAVA_OPTS
  如需自定义 JVM内存参数 等配置，可通过 "-e JAVA_OPTS" 指定，参数格式 `JAVA_OPTS="-Xmx512m"`

## 3. 开启防火墙

```sh
firewall-cmd --zone=dmz --permanent --add-port=9101/tcp
firewall-cmd --reload
```
