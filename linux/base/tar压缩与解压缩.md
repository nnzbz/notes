# tar压缩与解压缩

## 压缩

压缩当前目录下文件夹/文件test到test.tar.gz:

```sh
tar -zcvf test.tar.gz test
```

## 解压缩

解压缩当前目录下的file.tar.gz到file:

```sh
tar -zxvf file.tar.gz
```

## 参数详解

- -c
  建立压缩档案
- -x
  解压
- -z
  gzip
- -v
  显示过程
- -f
  文件名(参数后面要跟文件名)
