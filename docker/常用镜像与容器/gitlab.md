# 在Docker中搭建gitlab

[TOC]

## 1. 拉取镜像

```sh
docker pull gitlab/gitlab-ce
```

## 2. 创建并运行容器

```sh
docker run --name gitlab-data gitlab/gitlab-ce echo "data-only container for gitlab"
docker run -d --hostname 192.168.1.201 --name gitlab -p10443:443 -p10022:22 -p10080:80 --restart always --volumes-from gitlab-data -e 'GITLAB_SSH_PORT=10022' -e 'GITLAB_PORT=10080' -e 'GITLAB_HOST=IP_ADDRESS' gitlab/gitlab-ce
#    -e 'GITLAB_SECRETS_DB_KEY_BASE=long-and-random-alpha-numeric-string' \
#    -e 'GITLAB_SECRETS_SECRET_KEY_BASE=long-and-random-alpha-numeric-string' \
#    -e 'GITLAB_SECRETS_OTP_KEY_BASE=long-and-random-alpha-numeric-string' \
```

## 3. 打开防火墙端口

```sh
firewall-cmd --zone=dmz --permanent --add-port=10022/tcp
firewall-cmd --zone=dmz --permanent --add-port=10080/tcp
firewall-cmd --zone=dmz --permanent --add-port=10043/tcp
firewall-cmd --reload
```

## 4. 网页访问502

```sh
docker exec -it gitlab /bin/bash
gitlab-ctl restart sidekiq
gitlab-ctl hup unicorn
exit
```

## 初始化

- 第一次访问网页改变管理员密码:
 admin
 wbl123456
 5c466e8eb5875bf48a0705e9a850a912
 zbz123456
 
- 注册新用户
 zbz
 nnzbz@163.com
 wbl123456
 zbz123456
 
 rebue
 5c466e8eb5875bf48a0705e9a850a912

## 克隆项目

```sh
git clone http://zbz@192.168.1.201:10080/wboly/wboly-suc.git
```