# MySQL注意

## 设置unique

- 可以在生成脚本后查找脚本中是否有 `   key ` 来检查

## 1. 如果是非负数必须设置无符号的unsigned

在MySQL的物理图中 > 双击表 > 在 `Columns` 中选择要更改的字段 > 查看属性 > 切换到MySQL标签页 > 勾选 `Unsigned` > 确定并保存

- 常见的有tinyint,bigint
- 可以在生成脚本后查找脚本中是否有 `bigint not null` 、`bigint  comment` 、 `tinyint not null` 来检查

## 2. ID字段的数据类型请使用unsigned

生成的脚本应如下:

```txt
id                   bigint unsigned not null  comment 'XXX',
```

- 可以在生成脚本后查找脚本中是否有 `bigint not null` 来检查
