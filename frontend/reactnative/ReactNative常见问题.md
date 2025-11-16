# React Native常见问题

[TOC]

## 1. React Native: Can't find variable: require

要清缓存

```sh
expo r -c
```

## 2. Could not get unknown property 'mergeResourcesProvider' for object of type com.android.build.gradle.internal.api.ApplicationVariantImpl

在package.json引入和修改了一些依赖包后，编译出现了此问题。

1. In `gradle-wrapper.properties`
change distributionUrl to 
`distributionUrl=https\://services.gradle.org/distributions/gradle-4.10.1-all.zip`
2. and in root `build.gradle` file change gradle classpath to this: 
  `classpath 'com.android.tools.build:gradle:3.3.0'`
3. Copy file `metro.config.js` in [0.59-stable/template](https://github.com/facebook/react-native/tree/0.59-stable/template) to your project.
4. Remove `node_modules`, `yarn`, and `yarn run-android` again.
(And make sure version of metro in package.json "metro-react-native-babel-preset": "0.51.0" is the same with current metro's version)
