# ssh跳板

```sh
vi ~/.ssh/config
```

```ini
....

Host 跳板机名称
  HostName 跳板机IP地址
  Port 登录跳板机的端口号
  User 登录跳板机的用户名
Host 目的服务器名称
  HostName 目的服务器的IP地址（相对于跳板机可访问的IP地址）
  Port 登录目的服务器的端口号
  User 登录目的服务器的用户名
  ProxyJump 跳板机名称
....
```
