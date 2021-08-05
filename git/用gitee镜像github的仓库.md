# 用gitee镜像github的仓库

[TOC]

## 参考

[如何导入外部Git仓库到中国源代码托管平台（Git@OSC）](https://www.oschina.net/question/82993_133520)

## 镜像步骤

1. 从原始地址clone一份bare仓库

    ```sh
    # 这里以 nacos-docker 项目为示例
    git clone --bare  https://github.com/nacos-group/nacos-docker.git
    # https的方式容易被墙，推荐使用 ssh 方式
    git clone --bare  git@github.com:nacos-group/nacos-docker.git
    ```

2. 创建 gitee 仓库
   在 gitee 上创建一个项目（ <https://gitee.com/projects/new> ），这里注意，不要勾选使用Readme初始化项目，不要选择项目的授权协议和.gitignore 文件，因为这些会导致项目有第一个提交。
3. 将 clone 下来的仓库推送到 gitee

    ```sh
    cd nacos-docker.git
    git push --mirror https://gitee.com/nnzbz/nacos-docker.git
    ```
