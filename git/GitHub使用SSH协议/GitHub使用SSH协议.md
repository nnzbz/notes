# GitHub使用SSH协议

[TOC]

参考 [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/enterprise-server@2.21/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

## 1. 生成SSH密钥

### 1.1. MacOS

1. 打开 `Terminal`，运行命令

    ```sh
    ssh-keygen -t ed25519 -C "your_email@example.com"

    # 如果系统比较旧，不支持 ed25519 算法，请用下面的命令**
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```

    - your_email@example.com 你的GitHub服务器注册的邮箱地址
2. 这时 `Terminal` 提示如下：
    > Generating public/private ed25519 key pair.
    > Enter file in which to save the key (/Users/zbz/.ssh/id_ed25519):

    这里需要你输入密钥文件保存的位置，可以直接回车使用默认路径
3. 然后 `Terminal` 提示如下:
    > Enter passphrase (empty for no passphrase):
    > Enter same passphrase again: [Type passphrase again]

    这里需要你输入passphrase(口令短语)，它用来保护密钥的安全（每次使用密钥前都会要求再次输入核对），嫌麻烦的话可以直接回车
    - 参考 [Working with SSH key passphrases](https://docs.github.com/en/enterprise-server@2.21/github/authenticating-to-github/working-with-ssh-key-passphrases)
4. 如果出现如下提示，则表明成功了
    > SHA256:....... nnzbz@qq.com
    > The key's randomart image is:
    > +--[ED25519 256]--+
    > |.......          |
    > |.......          |
    > |.......          |
    > |.......          |
    > |.......          |
    > |.......          |
    > |.......          |
    > |.......          |
    > |.......          |
    > +----[SHA256]-----+

### 1.2. 其它系统(略)

## 2. 添加密钥到 `ssh-agent`

1. 后台启动 `ssh-agent`

    ```sh
    eval "$(ssh-agent -s)"
    ```

    显示

    > Agent pid xxxxx
2. 如果你是 MacOS Sierra 10.12.2及之后的版本，你需要修改 `~/.ssh/config` 文件使密钥自动加载到 `ssh-agent` 中，且存储 **passphrase**(口令短语)到 `keychain` 中

    ```sh
    vi ~/.ssh/config
    ```

    修改内容如下(生成密钥如果是默认的位置):

    ```ini
    Host *
      AddKeysToAgent yes
      UseKeychain yes
      IdentityFile ~/.ssh/id_ed25519
    
    ....
    ```

3. 添加私钥到 `ssh-agent` 中，且存储 **passphrase**(口令短语)到 `keychain` 中

    ```sh
    ssh-add -K ~/.ssh/id_ed25519
    ```

## 3. 添加密钥到 GitHub 账户

1. 复制公钥到剪贴板

    ```sh
    pbcopy < ~/.ssh/id_ed25519.pub
    ```

2. 添加密钥

   ![进入Settings](进入Settings.png)

   `Settings` -> `SSH and GPG keys` -> `New SSH key`

   略

## 4. 将 https 的链接换成 ssh 的链接

1. 进入 Git 仓库的本地目录
2. 查看远程仓库链接

   ```sh
   git remote -v
   ```

3. 改变命令

   ```sh
   git remote set-url origin ssh://git@github.com:REPOSITORY.git
   ```
