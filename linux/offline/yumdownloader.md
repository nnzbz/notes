# yumdownloader

`yumdownloader` 可以一次性下载 `RPM` 软件包及其所有依赖包。

使用示例如下(下载httpd软件包及其示例):

1. 配置 epel

   ```sh
   yum install epel-release -y
   ```

2. 安装(如已有则不用安装)

   ```sh
   yum install yum-utils -y
   ```

   - yum-utils 包含了 yumdownloader

3. 下载httpd软件包并压缩

   ```sh
   mkdir httpd
   yumdownloader --resolve --destdir=httpd httpd
   yumdownloader --resolve --destdir=httpd createrepo
   tar -zcvf httpd.tar.gz ./httpd
   ```

   - --resolve 仅下载，不安装
   - --destdir 指定下载路径
   - createrepo 下载createrepo包为制作离线源使用

4. 上传到服务器

   将 `httpd.tar.gz` 文件上传到服务器

5. 解压文件

   ```sh
   tar -zxvf httpd.tar.gz
   ```

6. 服务器上创建仓库

   ```sh
   cd httpd
   rpm -ivh createrepo-0.9.9-28.el7.noarch.rpm
   createrepo httpd
   ```

7. 服务器上编辑仓库文件

   ```sh
   vi /etc/yum.repos.d/httpd.repo
   ```

   ```ini
   [httpd]
   name=httpd
   baseurl=file:///root/httpd/
   gpgcheck=0
   enabled=1
   ```

8. 服务器上离线安装 httpd

   ```sh
   yum install httpd -y
   ```
