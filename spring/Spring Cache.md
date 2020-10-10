# Spring Cache

[TOC]

## 1. 核心思想

Spring Cache 是作用在方法上的，当我们在调用一个缓存方法时会把该方法参数和返回结果作为一个键值对存放在缓存中，等到下次利用同样的参数来调用该方法时将不再执行该方法，而是直接从缓存中获取结果进行返回。

## 2. 缓存方法的注解

### 2.1. @Cacheable

- 使用@Cacheable 标记的方法在执行后 Spring Cache 将缓存其返回结果。
- @Cacheable 可以标记在一个方法上，也可以标记在一个类上。当标记在一个方法上时表示该方法是支持缓存的，当标记在一个类上时则表示该类所有的方法都是支持缓存的。
- 有时候我们并不希望缓存所有的返回结果，设置 **condition** 属性的值，为true时缓存，false不缓存，默认缓存所有调用情形。

### 2.2. @CachePut

@CachePut也和@Cacheable一样可以声明一个方法支持缓存功能。不同的是使用@CachePut标注的方法在执行前不会去检查缓存中是否存在之前执行过的结果，而是每次都会执行该方法，并将执行结果以键值对的形式存入指定的缓存中。

### 2.3. @CacheEvict

- 使用@CacheEvict 标记的方法会在方法执行前或者执行后移除缓存中的某些元素。

## 3. 缓存的内容

**Spring Cache** 在缓存方法的返回值时是以 **键值对** 进行缓存的，值就是方法的返回结果，至于键的话，Spring 又支持两种策略，默认策略和自定义策略。

在缓存方法的注解参数中，**key** 属性是用来指定缓存结果对应的 key 的。该属性支持 **SpringEL** 表达式。当我们没有指定该属性时，Spring 将使用默认策略生成 key。

- **SpringEL** 表达式
  - "#" + 参数名
  - "#p" + 参数索引(遵守程序员潜规则，索引从 0 开始)

```java
@Cacheable(value="users", key="#id")
public User find(Integer id) {
    return null;
}

@Cacheable(value="users", key="#p0")
public User find(Integer id) {
    return null;
}

@Cacheable(value="users", key="#user.id")
public User find(User user) {
    return null;
}

@Cacheable(value="users", key="#p0.id")
public User find(User user) {
    return null;
}
```

- root 对象(root 可省略，因为 Spring 默认使用的就是 root 对象的属性)

  | 属性名称    | 描述                         | 示例                 |
  | :---------- | ---------------------------- | -------------------- |
  | methodName  | 当前方法名                   | #root.methodName     |
  | method      | 当前方法                     | #root.method.name    |
  | target      | 当前被调用的对象             | #root.target         |
  | targetClass | 当前被调用的对象的 class     | #root.targetClass    |
  | args        | 当前方法参数组成的数组       | #root.args[0]        |
  | caches      | 当前被调用的方法使用的 Cache | #root.caches[0].name |

## 4. 注意

- 在使用 Spring Cache 的时候我们要保证我们缓存的方法对于相同的方法参数要有相同的返回结果。
- 当一个支持缓存的方法在对象内部被调用时是不会触发缓存功能的。(这个与事务相同)
