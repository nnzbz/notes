# proxyBeanMethods

## 1. 简要说明

`@Configuration` 中的属性 `proxyBeanMethods` 指定注解了 `@Bean` 的方法是否使用代理
默认不写相当于 `proxyBeanMethods=true`

## 2. Full 模式 Lite 模式

- Full模式
  proxyBeanMethods = true 或不写
- Lite模式
  proxyBeanMethods = false
- 不带@Configuration的类叫Lite配置类

## 3. Full 模式 Lite 模式的区别

| 模式         | Full                  | Lite             |
| :----------- | --------------------- | ---------------- |
| 使用代理     | 使用代理              | 不使用代理       |
| 是否放入容器 | 是                    | 否               |
| 每次使用     | 从IOC容器之中取得对象 | 创建一个新的对象 |
| 是否单例     | 是                    | 否               |

## 4. 建议

Spring 5.2.0+的版本，建议你的配置类均采用Lite模式去做，即显示设置 `proxyBeanMethods = false`
因为默认要创建代理，并放入容器中，而设置为false时直接创建新的对象，在创建对象有限时，启动相对较快且使用性能相对较高

## 5. 我的理解

配置类中的Bean只在初始化的时候被使用一次，设置为false时可以提高SpringBoot的启动速度

但是注意，如果Bean中又关联了其它的Bean，那么那个Bean
