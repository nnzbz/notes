# LineBasedFrameDecoder

[TOC]

## 1. 重写 `decode` 方法

```java
/**
 * Create a frame out of the {@link ByteBuf} and return it.
 *
 * @param   ctx             the {@link ChannelHandlerContext} which this {@link ByteToMessageDecoder} belongs to
 * @param   buffer          the {@link ByteBuf} from which to read data
 * @return  frame           the {@link ByteBuf} which represent the frame or {@code null} if no frame could
 *                          be created.
*/
protected Object decode(ChannelHandlerContext ctx, ByteBuf buffer) throws Exception {
    // 查找换行符
    final int eol = findEndOfLine(buffer);
    // 如果处于正常状态
    if (!discarding) {
        // 如果找到了换行符，解析并返回数据包
        if (eol >= 0) {
            final ByteBuf frame;
            // 计算数据包的长度
            final int length = eol - buffer.readerIndex();
            // 计算换行符的长度
            final int delimLength = buffer.getByte(eol) == '\r'? 2 : 1;

            // 数据包的长度不允许超过数据包定义的最大长度
            if (length > maxLength) {
                // 丢弃这些字节，重新从换行符后开始读取数据
                buffer.readerIndex(eol + delimLength);
                fail(ctx, length);
                return null;
            }

            // 如果不解析换行符，读取数据完后跳过换行符的读取
            if (stripDelimiter) {
                frame = buffer.readRetainedSlice(length);
                buffer.skipBytes(delimLength);
            // 如果解析换行符，读取数据时完要包括换行符的读取
            } else {
                frame = buffer.readRetainedSlice(length + delimLength);
            }

            return frame;
        // 如果找不到换行符
        } else {
            ....
        }
    // 如果处于丢弃状态
    } else {
        ....
    }
}
```

下面分别解析各部分源码

## 2. 查找换行符位置 `findEndOfLine()`

```java
/**
 * Returns the index in the buffer of the end of line found.
 * Returns -1 if no end of line was found in the buffer.
 */
private int findEndOfLine(final ByteBuf buffer) {
    int totalLength = buffer.readableBytes();
    int i = buffer.forEachByte(buffer.readerIndex() + offset, totalLength - offset, ByteProcessor.FIND_LF);
    if (i >= 0) {
        // 如果找到了，设置offset为0，下次再查找时从readerIndex处查起
        offset = 0;
        // 如果\n前面的字符为\r，那就返回\r的位置
        if (i > 0 && buffer.getByte(i - 1) == '\r') {
            i--;
        }
    } else {
        // 如果没找到，设置offset为当前writerIndex处，下次有数据传过来时，再从这里开始查找
        offset = totalLength;
    }
    return i;
}
```

## 3. `offset` 标志

- 最后查找的位置，相对于readerIndex位置的偏移值。
- `findEndOfLine` 查找时将从 `buffer.readerIndex() + offset` 这里开始查找。

## 4. `discarding` 标志

1. `discarding` ，表示是否正处于丢弃状态。
2. 当在缓冲区中找不到换行符，而这里缓冲区的可读数据长度又大于数据包定义的最大长度，这说明目前的数据是脏数据，不能解析出来，所以将当前状态改为丢弃状态。

## 5. 正常状态下，如果找不到换行符

这里检查缓冲区的可读数据长度如果大于数据包定义的最大长度，就将正常状态改为丢弃状态

```java
// 查找换行符
final int eol = findEndOfLine(buffer);
// 如果处于正常状态
if (!discarding) {
    // 如果找到了换行符，解析并返回数据包
    if (eol >= 0) {
        ....
    // 如果找不到换行符
    } else {
        final int length = buffer.readableBytes();
        // 找不到换行符，检查缓冲区的可读数据长度如果大于数据包定义的最大长度，说明目前的数据是脏数据
        if (length > maxLength) {
            discardedBytes = length;
            // 丢弃前面的脏数据
            buffer.readerIndex(buffer.writerIndex());
            // 当前改为丢弃状态
            discarding = true;
            // 下次调用findEndOfLine查找时，将从readerIndex处开始查找
            offset = 0;
            if (failFast) {
                fail(ctx, "over " + discardedBytes);
            }
        }
        // 返回空，等待下次收到数据
        return null;
    }
// 如果处于丢弃状态
} else {
    ....
}
```

## 6. 如果处于丢弃状态

```java
// 查找换行符
final int eol = findEndOfLine(buffer);
// 如果处于正常状态
if (!discarding) {
    ....
// 如果处于丢弃状态
} else {
    // 如果找到了换行符，将换行符及其之前的数据全部丢弃，并将当前丢弃状态改为正常状态，准备开始正常解析数据
    if (eol >= 0) {
        final int length = discardedBytes + eol - buffer.readerIndex();
        final int delimLength = buffer.getByte(eol) == '\r'? 2 : 1;
        buffer.readerIndex(eol + delimLength);
        discardedBytes = 0;
        discarding = false;
        if (!failFast) {
            fail(ctx, length);
        }
    // 如果找不到换行符，直接清除缓冲区中所有读到的数据，准备接着读，一直到找到换行符，进入上面的过程
    } else {
        discardedBytes += buffer.readableBytes();
        buffer.readerIndex(buffer.writerIndex());
        // We skip everything in the buffer, we need to set the offset to 0 again.
        offset = 0;
    }
    return null;
}
```
