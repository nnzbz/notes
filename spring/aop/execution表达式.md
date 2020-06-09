# execution表达式

## 格式

`execution(modifiers-pattern? ret-type-pattern declaring-type-pattern?name-pattern(param-pattern)
throws-pattern?)`

## 说明

| 标识符                    | 含义                                                 |
| :------------------------ | ---------------------------------------------------- |
| execution()               | 表达式的主体                                         |
| 第一个“\*”符号            | 表示返回值的类型任意                                 |
| com.loongshawn.method.ces | AOP所切的服务的包名，即，需要进行横切的业务类        |
| 包名后面的“..”            | 表示当前包及子包                                     |
| 第二个“\*”                | 表示类名，\*即所有类                                 |
| .\*(..)                   | 表示任何方法名，括号表示参数，两个点表示任何参数类型 |
