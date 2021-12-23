# Git入门

[TOC]

## 1. 安装

### 1.1. debian(deepin,ubuntu)

```sh
sudo apt-get install git
```

### 1.2. 初次配置

首先必须配置用户信息，包括用户名和邮箱地址。这两条配置信息很重要，git每次提交时都会引用用户信息，说明是谁提交的更新，并且永久保存到历史记录中。

```sh
git config --global user.name "zbz"
git config --global user.email "nnzbz@qq.com"
# 保存用户名和密码，这样就不用每次push时都要输入用户名和密码
git config --global credential.helper store
# 统一设置LF格式
git config --global core.autocrlf input
# 设置代理
git config --global http.proxy 'socks5://127.0.0.1:12345'
git config --global https.proxy 'socks5://127.0.0.1:12345'
# 查看配置信息
git config --list
```

可以使用#git config --list来查看配置信息，不过有时候会看到重复的变量名，那就说明它们来自不同的配置文件（比如/etc/gitconfig和~/.gitconfig），最终Git 实际采用的是最后一个。
也可以直接查阅某个变量 `git config user.name`

## 2. 常用命令简图

![Git常用命令简图](Git常用命令简图.jpg)

## 3. Git常用操作

### 3.1. 初始化

#### 3.1.1. 创建仓库

- 初始化当前文件夹为一个仓库(文件夹里面可以有文件)

```sh
git init
```

- 初始化当前文件夹为一个空仓库(文件夹里面不能有文件)

```sh
git --bare init
```

#### 3.1.2. 克隆远程仓库

```sh
git clone http://zbz@192.168.1.201:10080/wboly/wboly-suc.git
```

#### 3.1.3. 添加远程仓库

进入项目的根路径执行操作

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

### 3.4. 移除文件

```sh
git rm file
```

**如果只想把文件从 Git 仓库中删除（亦即从暂存区域移除），但仍然希望保留在当前工作目录中，那么请用 --cached 选项**

```sh
git rm --cached file
git commit -a
# 上面的命令会进入一个编辑界面
# 按i编辑，然后将要delete的行去掉前面的#号，wq退出
```

### 3.5. 提交修改

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

### 3.6. 推送分支

推送分支就是把该分支上的所有本地提交推送到远程库

```sh
git push origin master
```

如果是要推送其它分支，比如dev，就改成

```sh
git push origin dev
```

 **注意：** 如果要覆盖远程分支，请加  ```-f```

### 3.7. 拉取分支

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

### 3.8. 创建分支

```sh
git branch xxx
```

### 3.9. 删除远程仓库链接

```sh
git remote remove origin
```

### 3.10. 只回退某个文件或文件夹到指定版本

```git
git checkout <版本号> <文件或文件夹>
```

### 3.11. 撤销文件的修改

其实， ```git status``` 提示了如何操作

```sh
git checkout -- <file>
```

### 3.12. .gitignore

```sh
target
.project
.classpath
.settings
logs
```

## 4. 几种常见场景

### 4.1. 放弃本地修改(谨慎)

```sh
git fetch --all
git reset --hard origin/master
git fetch
```

### 4.2. 修改远程仓库地址

```sh
git remote set-url origin [url]
```

### 4.3. 将代码推送到另一个仓库

1. 给本地仓库添加新的远程仓库

```sh
git remote add origin_repo_b git@server_ip:/path/repo_b.git
```

- origin_repo_b
 远程仓库映射在本地仓库的名字(自己起的名字，只要不与现有的remote名重复即可)
- git@server_ip:/path/repo_b.git
 repo_b的远程路径

2. 将代码推送到远程repo_b

```sh
git push origin_repo_b branch_a
```

### 4.4. 将代码同时推送到多个仓库

1. 将远程repo_c配置到当前的工作的本地git仓库中

```sh
git remote set-url --add origin_repo_b git@192.168.1.101:~/project/repo_c.git
```

这句话的意思是，将远程仓库git@192.168.1.101:~/project/repo_c.git也加入到origin_repo_b这个名字下面管理

2. 将代码同时提交到远程仓库repo_b和远程仓库repo_c

```sh
git push origin_repo_b branch_a
```

### 4.5. 作者请你帮助修改代码 ```Welcome PR```

帮助他人的GitHub项目修改代码

如何 **PR(Pull Request)** ?

1. Fork
 fork他人的项目到自己Github的仓库
2. Clone
 将fork到自己仓库中的项目Clone到本地
3. 与原项目建立连接
 用 ```git remote -v``` 命令检查已有链接
 用 ```git remote add upstream https://github.com/他人仓库/原项目名称.git``` 与原项目建立连接
 再用先前命令检查与原项目是否建立连接成功
4. 新建分支并Checkout
 用 ```git checkout -b 分支名称```
5. 修改
6. Add -> Commit -> Push
 注意Push的是自己的仓库
7. 发起PR
 在自己仓库Fork的项目中，点击 ```Pull Requests``` 页面 -> 点击 ```New pull requests``` 按钮 -> 进入 ```Comparing changes```
 ![ComparingChanges](ComparingChanges.png)
8. 建立PR
 点击 ```Create pull request``` 按钮 -> 填写相关信息 -> 点击 ```Create pull request``` 按钮
9. Merge
 这就是原项目开发人员的事了

### 4.6. 在GitLab中修改仓库名称及路径

进入仓库 -> ```Settings``` -> ```General``` -> ```Advanced settings``` -> ```Expand``` -> 设置 ```Project name``` 与 ```Path``` -> ```Rename project```

## 5. Eclipse中使用Git

### 5.1. 开启 ```Git Perspective``` 视图

 工具栏右上角的 ```Open Perspective``` ，选择 ```Git``` 选项打开。

### 5.2. 从Github中克隆项目到本地

1. 在 ```Git Perspective``` 中，左边有一个 ```Git Repostories``` 的 ```View``` ，鼠标点击左上方工具栏的 ```Clone a Git Repository and add the clone to this view``` 按钮；
2. 浏览器打开Githut仓库页面，鼠标点击 ```Clone or download```按钮，复制仓库链接，并将其粘贴到上一步弹出窗口的URI中；
3. 输入Github的用户和密码，选中 ```Store in Secure Store```；
4. 点击 ```next```，再点击 ```next```，在 ```Local Destination``` 页面中，注意修改 ```Directory``` 为自己的 workspace的路径，点击 ```Finish``` 完成；
5. 导入本地已经存在的项目（略）。

### 5.3. 将已有项目添加到远程仓库

1. 右击项目 > `Team` > `Share Project...` > 勾选 `Use or create repository in parent folder of project` > 选择下面列表框中的项目 > 点击 `Create Repository` 按钮 > `Finish`
2. 复制经典的 `.gitignore` 文件，或自己创建一个，到项目根目录下
3. 右击项目 > `Team` > `Commit...`，将有用的文件添加到 `Staged Changes` 的框
4. 点击 `Commit and Push...` 按钮
5. 如果要合并已有远程仓库有冲突，先pull->merge，再提交
6. 在弹出的框中输入远程git仓库的地址
7. 一路 `next` 直到 `Finish`
8. 如果与线上版本有冲突，请走下一节“解决冲突”

### 5.4. 解决冲突

1. 右击冲突文件 > `team` > `merge tool`
2. 将左边框中的代码修改为正确代码，保存（如果本来就是正确的，随便加一个空行，然后保存）
3. 将修正的文件从 `Unstaged Changes` 添加到 `Staged Changes`
4. 提交

## 6. 常见问题

### 6.1. Git检查不到文件的变化

有时候文件有了修改，而git却检测不出来，这个坑就大了，可能的原因是之前提交的文件"缓存"还在，所以相同的文件再提交时无法被检测。（也有可能是git文件的时间跟比仓库中文件晚，让SourceTree认为这不是新文件）

1. 首先, 提交全部更新
2. 执行 `git rm -r --cached .` //从 index 内删除所有变更过的文件
3. 执行 `git add .`
4. 执行 `git commit -m ".` //SourceTree自带推送按钮，这一步命令行可以省略.

### 6.2. 误用了pull，本地代码被产生冲突，如何恢复之前的本地代码

```sh
git reset --hard
```

### 6.3. git error：error: RPC failed

git clone时出现如下错误

```ini
error: RPC failed; curl 56 GnuTLS recv error (-54): Error in the pull function.
fatal: the remote end hung up unexpectedly
fatal: early EOF
fatal: index-pack failed
```

#### 6.3.1. 文件内容太多

##### 6.3.1.1. 修改压缩参数

```sh
git config --global --add core.compression -1
```

或

```ini
vi ~/.gitconfig 

----------------------------------------------------

....

[core]
    compression = -1

....

----------------------------------------------------
```

- compression 是压缩的意思，从 clone 的终端输出就知道，服务器会压缩目标文件，然后传输到客户端，客户端再解压。取值为 [-1, 9]，-1 以 zlib 为默认压缩库，0 表示不进行压缩，1..9 是压缩速度与最终获得文件大小的不同程度的权衡，数字越大，压缩越慢，当然得到的文件会越小。
- 在实际测试中，将参数-1改为1才成功，也可尝试改为0(`git config --global core.compression 0`)

##### 6.3.1.2. 修改git的内存限制

```ini
vi ~/.gitconfig 

----------------------------------------------------

....

[core] 
    packedGitLimit = 512m 
    packedGitWindowSize = 512m 
[pack] 
    deltaCacheSize = 2047m 
    packSizeLimit = 2047m 
    windowMemory = 2047m

....

----------------------------------------------------
```

##### 6.3.1.3. 修改克隆的深度

```sh
git clone --depth 1 <repo_URI>

# 克隆完成后再获取深度
git fetch --unshallow
# 或 alternately
git fetch --depth=2147483647

# 然后再正常pull
git pull --all
```

##### 6.3.1.4. 私有仓库的问题

我有几次出现此问题时是在克隆github上的私有仓库，尝试了后面的方式不行，后来手动编辑hosts解析了github就没问题了

```sh
13.229.188.59  github.com git
151.101.109.194 github.global.ssl.fastly.net
```

- **附上找github的IP的办法**: <http://tool.chinaz.com/dns/>，反复查找 `github`，然后查找TTL值最小的

~~在github的账户设置中添加了 **SSH keys**，并换成 **SSH** 的链接~~

~~注意克隆 **SSH** 链接的命令如下~~

```sh
git clone git@github.com:username/repo.git
```

~~这是由于git默认缓存大小不足导致的，使用下面的命令增加缓存大小~~

```sh
git config --global http.postBuffer 2000000000
```

### 6.4. ~~push时报 ```rejected - non-fast-forward``` 错误~~

简单来说，就是 ```fetch``` -> ```merge``` -> ```push``` ，详细步骤如下：

1. 打开 ```Git Repositories```，在 ```Working Directory``` 中确保可以看到要提交的工程
2. 在 ```Remotes``` 中可以看到远端分支，在分支下向左的绿色箭头图标代表 ```Fetch``` ，右键 -> ```Configure Fetch```
3. 确认 ```URI``` 和 ```Ref mappings``` 都是正确的，点击 ```Save and Fetch```，之后可以看到 Fetch Results 分支在一起，点击OK
4. 此时在 ```Branches``` 中应该可以看到 ```Remote Tracking``` 存在远端分支
5. 右键 ```Branches``` 中的 ```Local``` 中的 ```master``` ，选择 ```Merge```
6. 选择 ```Remote Tracking``` 中的 ```origin/master```，点击 ```Merge```
7. 这是合并后的反馈结果，之后就可以重新 ```push``` 代码了
