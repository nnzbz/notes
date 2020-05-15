# Sonatype Nexus Repository OSS安装方法

[TOC]

## 1. Nexus简介

### 1.1. Nexus是什么

Sonatype Nexus Repository OSS 是 Apache Maven 私服仓库，永久免费。

### 1.2. 官网

http://www.sonatype.com/nexus-repository-oss

## 2. 安装配置

### 2.1. 安装：解压到任意目录

我的安装路径为

```sh
/usr/local/maven/nexus-3.5.0-02-mac
```

### 2.2. Linux下的配置

- 创建用户及用户组，并设置密码

```sh
groupadd nexus
useradd -g nexus nexus
passwd nexus
nexus123
```

- 配置权限

```sh
sudo chown -R nexus:nexus /usr/local/maven/nexus-3.6.0-02/ /usr/local/maven/sonatype-work/
sudo chmod -R 755 /usr/local/maven/nexus-3.6.0-02/ /usr/local/maven/sonatype-work/
```

- 配置运行的nexus文件

```sh
# 修改运行服务的用户为nexus
sed -i "s/run_as_user=''/run_as_user='nexus'/" /usr/local/maven/nexus-3.6.0-02/bin/nexus
# 配置jre的路径
export a="/usr/local/java/jdk1.8.0_152"
sed -i "/# INSTALL4J_JAVA_HOME_OVERRIDE=/aINSTALL4J_JAVA_HOME_OVERRIDE=$a" /usr/local/maven/nexus-3.6.0-02/bin/nexus
```

### 2.3. 更改默认端口

一般使用默认配置就可以了

1、 修改配置文件：..\etc\org.sonatype.nexus.cfg
2、 配置属性：application-port=8084

### 2.4. 修改 Nexus 服务，启动时的内存

一般使用默认配置就可以了

1、 配置文件：../bin/nexus.vmoptions
2、 配置属性：-Xms1024M -Xmx1024M

## 3. 手动启动

### 3.1. Linux/Unix/MacOSX

```sh
./nexus run
```

### 3.2. Windows

```sh
nexus.exe /run
```

## 4. 注册服务

### 4.1. Linux下注册服务

- nexus.service

```sh
vi /etc/systemd/system/nexus.service
```

```ini
[Unit]
Description=nexus service
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/maven/nexus-3.6.0-02/bin/nexus start
ExecStop=/usr/local/maven/nexus-3.6.0-02/bin/nexus stop
User=nexus
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

- systemctl

```sh
systemctl daemon-reload
systemctl enable nexus
systemctl start nexus
```

### 4.2. Windows下注册服务

1、 使用**管理员权限**运行 cmd
2、 进入解压目录：..%nexus-install-dir%\bin
3、 在 cmd 中执行命令，注册服务：nexus.exe /install
4、 服务注册成功后，提示：“Installed service 'nexus'”
5、 在 cmd 中执行命令，卸载服务：nexus.exe /uninstall

### 4.3. Mac OS X下注册服务

创建com.sonatype.nexus.plist文件，保存在/Library/LaunchDaemons/目录下

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sonatype.nexus</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/nexus-3.5.0-02-mac/nexus-3.5.0-02/bin/nexus</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

改变文件的访问权限

```sh
sudo chown root:wheel /Library/LaunchDaemons/com.sonatype.nexus.plist
sudo chmod 644 /Library/LaunchDaemons/com.sonatype.nexus.plist
```

手动运行

```sh
sudo launchctl load /Library/LaunchDaemons/com.sonatype.nexus.plist
```

### 4.4. 运行 Nexus OSS 服务

1、 在 Windows 服务管理中，启动 名为 “nexus” 的服务，可设置为随操作系统自动启动
2、 访问地址：http://localhost:8081，默认账号密码：admin / admin123

## 5. 配置Nexus

### 5.1. 配置常用的仓库

1、登录后，进入菜单：```Nexus Repository Manager``` > ```Repository``` > ```Repositories```

2、常用的代理仓库如下
| name   | type  | url                                                  | remark                |
| ------ | ----- | ---------------------------------------------------- | --------------------- |
| aliyun | proxy | http://maven.aliyun.com/nexus/content/groups/public/ | 阿里国内镜像          |
| spring | proxy | http://repo.spring.io/milestone/                     | 有spring一些较新的jar |

> 注意： ```Maven 2``` > ```Version policy``` > 选择 ```Mixed```

### 5.2. 创建自己的部署仓库

创建**my-repository**或分别创建**my-releases**和**my-snapshots**仓库

- 操作步骤：
  - ```Create repository``` > ```maven2(hosted)```
- 填写的主要内容：
  - name : ```my-repository``` 或 ```my-releases``` 或 ```my-snapshots```
  - Version policy : ```Mixed``` 或 ```Release``` 或 ```Snapshot```
  - Deployment policy : ```Allow redeploy```

### 5.3. 配置默认的仓库组：maven-public

将上面添加的代理仓库及自己的仓库添加到 ```maven-public``` 组

### 5.4. 创建专门用于部署的角色

- 操作步骤：
  - ```Create role```
- 填写的主要内容：
  - Role ID : ```nx-my-deployment```
  - Role name : ```nx-my-deployment```
  - Role description : ```My releases and snapshots and docker image deployment role```
  - Privileges > Given :
    - ```nx-repository-admin-maven2-my-repository-*```
    - ```nx-repository-view-maven2-my-repository-*```
    - 或
    - ```nx-repository-admin-maven2-my-releases-*```
    - ```nx-repository-admin-maven2-my-snapshots-*```
    - ```nx-repository-view-maven2-my-releases-*```
    - ```nx-repository-view-maven2-my-snapshots-*```

### 5.5. 新建专门用于部署的用户

- 操作步骤：
  - ```Create user```
- 填写的主要内容：
  - ID : ```my-deployment```
  - Password : ```deployment123```
  - Status : ```Active```
  - Roles > Granted : ```nx-my-deployment```

## 6. 配置Maven的settings文件

修改配置文件：../M2_HOME/conf/setttings.xml

```xml
....

<!-- Nexus OSS 部署账号配置 -->
<servers>
    <server>
        <id>my-snapshots</id>
        <username>my-deployment</username>
        <password>deployment123</password>
    </server>
    <server>
        <id>my-releases</id>
        <username>my-deployment</username>
        <password>deployment123</password>
    </server>
    <!-- Maven中央仓库 -->
    <!-- <server>
        <id>oss</id>
        <username>Username Of User Token</username>
        <password>Password Of User Token</password>
    </server> -->
    <!-- <server>
        <id>docker.io</id>
        <username>nnzbz</username>
        <password>＊＊＊＊＊＊</password>
    </server> -->
</servers>

....

<profiles>
    <profile>
        <!-- 仓库的配置，在上面设置无效，或者可以在pom.xml中设置 -->
        <id>repository</id>
        <properties>
            <!-- Mac中gpg的路径，从eclipse将项目部署到中央仓库时需要指定 -->
            <!-- <gpg.executable>/usr/local/bin/gpg</gpg.executable> -->
            <!-- 使用gpg的密码，如果不想每次部署时都手动输入，可在这里配置 -->
            <!-- <gpg.passphrase>******</gpg.passphrase> -->
        </properties>
        <repositories>
            <!-- 仓库（私服） -->
            <repository>
                <id>repository</id>
                <url>${repository.url}</url>
                <releases>
                    <enabled>true</enabled>
                </releases>
                <snapshots>
                    <enabled>true</enabled>
                </snapshots>
            </repository>
        </repositories>

        <!-- 插件仓库（私服） -->
        <pluginRepositories>
            <pluginRepository>
                <id>pluginRepository</id>
                <url>${repository.url}</url>
                <releases>
                    <enabled>true</enabled>
                </releases>
                <snapshots>
                    <enabled>true</enabled>
                </snapshots>
            </pluginRepository>
        </pluginRepositories>
    </profile>

    <profile>
        <id>aliyun-url</id>
        <properties>
            <repository.url>http://maven.aliyun.com/nexus/content/groups/public/</repository.url>
        </properties>
    </profile>

    <profile>
        <id>nexus-url</id>
        <properties>
            <repository.url>http://${nexus.host}/repository/maven-public/</repository.url>
        </properties>
    </profile>

    <!-- 本机私服配置 -->
    <profile>
        <id>local-nexus-host</id>
        <properties>
            <nexus.host>127.0.0.1:8081</nexus.host>
            <!-- 配置部署的远程仓库url -->
            <my-snapshots.url>http://${nexus.host}/repository/my-repository/</my-snapshots.url>
            <my-releases.url>http://${nexus.host}/repository/my-repository/</my-releases.url>
            <!-- Docker服务器地址 -->
            <!-- <my-docker.host>127.0.0.1:8082</my-docker.host> -->
        </properties>
    </profile>

    <!-- 内网私服配置 -->
    <profile>
        <id>intranet-nexus-host</id>
        <properties>
            <nexus.host>192.168.1.201:8081</nexus.host>
            <!-- 配置部署的远程仓库url -->
            <my-snapshots.url>http://${nexus.host}/repository/my-snapshots/</my-snapshots.url>
            <my-releases.url>http://${nexus.host}/repository/my-releases/</my-releases.url>
            <!-- Docker服务器地址 -->
            <!-- <my-docker.host>192.168.1.201:8082</my-docker.host> -->
        </properties>
    </profile>
</profiles>

<activeProfiles>
    <activeProfile>repository</activeProfile>
    <!-- <activeProfile>aliyun-url</activeProfile> -->
    <activeProfile>nexus-url</activeProfile>
    <!-- 本机私服配置 -->
    <!-- <activeProfile>local-nexus-host</activeProfile> -->
    <!-- 内网私服配置 -->
    <activeProfile>intranet-nexus-host</activeProfile>
</activeProfiles>
```

## 7. 配置pom.xml文件

```xml
<project ....>
    ....

    <!-- 配置部署的远程仓库 -->
    <distributionManagement>
        <snapshotRepository>
            <id>my-snapshots</id>
            <name>my-snapshots</name>
            <url>${my-snapshots.url}</url>
            <uniqueVersion>true</uniqueVersion>
        </snapshotRepository>
        <repository>
            <id>my-releases</id>
            <name>my-releases</name>
            <url>${my-releases.url}</url>
        </repository>
    </distributionManagement>

    或
    <!-- 部署中央仓库 -->
    <distributionManagement>
        <snapshotRepository>
            <id>oss</id>
            <url>https://oss.sonatype.org/content/repositories/snapshots/</url>
        </snapshotRepository>
        <repository>
            <id>oss</id>
            <url>https://oss.sonatype.org/service/local/staging/deploy/maven2/</url>
        </repository>
    </distributionManagement>

    ....
</project>
```
