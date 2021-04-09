# SpringCacheRedis 参考

[TOC]

## 1. 参考

<https://docs.spring.io/spring-data/redis/docs/2.4.7/reference/html/#redis:support:cache-abstraction>

## 2. 支持的包

Spring 通过 `org.springframework.data.redis.cache` 包对 `Spring Cache` 提供支持

## 3. 多缓存机制

```java
@Configuration
public class CacheConfig {
    @Bean(CacheManagerName.REDIS_CACHE_MANAGER)
    @Primary
    public RedisCacheManager cacheManager(final RedisConnectionFactory connectionFactory) {
        return RedisCacheManager.create(connectionFactory);
    }
}
```

- @Primary 多个缓存管理必须有一个要设置 `@Primary`，否则 Spring 加载注入时会报错
- @Bean 多个缓存管理每个都要指定自己的名称，以便在 @CacheConfig 中配置 `cacheManager` 来指定缓存管理

## 4. 自定义配置

```java
@Bean
public RedisCacheManager redisCacheManager(RedisConnectionFactory connectionFactory) {
    return RedisCacheManager.builder(connectionFactory)
        .cacheDefaults(defaultCacheConfig())
        .withInitialCacheConfigurations(singletonMap("predefined", defaultCacheConfig().disableCachingNullValues()))
        .transactionAware()
        .build();
}
```

### 4.1. RedisCacheManager 的默认设置

| Setting             | Value                                        |
| :------------------ | -------------------------------------------- |
| Cache Writer        | Non-locking                                  |
| Cache Configuration | RedisCacheConfiguration#defaultConfiguration |
| Initial Caches      | None                                         |
| Transaction Aware   | No                                           |

### 4.2. RedisCacheConfiguration 的默认设置

| Setting            | Value                                                                |
| :----------------- | -------------------------------------------------------------------- |
| Key Expiration     | None                                                                 |
| Cache null         | Yes                                                                  |
| Prefix Keys        | Yes                                                                  |
| Default Prefix     | The actual cache name                                                |
| Key Serializer     | StringRedisSerializer                                                |
| Value Serializer   | JdkSerializationRedisSerializer                                      |
| Conversion Service | DefaultFormattingConversionService with default cache key converters |
