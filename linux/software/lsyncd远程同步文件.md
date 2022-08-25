# lsyncd远程同步文件

## 简介

lsyncd是linux上的一款实时文件同步工具，使用lua语言封装了 inotify 和 rsync

## 安装

```sh
yum install lsyncd -y
lsyncd -version
```

## 配置

```sh
vi /etc/lsyncd.conf
```

```ini
settings {
    logfile = "/tmp/lsyncd.log",        # 日志
    statusFile = "/tmp/lsyncd.status",  # 记录同步的文件和目录
    maxProcesses = 1,                   # 同步进程的最大个数
}
targets = {                             # 目的主机的列表
    'xxx.xxx.xxx.xxx:/usr/local',
    'xxx.xxx.xxx.xxx:/usr/local'
}
for _, target in ipairs( targets )      # 循环同步的目的主机
do
    sync {
        source = "/usr/local",          # 源地址
        target = target,                # 目的地址
        exclude = { "logs" },           # 排除不需要同步的文件或文件夹
        rsync = {
            archive = true,
            compress = true
        }
        ssh = {
            port = xxxxx
        }
    }
end
```

## 启动和启用

```sh
systemctl start lsyncd
systemctl enable lsyncd
```
