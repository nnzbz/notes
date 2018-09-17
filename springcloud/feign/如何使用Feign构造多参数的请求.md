# 如何使用Feign构造多参数的请求

[TOC]

## 1. GET请求多参数的URL

### 1.1. 方法一

```java
@FeignClient(name = "microservice-provider-user")
public interface UserFeignClient {
  @RequestMapping(value = "/get", method = RequestMethod.GET)
  public User get1(@RequestParam("id") Long id, @RequestParam("username") String username);
}
```

这是最为直观的方式，URL有几个参数，Feign接口中的方法就有几个参数。使用@RequestParam注解指定请求的参数是什么。

### 1.2. 方法二

```java
@FeignClient(name = "microservice-provider-user")
public interface UserFeignClient {
  @RequestMapping(value = "/get", method = RequestMethod.GET)
  public User get2(@RequestParam Map<String, Object> map);
}
```

多参数的URL也可以使用Map去构建。当目标URL参数非常多的时候，可使用这种方式简化Feign接口的编写。

## 2. POST请求包含多个参数

```java
@FeignClient(name = "microservice-provider-user")
public interface UserFeignClient {
  @PostMapping(value = "/post", consumes = MediaType.APPLICATION_JSON_VALUE)
  public User post(@RequestBody User user);
}
```