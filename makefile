aggToPg: 
	sudo docker exec -it spark-master bash spark-submit --master spark://spark-master:7077 \
    --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,com.datastax.spark:spark-cassandra-connector_2.12:3.5.0 \
    --conf spark.executor.cores=1 \
    --conf spark.executor.memory=1G ./consumers/streaming/WriteIpToCassandra.py

down: 
	sudo docker-compose down 

