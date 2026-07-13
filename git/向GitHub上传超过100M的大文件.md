# 向GitHub上传超过100M的大文件

[TOC]

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

## 9. 查找大于50MB的文件

```sh
find ./ -size +50M
```

## 10. 查找大于50MB的文件并添加到lfs追踪

```sh
# 可能会反.git目录下的大文件也搜索出来，注意删除已经写入到.gitattributes文件中的这些文件
find . -type f -size +50M -exec git lfs track {} \;
```

## 11. 查找大于50MB的文件并添加到lfs追踪，排除不查找指定目录下的文件

```sh
# 排除单个目录下的文件
find . -path "./.git" -prune -o -type f -size +50M -exec git lfs track {} \;
# 排除多个目录下的文件
find . <inline_LaTeX_Formula> -path "./.git" -o -path "./node_modules" <\inline_LaTeX_Formula> -prune -o -type f -size +50M -exec git lfs track {} \;
```

* -path "./.git" -prune
匹配到 .git 文件夹后直接剪枝，不再进入该目录递归查找，彻底跳过版本库内部文件，不会误把 Git 对象库内文件加入 LFS 追踪。
* -o
逻辑或：如果没有匹配到 .git 目录，就执行后面的文件查找逻辑。


## 12. 如果已经提交了大于50MB的文件，但是没有添加到lfs追踪，需要重新提交覆盖之前的提交

```sh
git commit --amend --no-edit
```

* `--amend` 选项表示覆盖上一次的提交
* `--no-edit` 选项表示直接使用上一次的提交信息
