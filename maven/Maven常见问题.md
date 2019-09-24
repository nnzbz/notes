# Maven常见问题

[TOC]

## 1. 指定特别的版本

如果不想用父pom的版本，在本pom中指定一个特别的版本，会有警告 `Overriding managed version XXX for XXX` ，这时可以在 `<version>....<version>` 行的后面加上注释 `<!--$NO-MVN-MAN-VER$ -->` 就可以了。

## 2. `pom.xml` 第一行出现 `Unknow` 错误

方法1：从 <https://download.eclipse.org/m2e-wtp/releases/1.4/> 安装 `m2e connector for mavenarchiver plugin 0.17.3`
 （推荐）。
 eclipse:help-->Install New  Software -->粘贴上面的链接后回车-->全选搜索出来的选项-->然后不断地next就行
方法2：降级 `Maven JAR Plugin` (旧方法，未测试)。`pom.xml` 添加内容如下：

```xml
<properties>
    <!-- ... -->
    <maven-jar-plugin.version>3.1.1</maven-jar-plugin.version>
</properties>
```
