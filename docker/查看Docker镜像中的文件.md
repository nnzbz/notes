# 查看Docker镜像中的文件

## 导出镜像并解压的方式

```sh
docker save nginx:latest > nginx.tar
tar -xvf nginx.tar
```

## 创建容器并运行的方式

```sh
docker run --rm -it --entrypoint sh nginx:latest
```

## 进入容器的方式

```sh
docker run --rm nginx:latest ls -alR
```

## Docker镜像工具dive

<https://github.com/wagoodman/dive>

```sh
dive nginx:latest
```
