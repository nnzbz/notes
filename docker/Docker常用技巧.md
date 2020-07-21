# Docker常用技巧

## 1. 用root进入容器

```sh
docker exec -it -u root mysql /bin/bash
```

## 2. 容器内无vi如何编辑文件

```sh
# 1. 先查看原文件内容
cat /etc/mysql/my.cnf


....

# 2. 写入
# aaa.txt是希望使用cat写入的目标文件，EOF是指定的交互式输入终止符
cat > aaa.txt << EOF
# 下方会出现 “>”，在 “>” 后面粘贴文本内容
>....
# 最后输入 “EOF” 结束编辑
>EOF
```
