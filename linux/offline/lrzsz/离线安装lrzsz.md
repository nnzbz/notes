# 离线安装lrzsz

1. 获取安装包
   <https://ohse.de/uwe/releases/lrzsz-0.12.20.tar.gz>

2. 将下载好的包复制到要安装的机器。

3. 登录到要安装的机器， cd 到安装包所在目录

```sh
tar  zxvf  lrzsz-0.12.20.tar.gz 解压安装包
```

4. 进入解压好的目录里

```sh
cd  lrzsz-0.12.20
```

5. 配置安装路径

./configure --prefix=/usr/local/lrzsz

6. 编译

```sh
make
```

7. 安装

```sh
make install
```

8. 配置系统命令

```sh
cd /usr/bin

ln -s /usr/local/lrzsz/bin/lrz rz 

ln -s /usr/local/lrzsz/bin/lsz sz
```

如果/usr/bin下已存在，删除

9. 测试是否安装成功

输入 rz  弹出文件选择框，这样就成功了
