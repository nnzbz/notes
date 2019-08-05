# 热更新配置

[TOC]

## 1. 在 `bootstrap.yml` 文件最下面添加如下内容

```yaml
management:
  endpoints:
    web:
      exposure:
        include: refresh
```

## 2. 在SpringBoot的配置文件中添加配置，例如

```yaml
refreshScope: bbb
```

## 3. 在控制器的类名添加 `@RefreshScope` 注解

```java
....

/**
 * 学生信息
 */
@RestController
@RefreshScope
public class HlwStudentCtrl {

....
```

## 4. 在控制器中添加 `@Value` 注解，将配置注入属性，例如

```java
....

@Value("${refreshScope:default}")
private String refreshScope;

....
```

## 5. 发送POST请求，刷新配置

### 5.1. 全部刷新

<http://127.0.0.1:9009/actuator/refresh>

### 5.2. 局部刷新

添加 `destination` 参数来指定刷新的微服务

<http://127.0.0.1:9009/actuator/refresh?destination=hlw-svr:9009>

如果要刷新此微服务的所有实例，可用 `**` 代替

<http://127.0.0.1:9009/actuator/refresh?destination=hlw-svr:**>
