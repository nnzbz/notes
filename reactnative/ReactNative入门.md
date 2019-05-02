# React Native入门

[TOC]

## 1. 网站

官网
<https://facebook.github.io/react-native/docs/getting-started>

中文翻译
<https://reactnavigation.org/docs/zh-Hans/getting-started.html>

## 2. 安装

## 3. 初始化项目

### 3.1. Expo CLI Quickstart

### 3.2. React Native CLI Quickstart方式

按官网 `React Native CLI Quickstart` ，选择 `macOS` 及 `Android` 开发，安装完成运行 ```react-native run-android``` ，手机端出现提示
 `unable to load script from assets` 的错误

1. 在 `android/app/src/main` 目录下创建一个 `assets` 空文件夹

2. 运行下面命令

```sh
react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res
```

## 4. 调试

### 4.1. expo

#### 4.1.1. Android本机调试

1. 手机连上电脑
2. 在电脑上运行 ```react-native run-android --port=13080``` ，13080是端口号
3. 在手机上出现出错页面，请摇一摇 -> `Dev Settings` -> `Debug server host & port for device` -> 设置连接的电脑的地址(如:192.168.1.54:13080) -> 返回 -> 摇一摇 -> `Reload`
