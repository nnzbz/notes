# Kibana

## 单机

- 前置

```sh
docker run --name es01-test --net elastic -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.16.2
```

- 创建并运行容器

```sh
docker run --name kib01-test --net elastic -p 127.0.0.1:5601:5601 -e "ELASTICSEARCH_HOSTS=http://es01-test:9200" docker.elastic.co/kibana/kibana:7.16.2
```

## Swarm

```sh
mkdir -p /usr/local/kibana
vi /usr/local/kibana/stack.yml
```

```yml{.line-numbers}
version: "3.9"
services:
  kibana:
    image: docker.elastic.co/kibana/kibana:7.16.2
    ports:
      - 5601:5601
    environment:
      SERVER_NAME: kibana
      ELASTICSEARCH_HOSTS: '["http://es01:9200","http://es02:9200","http://es03:9200"]'

networks:
  default:
    external: true
    name: rebue
```

```sh
docker stack deploy -c /usr/local/kibana/stack.yml kibana
```
