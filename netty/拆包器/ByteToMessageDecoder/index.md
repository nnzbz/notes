# ByteToMessageDecoder

[TOC]

## 1. 累加器

### 1.1. 累加器接口

```java
/**
  * Cumulate {@link ByteBuf}s.
  */
public interface Cumulator {
    /**
      * Cumulate the given {@link ByteBuf}s and return the {@link ByteBuf} that holds the cumulated bytes.
      * The implementation is responsible to correctly handle the life-cycle of the given {@link ByteBuf}s and so
      * call {@link ByteBuf#release()} if a {@link ByteBuf} is fully consumed.
      */
    ByteBuf cumulate(ByteBufAllocator alloc, ByteBuf cumulation, ByteBuf in);
}
```

### 1.2. 两个累加器接口的实现

```java
public static final Cumulator MERGE_CUMULATOR = ...;
public static final Cumulator COMPOSITE_CUMULATOR = ...;
```

默认情况下，会使用 `MERGE_CUMULATOR` 。

#### 1.2.1. `MERGE_CUMULATOR` 实现

`MERGE_CUMULATOR` 的原理是每次都将读取到的数据通过内存拷贝的方式，拼接到一个大的字节容器中，这个字节容器在 `ByteToMessageDecoder` 中叫做 `cumulation` 。

```java
@Override
public ByteBuf cumulate(ByteBufAllocator alloc, ByteBuf cumulation, ByteBuf in) {
    try {
        final ByteBuf buffer;
        if (cumulation.writerIndex() > cumulation.maxCapacity() - in.readableBytes()
            || cumulation.refCnt() > 1 || cumulation.isReadOnly()) {
            // Expand cumulation (by replace it) when either there is not more room in the buffer
            // or if the refCnt is greater then 1 which may happen when the user use slice().retain() or
            // duplicate().retain() or if its read-only.
            //
            // See:
            // - https://github.com/netty/netty/issues/2327
            // - https://github.com/netty/netty/issues/1764
            buffer = expandCumulation(alloc, cumulation, in.readableBytes());
        } else {
            buffer = cumulation;
        }
        buffer.writeBytes(in);
        return buffer;
    } finally {
        // We must release in in all cases as otherwise it may produce a leak if writeBytes(...) throw
        // for whatever release (for example because of OutOfMemoryError)
        in.release();
    }
}
```

netty中 `ByteBuf` 的抽象，使得累加非常简单，通过简单调用 `buffer.writeBytes(in);` ，便将新数据累加到字节容器中，为了防止字节容器大小不够，在累加之前还进行了扩容处理。

扩容也是一个内存拷贝操作，新增的大小即是新读取数据的大小，代码如下：

```java
static ByteBuf expandCumulation(ByteBufAllocator alloc, ByteBuf cumulation, int readable) {
    ByteBuf oldCumulation = cumulation;
    cumulation = alloc.buffer(oldCumulation.readableBytes() + readable);
    cumulation.writeBytes(oldCumulation);
    oldCumulation.release();
    return cumulation;
}
```

#### 1.2.2. `COMPOSITE_CUMULATOR` 实现

暂时略

## 2. 拆包

### 2.1. `ChannelRead` 方法

1. 累加数据
2. 对累加后的数据进行解码
3. 清理累加器中的数据
4. 传递数据包给处理器处理
5. 清理已经传递给处理器处理过的数据包

```java
@Override
public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
    if (msg instanceof ByteBuf) {
        CodecOutputList out = CodecOutputList.newInstance();
        try {
            // 1. 累加数据
            ByteBuf data = (ByteBuf) msg;
            first = cumulation == null;
            if (first) {
                cumulation = data;
            } else {
                cumulation = cumulator.cumulate(ctx.alloc(), cumulation, data);
            }
            // 2. 对累加后的数据进行解码
            callDecode(ctx, cumulation, out);
        } catch (DecoderException e) {
            throw e;
        } catch (Exception e) {
            throw new DecoderException(e);
        } finally {
            // 3. 清理累加器中的数据
            if (cumulation != null && !cumulation.isReadable()) {
                numReads = 0;
                cumulation.release();
                cumulation = null;
            } else if (++ numReads >= discardAfterReads) {
                // We did enough reads already try to discard some bytes so we not risk to see a OOME.
                // See https://github.com/netty/netty/issues/4275
                numReads = 0;
                discardSomeReadBytes();
            }

            int size = out.size();
            decodeWasNull = !out.insertSinceRecycled();
            // 4. 传递数据包给处理器处理
            fireChannelRead(ctx, out, size);
            // 5. 清理已经传递给处理器处理过的数据包
            out.recycle();
        }
    } else {
        // 传递对象给处理器处理
        ctx.fireChannelRead(msg);
    }
}
```

### 2.2. `callDecode` 方法

```java
/**
  * Called once data should be decoded from the given {@link ByteBuf}. This method will call
  * {@link #decode(ChannelHandlerContext, ByteBuf, List)} as long as decoding should take place.
  *
  * @param ctx           the {@link ChannelHandlerContext} which this {@link ByteToMessageDecoder} belongs to
  * @param in            the {@link ByteBuf} from which to read data
  * @param out           the {@link List} to which decoded messages should be added
  */
protected void callDecode(ChannelHandlerContext ctx, ByteBuf in, List<Object> out) {
    try {
        while (in.isReadable()) {
            int outSize = out.size();

            // 如果还有数据包要处理，那么将数据包交给处理器去处理，然后清空数据包
            if (outSize > 0) {
                fireChannelRead(ctx, out, outSize);
                out.clear();

                // Check if this handler was removed before continuing with decoding.
                // If it was removed, it is not safe to continue to operate on the buffer.
                //
                // See:
                // - https://github.com/netty/netty/issues/4635
                if (ctx.isRemoved()) {
                    break;
                }
                outSize = 0;
            }
            // 经过上面的过程，outSize==0

            // 记录一下字节容器中有多少字节待拆
            int oldInputLength = in.readableBytes();
            // 解码，调用decode方法
            decodeRemovalReentryProtection(ctx, in, out);

            // Check if this handler was removed before continuing the loop.
            // If it was removed, it is not safe to continue to operate on the buffer.
            //
            // See https://github.com/netty/netty/issues/1664
            if (ctx.isRemoved()) {
                break;
            }

            // 解码后，如果decode没有返回新的数据包要处理
            if (outSize == out.size()) {
                // 如果decode并未读取任何数据，可能数据还未读完，break等待新的数据
                if (oldInputLength == in.readableBytes()) {
                    break;
                // 否则，说明decode已经读取了一段完整数据，但累加器中还有数据未读取，继续解码读取下一段完整数据
                } else {
                    // +--------------+----------+----------+
                    // |   readed     | unreaded | writable |
                    // +--------------+----------+----------+
                    continue;
                }
            }

            // 解码后，如果发现其并没有读取任何数据而解出了数据包，那么就会抛出一个异常
            if (oldInputLength == in.readableBytes()) {
                throw new DecoderException(
                        StringUtil.simpleClassName(getClass()) +
                                ".decode() did not read anything but decoded a message.");
            }

            if (isSingleDecode()) {
                break;
            }
        }
    } catch (DecoderException e) {
        throw e;
    } catch (Exception cause) {
        throw new DecoderException(cause);
    }
}
```

### 2.3. `decode` 方法

```java
protected abstract void decode(ChannelHandlerContext ctx, ByteBuf in, List<Object> out) throws Exception;
```

netty中对各种用户协议的支持就体现在这个抽象函数中，传进去的是当前读取到的未被消费的所有的数据，以及业务协议包容器，所有的拆包器最终都实现了该抽象方法。

