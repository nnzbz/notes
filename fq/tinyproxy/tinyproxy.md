# tinyproxy

1. 安装

   ```sh
   yum install -y tinyproxy
   ```

2. 修改配置

   ```sh
   vi /etc/tinyproxy.conf
   ```

   ```ini
   # 默认是8888
   Port 12345

   ....

   # 注释下面这行
   # Allow 127.0.0.1
   ```

3. 运行

   ```sh
   service tinyproxy start
   ```

4. 打开防火墙

   ```sh
   iptables -I INPUT -p tcp --dport 12345 -j ACCEPT
   ```

5. 检测

   ```sh
   telnet <IP地址> 12345
   # 下面命令没有测试成功，报错 `curl: (56) Recv failure: Connection reset by peer`
   curl --proxy <IP地址> -k https://www.google.com/
   ```
