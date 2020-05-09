# Docker Hub

## 1. DockerHub网址

<https://hub.docker.com>

## 2. 上传或拉取镜像

- 登录DockerHub

    要向DockerHub上传本地的镜像，需要在命令行登录DockerHub

    ```sh
    docker login -u用户名 -p密码
    ```

- 上传镜像：

    ```sh
    docker push nnzbz/debian-jre:8
    ```

- 拉取镜像

    ```sh
    docker pull nnzbz/debian-jre:8
    ```

## 3. 手动构建与自动构建

- DockerHub可以手动从GitHub仓库拉取Dockerfile文件进行编译
- DockerHub也可以让GitHub仓库有新提交时触发Docker镜像的自动编译

在 `Repositories` > XXX仓库 > `Builds` > `Configure Automated Builds` > ....

注意在此页面下方生成 `Build triggers` ，然后在GitHub仓库中的 `Webhooks` 里添加，注意一般选择 `Just the push event.` 就可以了

## 4. 常见问题

- 已经授权连接上github，如果要修改连接，怎么办？
  要从DockerHub和GitHub两边各自删除连接，然后再重新连接。
  参考: <https://docs.docker.com/docker-hub/builds/link-source/#unlink-a-github-user-account>

    ```ini
    To revoke Docker Hub’s access to your GitHub account, you must unlink it both from Docker Hub, and from your GitHub account.

    Click Account Settings in the top-right dropdown navigation, then open the Linked Accounts section.

    Click the plug icon next to the source provider you want to remove.

    Go to your GitHub account’s Settings page.

    Click Applications in the left navigation bar.

    Click the ... menu to the right of the Docker Hub Builder application and select Revoke.
    ```
