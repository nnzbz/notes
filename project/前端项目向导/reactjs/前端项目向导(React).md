# 前端项目向导(React)

[TOC]

## 1. 安装nodejs

## 2. 安装cnpm及升级npm

### 2.1. 安装cnpm

```sh
npm install -g cnpm --registry=https://registry.npm.taobao.org
```

### 2.2. 升级npm

```sh
cnpm install npm@latest -g
```

## 3. 安装模拟后台的服务器

### 3.1. 安装json-server

```sh
cnpm i json-server -g
```

### 3.2. 新建服务器目录及放置模拟数据的文件

在项目的目录下，新建```/json-server```目录用于放置服务端的文件

新建```/json-server/db.json```文件

db.json的内容示例如下:

```json
{
    "user": [
        {
            "id": 10000,
            "name": "一韬",
            "age": 25,
            "gender": "male"
        },
        {
            "id": 10001,
            "name": "张三",
            "age": 30,
            "gender": "female"
        }
    ],
    "book": [
        {
            "id": 10000,
            "name": "JavaScript从入门到精通",
            "price": 9990,
            "owner_id": 10000
        },
        {
            "id": 10001,
            "name": "Java从入门到放弃",
            "price": 1990,
            "owner_id": 10001
        }
    ]
}
```

### 3.3. 启动json-server

```sh
json-server db.json -w -p 3000
```

### 3.4. 检查json-server是否启动成功

```sh
http://localhost:3000
```

## 4. 创建项目

### 4.1. 创建项目文件夹

```text
[project]                                     //模拟项目文件夹
   │
   ├───────── [mock]                          //json-server部署目录
   │
   ├───────── [public]                        //项目的静态文件（图片等）
   │             │
   │             └─────────index.html         //页面的入口文件
   └───────── [src]                           //前端源码
                 │
                 └─────────index.js           //应用的入口文件
```

### 4.2. 两个文件的基础内容

index.html

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>商会管理系统</title>
</head>

<body id="body">

    <script src="./index.js"></script>
</body>

</html>
```

index.js

```jsx

```

### 4.3. package.json

#### 4.3.1. 初始化项目文件夹

```sh
cnpm init -y
```

#### 4.3.2. 配置package.json文件

上节的命令会生成一个package.json文件，修改script节点的配置

```json
    "scripts": {
        "server": "cd json-server && json-server db.json -w -p 3000",
        "dev": "roadhog server"
    },
```

> 注意不同的操作系统启动roadhog各不相同：
\# Mac, Ubuntu
\$ BROWSER=none roadhog server
\# Windows
\$ set BROWSER=none&&roadhog server
\# Or use cross-env for all platforms
\$ cross-env BROWSER=none roadhog server

### 4.4. 安装roadhog

roadhog是一个快速且功能强大的react项目搭建工具

```sh
cnpm i roadhog -g
```

## 5. 安装一些常用的包

### 5.1. 全局安装

```sh

```

### 5.2. 本地安装

```sh
cnpm i react react-dom react-router-dom -S
cnpm i antd -S
cnpm i babel-plugin-import -D
```

安装babel-plugin-import插件用于做组件的按需加载（否则项目会打包整个组件库，非常大）

根目录下新建.roadhogrc文件（别忘了前面的点，这是roadhog工具的配置文件，下面的代码用于加载上一个命令安装的import插件），写入：

```json
{
    ....
    "extraBabelPlugins": [
        [
            "import",
            {
                "libraryName": "antd",
                "style": "css"
            }
        ]
    ]
}
```

## 6. 打包运行

### 6.1. 运行roadhog

```sh
cnpm run server
```

### 6.2. 运行调试

```sh
cnpm run dev
```