# 拆包器

[TOC]

## 1. 拆包器的基类(ByteToMessageDecoder)

详见 `ByteToMessageDecoder` 的笔记，此处略。

## 2. 自定义拆包器

1. 继承 `ByteToMessageDecoder`
2. 重写 `decode` 方法

```java
void decode(ChannelHandlerContext ctx, ByteBuf in, List<Object> out)
```

其中 `in` 表示目前为止还未拆的数据，拆完之后的包添加到 `out` 这个list中即可实现包向下传递。

