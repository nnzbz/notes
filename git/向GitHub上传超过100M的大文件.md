# 向GitHub上传超过100M的大文件

## 1. 安装lfs

https://github.com/git-lfs/git-lfs/wiki/Installation

## 2. 移除错误缓存并重新提交

### 2.1. 移除错误缓存

首先应该移除所有错误的 cache，对于文件：

```sh
git rm --cached path_of_a_giant_file
```

对于文件夹：

```sh
git rm --cached -r path_of_a_giant_dir
```

### 2.2. 重新提交与推送：

```sh
git commit --amend
git push
```

## 3. 将大文件加入 Git Large File Storage

将想要保存的大文件 “路径” 或者 “类型” 添加进 track

```sh
git lfs track "name_of_a_giant_file"
```

**注意：这里面仅能添加类型的扩展名或者文件名作为跟踪方式，不可以添加路径或者目录进行跟踪。**

## 4. 将想要保存的大文件正常添加进 git

```sh
git add path_of_a_giant_file
```

## 5. 正常进行提交&推送

```sh
git commit -m "Add large files"
git push origin master
```

## 6. 补充技巧

提交以后出错再进行上面的步骤可能比较麻烦，如果你已知自己提交的版本库中确实存在一些大于 100MB 的文件，不妨先搜索：

```sh
find ./ -size +100M
```

然后将这些文件移除，等待其他文件提交完后再复制回来，这样只需要从步骤3的操作开始就可以了。