# Gradle入门

## 安装

- 下载
  <https://gradle.org/releases>
- 安装
  将压缩文件解压到 `/usr/local/lib/gradle-6.5` 目录下
- 配置环境
  编辑 `/etc/profile`

  ```sh
  export GRADLE_HOME=/usr/local/lib/gradle-6.5
  export PATH=$JAVA_HOME/bin:$GRADLE_HOME/bin:$PATH
  ```
  
  `. /etc/profile`

