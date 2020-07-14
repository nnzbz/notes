# 前端项目向导(AntDesignPro)

[TOC]

## 1. 安装nodejs/npm/yarn

略

## 2. 创建项目

```sh
git clone --depth=1 https://github.com/ant-design/ant-design-pro.git 项目名
```

## 3. 安装依赖

```sh
cd 项目根路径
yarn install
```

## 4. 开发调试

```sh
cd 项目根路径
yarn start
```

启动完成后会自动打开浏览器访问 http://127.0.0.1:8000

### 4.1. 动态查询菜单

https://github.com/ant-design/ant-design-pro/commit/3d7d0fd87d7ead34999a2d56bc5d73c9cf4b2c8b#diff-fb32c22981db5099518584991bd60917

### 4.2. 响应请求延迟1秒

- .roadhogrc.mock.js

```js
export default (noProxy ? {} : delay(proxy, 1000));
```

### 4.3. 从mock切换切换到服务端请求

- .roadhogrc.mock.js

```js
// 响应请求不延迟
export default (noProxy ? {
  'GET /pfm-svr/(.*)': 'http://192.168.1.24:20182/',
  'POST /pfm-svr/(.*)': 'http://192.168.1.24:20182/',
  'PUT /pfm-svr/(.*)': 'http://192.168.1.24:20182/',
  'DELETE /pfm-svr/(.*)': 'http://192.168.1.24:20182/',
} : proxy);
```

- 启动代理

```sh
yarn start:no-proxy
```

## 5. 部署配置

.webpackrc.js

```js
....
  env: {
    // 开发环境
    development: {
      publicPath: '/',
      extraBabelPlugins: ['dva-hmr'],
    },
    // build 时的生产环境
    production: {
      publicPath: '/damai-admin-web/',
    }
  },  
  ....
  // 开启代码分割和动态加载
  //"disableDynamicImport": true
```

## 6. 打包

```sh
yarn run build
```

## 7. 引入自定义图标字体库

### 7.1. iconfont维护项目

http://www.iconfont.cn/

注意：项目编辑一定要编辑 ```FontClass/Symbol``` 前缀，antd用的是anticon，我们用的是rebue

### 7.2. 将项目下载到本地

### 7.3. 解压zip中的文件到项目中的静态资源目录中

打开zip文件，demo那几个文件可不要

例如 ```assets/icon/rebue```
