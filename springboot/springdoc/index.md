# springdoc

[TOC]

## 1. 简介

- springdoc-openapi-ui 基于OpenApi3，整合了swagger进来，一些注解的包名都是 `io.swagger.v3.oas.annotations`
- swagger 2.X是springboot用于生成在线文档的工具，基于OpenApi2

## 2. 依赖

- 带swagger-ui的依赖

  ```xml
  <dependency>
      <groupId>org.springdoc</groupId>
      <artifactId>springdoc-openapi-ui</artifactId>
      <version>x.x.x</version>
  </dependency>
  ```

- 不带swagger-ui的依赖

  ```xml
  <dependency>
      <groupId>org.springdoc</groupId>
      <artifactId>springdoc-openapi-webmvc-core</artifactId>
      <version>x.x.x</version>
  </dependency>
  ```

## 3. 使用

- 在线文档访问页面地址为
  - 默认(`/swagger-ui.html`)
    <http://server:port/context-path/swagger-ui.html>
  - 可从配置中修改默认路径
  
    ```yml
    springdoc:
      swagger-ui:
        path: /swagger-ui.html
    ```

- JSON接口访问地址为
  - 默认(`/v3/api-docs`)
    <http://server:port/context-path/v3/api-docs>
  - 可从配置中修改默认路径
  
    ```yml
    springdoc:
      api-docs:
        path: /v3/api-docs
    ```

- 禁用(默认是打开)

  ```yml
  springdoc:
    api-docs:
      enabled: false
  ```

## 4. 注解说明

### 4.1. @OpenAPIDefinition

```java
@OpenAPIDefinition(
        info = @Info(
                title = "标题",
                version = "1.0",
                description = "描述信息"
        ),
        externalDocs = @ExternalDocumentation(description = "参考文档",
                url = "https://github.com/swagger-api/swagger-core/wiki/Swagger-2.X---Annotations"
        )
)
```

@OpenAPIDefinition在springboot之中只会生效一个，用于描述该服务的全局信息

### 4.2. @Tag

```java
@RestController
@Tag(name = "HelloController")
public class HelloController {

    @GetMapping("/hello2")
    public String hello2() {
        return "hello world v3";
    }

}
```

@Tag可以加在类和方法上，默认会自动加成 `hello-controller`，用来在页面中分组显示下面的接口，有强迫症的就加上

### 4.3. @Operation

```java
@Operation(summary = "测试登录的接口",
            description = "描述的文字",
            responses = {
                    @ApiResponse(description = "登录信息",
                            content = @Content(mediaType = "application/json",
                                    schema = @Schema(implementation = UserModel.class))),
                    @ApiResponse(responseCode = "400", description = "返回400时候错误的原因")},
            security = @SecurityRequirement(name = "需要认证"))
@GetMapping("/login")
public UserModel login(
        @Parameter(description = "用户名")
        @RequestParam(value = "username", required = false) String username,
        @Parameter(description = "密码")
        @RequestParam(value = "password") String password) {
    UserModel userModel = new UserModel();
    userModel.setUsername(username);
    userModel.setPassword(password);
    return userModel;
}
```

接口的注解@Operation，主要用来描述一些接口的信息

### 4.4. @Parameter

@Parameter用来描述一些传入参数的信息，但是我个人不建议使用这种方式

```java
 @Operation(summary = "swagger v3 信息全部写头上", description = "描述的文字",
            parameters = {
                    @Parameter(name = "auth", description = "请求头", in = ParameterIn.HEADER),
                    @Parameter(name = "id", description = "id", in = ParameterIn.PATH),
                    @Parameter(name = "param", description = "参数"),
            },
            responses = {@ApiResponse(responseCode = "400", description = "400错误")},
            security = @SecurityRequirement(name = "需要认证"))
@GetMapping("/param/{id}")
public String param(HttpServletRequest httpServletRequest,
                    @RequestParam(value = "param") String param,
                    @PathVariable(value = "id") String id) {
    String auth = httpServletRequest.getHeader("auth");
    return "查看参数： " + auth;
}
```

这种方式则是把参数都放在了 @Operation之中，in可以指定参数来源

### 4.5. @Schema

```java
@Data
@Schema(name="UserModel", description="用户model")
public class UserModel {

    @Schema(description = "用户名")
    private String username;
    @Schema(description="密码")
    private String password;

}
```

@Schema可以注解实体类，swagger页面上显示实体类的信息
