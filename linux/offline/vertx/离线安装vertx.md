# 离线安装vertx

## 1. 安装openjdk(略)

## 2. 上传vertx的离线压缩包(略)

## 3. 解压

```sh
cd /usr/local
tar -zxvf vertx-offline-*.tar.gz
```

## 4. 设置环境变量

```sh
vi /etc/profile
```

```ini
....

export VERTX_HOME=/usr/local/vertx
export PATH=$VERTX_HOME/bin:$PATH

....
```

- 注意: 这里假设openjdk解压的路径为/usr/local/openjdk/jdk-18.0.1.1

```sh
. /etc/profile
# 验证
vertx version
```

## 5. 后台运行vertx程序

```sh
vertx start -ha -Dhazelcast.logging.type=slf4j \
    --launcher-class=io.vertx.core.Launcher \
    --java-opts="--add-modules java.se --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/java.nio=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED --add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED" \
    --vertx-id=xxx -cp conf/*:lib/*.jar:myservice.jar xxx.xxx.verticle.MainVerticle
```

- 注意:
  - 这里假设运行的jar包名为 myservice.jar，
  - 这里假设main 类为 xxx.xxx.verticle.MainVerticle
  - 这里设置id为xxx，提供查看时可分辨运行的程序
