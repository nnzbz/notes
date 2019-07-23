# 如何使用Feign构造多参数的请求

[TOC]

## 1. GET请求多参数的URL

### 1.1. 方法一

```java
@FeignClient(name = "microservice-provider-user")
public interface UserFeignClient {
  @GetMapping("/get")
  public User get1(@RequestParam("id") Long id, @RequestParam("username") String username);
}
```

这是最为直观的方式，URL有几个参数，Feign接口中的方法就有几个参数。使用@RequestParam注解指定请求的参数是什么。

### 1.2. 方法二

```java
@FeignClient(name = "microservice-provider-user")
public interface UserFeignClient {
  @GetMapping("/get")
  public User get2(@RequestParam Map<String, Object> map);
}
```

多参数的URL也可以使用Map去构建。当目标URL参数非常多的时候，可使用这种方式简化Feign接口的编写。

## 2. POST请求包含多个参数

```java
@FeignClient(name = "microservice-provider-user")
public interface UserFeignClient {
  @PostMapping("/post")
  public User post(@RequestBody User user);
}
```
## 3. POST请求使用okhttp3单元测试时出现问题
有两个服务A与B
当A服务的控制层使用的是form的方式接收参数，而在A的实现层通过feign去调用B的方法，参数是对象，B暴露出来的
接口参数(feign和控制层)都加上了@RequestBody，那么将出现415(Unsupported Media Type")错误，意思是A传
过去的参数不是json格式，但是明明都加了@RequestBody，原因是因为在单元测试的时候，传过去A控制层的参数是以
form的形式的，解决方法是：将A控制层改为使用对象和加上@RequestBody注解，且单元测试传过去的参数是以json格式
传输过去即可。但是这个问题貌似只存在与单元测试才会出现，发出的请求比如说是一个服务C远程调用A的，以form传参的方式，
A的控制层也是以form的形式接收参数，B哪里使用同样是使用@RequestBody注解就没有问题。
```
