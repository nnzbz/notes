# publisher-confirms、publisher-return和mandatory

## 1. publiser-confirm

publiser-confirm模式可以确保生产者到交换器exchange消息有没有发送成功

```yaml
spring:
  rabbitmq:
    # 确保消息成功发送到交换器
    publisher-confirm-type: SIMPLE
```

## 2. publisher-return

publisher-return模式可以在消息没有被路由到指定的queue时将消息返回，而不是丢弃

```yaml
spring:
  rabbitmq:
    # 确保消息在未被队列接收时返回
    publisher-returns: true
```

## 3. mandatory

```yaml
spring:
  rabbitmq:
    template:
      # 指定消息在没有被队列接收时是否强行退回还是直接丢弃
      mandatory: true
```

## 4. publisher-returns 与 mandatory 的关系

从上面来看，publisher-returns 与 mandatory 所起的作用是一样的，那它们是如何生效的呢？

分析 RabbitTemplateConfigurer 类

```java
private boolean determineMandatoryFlag() {
  Boolean mandatory = this.rabbitProperties.getTemplate().getMandatory();
  return (mandatory != null) ? mandatory : this.rabbitProperties.isPublisherReturns();
}
```

阅读上面的源码可以获取如下信息：

1. `mandatory` 可能会返回三种值 **true**、**false**、**null**（即不配置）
2. `mandatory` 结果为 **true**、**false** 时会忽略 `publisher-returns`
3. `mandatory` 结果为 **null**（即不配置）时结果由 `publisher-returns` 确定

得出结论:
> **mandatory** 的优先级高于 **publisher-returns** 的优先级
