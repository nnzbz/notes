# kafka connect

```sh
docker run -it --rm \
    --name kafka-connect \
    -p 28082:28082 \
    -e CONNECT_BOOTSTRAP_SERVERS=172.17.0.1:9092 \
    -e CONNECT_REST_PORT=28082 \
    -e CONNECT_REST_ADVERTISED_HOST_NAME=127.0.0.1 \
    -e CONNECT_GROUP_ID=quickstart \
    -e CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR=1 \
    -e CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR=1 \
    -e CONNECT_STATUS_STORAGE_REPLICATION_FACTOR=1 \
    -e CONNECT_CONFIG_STORAGE_TOPIC=quickstart-config \
    -e CONNECT_OFFSET_STORAGE_TOPIC=quickstart-offset \
    -e CONNECT_STATUS_STORAGE_TOPIC=quickstart-status \
    -e CONNECT_KEY_CONVERTER=org.apache.kafka.connect.json.JsonConverter \
    -e CONNECT_VALUE_CONVERTER=org.apache.kafka.connect.json.JsonConverter \
    -e CONNECT_PLUGIN_PATH=/opt/connector \
    -v ~/workspaces/kafka/connector/:/opt/connector/:z \
    confluentinc/cp-kafka-connect-base
    #-e KAFKA_CFG_PLUGIN_PATH=/opt/connector/ \
```
