# gpg

[TOC]

## 1. 生成密钥对

```sh
gpg --gen-key
```

为用户生成新密钥对。需提供：密钥类型（默认为RSA/RSA）；密钥长度（以位为单位，越长越强）；过期时间（以防密钥损坏）；（通常我都是一路回车过去）接下来的还是要填一填的：名称、电子邮箱、标识密钥所有者的注释；密码短语（必须提供，如果私钥被盗，将无法使用）。 

## 2. 列出公钥

```sh
gpg --list-keys
```

列出所拥有的公钥：他们自己的公钥以及从与之通信的其他人那里导入的任何公钥。

## 3. 上传你的公钥到秘钥服务器

```sh
# 直接
gpg --send-keys [Key ID]
# 或指定服务器
gpg --keyserver [密钥服务器地址] --send-keys [Key ID]
```

Key ID为生成key时的 ```gpg: key XXXXXXXXXXX marked as ultimately trusted``` 字样
密钥服务器地址可以为 ```hkp://subkeys.pgp.net```

## 4. 在另一台服务器上搜索刚才上传的公钥

```sh
gpg --search-keys [Key ID]
```

## 5. 导出/导入公钥

### 5.1. 导出公钥

```sh
gpg --armor -o ~/keys/key-pub.key --export [Key ID]```
```

公钥文件（.gnupg/pubring.gpg）以二进制形式储存，armor参数可以将其转换为ASCII码显示。

将公钥导出至文件，以便于其他人使用。--armor选项以文本形式显示输出，而非二进制格式。key-id是电子邮箱地址或在--list-keys的pub行中列出的八位十六进制数。

### 5.2. 导入公钥

```sh
gpg --import file.key 
```

从发送给您的密钥文件中导入其他人的公钥 

信任此公钥

```sh
gpg --edit-key <KEY_ID>
gpg> trust
....
5
```

## 6. 加密文件

```sh
gpg --encrypt --armor -r key-id file 
```

用key-id的公钥加密消息。如果未提供-r key-id，命令将提示收件人输入。默认输出文件为 `file.asc` .

## 7. 解密文件

```sh
gpg --recipient 5696B4F6145492EB -o ./file.sql.gz --decrypt ./file.sql.gz.asc
```

用您的私钥之一解密用公钥加密的消息。 

## 8. 导出/导入私钥

### 8.1. 导出私钥

```sh
gpg --output mygpgkey_sec.gpg --armor --export-secret-key 5696B4F6145492EB
```

### 8.2. 导入私钥

```sh
gpg --allow-secret-key-import --import ~/mygpgkey_sec.gpg
```
