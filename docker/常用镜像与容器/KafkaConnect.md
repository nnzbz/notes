# kafka connect

```sh
docker run -it --rm \
    --name kafka-connect \
    -e CONNECT_BOOTSTRAP_SERVERS=172.17.0.1:9092 \
    -e CONNECT_GROUP_ID=testgroup \
    -e CONNECT_CONFIG_STORAGE_TOPIC=testconfigtopic \
    -e CONNECT_OFFSET_STORAGE_TOPIC=testoffsettopic \
    -e CONNECT_STATUS_STORAGE_TOPIC=teststatustopic \
    -e CONNECT_KEY_CONVERTER=org.apache.kafka.connect.storage.StringConverter \
    -e CONNECT_VALUE_CONVERTER=org.apache.kafka.connect.storage.StringConverter \
    -e CONNECT_REST_ADVERTISED_HOST_NAME=127.0.0.1 \
    confluentinc/cp-kafka-connect-base
    #-e KAFKA_CFG_PLUGIN_PATH=/opt/connector/ \
    #-v ~/workspaces/kafka/connector/:/opt/connector/:z \
```
