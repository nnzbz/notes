# ByteBuf解析

[TOC]

## 1. netty为什么用ByteBuf代替Java原生的java.nio.ByteBuffer

- `ByteBuffer` 只有一个标识位置的指针position，需要和flip()方法一起使用在读写模式间切换。
- `ByteBuffer` 长度固定，一旦分配完成，就不能动态的扩展，当需要存储的POJO对象大于ByteBuffer容量时，会发生索引越界异常。

## 2. ByteBuf 缓冲区结构图示

```text
+-------------------+------------------+------------------+
| discardable bytes |  readable bytes  |  writable bytes  |
+-------------------+------------------+------------------+
|                   |                  |                  |
0      <=      readerIndex   <=   writerIndex    <=    capacity
```

**可以调用 `discardReadBytes` 方法重用 `discardable` 部分缓冲区，防止ByteBuf动态扩张（缓冲区的分配和释放是个耗时的操作，所以要尽可能的重用）。**

## 3. `discardReadBytes()` 方法执行前后

```text
 *  BEFORE discardReadBytes()
 *
 *      +-------------------+------------------+------------------+
 *      | discardable bytes |  readable bytes  |  writable bytes  |
 *      +-------------------+------------------+------------------+
 *      |                   |                  |                  |
 *      0      <=      readerIndex   <=   writerIndex    <=    capacity
 *
 *
 *  AFTER discardReadBytes()
 *
 *      +------------------+--------------------------------------+
 *      |  readable bytes  |    writable bytes (got more space)   |
 *      +------------------+--------------------------------------+
 *      |                  |                                      |
 * readerIndex (0) <= writerIndex (decreased)        <=        capacity
```

## 4. `clear()` 方法执行前后

```text
 *  BEFORE clear()
 *
 *      +-------------------+------------------+------------------+
 *      | discardable bytes |  readable bytes  |  writable bytes  |
 *      +-------------------+------------------+------------------+
 *      |                   |                  |                  |
 *      0      <=      readerIndex   <=   writerIndex    <=    capacity
 *
 *
 *  AFTER clear()
 *
 *      +---------------------------------------------------------+
 *      |             writable bytes (got more space)             |
 *      +---------------------------------------------------------+
 *      |                                                         |
 *      0 = readerIndex = writerIndex            <=            capacity
```

## 5. 查找操作

### 5.1. indexOf()

### 5.2. forEachByte()

