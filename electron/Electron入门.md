# Electron入门

[TOC]

## 1. 官方 Demo

```sh
git clone https://github.com/electron/electron-api-demos
cd electron-api-demos
yarn install
yarn start
```

## 2. 全局安装 Electron

```sh
yarn add electron --g
```

## 3. 新建项目

### 3.1. 新建项目文件夹

```sh
mkdir hello
cd hello/
```

### 3.2. 初始化项目

```sh
npm init
```

生成 ```package.json```

```json
{
  "name": "hello",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "author": "",
  "license": "ISC"
}
```

修改内容

```json
{
    ....
    "scripts": {
        "start": "electron ."
    }
    ....
}
```

### 3.3. 创建项目文件

新建 ```index.html``` 文件

```html
<html>
    <head>
        <meta charset="UTF-8">
        <title>这是个html文件>/title>
    </head>
    <body>
        随便
    </body>
</html>
```

新建 ```index.js``` 文件

```js
// 引入electron模块
var electron = require('electron');

// 用来控制应用的生命周期
var app = electron.app;


// 用来创建浏览器窗口
var BrowserWindow = electron.BrowserWindow;


// 创建一个全局变量，名字随便取，相当于普通网页中的 window 对象
var mainWindow;

// 当软件触发 ready 事件之后，创建浏览器窗口
app.on('ready', function() {
    // 创建浏览器窗口。
    mainWindow = new BrowserWindow({
        width:400,
        height: 200,
    });

    // 加载 example 目录下的index.html，就是刚才我们新建的那个
    mainWindow.loadURL('file://'+__dirname+'/index.html');
});
```

### 3.4. 查看效果

```sh
yarn start
```

## 4. 调试应用

打开开发者工具

```js
let win = new BrowserWindow();
win.openDevTools();
```
