# Jenkins

[TOC]

## 1. 单机

```sh
docker run --name jenkins \
    -dp8080:8080 \
    -p50000:50000 \
    -v /your/home:/var/jenkins_home \
    --restart always \
    jenkins
```

## 2. Swarm

```sh
mkdir /usr/local/jenkins
vi /usr/local/jenkins/stack.yml
```

```yaml{.line-numbers}
version: "3.9"
services:
  jenkins:
    image: jenkins/jenkins
    hostname: jenkins
    ports:
      - 50080:8080
      - 50000:50000
    environment:
      # 最好使用此设定时区，其它镜像也可以使用
      - TZ=CST-8
    volumes:
      - jenkinsdata:/var/jenkins_home

volumes:
  jenkinsdata:

networks:
  default:
    external: true
    name: rebue
```

- 部署

```sh
docker stack deploy -c /usr/local/jenkins/stack.yml jenkins
```

## 3. 浏览

<xxx.xxx.xxx.xxx:50080>

## 4. 初始化

- 查看初始化密码(也可通过日志查看)

```sh
docker exec -it xxxx bash
cat /var/jenkins_home/secrets/initialAdminPassword
```

- 安装推荐插件

## 配置

- 进入 `Manage Jenkins` > `Global Tool Configuration`
- 配置JDK/Git/Maven
- 可通过进入容器查看相关信息(Maven需选择自动安装)

```sh
docker exec -it jenkins容器id bash
# 查看Java的安装路径
echo $JAVA_HOME     # /opt/java/openjdk
# 查看git的安装路径
which git           # /usr/bin/git
```
