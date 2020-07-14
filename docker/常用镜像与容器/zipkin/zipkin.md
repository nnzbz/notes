# zipkin

[TOC]

- Zipkin

```sh
docker run --name zipkin --restart=always -dp 9411:9411 openzipkin/zipkin
```

- Zipkin Slim

只支持in-memory与Elasticsearch的精简版

```sh
docker run -dp 9411:9411 --name zipkin --restart=always openzipkin/zipkin-slim
```
