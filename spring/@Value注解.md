# @Value注解

## 官方文档

<https://docs.spring.io/spring-boot/docs/current/reference/html/appendix-configuration-metadata.html#configuration-metadata-format>

## 默认及计算示例

```java
@Value("#{${jwt.expiration:30}*60*1000}")
```

## 调用对象的方法示例

```java
@Value("#{'${jwt.key}'.getBytes('utf-8')}")
```
