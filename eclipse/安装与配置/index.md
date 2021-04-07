# eclipse配置

[TOC]

## 1. 加入staff组

因为一般要将软件安装在 `/usr/local` 下并运行，所以要先将当前用户加入 `staff` 组。

```sh
sudo usermod -a -G staff `whoami`
```

## 2. 安装Java

### 2.1. 下载java

<https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html>

### 2.2. 解压

- debian(ubuntu,deepin)

下载好Linux64位版本的tar.gz包并且解压。
解压到 /usr/local/lib/ 目录下，完整路径如: `/usr/local/lib/jdk1.8.0_231/`

### 2.3. 配置Java环境

- linux

编辑 `/etc/profile` 文件（root/管理员权限）

```sh
sudo vi /etc/profile
```

在文件末尾添加如下内容

```sh
....
# 加入Java变量和路径
export JAVA_HOME=/usr/local/lib/jdk1.8.0_251
export PATH=$JAVA_HOME/bin:$PATH
# export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
```

使 `/etc/profile` 文件生效

```sh
. /etc/profile
```

## 3. 安装eclipse

### 3.1. 下载eclipse

<https://www.eclipse.org/downloads/packages/>

请下载 `Eclipse IDE for Enterprise Java Developers` 下对应的版本

### 3.2. 解压

- debian(ubuntu,deepin)

下载好Linux64位版本的tar.gz包并且解压。
解压到/usr/local/bin/目录下，完整路径如: `/usr/local/bin/eclipse202003R/`

### 3.3. 运行

**注意，请不要在文件管理器中双击运行eclipse，这样会导致一系列乱七八糟的问题，莫名的报错，安装lombok的时候会不成功等等。应该用命令行进入eclipse目录，执行 `./eclipse`），然后dock创建图标**

## 4. Preferences配置

### 4.1. 配置换行符(必须)

`[Window]` -> `[Preferences]` -> `[General]` -> `[Workspace]` -> `New Text file line delimiter` -> 保证选择的是 **Unix**

![eclipse配置-设置换行符](eclipse配置-设置换行符.png)

### 4.2. 配置utf-8(必须)

Preferences -> 在左上角用于过滤关键字的输入框输入 `enc` -> 把不是UTF-8设置的改为UTF-8设置(如为空可忽略)

**注意：一定要每一项都要检查，树节点的要展开检查所有层的子节点**

### 4.3. 配置自动激活内容辅助触发器

- 在下图的输入框中填入: `.abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXYZ`

![自动激活内容辅助触发器](自动激活内容辅助触发器.png)

- 在下图的输入框中填入: `<=:.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW(,`

![自动激活XML内容辅助触发器](自动激活XML内容辅助触发器.png)

### 4.4. 配置养眼的背景

1. 偏好设置->Preferences->General->Editor->Text Editors
2. 右边是Text Editors的面板，在下面 `Appearance color options` 选项中选 `Background color` 选择背景颜色，去掉默认勾选的System default
3. 点击Color来调整背景色：调整RGB为199，237，204(#c7edcc)

### 4.5. 配置字体

修改Project Explorer的字体大小

- Mac

(似乎并不起作用)

 在 `Contents/MacOS/eclipse.ini` 下把 `-Dorg.eclipse.swt.internal.carbon.smallFonts` 全部删除

 在 `应用程序` 中找到eclipse，选择 `显示包内容` ， 然后到 `Contents/Eclipse/plugins/org.eclipse.ui.themes_1.2.1.v20170809-1435/css` 目录下找到 `e4_default_mac.css` 文件，将下面的内容添加进去

```css
#org-eclipse-jdt-ui-PackageExplorer Tree,
#org-eclipse-ui-navigator-ProjectExplorer Tree,
#org-eclipse-ui-views-ContentOutline Tree,
#PerspectiveSwitcher ToolBar {
    font-size: 15px; 
    background-color: rgb(204,238,205);
}
```

### 4.6. 未捕获的异常直接抛出

 `Preferences` > `Java` > `Debug` > 取消勾选 `Suspend execution on uncaught exceptions`

### 4.7. java格式化代码(必须)

#### 4.7.1. 导入配置文件

[格式化配置文件](eclipse-code-style-zbz.xml)

#### 4.7.2. 配置详解

`Preferences` > `Java` > `Code Style` > `formatter` > `Edit...`

- Tab用Space替换
  在 `Indentation` > `Tab policy` > 勾选 `Spaces only`(201909版本的是下拉框选择)
- 垂直对齐
  - 201909之前的版本是：`Indentation` > 勾选 `Indentation` 选项卡中的 `Align fields in columns` / `Blank lines separating independent groups`
  - 201909版本是： `Indentation` > `Align items in columns` > 勾选下面所有可勾选的选项
- 保留长句手动换行原状
  在 `Line Wrapping` > 勾选 `Never join already wrapped lines`
- 注释不改变原本的格式
  在 `Comments` > 取消勾选 `Formater line comments on first column`
  在 `Comments` > 勾选 `Never join lines`
- 优化注释
  在 `Comments` > 勾选 `Enable header comment formatting`
- 写在语句后面的注释 `//` 对齐
  在 `Comments` > 勾选 `Preserve white space between code and line comments`
- 识别忽略格式化的标记
  在 `Off/On Tags` > 勾选 `Enable Off/On tags`

### 4.8. 保存时自动系统化imports以及格式化代码(必须)

菜单 `Preferences` > `Java` > `Editor` > `Save Actions`

配置如下图：

![eclipse配置-保存自动系统化imports和格式化代码](eclipse配置-保存自动系统化imports和格式化代码.png)
![eclipse配置-保存自动系统化imports和格式化代码1](eclipse配置-保存自动系统化imports和格式化代码1.png)
![eclipse配置-保存自动系统化imports和格式化代码2](eclipse配置-保存自动系统化imports和格式化代码2.png)
![eclipse配置-保存自动系统化imports和格式化代码3](eclipse配置-保存自动系统化imports和格式化代码3.png)
![eclipse配置-保存自动系统化imports和格式化代码4](eclipse配置-保存自动系统化imports和格式化代码4.png)
![eclipse配置-保存自动系统化imports和格式化代码5](eclipse配置-保存自动系统化imports和格式化代码5.png)

### 4.9. HTML与XML延长换行宽度

在 `Web` > `HTML Files` > `Editor` > Line width > 180

在 `XML` > `XML Files` > `Editor` > Line width > 180

### 4.10. 配置Maven(必须)

- maven通用配置

![eclipse配置-maven通用配置](eclipse配置-maven通用配置.png)

- Archetypes

![eclipse配置-添加自定义archetype1](eclipse配置-添加自定义archetype1.png)

填入类似<http://192.168.1.201:8081/repository/my-repository/archetype-catalog.xml>的私服仓库地址的链接

![eclipse配置-添加自定义archetype1](eclipse配置-添加自定义archetype2.png)

- 默认打开pom.xml文件时打开XML页面

 在 `Maven` > `User Interface` > 勾选 `Open XML page in the POM editor by default`

- Installations

### 4.11. 配置GIT(必须)

下面是我个人配置示范，请参考配置

- Configuration

Location: /home/zbz/.gitconfig

```ini
[user]
    name = zbz
    email = nnzbz@qq.com
[core]
    autocrlf = input
```

### 4.12. 关闭校验

- 关闭Validation

 在 `Validation` > 取消勾选 `Suspend all validators`

- 关闭拼写

 在 `General` > `Editors` > `Text Editors` > `Spelling` > 取消勾选 `Enable spell checking`

### 4.13. 去掉多余的启动项

 在 `Genaral` > `Startup and Shutdown`

### 4.14. 打开过多自动关闭前面的页面

 在 `General` > `Editors` > 勾选 `Close editors automatically`

### 4.15.  


org.eclipse.epp.package.jee.product


## 5. 创建桌面快捷方式（Ubuntu）

```sh
vi ~/Desktop/eclipse.desktop
```

```ini
[Desktop Entry]
Encoding=UTF-8
Name=Eclipse
Comment=Eclipse
Exec=/usr/local/eclipse/eclipse-oxygen/eclipse
Icon=/usr/local/eclipse/eclipse-oxygen/icon.xpm
Terminal=fasle
StartupNotify=true
Type=Application
Categories=Application;Development;
```

```sh
sudo chmod u+x ~/Desktop/eclipse.desktop
```

## 6. 安装插件

### 6.1. 反编译(Enhanced Class Decompiler)

### 6.2. STS(Spring Tools)

**注意:**
安装STSv3.9.0之后， 与Organize Imports冲突，导致ctrl+shift+o热键失效
解决方案：

> 1. `Preferences` > `General` > `Keys` > `Filters...` > 取消选择 `Filter uncategorized commands` > `OK`
> 2. `Keys` > `"Go To Symbol in File"` > `Unbind Command` > `Apply and Close`

### 6.3. ~~Docker工具(Eclipse Docker Tooling)~~

管理docker的镜像及容器

或docker editor 1.0.0

### 6.4. ~~YEdit~~

YAML文件编辑插件

### 6.5. Lombok(必须)

- 下载
  <https://projectlombok.org/downloads/lombok.jar>
- 安装说明
  <https://projectlombok.org/setup/eclipse>
- 运行安装
  双击运行jar包安装，或命令行执行 `java -jar ./lombok.jar`
  如果出现 `Exception in thread "main" java.awt.AWTError: Assistive Technology not found: org.GNOME.Accessibility.AtkWrapper` 的错误，

```sh
sudo vi /etc/java-8-openjdk/accessibility.properties
```

注释下面这行，如下

```ini
# assistive_technologies=org.GNOME.Accessibility.AtkWrapper
```

也可以直接运行

```sh
sudo sed -i -e '/^assistive_technologies=/s/^/#/' /etc/java-*-openjdk/accessibility.properties
```

- 勾选eclipse的目录
  如果没有可勾选的选项，可用 `Specify location...` 添加
- Install / Update
- 重启eclipse
  如果elipse.ini有参数`-vm`，那么请加入`-vmargs -javaagent:lombok.jar`
- 查看是否安装成功
  在 eclipse about 中看到文本最后一行有 Lombok.... 字样表示安装成功
- 如果没有安装成功，可能是linux的文件权限问题，用chown和chmod设置一下eclipse的安装目录下lombok.jar文件的权限
- **我碰到的启动不成功的情况，命令行直接在非eclipse目录下运行eclipse后dock，就没有安装成功，后来直接用文件管理器跑到eclipse目录下双击运行eclipse(或命令行下cd到eclipse目录，执行 `./eclipse`)，进入到eclipse主界面(非选择workspace的界面)再dock，又能成功了，非常奇怪，记录一下**

## 7. ~~配置Tomcat~~
