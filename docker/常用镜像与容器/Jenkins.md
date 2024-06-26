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
    # 提升容器权限(方便进入容器安装软件)
    privileged: true
    # 使用 root 用户(方便进入容器安装软件)
    user: root
    environment:
      # - JAVA_OPTS="-server -Xms1024m -Xmx2048m -XX:PermSize=256m -XX:MaxPermSize=512m"
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

## 5. 配置

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

- git去掉ssl校验(否则pull以https开头的地址时可能会报错)

```sh
git config --global http.sslVerify false
```

## 6. 安装Maven

```sh
MAVEN_VERSION=3.8.3
MAVEN_ZIP_FILE_NAME=apache-maven-${MAVEN_VERSION}-bin.tar.gz
MAVEN_URL=https://dlcdn.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/${MAVEN_ZIP_FILE_NAME}
curl -fsSL ${MAVEN_URL} -o /usr/local/${MAVEN_ZIP_FILE_NAME}
tar zxvf /usr/local/${MAVEN_ZIP_FILE_NAME} && rm -f /usr/local/${MAVEN_ZIP_FILE_NAME}
# 写入PATH并添加到启动文件
cat >> ~/.bash_profile << EOF
export MAVEN_HOME=/usr/local/apache-maven-${MAVEN_VERSION}
export PATH=${MAVEN_HOME}/bin:${PATH}
EOF
```

## 7. 添加插件

- Maven Integration
- Maven Info
- SSH Pipeline Steps
- Publish Over SSH
- Extended Choice Parameter
- Git Parameter

## 8. 参考

<https://www.jenkins.io/zh/doc/>
