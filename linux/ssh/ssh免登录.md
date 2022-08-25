# ssh免登录

## 本机生成公私钥

```sh
ssh-keygen
```

默认会生成 `~/.ssh/id_rsa.pub` 公钥和 `~/.ssh/id_rsa` 私钥两个文件

## 上传公钥至服务器

```sh
cat ~/.ssh/id_rsa.pub | ssh xxx.xxx.xxx.xxx -pxxxxx "umask 077;mkdir -p .ssh;cat >> .ssh/authorized_keys"
```

## 测试是否免密码登录

略
