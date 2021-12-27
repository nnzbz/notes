# 制作ElasticSearch的Docker容器

[TOC]

## 1. 单机


### 1.1. 调整docker配置(Mac)

![调整docker配置](调整docker配置.png)

### 1.2. 开发模式(命令行)

```sh
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.2
```

### 1.3. 检查是否正常运行

在浏览器中浏览 <http://127.0.0.1:9200/>，如果返回类似如下内容，说明正常运行

```json
{
  "name" : "93e8e4378a4d",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "xgDxGORZSlSiQElPzuvGtQ",
  "version" : {
    "number" : "7.3.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "de777fa",
    "build_date" : "2019-07-24T18:30:11.767338Z",
    "build_snapshot" : false,
    "lucene_version" : "8.1.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

### 1.4. 安装插件注意

- 安装插件也就是把release的文件复制到plugin目录下
- 如果用install安装出现类似下面的问题:

```text
java.lang.IllegalArgumentException: Plugin [analysis-xxx] was built for Elasticsearch version x.x.x but version x.x.x is running
```

把release中的 `plugin-descriptor.properties` 文件修改内容如下:

```ini
elasticsearch.version=ElasticSearch当前的版本
```

- 安装后，记得重启es

### 1.5. 安装ik插件

注意安装后可能需要重启 `ElasticSearch`

```sh
./bin/elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.3.0/elasticsearch-analysis-ik-7.3.0.zip
```

最好是先下载下来，复制到容器中去，再安装

```sh
./bin/elasticsearch-plugin install --batch file:./elasticsearch-analysis-ik-6.8.2.zip
```

### 1.6. 安装pinyin分词插件

```sh
./bin/elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-pinyin/releases/download/v7.3.0/elasticsearch-analysis-pinyin-7.3.0.zip
```

## 2. Swarm

### 2.1. 参考

<https://www.elastic.co/guide/en/elasticsearch/reference/7.16/docker.html#docker-compose-file>

### 2.2. Docker Compose

```sh
mkdir -p /usr/local/es
vi /usr/local/es/stack.yml
```

```yml{.line-numbers}
version: "3.9"
services:
  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.16.2
    container_name: es01
    environment:
      - node.name=es01
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es02,es03
      - cluster.initial_master_nodes=es01,es02,es03
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - es01data:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
  es02:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.16.2
    container_name: es02
    environment:
      - node.name=es02
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01,es03
      - cluster.initial_master_nodes=es01,es02,es03
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - es02data:/usr/share/elasticsearch/data
  es03:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.16.2
    container_name: es03
    environment:
      - node.name=es03
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01,es02
      - cluster.initial_master_nodes=es01,es02,es03
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - es03data:/usr/share/elasticsearch/data

volumes:
  es01data:
  es02data:
  es03data:

networks:
  default:
    external: true
    name: rebue
```

### 2.3. 部署

```sh
docker stack deploy -c /usr/local/es/stack.yml es
```

## 3. 生产模式推荐

### 3.1. 参考

<https://www.elastic.co/guide/en/elasticsearch/reference/7.16/docker.html#docker-prod-prerequisites>

### 3.2. 设置 `vm.max_map_count`

设置 `vm.max_map_count` 至少 `262144`

- Linux

持久化

```sh
vi /etc/sysctl.conf
```

```ini
....
vm.max_map_count=262144
....
```

立即生效

```sh
sysctl -w vm.max_map_count=262144
```

### 3.3. ulimit

可增加 `nofile` 和 `nproc`，例如: `--ulimit nofile=65535:65535`

### 3.4. 禁用 swapping

为了性能和节点的稳定性，需要禁用 `swapping`

如果设置了选项 `bootstrap.memory_lock: true`，那就需要定义 `memlock: true`

```sh
-e "bootstrap.memory_lock=true" --ulimit memlock=-1:-1
```

### 3.5. 优化内存

使用 `ES_JAVA_OPTS` 环境变量来设置内存使用大小，默认 `-Xms2g -Xmx2g`，开发根据实际需要可以改小些，如: `-e ES_JAVA_OPTS="-Xms1g -Xmx1g"` 。

