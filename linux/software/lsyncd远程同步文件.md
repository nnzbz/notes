# lsyncd远程同步文件

## 简介

lsyncd是linux上的一款实时文件同步工具，使用lua语言封装了 inotify 和 rsync

## 安装

```sh
# 没有安装EPEL的要安装EPEL
yum install epel-release -y
# 更新
yum update -y
# 已安装EPEP直接运行下面这行
yum install lsyncd -y
# 查看版本
lsyncd -version
```

## 配置

```sh
vi /etc/lsyncd.conf
```

```ini
settings {
    logfile = "/var/log/lsyncd/lsyncd.log",         -- 日志
    statusFile = "/var/log/lsyncd/lsyncd.status",   -- 记录同步的文件和目录
    maxProcesses = 1                                -- 同步进程的最大个数
}
dests = {                                           -- 目的主机的列表
    'xxx.xxx.xxx.xxx',
    'xxx.xxx.xxx.xxx'
}
for _, dest in ipairs(dests) do                     -- 循环同步的目的主机
    sync {
        default.rsyncssh,
        source = "/usr/local",                      -- 源地址
        host = dest,                                -- 目的主机
        targetdir = "/usr/local",                   -- 目的路径
        exclude = { "log/*/*" },                    -- 排除不需要同步的文件或文件夹
        rsync = {
            archive = true,
            compress = true
        },
        ssh = {
          port = 22
        }
    }
end
```

## 启动和启用

```sh
systemctl start lsyncd
systemctl enable lsyncd
```

## 查看启动状态

```sh
systemctl status lsyncd
```


## 查看日志

```sh
cat /var/log/lsyncd/lsyncd.log
cat /var/log/lsyncd/lsyncd.status
```
