# SpringCloud配置Nacos

[TOC]

## 1. 前提条件

启动好 `Nacos Server`。详见<https://github.com/nnzbz/notes/blob/master/docker/%E5%B8%B8%E7%94%A8%E9%95%9C%E5%83%8F%E4%B8%8E%E5%AE%B9%E5%99%A8/Nacos.md>

## 2. 服务发现

- 添加依赖

  ```sh
  <dependency>
      <groupId>com.alibaba.cloud</groupId>
      <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
      <version>${latest.version}</version>
  </dependency>
  ```

  **注意**：版本 2.1.x.RELEASE 对应的是 Spring Boot 2.1.x 版本。版本 2.0.x.RELEASE 对应的是 Spring Boot 2.0.x 版本，版本 1.5.x.RELEASE 对应的是 Spring Boot 1.5.x 版本。
  更多版本对应关系参考：[版本说明 Wiki](https://github.com/spring-cloud-incubator/spring-cloud-alibaba/wiki/%E7%89%88%E6%9C%AC%E8%AF%B4%E6%98%8E)

- 在配置文件中配置 `Nacos Server` 的地址

  ```yml
  spring:
    cloud:
      nacos:
        discovery:
          server-addr: 127.0.0.1:8848
  ```

- 通过注解 `@EnableDiscoveryClient` 开启服务注册发现功能
  
  **注意**: 实际上我们规范中是用 `@SpringCloudApplication`，已经内含此注解，无需理会此条内容

## 3. 配置管理

- 添加依赖

  ```sh
  <dependency>
      <groupId>com.alibaba.cloud</groupId>
      <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
      <version>${latest.version}</version>
  </dependency>
  ```

- 在配置文件中配置 `Nacos Server` 的地址

  ```yml
  spring:
    cloud:
      nacos:
        config:
          server-addr: 127.0.0.1:8848
          # 默认是properties的方式
          file-extension: yaml
  ```

- 在 `Nacos Spring Cloud` 中，`dataId` 的完整格式如下：

  ```ini
  ${prefix}-${spring.profile.active}.${file-extension}
  ```

  - prefix
    默认为 `spring.application.name` 的值，也可以通过配置项 `spring.cloud.nacos.config.prefix` 来配置。
  - spring.profile.active
    即为当前环境对应的 `profile`，详情可以参考 `Spring Boot` 文档。 注意：当 `spring.profile.active` 为空时，对应的连接符 `-` 也将不存在，dataId 的拼接格式变成 `${prefix}.${file-extension}`
  - file-exetension
    为配置内容的数据格式，可以通过配置项 `spring.cloud.nacos.config.file-extension` 来配置。目前只支持 `properties` 和 `yaml` 类型。

- 将 `dataId` 及内容发布到 `Nacos Server` 中
- 控制器类加上注解 `@RefreshScope`
- 启动后就可以自动刷新配置了
