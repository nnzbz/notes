# webpack插件

[TOC]

## 1. html-webpack-plugin

自动帮你生成一个 html 文件，并且引用相关的 assets 文件(如 css, js)。

### 1.1. 安装

```sh
cnpm i html-webpack-plugin --save-dev
```

### 1.2. 使用

```js
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    ...
    plugins: [
        new HtmlWebpackPlugin()
    ]
}
```

### 1.3. 选项简介

|   选项    |                说明                |
| :-------- | ---------------------------------- |
| template  | 本地模板文件的位置                 |
| filename* | 生成 html 文件的文件名             |
| inject*   | 静态资源(js css ...)注入位置的选项 |

### 1.4. 选项补充说明

- filename
  - 默认为 index.html
  - 也可以直接指出输出文件的目录位置
  - 此路径是相对output.path而言的
  - 如果template指定的模板文件没有指定任何loader的话，默认使用 ```ejs-loader```
- inject
  - **true** 位于html文件的 body 底部，默认值
  - body 同true
  - head 位于 head 标签内
  - false 不插入生成的 js 文件，只是单纯的生成一个 html 文件

## 2. extract-text-webpack-plugin

抽离css样式，防止将样式打包在js中引起页面样式加载错乱的现象

### 2.1. 安装

```sh
cnpm install extract-text-webpack-plugin --save-dev
```

### 2.2. 使用

```js
const ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    module: {
        rules: [{
            test: /\.css$/,
            use: ExtractTextPlugin.extract({
                fallback: "style-loader",
                use: "css-loader"
            })  
        }]
    },
    plugins: [
        new ExtractTextPlugin("styles.css"),
    ]
}
```

### 2.3. 选项

|    参数    |                                  说明                                  |
| :--------- | ---------------------------------------------------------------------- |
| use        | 指需要什么样的loader去编译文件，这里由于源文件是.css所以选择css-loader |
| fallback   | 编译后用什么loader来提取css文件                                        |
| publicfile | 用来覆盖项目路径,生成该css文件的文件路径                               |

## 3. clean-webpack-plugin

用于在building之前删除你以前build过的文件

### 3.1. 安装

```sh
cnpm install clean-webpack-plugin --save-dev
```

### 3.2. 使用

```js
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
    ...
    plugins: [
        new CleanWebpackPlugin(['dist','build'], {
            root:'/full/project/path',
            verbose: true,
            dry: false,
            exclude: ['shared.js']
        })
    ]
}
```

- ['dist','build']
 一个数组，数组的每一个元素为要删除的路径

### 3.3. 选项

|  选项   |       说明       |
| :------ | ---------------- |
| root    | 项目根路径       |
| verbose | 是否打印详细日志 |
| dry     | 不要删除任何东西 |
| exclude | 排除不删除的目录 |

## 4. DefinePlugin

DefinePlugin 允许创建一个在编译时可以配置的全局常量。

这可能会对开发模式和发布模式的构建允许不同的行为非常有用。如果在开发构建中，而不在发布构建中执行日志记录，则可以使用全局常量来决定是否记录日志。这就是 DefinePlugin 的用处，设置它，就可以忘记开发和发布构建的规则。