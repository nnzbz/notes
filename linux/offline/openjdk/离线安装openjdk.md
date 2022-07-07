# 离线安装openjdk

## 1. 下载

- openjdk 下载网址
<https://jdk.java.net/>

## 2. 解压

```sh
tar xvf openjdk-18*_bin.tar.gz
```

## 3. 设置环境变量

```sh
vi /etc/profile
```

```ini
....

export JAVA_HOME=/usr/local/openjdk/jdk-18.0.1.1
export PATH=$JAVA_HOME/bin:$PATH

....
```

- 注意: 这里假设openjdk解压的路径为/usr/local/openjdk/jdk-18.0.1.1

```sh
. /etc/profile
# 验证
java -version
```
