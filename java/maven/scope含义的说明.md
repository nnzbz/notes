# scope与optional

[TOC]

## 1. scope含义说明

依赖范围控制哪些依赖在哪些classpath 中可用，哪些依赖包含在一个应用中。让我们详细看一下每一种范围：

### 1.1. compile （编译范围）

 ```compile``` 是默认的范围；如果没有提供一个范围，那该依赖的范围就是编译范围。编译范围依赖在所有的classpath 中可用，同时它们也会被打包。

### 1.2. provided （已提供范围）

 ```provided``` 依赖只有在当JDK 或者一个容器已提供该依赖之后才使用。例如， 如果你开发了一个web 应用，你可能在编译 classpath 中需要可用的Servlet API 来编译一个servlet，但是你不会想要在打包好的WAR 中包含这个Servlet API；这个Servlet API JAR 由你的应用服务器或者servlet 容器提供。已提供范围的依赖在编译classpath （不是运行时）可用。它们不是传递性的，也不会被打包。

### 1.3. runtime （运行时范围）

 ```runtime``` 依赖在运行和测试系统的时候需要，但在编译的时候不需要。比如，你可能在编译的时候只需要JDBC API JAR，而只有在运行的时候才需要JDBC驱动实现。

### 1.4. test （测试范围）

 ```test``` 范围依赖 在一般的编译和运行时都不需要，它们只有在测试编译和测试运行阶段可用。

### 1.5. system （系统范围）

 ```system``` 范围依赖与 ```provided``` 类似，但是你必须显式的提供一个对于本地系统中JAR 文件的路径。这么做是为了允许基于本地对象编译，而这些对象是系统类库的一部分。这样的构件应该是一直可用的，Maven 也不会在仓库中去寻找它。如果你将一个依赖范围设置成系统范围，你必须同时提供一个 systemPath 元素。**注意该范围是不推荐使用的**（你应该一直尽量去从公共或定制的 Maven 仓库中引用依赖）。

## 2. scope 打包及传递特性

scope决定依赖的包是否加入本工程的classpath下

| Scope    | 编译classpath | 测试classpath | 运行时classpath | 传递性 |
| :------- | ------------- | ------------- | --------------- | ------ |
| compile  | Y             | Y             | Y               | Y      |
| test     | -             | Y             | -               | -      |
| provided | Y             | Y             | -               | -      |
| runtime  | -             | Y             | Y               | Y      |
| system   | Y             | Y             | -               | Y      |

## 3. optional

- 如果optional设置为true，表示依赖它的项目引用这个依赖是可选的，不会自动引入这个依赖，如果要引入，必须要显示的写依赖
- 默认optional为false，如果依赖它的项目不想引用这个依赖，可以使用 `exclusion`
- 与scope区别在于：仅限制依赖包的传递性，不影响依赖包的classpath
