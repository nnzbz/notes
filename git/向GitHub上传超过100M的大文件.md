# 向GitHub上传超过100M的大文件

## 1. 安装lfs

Git LFS 是 Github 开发的一个 Git 的扩展，用于实现 Git 对大文件的支持

<https://github.com/git-lfs/git-lfs/wiki/Installation>

- Deepin

    ```sh
    # stretch是debian的代号，Deepin按官网方式不能安装，只能假装是debian
    sudo curl -o /etc/apt/sources.list.d/git-lfs.list "https://packagecloud.io/install/repositories/github/git-lfs/config_file.list?os=debian&dist=stretch&source=script"
    curl -L "https://packagecloud.io/github/git-lfs/gpgkey" 2> /dev/null | sudo apt-key add -
    sudo apt update && sudo apt install git-lfs
    ```

- Debian/Ubuntu

    ```sh
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
    sudo apt-get install git-lfs
    ```

- Mac

    ```sh
    brew update
    brew install git-lfs
    ```

- CentOS
  
  ```sh
  curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | sudo bash
  sudo yum install git-lfs -y
  git lfs install
  ```

## 2. 开启lfs功能

```sh
git lfs install
```

## 3. 使用命令查看追踪了哪些大文件

```sh
git lfs track
```

## 4. 使用命令配置追踪哪些大文件

将想要保存的大文件 “路径” 或者 “类型” 添加进 track

```sh
git lfs track "name_of_a_giant_file"
```

**注意：这里面仅能添加类型的扩展名或者文件名作为跟踪方式，不可以添加路径或者目录进行跟踪。**

例如追踪所有后缀名为png的文件

```sh
git lfs track "*.png"
```

## 5. 与 `.gitattributes` 文件一并提交

`.gitattributes` 文件保存了文件的追踪记录

## 6. 将大文件添加进本地仓库

```sh
git add path_of_a_giant_file
```

## 7. 提交&推送

```sh
git commit -m "Add large files"
git push origin master
```

## 8. 显示当前追踪到的文件列表

```sh
git lfs ls-files
```

## 9. 补充技巧

提交以后出错会比较麻烦，所以要在提交前注意有没有大于 100MB 的文件，搜索命令如下：

```sh
find ./ -size +100M
```
