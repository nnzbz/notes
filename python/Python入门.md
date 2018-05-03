# Python入门

[TOC]

## 1. 安装

### 1.1. MAC下安装

```sh
xcode-select --install
brew install python3
```

### 1.2. CentOS7

1. 安装依赖环境

```sh
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
```

2. 创建Python3的目录

```sh
mkdir /usr/local/python3
```

3. 从官网下载相应的版本文件

浏览器打开 https://www.python.org/ftp/python/ 查看最新的Python版本，标记为3.A.B

```sh
wget https://www.python.org/ftp/python/3.A.B/Python-3.A.B.tgz
```

目前最高的正式版为3.6.5

4. 解压并编译

```sh
# 解压
tar -zxvf Python-3.A.B.tgz
# 进入解压后的目录
cd Python-3.A.B
# 编译
./configure --prefix=/usr/local/python3
make && make install
# 创建Python3的软链接
ln -s /usr/local/python3/bin/python3 /usr/bin/python3
# 创建Pip3的软链接
ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```

5. 测试

```sh
python3 --version
pip3 --version
```

## 2. 运行与退出

- 运行

```sh
python
```

- 退出环境

```sh
exit()
```

## 3. Python解释器

| 解释器     | 说明                                                                                                                                                                                                             |
|:-----------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CPython    | 安装好Python后，就直接获得了一个官方版本的解释器：CPython。这个解释器是用C语言开发的，所以叫CPython。在命令行下运行python就是启动CPython解释器。                                                                 |
| IPython    | 基于CPython之上的一个交互式解释器。它只是在交互方式上有所增强，但执行代码的功能和CPython完全一样。                                                                                                               |
| PyPy       | Pypt的目标是执行速度。PyPy采用JIT技术，对Python代码进行动态编译（注意不是解释），所以可以显著提高Python代码的执行速度。绝大部分Python代码都可以在PyPy下运行，但是可能会有不同的结果。了解PyPy和CPython的不同点。 |
| Jython     | 运行在Java平台上的Python解释器，可以直接把Python代码编译成Java字节码执行。                                                                                                                                       |
| IronPython | 运行在微软.Net平台上的Python解释器，可以直接把Python代码编译成.Net的字节码。                                                                                                                                     |

## 4. Python程序后台执行

```sh
nohup python -u myscript.py params1 > nohup.out 2>&1 & 
```

使用-u参数，使得python不启用缓冲，这样就可以同步看到输出结果。