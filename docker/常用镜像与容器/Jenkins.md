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

## 4. 查看密码

```sh
docker exec -it xxxx bash
cat /var/jenkins_home/secrets/initialAdminPassword
```
