# RabbitMQ入门

[TOC]

## 1. 安装

### 1.1. CentOS下安装

安装EPEL软件仓库(EL6)

```sh
su -c 'rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm'
...
su -c 'yum install foo'
```

安装EPEL软件仓库(EL7)

```sh
su -c 'rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm'
...
su -c 'yum install foo'
```

安装wget

```sh
# yum install wget
```

下载并安装Erlang

```sh
# wget https://www.rabbitmq.com/releases/erlang/erlang-18.2-1.el6.x86_64.rpm
# yum -y install erlang-18.2-1.el6.x86_64.rpm
```

直接用yum安装Erlang

```sh
# yum install erlang
```

安装rabbitmq-server

```sh
rpm --import https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
yum install rabbitmq-server
```

直接安装rabbitmq-server

```sh
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.rpm.sh | sudo bash
yum install rabbitmq-server-3.6.1-1.noarch.rpm
```

### 1.2. Debian下安装

使用rabbitmq.com的APT Repository

```sh
# sudo vi /etc/apt/sources.list
```

加入下面这行

```text
deb http://www.rabbitmq.com/debian/ testing main
add our public key to your trusted key list using apt-key(8)
cd /etc/apt/
sudo wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
sudo apt-key add rabbitmq-signing-key-public.asc
```

更新

```sh
# sudo apt-get update
```

安装

```sh
# sudo apt-get install rabbitmq-server
```

### 1.3. 启动

```sh
# sudo service rabbitmq-server start
```

### 1.4. 添加用户

```sh
sudo rabbitmqctl add_user admin admin
sudo rabbitmqctl set_user_tags admin administrator
sudo rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*"
```

### 1.5. 安装管理插件

```sh
# sudo rabbitmq-plugins enable rabbitmq_management
```

### 1.6. 自动启动

```sh
# sudo chkconfig rabbitmq-server on
```

### 1.7. 检测端口

```text
4369 (epmd), 25672 (Erlang distribution)
5672, 5671 (AMQP 0-9-1 without and with TLS)
15672 (if management plugin is enabled, 访问http://127.0.0.1:15672，用户名密码都是guest)
61613, 61614 (if STOMP is enabled)
1883, 8883 (if MQTT is enabled)
```

## 2. 配置环境变量(rabbitmq-env.conf)

文件路径是/etc/rabbitmq/rabbitmq-env.conf（这个文件的位置是确定和不能改变的，目录需要自己创建）。
环境变量有统一的前缀RABBITMQ_，具体的列表见：http://www.rabbitmq.com/configure.html#define-environment-variables
……
RABBITMQ_CONFIG_FILE=/etc/rabbitmq/rabbitmq.config
RABBITMQ_NODE_PORT=5672                            //AMQP监听端口号
RABBITMQ_DIST_PORT=RABBITMQ_NODE_PORT+20000        //集群使用的端口号
RABBITMQ_MNESIA_BASE=/app/rabbitmq/data            //MNESIA数据库的路径
RABBITMQ_LOG_BASE=/app/rabbitmq/logs               //log的路径
RABBITMQ_PLUGINS_DIR=/app/rabbitmq/plugins         //插件的路径
……
注意，记得要改变/app/rabbitmq路径的所有者

```sh
# chown rabbitmq:rabbitmq -R /app/rabbitmq/
```

## 3. 配置信息（rabbitmq.config）

默认路径是/etc/rabbitmq/rabbitmq.config，也可由上面的环境变量配置。示例配置文件默认安装在/usr/share/doc/rabbitmq-server-3.5.4/rabbitmq.config.example

## 4. 四、	

1. channel.basicConsume(QUEUE_NAME, true, consumer)方法调用后，服务器端开始向消费者投递消息，投递消息是个异步过程，因此消费者需要提供一个回调临时队列，用于缓存消息，临时队列封装在QueueingConsumer对象中，以LinkedBlockingQueue类型存在，因此，如果不注意，服务器端会源源不断向消费者投递消息，直到挤爆内存。

```java
LinkedBlockingQueue<QueueingConsumer.Delivery> bq = new 
    LinkedBlockingQueue<QueueingConsumer.Delivery>();
QueueingConsumer consumer = new QueueingConsumer(channel, bq);
channel.basicConsume(QUEUE_NAME, false, consumer);
 while (true) {
    QueueingConsumer.Delivery delivery = consumer.nextDelivery();
    String message = new String(delivery.getBody());
    System.out.println(" [x] Received '" + message + "'");}
```

2. 当一个队列上有多个消费者时，broke会以round-robin的方式按序投递消息，每个消费者得到平均数量的消息。
3. 默认情况下，broke会要求消费者显式对消息进行确认(channel.basicAck)，broke收到ack消息后才从服务器端删去消息。RabbitMQ并没有对ack的时间进行限制，未做超时控制，这样能使得消费者有充足的时间处理消息。重发消息的唯一触发点是目标消费者连接断开，这时broke会重新选择一个消费者投递此消息。
4. 服务器端的消息可靠性需由队列持久化机制和消息持久化机制共同保障。队列持久化通过channel.queueDeclare方法的durable参数为true来实现。消息持久化通过channel.basicPublish方法的BasicProperties参数设置为MessageProperties.PERSISTENT_TEXT_PLAIN来实现。一条队列一旦声明完毕，就能不能再改变其属性，包括是否持久化durable、autoDelete, exclusive等参数。另外持久化参数并未保证消息100%写入磁盘，它可能只是写到磁盘缓存，在刷到磁盘之前服务器挂掉仍会造成消息丢失，确保消息完全可靠需配合生产者confirm机制。
5. channel.basicQos使得broke可以根据消费者负载投递消息，消费者指定basicQos参数，broke会根据参数值最多投递多少条消息过去，等消费者ack消息后继续投递，因此channel.basicQos需跟channel.basicAck配合使用，能解决round-robin算法带来的实际负载不均衡缺陷。
6. exchange负责路由，它从生产者端接收消息，根据策略(消息的routeKey和队列exchange之间的bindKey)将消息放入不同队列。消费者从队列消费消息。exchange有fanout, direct, topic等几种类型。fanout是广播类型，它忽略channel.basicPublish的routeKey参数，将消息投递到所有与自己bind的队列。direct是直接投递类型，需要消息的routeKey和队列bindKey严格匹配才能投递。topic类型介于两者之间，它要求routeKey和bindKey必须以点号分隔的字符串形式出现，其中bindKey和routeKey均支持*和#通配符，前者表示严格匹配一个单词，后者表示匹配0个或多个单词。当bindKey为#时，topic类型同fanout类型。当bindKey不含*和#通配符时，topic类型退化为direct类型。
7. 队列和exchange之间可以有多个bindKey，当一条消息的routeKey匹配多个bindKey时，同一个队列收到的消息仍是一条。
8. channel.basicPublish如果不指定队列名称，则broke默认会将消息投递到以routeKey命名的队列中，如果此队列不存在，则消息丢失。
9. 为了消息可靠性考虑，一般exchange和queue以及binding会在生产者和消费者两端一起声明。生产者声明queue为了保证消息发送到exchange后可以入队列，此时如果队列不存在，消息会丢弃。消费者声明exchange可以保证binding正确进行，若exchange不存在，binding异常退出。

