# 前端项目向导(基础项目)

[TOC]

## 1. 安装nodejs

## 2. 安装yarn

## 3. 创建项目

### 3.1. 创建项目文件夹

```text
[project-demo]                //模拟项目文件夹
   │
   ├────────────── [dist]     //打包输出文件夹
   ├────────────── [mock]     //json-server部署目录
   └────────────── [src]      //开发资源文件夹
```


### 3.2. 初始化项目文件夹

```sh
yarn init -y
```

### 3.3. 编辑packege.json

```json
...
"scripts": {
    "dev": "webpack-dev-server --config webpack.config.dev.js --hot --inline",
    "prod": "webpack --config webpack.config.prod.js -p",
    "mock": "json-server ./mock/db.json -w -p 3000"
},
...
```

### 3.4. 创建webpack.config.js

#### 3.4.1. webpack.config.dev.js

```js
'use strict';
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
module.exports = {
    entry: {
        app: './app.js'
    },
    output: {
        path: path.join(__dirname, '/dist'),
        publicPath: '/',
        filename: '[name].bundle.js'
    },
    plugins: [new HtmlWebpackPlugin({
            template: path.join(__dirname, '/src/html/index.html')
        })],
    module: {
        rules: [
            {
                test: /\.css$/, // 匹配特定文件的正则表达式或正则表达式数组
                use: [
                    'style-loader', {
                        loader: 'css-loader',
                        options: {
                            modules: true
                        }
                    }
                ]
            }, {
                test: /\.scss$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            }, {
                test: /\.less$/,
                use: ['style-loader', 'css-loader', 'less-loader']
            }, {
                test: /\.(png|svg|jpg|gif)$/,
                use: ['file-loader']
            }, {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: ['file-loader']
            }, {
                test: /\.jsx$/,
                use: {
                    loader: 'babel-loader'
                },
                exclude: path.resolve(__dirname, 'node_modules')
            }
        ]
    },
    devtool: 'cheap-module-eval-source-map',
    devServer: {
        contentBase: path.join(__dirname, '/dist')
    }
};
```

#### 3.4.2. webpack.config.prod.js

```js
'use strict';
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
module.exports = {
    entry: {
        app: './app.js'
    },
    output: {
        path: path.join(__dirname, '/dist'),
        publicPath: '/',
        filename: '[name].bundle.js'
    },
    plugins: [new HtmlWebpackPlugin({
            template: path.join(__dirname, '/src/html/index.html')
        })],
    module: {
        rules: [
            {
                test: /\.css$/, // 匹配特定文件的正则表达式或正则表达式数组
                use: [
                    'style-loader', {
                        loader: 'css-loader',
                        options: {
                            modules: true
                        }
                    }
                ]
            }, {
                test: /\.scss$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            }, {
                test: /\.less$/,
                use: ['style-loader', 'css-loader', 'less-loader']
            }, {
                test: /\.(png|svg|jpg|gif)$/,
                use: ['file-loader']
            }, {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                use: ['file-loader']
            }, {
                test: /\.jsx$/,
                use: {
                    loader: 'babel-loader'
                },
                exclude: path.resolve(__dirname, 'node_modules')
            }
        ]
    }
};
```

### 3.5. 文件.babelrc

```json
{
    "presets": [
        [
            "env",
            ....
        ]
    ]
}
```

## 4. 安装一些常用的包

### 4.1. 全局安装

```sh
cnpm i webpack-dev-server -g
```

### 4.2. 本地安装

```sh
cnpm i webpack --save-dev
cnpm i html-loader --save-dev
cnpm i html-webpack-plugin --save-dev
cnpm i webpack-merge --save-dev
cnpm i clean-webpack-plugin --save-dev
cnpm i style-loader css-loader --save-dev
cnpm i file-loader --save-dev
cnpm i babel-core babel-loader babel-preset-env --save-dev
cnpm i eslint-loader --save-dev
cnpm i react react-dom react-router-dom -S
cnpm i vue vue-loader --save-dev
```

## 5. 打包运行

### 5.1. 运行调试

```sh
yarn run dev
```

### 5.2. 编译打包

```sh
yarn run prod
```

## 6. 安装模拟后台的服务器

### 6.1. 安装json-server

```sh
yarn i json-server -g
```

### 6.2. 新建服务器目录及放置模拟数据的文件

新建```/json-server```目录用于放置服务端的文件

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

### 6.3. 启动json-server

```sh
json-server db.json -w -p 3000
```

### 6.4. 检查json-server是否启动成功

```sh
http://localhost:3000
```

