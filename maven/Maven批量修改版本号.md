# Maven批量修改版本号

1. 进入Maven项目根目录

2. 设置新的版本号

```sh
mvn versions:set -DnewVersion=1.1.3
```

2. 当新版本号设置不正确时可以撤销新版本号的设置

```sh
mvn versions:revert
```

3. 确认新版本号无误后提交新版本号的设置

```sh
mvn versions:commit
```
