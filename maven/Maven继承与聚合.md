# Maven继承与聚合

[TOC]

## 1. 继承

### 1.1. 为什么要继承

- 继承是父pom对插件或者依赖jar进行了表述，使得子孙可以继承这样的规范和依赖
- Maven在这里的坑很多，不要滥用继承

### 1.2. 如何定义继承关系

#### 1.2.1. 父子项目的目录结构是父子关系

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">  
    <parent>  
        <groupId>com.tiantian.mavenTest</groupId>  
        <artifactId>projectA</artifactId>  
        <version>1.0-SNAPSHOT</version>  
    </parent>  
    <modelVersion>4.0.0</modelVersion>  
    <groupId>com.tiantian.mavenTest</groupId>  
    <artifactId>projectB</artifactId>  
    <packaging>jar</packaging>  
    <version>1.0-SNAPSHOT</version>  
</project>
```

#### 1.2.2. 父子项目的目录结构不是父子关系

在子项目的 `pom.xml` 文件定义中的 `parent` 元素下再加上一个 `relativePath` 元素的定义，用以描述父项目的 `pom.xml` 文件相对于子项目的pom.xml文件的位置。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">  
    <parent>  
        <groupId>com.tiantian.mavenTest</groupId>  
        <artifactId>projectA</artifactId>  
        <version>1.0-SNAPSHOT</version>  
        <relativePath>../projectA/pom.xml</relativePath>  
    </parent>  
    <modelVersion>4.0.0</modelVersion>  
    <groupId>com.tiantian.mavenTest</groupId>  
    <artifactId>projectB</artifactId>  
    <packaging>jar</packaging>  
    <version>1.0-SNAPSHOT</version>  
</project>
```

### 1.3. 继承的特点

- 子pom会完全继承父pom中所有的元素
- 子pom与父pom有相同元素
  - 覆盖: 大部分元素，子pom会覆盖父pom中相同的元素
  - 合并: 下面几个特殊元素，不会被子元素覆盖，而是合并
    - dependencies
    - developers
    - contributors
    - plugin列表（包括plugin下面的reports）
    - resources

### 1.4. 依赖管理 `<dependencyManagement>`

并不是父POM中配置的所有依赖在不同的子类中都能用到、或者用到了但是不是统一版本、为解决这个、在父POM标签中用 `<dependencyManagement>` 节点定义依赖信息、在子POM中声明依赖的引入

#### 1.4.1. 使用

- 父pom中在 `<dependencyManagement>` 节点中定义

```xml
<properties>
    <junit.version>4.1</junit.version>
</properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

- 子pom中声明

```xml
<dependencies>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
    </dependency>
</dependencies>
```

#### 1.4.2. 依赖范围import

- 依赖范围有一种是import，只在dependencyManagement元素下才起作用
- 该范围的依赖指向一个POM，作用是将源POM中的 `<dependencyManagement>` 配置导入并合并到当前POM的`<dependencyManagement>` 元素中

### 1.5. 插件管理 `<pluginManagement>`

- 插件管理与依赖管理原理一样
- 插件管理标签是 `<build>` 标签的子标签 `<pluginManagement>`

### 1.6. 超级父pom

- 任何一个maven项目都隐式的继承了超级POM、有点类似与Java所有的类都继承Object类

- 超级POM位置：`$M2_HOME/lib/maven-model-builder-x.x.x.jar` 中的 `org/apache/maven/model/pom-4.0.0.xml`

## 2. 聚合

### 2.1. 聚合的目的

聚合的目的是实现一键build的功能，即A进行build的时候，下面聚合了的b,c,d都会进行build构建

### 2.2. 如果定义聚合

在聚合项目的 `pom.xml` 中的 `modules` 元素下指定它的子模块项目

#### 2.2.1. 如果聚合项目的目录结构是父子关系

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">  
    <modelVersion>4.0.0</modelVersion>  
    <groupId>com.tiantian.mavenTest</groupId>  
    <artifactId>projectA</artifactId>  
    <version>1.0-SNAPSHOT</version>  
    <packaging>pom</packaging>  
    <modules>  
        <module>projectB</module>  
    </modules>  
</project>
```

#### 2.2.2. 如果聚合项目的目录结构不是父子关系

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">  
    <modelVersion>4.0.0</modelVersion>  
    <groupId>com.tiantian.mavenTest</groupId>  
    <artifactId>projectA</artifactId>  
    <version>1.0-SNAPSHOT</version>  
    <packaging>pom</packaging>  
    <modules>  
        <module>../projectB</module>  
    </modules>  
</project>
```
