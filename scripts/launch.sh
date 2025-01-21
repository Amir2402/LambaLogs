#/usr/bin/bash

COMPOSE_FILE="../docker-compose.yml"
containers=$(sudo docker-compose -f "$COMPOSE_FILE" ps -q)

if [ -n "$containers" ]; then 
    echo "containers are up"; 

else
    echo "launching containers"; 
    sudo docker-compose -f "$COMPOSE_FILE" up -d 
fi 

TOPIC_NAME="logTopic"
kafka_topics=$(sudo docker exec -it kafka-broker-1 kafka-topics.sh --bootstrap-server localhost:9092 --list | grep "$TOPIC_NAME")

if [ -n "$kafka_topics" ]; then 
    echo "Topic exists"; 

else
    echo "Creating topic"; 
    sudo docker exec -it kafka-broker-1 kafka-topics.sh \
    --create --bootstrap-server kafka-broker-1:9092,kafka-broker-2:9093 \
    --replication-factor 2 --partitions 2 --topic logTopic
fi 