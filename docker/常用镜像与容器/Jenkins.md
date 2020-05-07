# Jenkins

[TOC]

## 1. 创建并运行容器

```sh
docker run --name jenkins -dp8080:8080 -p50000:50000 -v /your/home:/var/jenkins_home --restart always jenkins
```

- /your/home
  为映射到宿主机的目录，请注意容器内jenkins用户(uid 1000)对它的访问权限

## 2. 典型示例

在宿主机上执行

```sh
mkdir /var/jenkins_home


# 添加jenkins用户并指定uid为1000
useradd jenkins -u 1000
sudo chown -R jenkins:jenkins /var/jenkins_home
# 或
sudo chown -R 1000:1000 /var/jenkins_home

# sudo chmod 774 -R /var/jenkins_home

docker run --name jenkins -dp13080:8080 -p50000:50000 -v /var/jenkins_home:/var/jenkins_home --restart always jenkins

# 查看管理员密码
cat /var/jenkins_home/secrets/initialAdminPassword
```

- 初始化安装插件时jenkins需要访问外网，需要docker开放容器访问外网的能力
- `An error occurred during installation: No such plugin: cloudbees-folder`错误
  重启容器
