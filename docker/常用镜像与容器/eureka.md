# 制作eureka-server的Docker容器

[TOC]

## 1. 制作eureka-server单机版

### 1.1. 准备配置文件

- application.yml

```yaml
spring:
  profiles:
    active: dev

logging:
  config: classpath:config/log4j2.xml
```

- application-dev.yml(单机版用)

```yaml
debug: true

server:
  # eureka服务端启动的端口号
  port: 8761

eureka:
  server:
    # 在集群里中，Eureka服务器获取不到其它服务器上的实例时，需要等待的时间，单位为毫秒，默认为1000 * 60 * 5
    waitTimeInMsWhenSyncEmpty: 0
  client:
    # 下面两项实为关闭eureka客户端，表示是eureka的独立服务端
    register-with-eureka: false
    fetch-registry: false
```

### 1.2. 从eureka-server项目中制作镜像(略)

### 1.3. 创建并运行容器

```sh
docker run -dp8761:8761 --name eureka-server -e "ES_JAVA_OPTS=-Xms256m -Xmx256m" --restart=always nnzbz/eureka-server
```

## 2. 制作eureka集群

### 2.1. 准备配置文件

```sh
sudo mkdir -p /usr/local/eureka-server
cd /usr/local/eureka-server/
```

本机远程复制配置文件

```sh
cd ~/workspaces/02/scx/eureka-server/

scp -r src/main/resources/ root@192.168.1.201:/usr/local/eureka-server/8761/

scp -r src/main/resources/ root@192.168.1.201:/usr/local/eureka-server/8762/

scp -r src/main/resources/ root@192.168.1.201:/usr/local/eureka-server/8763/
```

- 部署服务器

```sh
# 修改为生产模式
sudo sed -i 's/active: dev/active: prod/' 8761/config/application.yml
sudo sed -i 's/active: dev/active: prod/' 8762/config/application.yml
sudo sed -i 's/active: dev/active: prod/' 8763/config/application.yml

#sudo sed -i 's#defaultZone: http://eureka-server-b:8762/eureka/,http://eureka-server-c:8763/eureka/$#defaultZone: http://eureka-server-a:8761/eureka/,http://eureka-server-c:8763/eureka/#' 8762/config/application-prod.yml
#sudo sed -i 's#defaultZone: http://eureka-server-b:8762/eureka/,http://eureka-server-c:8763/eureka/$#defaultZone: http://eureka-server-a:8761/eureka/,http://eureka-server-b:8762/eureka/#' 8763/config/application-prod.yml

sudo sh -c "echo '' >>8761/config/application-prod.yml"
sudo sh -c "echo 'eureka:' >>8761/config/application-prod.yml"
sudo sh -c "echo '  client:' >>8761/config/application-prod.yml"
sudo sh -c "echo '    serviceUrl:' >>8761/config/application-prod.yml"
sudo sh -c "echo '      # 这里指向的是集群的另两台节点' >>8761/config/application-prod.yml"
sudo sh -c "echo '      defaultZone: http://eureka-server-b:8762/eureka/,http://eureka-server-c:8763/eureka/' >>8761/config/application-prod.yml"

sudo sh -c "echo '' >>8762/config/application-prod.yml"
sudo sh -c "echo 'eureka:' >>8762/config/application-prod.yml"
sudo sh -c "echo '  client:' >>8762/config/application-prod.yml"
sudo sh -c "echo '    serviceUrl:' >>8762/config/application-prod.yml"
sudo sh -c "echo '      # 这里指向的是集群的另两台节点' >>8762/config/application-prod.yml"
sudo sh -c "echo '      defaultZone: http://eureka-server-a:8761/eureka/,http://eureka-server-c:8763/eureka/' >>8762/config/application-prod.yml"

sudo sh -c "echo '' >>8763/config/application-prod.yml"
sudo sh -c "echo 'eureka:' >>8763/config/application-prod.yml"
sudo sh -c "echo '  client:' >>8763/config/application-prod.yml"
sudo sh -c "echo '    serviceUrl:' >>8763/config/application-prod.yml"
sudo sh -c "echo '      # 这里指向的是集群的另两台节点' >>8763/config/application-prod.yml"
sudo sh -c "echo '      defaultZone: http://eureka-server-a:8761/eureka/,http://eureka-server-b:8762/eureka/' >>8763/config/application-prod.yml"

```

> **注意：不同的节点要相应的修改ip和port的地方**

### 2.2. 修改hosts文件

```sh
vi /etc/hosts
```

### 2.3. 从eureka-server项目中制作镜像(同单机版)

### 2.4. 创建并启动容器

```sh
docker run -d --net=host --name eureka-server-a -e "SERVER_PORT=8761" \
--restart=always \
-v /usr/local/eureka-server/8761/config:/usr/local/myservice/config \
-v /usr/local/eureka-server/8761/logs:/usr/local/myservice/logs \
nnzbz/eureka-server:1.0.3-SNAPSHOT
docker run -d --net=host --name eureka-server-b -e "SERVER_PORT=8762" \
--restart=always \
-v /usr/local/eureka-server/8762/config:/usr/local/myservice/config \
-v /usr/local/eureka-server/8762/logs:/usr/local/myservice/logs \
nnzbz/eureka-server:1.0.3-SNAPSHOT
docker run -d --net=host --name eureka-server-c -e "SERVER_PORT=8763" \
--restart=always \
-v /usr/local/eureka-server/8763/config:/usr/local/myservice/config \
-v /usr/local/eureka-server/8763/logs:/usr/local/myservice/logs \
nnzbz/eureka-server:1.0.3-SNAPSHOT
```

### 2.5. 开启防火墙

```sh
firewall-cmd --zone=dmz --permanent --add-port=8761/tcp
firewall-cmd --zone=dmz --permanent --add-port=8762/tcp
firewall-cmd --zone=dmz --permanent --add-port=8763/tcp
firewall-cmd --reload
```
