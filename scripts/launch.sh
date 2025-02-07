#!/usr/bin/bash

COMPOSE_FILE="../docker-compose.yml"

source ~/dirs/myenv/bin/activate

sudo docker-compose -f "$COMPOSE_FILE" down

echo "launching containers"; 
sudo docker-compose -f "$COMPOSE_FILE" up -d 

sleep 10 

TOPIC_NAME="logTopic"
kafka_topics=$(sudo docker exec -it kafka-broker-1 kafka-topics --bootstrap-server localhost:9092 --list | grep "$TOPIC_NAME")

if [ -n "$kafka_topics" ]; then 
    echo "Topic exists"; 

else
    echo "Creating topic"; 
    sudo docker exec -it kafka-broker-1 kafka-topics \
    --create --bootstrap-server kafka-broker-1:9092,kafka-broker-2:9093,kafka-broker-3:9094 \
    --replication-factor 2 --partitions 2 --topic logTopic
fi 

./setUpCassandra.sh

sudo docker exec -i postgres_db psql -U admin -d logs_db -f /dev/stdin < ./PostgresSchema.sql

../input/flog -l -d 2 -f json | python ../input/logProducer.py & 

ProcessID="$!"
echo "Producer PID: $ProcessID"

sudo docker exec -it spark-master pip install requests
sudo docker exec -it spark-worker-1 pip install requests
sudo docker exec -it spark-worker-2 pip install requests

sudo docker exec -it spark-master bash spark-submit --master spark://spark-master:7077 \
    --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,org.postgresql:postgresql:42.5.0 \
    --conf spark.executor.cores=1 \
    --total-executor-cores 1 \
    --conf spark.executor.memory=1G ./consumers/streaming/AggregateToPg.py

kill "$ProcessID"
