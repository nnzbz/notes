# Scrapy

[TOC]

## 1. 官网及文档

官网: <https://scrapy.org/>

文档: <https://doc.scrapy.org/en/latest/>

## 2. Scrapy组件

- 引擎(Scrapy):
 用来处理整个系统的数据流处理, 触发事务(框架核心)
- 调度器(Scheduler):
 用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址
- 下载器(Downloader):
 用于下载网页内容, 并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)
- 爬虫(Spiders):
 爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面
- 项目管道(Pipeline):
 负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。
- 下载器中间件(Downloader Middlewares):
 位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。
- 爬虫中间件(Spider Middlewares):
 介于Scrapy引擎和爬虫之间的框架，主要工作是处理蜘蛛的响应输入和请求输出。
- 调度中间件(Scheduler Middewares):
 介于Scrapy引擎和调度之间的中间件，从Scrapy引擎发送到调度的请求和响应。

## 3. Scrapy 运行流程

1. 引擎从调度器中取出一个链接(URL)用于接下来的抓取
2. 引擎把URL封装成一个请求(Request)传给下载器，下载器把资源下载下来，并封装成应答包(Response)
3. 爬虫解析Response
4. 若是解析出实体（Item）,则交给实体管道进行进一步的处理;若是解析出的是链接（URL）,则把URL交给Scheduler等待抓取

默认情况下，Scrapy使用 **LIFO** 队列来存储等待的请求。简单的说，就是 **深度优先顺序** 。如果想要 **广度优先顺序** 进行爬取，需要进行设定。

## 4. 安装

```sh
pip3 install Scrapy
# 上面的命令在天朝会被墙，这里可用下面的命令换源
pip3 install scrapy -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```

## 5. 创建项目

```sh
scrapy startproject 项目名
```

文件说明：

| 文件        | 说明                                                                                                        |
|:------------|:------------------------------------------------------------------------------------------------------------|
| scrapy.cfg  | 项目的配置信息，主要为Scrapy命令行工具提供一个基础的配置信息。（真正爬虫相关的配置信息在settings.py文件中） |
| items.py    | 设置数据存储模板，用于结构化数据，如：Django的Model                                                         |
| pipelines   | 数据处理行为，如：一般结构化的数据持久化                                                                    |
| settings.py | 配置文件，如：递归的层数、并发数，延迟下载等                                                                |
| spiders     | 爬虫目录，如：创建文件，编写爬虫规则                                                                        |

## 6. 通过模板创建爬虫

```sh
scrapy genspider -t crawl 爬虫名 网站域名
```

- 参数-t: 指出使用的模板
- 要显示可用的模板，用下面的命令：

```sh
scrapy genspider -l
```

## 7. 编写爬虫

Scrapy框架中分两类爬虫，Spider类和CrawlSpider类。

- Spider类的设计原则是只爬取start_url列表中的网页
- CrawlSpider是Spider的派生类，定义了一些规则(rule)来提供跟进link的方便的机制，从爬取的网页中获取link并继续爬取的工作更适合。

### 7.1. Spider

在spiders目录中新建 area_spider.py 文件

```py
# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from area.items import AreaItem

# from scrapy.http import Http


class AreaSpider(scrapy.Spider):
    # 爬虫名
    name = 'area'
    allowed_domains = ['stats.gov.cn']
    # 爬取的URL，可以是多个
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html']

    def parse(self, response):
        pass
```

### 7.2. CrawlSpider

```py
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class StatsSpider(CrawlSpider):
    name = 'stats'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
```

## 8. 运行爬虫

### 8.1. 命令行

进入项目目录，运行命令

```sh
scrapy crawl 爬虫名 --nolog
```

 **-nolog:** 不显示日志

### 8.2. PyCharm

- 项目根目录下创建 ```main.py```

```py
from scrapy import cmdline

cmdline.execute("scrapy crawl area".split())
```

- 添加项目运行的配置

## 9. Scrapy查询语法

Selector有四个基本的方法(点击相应的方法可以看到详细的API文档):

- xpath()
 传入xpath表达式，返回该表达式所对应的所有节点的selector list列表 。
- css()
 传入CSS表达式，返回该表达式所对应的所有节点的selector list列表.
- extract()
 序列化该节点为unicode字符串并返回list。
- re()
 根据传入的正则表达式对数据进行提取，返回unicode字符串list列表。

xpath()方法示例:
查询儿子中的某个标签(以div标签为例)：/div
查询子子孙孙中的某个标签(以div标签为例)：//div
查询标签中带有某个class属性的标签：//div[@class='c1']即子子孙孙中标签是div且class=‘c1’的标签
查询标签中带有某个class=‘c1’并且自定义属性name=‘alex’的标签：//div[@class='c1'][@name='alex']
查询某个标签的文本内容：//div/span/text() 即查询子子孙孙中div下面的span标签中的文本内容
查询某个属性的值（例如查询a标签的href属性）：//a/@href

## 10. 格式化处理

- 修改items.py

```py
class AreaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 编码
    code = scrapy.Field()
    # 名称
    name = scrapy.Field()
```

- 修改settings.py

```py
# 激活Pipeline组件
ITEM_PIPELINES = {
    'area.pipelines.AreaPipeline': 300,
}
LOG_LEVEL = 'INFO'
```

- 修改spider

```py
class AreaSpider(scrapy.Spider):
    # 爬虫名
    name = 'area'
    allowed_domains = ['stats.gov.cn']
    # 爬取的URL，可以是多个
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html']

    def parse(self, response):
        # 创建选择器对象
        selector = Selector(response)
        items = selector.css('tr.provincetr a')
        for item in items:
            areaitem = AreaItem()
            # areaitem['code'] = item.xpath('@href').re_first('(.*)\.html')
            areaitem['code'] = item.css('::attr(href)').re_first('(.*)\.html')
            # areaitem['name'] = item.xpath('text()').extract_first()
            areaitem['name'] = item.css('::text').extract_first()
            yield areaitem
```

## 11. 获取响应的Cookie

```py
def parse(self, response):
    from scrapy.http.cookies import CookieJar
    cookieJar = CookieJar()
    cookieJar.extract_cookies(response, response.request)
    print(cookieJar._cookies)
```

## 12. Scrapyd

<http://scrapyd.readthedocs.io/en/latest>

### 12.1. 安装服务器

```sh
# CentOS下先安装需要的环境
# (无效)可用yum search python | grep -i devel查看
# yum install python36-devel.x86_64
# 有效
yum install python-devel
# 安装scrapyd
pip install scrapyd
```

注意：但目前不是最新版本，建议到 https://github.com/scrapy/scrapyd 网站下载最新源码版本，然后解压到任意目录，再用 ```python setup.py install``` 命令手动安装。

### 12.2. 让非本地也可访问服务器

```sh
vi /usr/lib/python2.7/site-packages/scrapyd/default_scrapyd.conf
```

将 ```bind_address = 127.0.0.1``` 改为 ```bind_address = 0.0.0.0```

### 12.3. 运行服务器

下面命令用于启动scrapyd服务器

```sh
scrapyd
# 后台运行
nohup scrapyd > nohup.out 2>&1 &
```

服务启动默认监听 ```6800``` 端口

### 12.4. 服务器的守护进程supervisor

scrapyd服务器实在是太脆弱了，用supervisor保护一下

- 安装supervisor

```sh
pip install supervisor
```

- 配置supervisor

```sh
sudo mkdir -p /etc/supervisor/
# 导入默认配置
sudo su - root -c "echo_supervisord_conf > /etc/supervisor/supervisord.conf"
# 编辑
vi /etc/supervisor/supervisord.conf
```

主要修改内容如下

```ini
....
# 链接管理
[inet_http_server]         ; inet (TCP) server disabled by default
port=127.0.0.1:9001        ; ip_address:port specifier, *:port for all iface
....
[supervisorctl]
;serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket
serverurl=http://127.0.0.1:9001 ; use an http:// url to specify an inet socket
....
# 设置管理进程
[program:scrapyd]
command=scrapyd
autostart=true
autorestart=unexpected
```

- 创建supervisor服务

```sh
vi /usr/lib/systemd/system/supervisord.service
```

```ini
[Unit]
Description=supervisord - Supervisor process control system for UNIX
Documentation=http://supervisord.org
After=network.target

[Service]
Type=forking
ExecStart=/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
ExecReload=/usr/bin/supervisorctl reload
ExecStop=/usr/bin/supervisorctl shutdown
User=<user>

[Install]
WantedBy=multi-user.target
```

```sh
# 启动
systemctl enable supervisord
systemctl start supervisord

# 查看
supervisorctl

# 如一切正常，显示如下
scrapyd                          RUNNING   pid 21599, uptime 0:00:35
```

### 12.5. 部署项目

- 修改项目的 ```scrapy.cfg``` 文件，去掉url前的注释符号，并将地址改为真正的IP地址

```ini
....
[deploy]
url = http://localhost:6800/
....
```

- 安装scrapyd-deploy

```sh
pip install Scrapyd-client
```

- 部署

```sh
cd <项目目录>
sudo scrapyd-deploy
```

### 12.6. API控制

```sh
# 启动任务
curl http://localhost:6800/schedule.json -d project=myproject -d spider=somespider
curl http://localhost:6800/cancel.json -d project=<项目名> -d job=<JobID>
```

1、启动API（POST）: 

http://192.168.0.2:6800/schedule.json -d project=xxxspider -d spider=cplusplus -d word=['hahaha'] -d version=1.0.2

1
{"status": "ok", "jobid": "dcc25dda594b11e6b757fc4dd43b1961", "node_name": "ubuntu-16"}
2、取消API（POST）:

 http://192.168.0.2:6800/cancel.json -d project=xxxspider -d job=6487ec79947edab326d6db28a2d86511e8247444(启动爬虫后,API返回任务ID号)

3、删除工程某版本API（POST）: 

http://192.168.0.2:6800/delversion.json -d project=xxxspider -d version=1470208884'

4、删除工程API（POST）: 

http://192.168.0.2:6800/delproject.json -d project=myproject

5、已经发布的工程列表：

http://192.168.0.2:6800/listprojects.json

6、已经发布的工程(xxxspider)中的爬虫列表：

http://192.168.0.2:6800/listspiders.json?project=xxxspider

7、已经发布的工程(xxxspider)的版本号：

http://192.168.0.2:6800/listversions.json?project=xxxspider

8、已经发布的工程(xxxspider)的任务清单，即状态（已结束、正在运行、准备启动）：

http://192.168.0.2:6800/listjobs.json?project=xxxspider

## 13. 如何防止被ban

### 13.1. 官网建议

Scrapy官方文档：http://doc.scrapy.org/en/master/topics/practices.html#avoiding-getting-banned

- rotate your user agent from a pool of well-known ones from browsers (google around to get a list of them)
- disable cookies (see COOKIES_ENABLED) as some sites may use cookies to spot bot behaviour
- use download delays (2 or higher). See DOWNLOAD_DELAY setting.
- if possible, use Google cache to fetch pages, instead of hitting the sites directly
- use a pool of rotating IPs. For example, the free Tor project or paid services like ProxyMesh. An open source alternative is scrapoxy, a super proxy that you can attach your own proxies to.
- use a highly distributed downloader that circumvents bans internally, so you can just focus on parsing clean pages. One example of such downloaders is Crawlera

### 13.2. settings.py

- url去重

```py
DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'
```

- 设置下载延迟

```py
DOWNLOAD_DELAY = 3
```

- 禁用cookies

```py
COOKIES_ENABLED = False
```

- 重试次数

```py
# 重试次数
RETRY_TIMES = 12
```

- 减小下载超时

```py
# 减小下载超时(秒)
DOWNLOAD_TIMEOUT = 5
```

- 设置USER_AGENT

```py
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/65.0.3325.162 Safari/537.36 "
# 使用user agent池，轮流选择之一来作为user agent
# USER_AGENTS = [
#     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
#     "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
#     "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
#     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
#     "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
#     "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
#     "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
#     "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
#     "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
#     "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
#     "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
# ]
```

- 添加代理IP(须修改中间件)

```py
PROXIES = [
    'https://125.118.79.208:6666',
    'https://183.159.93.90:18118',
    'https://60.177.226.5:18118',
    'https://183.159.87.111:18118',
    'http://113.121.244.193:808',
    'http://110.73.14.243:8123',
    'https://120.92.88.202:10000',
    'https://183.159.93.174:18118',
    'https://110.73.34.205:8123',
    'https://14.118.253.203:6666',
    'http://14.112.76.205:61234',
    'https://223.241.119.158:18118',
    # {'ip_port': '111.11.228.75:80', 'user_pass': ''},
    # {'ip_port': '120.198.243.22:80', 'user_pass': ''},
    # {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
    # {'ip_port': '101.71.27.120:80', 'user_pass': ''},
    # {'ip_port': '122.96.59.104:80', 'user_pass': ''},
    # {'ip_port': '122.224.249.122:8088', 'user_pass': ''},
]

....

DOWNLOADER_MIDDLEWARES = {
    # 'area.middlewares.RandomUserAgent': 1,
    'area.middlewares.ProxyMiddleware': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # 'scrapy_crawlera.CrawleraMiddleware': 600
}
```

- 设置下载中间件

https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

```py
import random
import logging
from settings import PROXIES#, USER_AGENTS
# class RandomUserAgent(object):
#     # 随机切换User Agent
#     def process_request(self, request, spider):
#         agent = random.choice(USER_AGENTS)
#         print("switch user agent:" + agent)
#         request.headers.setdefault('User-Agent', agent)

# class ProxyMiddleware(object):
#     # 随机切换代理
#     def process_request(self, request, spider):
#         proxy = random.choice(PROXIES)
#         print("switch proxy:" + proxy['ip_port'])
#         request.meta['proxy'] = proxy['ip_port']
#         if proxy['user_pass'] is not None:
#             encoded_user_pass = base64.encodestring(proxy['user_pass'])
#             request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
class ProxyMiddleware(object):
    # 随机切换代理
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        logging.info("switch proxy:" + proxy + '*******************************')
        request.meta['proxy'] = proxy
```

### 13.3. Scrapinghub

#### 13.3.1. 注册

https://app.scrapinghub.com/account/signup/

#### 13.3.2. 安装

```sh
pip install scrapy-crawlera
```

#### 13.3.3. Scrapy Cloud（免费）

提供部署爬虫服务器的地方

- Code & Deploys

```sh
pip install shub
# 先进入本地项目源码的根目录
shub login
API key: <API Key>
shub deploy <Project ID>
```

#### 13.3.4. Crawlera（付费)

提供了防止 ban 的机制，通过 ip、user-agent、cookie 等设置，防止爬虫被禁。

- settings.py

```py
DOWNLOADER_MIDDLEWARES = {
    'scrapy_crawlera.CrawleraMiddleware': 600
}
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '<API key>'
# 适当调整下列选项
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32
AUTOTHROTTLE_ENABLED = False
DOWNLOAD_TIMEOUT = 600
# 如果在代码中设置有 DOWNLOAD_DELAY的话，添加下面一行
# CRAWLERA_PRESERVE_DELAY = True
# 如果你的spider中保留了cookies,那么需要在Headr中添加
# DEFAULT_REQUEST_HEADERS = {
#     # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     # 'Accept-Language': 'zh-CN,zh;q=0.8',
#     'X-Crawlera-Cookies': 'disable'
# }
```

- 407错误

一般是API Key不正确，这里的API Key是Crawlera的（付费），而不是部署项目的API Key(免费)，用下面的命令行检测一下

```sh
curl -vx proxy.crawlera.com:8010 -U <API Key> http://httpbin.org/ip
```