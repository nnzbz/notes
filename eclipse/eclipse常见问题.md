# eclipse常见问题

[TOC]

## 1. 项目报警告 `Access restriction: The type 'BASE64Encoder'`

右键项目，点属性（Properties）

java bulid path-->Libraries-->jre System Library

Access Rules-->Edit

Add，resolution选择accessible，下面填上** 点击确定即可！

## 2. Ubuntu下不能删除项目及文件

### 2.1. 方案一

此方案只能将项目改成一个不用的名字

1、关闭eclispe

2、修改相关文件内容

```sh
ls ~/workspaces/02/.metadata/.plugins/org.eclipse.core.resources/.projects
```

在上面的文件中删除该项目的内容

3、重新打开eclipse

4、重新打开该项目

出错，没关系，可以改名了，改成一个不用的项目名吧，最后记得在硬盘中将项目的目录删除

如果是Maven子模块的，还要记得在父pom中将本module删除

此方案只能这样～～～

如果使用了 ```working sets``` ，还要在下面的文件中删除 ```/.metadata/.plugins/org.eclipse.ui.workbench/workingsets.xml```

### 2.2. 方案二

此方案会清空所有项目

清空了项目了，可以重新加载项目

```sh
rm ~/workspaces/02/.metadata/.plugins/org.eclipse.core.resources/.safetable/org.eclipse.core.resources
```