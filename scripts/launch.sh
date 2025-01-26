#/usr/bin/bash

COMPOSE_FILE="../docker-compose.yml"

containers=$(sudo docker-compose -f "$COMPOSE_FILE" ps -q)

if [ -n "$containers" ]; then 
    echo "containers are up"; 
    sudo docker-compose -f "$COMPOSE_FILE" restart

else
    echo "launching containers"; 
    sudo docker-compose -f "$COMPOSE_FILE" up -d 
fi 
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

../input/flog -l -d 2 -f json | python ../input/logProducer.py & 

ProcessID="$!"
echo "Producer PID: $ProcessID"

sudo docker exec -it spark-master bash spark-submit --master spark://spark-master:7077 --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 --conf spark.executor.cores=4 --conf spark.executor.memory=512m ./consumers/streaming/sparkStreamingJob.py 

kill "$ProcessID"