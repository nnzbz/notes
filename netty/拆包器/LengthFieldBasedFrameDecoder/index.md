# LengthFieldBasedFrameDecoder

[TOC]

## 1. 构造参数详解

```java
public LengthFieldBasedFrameDecoder(
        ByteOrder byteOrder, int maxFrameLength, int lengthFieldOffset, int lengthFieldLength,
        int lengthAdjustment, int initialBytesToStrip, boolean failFast)
```

| 参数                | 说明                                               |
| :------------------ | -------------------------------------------------- |
| byteOrder           | 长度字段的字节顺序                                 |
| maxFrameLength      | frame最大的长度，长度超过此值则认为是脏数据，丢弃  |
| lengthFieldOffset   | 长度字段的开始位置                                 |
| lengthFieldLength   | 长度字段的字节数                                   |
| lengthAdjustment    | 长度的调整值                                       |
| initialBytesToStrip | 开始读取数据时跳过的字节数                         |
| failFast            | 长度超过最大帧长度时，是否直接抛出异常而不等待读完 |

**数据包整包长度=长度字段的值+长度字段的字节数+此调整值**

## decode

### 

```java
protected Object decode(ChannelHandlerContext ctx, ByteBuf in) throws Exception {
    ....

    // 如果当前可读字节小于长度字段的结束位置，即不能完整读出长度字段的内容，则退出读下次数据传来的时候再判断
    if (in.readableBytes() < lengthFieldEndOffset) {
        return null;
    }

    // 计算长度字段实际开始位置位置，=readerIndex()+长度字段开始的位置
    int actualLengthFieldOffset = in.readerIndex() + lengthFieldOffset;
    // 计算数据包长度
    long frameLength = getUnadjustedFrameLength(in, actualLengthFieldOffset, lengthFieldLength, byteOrder);

    // 如果数据包长度为负数，直接跳过长度字段，并抛出异常
    if (frameLength < 0) {
        in.skipBytes(lengthFieldEndOffset);
        throw new CorruptedFrameException(
           "Adjusted frame length (" + frameLength + ") is less " +
              "than lengthFieldEndOffset: " + lengthFieldEndOffset);
    }

```

