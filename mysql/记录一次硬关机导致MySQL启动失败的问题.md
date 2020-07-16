# 记录一次硬关机导致MySQL启动失败的问题

## 出现问题

因系统死机，按任何键都没有反应，硬重启后MySQL启动报错

```ini
[ERROR] InnoDB: Ignoring the redo log due to missing MLOG_CHECKPOINT between the checkpoint 30903245 and the end 30904484.
```

## 解决过程

1. 如果是docker中的MySQL，停止运行docker
   
   ```sh
   systemctl stop docker
   ```

2. 运行下面的命令
   
   ```sh
   rm -rf /var/lib/mysql/ib_logfile*
   ```