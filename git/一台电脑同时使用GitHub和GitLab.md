# 一台电脑同时使用GitHub和GitLab

[TOC]

## 1. 用Git生成两把钥匙

### 1.1. 命令

```sh
# GitHub的钥匙
ssh-keygen -t rsa -C "GitHub的钥匙/GitLab的钥匙"
```

- **```-C```**: 注释
- 注意key保存的文件要不一样

### 1.2. 示例

```sh
~$ ssh-keygen -t rsa -C "GitHub的钥匙"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/zbz/.ssh/id_rsa): /home/zbz/.ssh/id_rsa_github
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/zbz/.ssh/id_rsa_github.
Your public key has been saved in /home/zbz/.ssh/id_rsa_github.pub.
The key fingerprint is:
SHA256:lnfJ7/53eI24KX751l/zkLW/vmgORY9O5tMohwkzFXQ GitHub的钥匙
The key's randomart image is:
+---[RSA 2048]----+
|          .o E   |
|            o    |
|           . .   |
|         .....o  |
|        S+. += ..|
|       . .+.O.oo.|
|           = O+Bo|
|          . B+*.@|
|         ..o=B=*@|
+----[SHA256]-----+

~$ ssh-keygen -t rsa -C "GitLab的钥匙"
Generating public/private rsa key pair.
Enter file in which to save the key (/home/zbz/.ssh/id_rsa): /home/zbz/.ssh/id_rsa_gitlab
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/zbz/.ssh/id_rsa_gitlab.
Your public key has been saved in /home/zbz/.ssh/id_rsa_gitlab.pub.
The key fingerprint is:
SHA256:BBqAwXuOqprTA47bBU6B9PciOGFszfgLWEMGZYHWeEQ GitLab的钥匙
The key's randomart image is:
+---[RSA 2048]----+
|+B%E. .          |
|=O=o o .         |
|o**+..  .        |
|+o++. ..         |
|.+*o . .S        |
|.+ooo .          |
|+o...            |
|++o.             |
|Bo..             |
+----[SHA256]-----+
```

完成后会在~/.ssh/目录下生成以下文件:

- id_rsa_github
- id_rsa_github.pub
- id_rsa_gitlab
- id_rsa_gitlab.pub

## 2. 配置pub到github和gitlab中

将两个pub文件分别配置到github和gitlab的sshkey中

### 2.1. github

项目 -> Settings -> Deploy keys -> Add deploy key

复制id_rsa_github.pub的全部内容示例如下

```text
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDHgmthZMFmX3umkzF9ioGgfLWw24EMuAyvCiP1qeTq3KPWs6tbD28lcbbmI2B0CpSNVFDkYBB/cFhJg7Oi50gkCi9Rarhx5Tq8GysGt2SoyoEYNvzvV9B/aJXwokRX0/zrnZCRVyx8hFA3XwlZgdGv9GHHkdU/mAFHcVIqY02zA0IJ/aT+GJ8PiMeN9fRs1LW5La6AAxWGpeTVb4CkuKM+gXkSzyYYcTkBdyDmPbs1lkMNW4BVyNDKSzqyDvbNNfME1o3wV1z4c8BhGF4bxk4PDavEV2YMrTDkW7sDoOMN2SwAEPjFcMsQNG7pIBijKDo4st7YtC2sTuA9aFpxmtv5 GitHub的钥匙
```

### 2.2. gitlab

打开gitlab账户 -> SSH Keys -> key粘贴内容如上 -> title -> Add key

## 3. 配置GIT的config文件

```sh
cd ~/.ssh/
vi config
```

配置内容示例如下：

```text
#github
Host github
        HostName github.com
        IdentityFile ~/.ssh/id_rsa_github

#gitlab
Host gitlab
        HostName gitlab.com
        IdentityFile ~/.ssh/id_rsa_gitlab
```

## 4. 配置仓库

例如:

github工作仓库:~/workspace/github
gitlab工作仓库:~/workspace/gitlab

- gitlab

```sh
cd ~/workspace/gitlab
git init
git config --global user.name 'personal'
git config --global user.email 'personal@company.com'
```

- github

```sh
cd ~/workspace/github
git init
git config --local user.name 'kingboy'
git config --local user.email 'kingboy@163.com'
```

接下来在两个目录下新建或者clone项目开发即可.
