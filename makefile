ipToCass: 
	sudo docker exec -it spark-master bash spark-submit --master spark://spark-master:7077 \
    --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,com.datastax.spark:spark-cassandra-connector_2.12:3.5.0 \
    --conf spark.executor.cores=1 \
	--total-executor-cores 1 \
    --conf spark.executor.memory=1G ./consumers/streaming/WriteIpToCassandra.py

batchJob: 
	sudo docker exec -it spark-master bash spark-submit --master spark://spark-master:7077 \
    --deploy-mode client --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,com.datastax.spark:spark-cassandra-connector_2.12:3.5.0,org.postgresql:postgresql:42.5.0 \
    --conf spark.executor.cores=1 \
	--total-executor-cores 1 \
    --conf spark.executor.memory=1G ./consumers/batch/batchQueries.py

down:
	sudo docker-compose down

up:
	sudo docker-compose up -d