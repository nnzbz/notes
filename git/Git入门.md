# Git入门

[TOC]

## 1. 初次配置

首先必须配置用户信息，包括用户名和邮箱地址。这两条配置信息很重要，git每次提交时都会引用用户信息，说明是谁提交的更新，并且永久保存到历史记录中。

```sh
git config --global user.name "zbz"
git config --global user.email "nnzbz@163.com"
# 查看配置信息
git config --list
```

可以使用#git config --list来查看配置信息，不过有时候会看到重复的变量名，那就说明它们来自不同的配置文件（比如/etc/gitconfig和~/.gitconfig），最终Git 实际采用的是最后一个。
也可以直接查阅某个变量#git config user.name

## 2. 常用命令简图

![Git常用命令简图](Git常用命令简图.jpg)

## 3. Git常用操作

### 3.1. 初始化

#### 3.1.1. 创建仓库

```sh
#初始化此文件夹为一个空的仓库
git --bare init
```

#### 3.1.2. 将远程已有仓库克隆到本地

```sh
git clone http://zbz@192.168.1.201:10080/wboly/wboly-suc.git
```

#### 3.1.3. 第一次将本地仓库添加到远程仓库

```sh
git remote add origin https://github.com/nnzbz/notes.git
```

### 3.2. 检查当前状态

```sh
git status
```

### 3.3. 添加文件

```sh
git add file
```

### 3.4. 提交修改

```sh
git commit -m "提交备注"
```

- 重新提交

刚才的提交可能漏了几个文件，重新提交把最后一次的提交覆盖了

```sh
git commit --amend -m "提交备注"
```

可能操作如下

```sh
# 一次错误的提交
git commit -m 'initial commit'
# 重新加入文件
git add forgotten_file
# 重新提交
git commit --amend
```

### 3.5. 推送分支

推送分支就是把该分支上的所有本地提交推送到远程库

```sh
git push origin master
```

如果是要推送其它分支，比如dev，就改成

```sh
git push origin dev
```

### 3.6. 拉取分支

- ```git fetch```

相当于是从远程获取最新版本到本地，不会自动merge

```sh
git fetch origin master
```

- ```git pull```

相当于是从远程获取最新版本并merge到本地

```sh
git pull origin master
```

### 3.7. 撤销文件的修改

其实， ```git status``` 提示了如何操作

```sh
git checkout -- <file>
```

### 3.8. .gitignore

```text
target
.project
.classpath
.settings
logs
```

## 4. Eclipse中使用Git

### 4.1. 打开 ```Git Perspective```

 工具栏右上角的 ```Open Perspective``` ，选择 ```Git``` 选项打开。

### 4.2. 从Github中克隆项目到本地

1. 在 ```Git Perspective``` 中，左边有一个 ```Git Repostories``` 的 ```View``` ，鼠标点击左上方工具栏的 ```Clone a Git Repository and add the clone to this view``` 按钮；
2. 浏览器打开Githut仓库页面，鼠标点击 ```Clone or download```按钮，复制仓库链接，并将其粘贴到上一步弹出窗口的URI中；
3. 输入Github的用户和密码，选中 ```Store in Secure Store```；
4. 点击 ```next```，再点击 ```next```，在 ```Local Destination``` 页面中，注意修改 ```Directory``` 为自己的 workspace的路径，点击 ```Finish``` 完成；
5. 导入本地已经存在的项目（略）。

## 5. 常见问题

### 5.1. 误用了pull，本地代码被产生冲突，怎么恢复？

```sh
git reset --hard
```