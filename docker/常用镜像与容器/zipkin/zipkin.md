# zipkin

[TOC]

- Zipkin

```sh
docker run --name zipkin --restart=always -dp 9411:9411 openzipkin/zipkin
```

- Zipkin Slim

```sh
docker run --name zipkin --restart=always -dp 9411:9411 openzipkin/zipkin-slim -name zipkin
```
