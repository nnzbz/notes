# Maven常用插件

[TOC]

## 1. maven-enforcer-plugin

用来校验约定遵守情况(或者说校验开发环境)。

### 1.1. 参考配置

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-enforcer-plugin</artifactId>
    <!-- <version>1.2</version> -->
    <executions>
        <execution>
            <id>enforce-banned-dependencies</id>
            <goals>
                <goal>enforce</goal>
            </goals>
            <configuration>
                <rules>
                    <!-- <requireMavenVersion> -->
                    <!-- <version>${maven.version}</version> -->
                    <!-- </requireMavenVersion> -->
                    <requireJavaVersion>
                        <version>${java.version}</version>
                    </requireJavaVersion>
                    <bannedDependencies>
                        <searchTransitive>true</searchTransitive>
                        <excludes>
                            <exclude>commons-logging:commons-logging</exclude>
                            <exclude>aspectj:aspectj*</exclude>
                            <exclude>org.springframework:2.*</exclude>
                            <exclude>org.springframework:3.*</exclude>
                            <exclude>spring-boot-starter-logging</exclude>
                            <exclude>hibernate-jpa-2.0-api</exclude>
                        </excludes>
                    </bannedDependencies>
                </rules>
                <fail>true</fail>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### 1.2. excludes节点

禁止依赖列表，规则如下(括号内为可选,可使用通配符替换整体或者部分)：

```text
groupId[:artifactId][:version][:type][:scope][:classifier]
```

### 1.3. 版本范围规则

|     范围      |                 说明                  |
| :------------ | ------------------------------------- |
| 1.0           | x >= 1.0                              |
| (,1.0]        | x <= 1.0                              |
| (,1.0)        | x < 1.0                               |
| [1.0]         | x == 1.0                              |
| [1.0,)        | x >= 1.0                              |
| (1.0,)        | x > 1.0                               |
| (1.0,2.0)     | 1.0 < x < 2.0                         |
| [1.0,2.0]     | 1.0 <= x <= 2.0                       |
| (,1.0],[1.2,) | x <= 1.0 or x >= 1.2. 多范围用“,”隔开 |
| (,1.1),(1.1,) | x != 1.1                              |

### 1.4. 扩展插件

https://github.com/eeichinger/maven-enforcer-plugin-enforcer-rule-extensions

## 2. versions-maven-plugin

### 2.1. 项目满足条件

必须规范模块中pom.xml文件的编写，显式声明其父子节点信息(```parent``` 和 ```modules```)

### 2.2. 命令行运行

官网：http://www.mojohaus.org/versions-maven-plugin/index.html

#### 2.2.1. 更新全部子项目的版本号

当使用此插件在父Maven项目时，运行如下命令将更新全部项目的版本号，包括子项目之间的依赖也都同步更新：

```sh
mvn versions:set -DoldVersion=* -DnewVersion=1.0.1-SNAPSHOT -DprocessAllModules=true -DallowSnapshots=true
```

#### 2.2.2. 更新全部项目对子项目引用的版本号

当进入到子Maven项目时，运行如下命令将更新全部项目对该子项目引用的版本号：

```sh
mvn versions:set -DnewVersion=2.1-SNAPSHOT
```

- 注意：更新后需要刷新Eclipse中打开的项目

#### 2.2.3. 回滚

当更改版本号时有问题，可以通过以下命令进行版本号回滚：

```sh
mvn versions:revert
```

#### 2.2.4. 提交

如果一切都没有问题，那就直接提交版本号：

```sh
mvn versions:commit
```

#### 2.2.5. 注意

还有使用此插件需要注意的，比如自己手动修改了某个文件的版本号，那么这样通过这个插件去更新时是更新不到的，因为匹配不上手动修改的版本号。如果要使其生效，就必须更改成统一的版本号。