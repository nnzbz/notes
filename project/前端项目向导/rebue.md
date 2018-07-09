# 创建一个项目过程

## 先创建一个远程仓库

## 再创建一个本地maven项目，名字于远程仓库一致

## 在前面创建的maven项目中依次创建以下几个maven子项目（创建完成后按照前辈已经完成的项目配置基本的pom.xml,要从父项目开始配置）

### (1)gen

#### 代码生成器

###  (2)api

#### 存放接口来定义规范，还有mo与ro实体。

### (3)bll

#### 业务逻辑层，实现类等会放在里面

### (4)svr

#### 微服务启动类，控制层会放在里面

### (5)feign

#### 一个声明式的Web服务客户端，使用Feign可使得Web服务客户端的写入更加方便，可以轻松的访问远程的URL，不依赖其他服务。

## 在maven父项目中创建普通目录

#### db

##### 存放sql和powerdesigner的概念模型

#### doc

##### 对本项目的描述

#### 项目创建完成后右键创建本地仓库

##### team -> share project

###### 点击create repository 再点击finish

![创建本地残仓库](创建本地仓库.png)

# 将本地仓库项目上传到远程仓库

## 看git笔记，先cd切换到要上传项目的根路径再进行git命令的操作。

# 使用PowerDesigner创建模型

## 先创建逻辑模型logical(LDM)

### file -> new model -> logical data model ->修改model name 再ok，这时候可能工具栏没有出来，

### （version：16.5）toos -> customize Menus and tools -> toolbars ->将palette打勾。

![创建模型](0.png)

![创建模型](1.png)

![创建模型](2.png)

![创建模型](3.png)

![创建模型](4.png)

![创建模型](5.png)



