# OnlyOffice

## 参考

<https://helpcenter.onlyoffice.com/installation/docs-developer-install-docker.aspx?from=api_csharp_example>

## 如果容器不能连网

Docker specifies Google DNS servers by default. If your ONLYOFFICE Docs is not going to have access to the Internet, we recommend that you change the default Docker DNS address to the address of your local DNS server. To do that go to the /etc/default/docker file and change the IP address in the following line to the IP address of a DNS server in your local network:
docker_OPTS="--dns 8.8.8.8"
For the RPM based operating systems like CentOS, the configuration file can be located here: /etc/docker/daemon.json

## 创建并运行容器

-HTTP

```sh
docker run --name onlyoffice --network rebue -it -dp 17080:80 --restart=always onlyoffice/documentserver-de
```

- HTTPS

```sh
docker run --name onlyoffice --network rebue -it -dp 17443:443 --restart=always onlyoffice/documentserver-de
```

Private key (.key)
SSL certificate (.crt)

/app/onlyoffice/DocumentServer/data/certs/onlyoffice.key
/app/onlyoffice/DocumentServer/data/certs/onlyoffice.crt

## 容器内路径

- /var/log/onlyoffice 日志
- /var/www/onlyoffice/Data 证书
- /var/lib/onlyoffice 文件缓存
- /var/lib/postgresql 数据库
