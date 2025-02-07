#!/usr/bin/bash

echo "Waiting for Cassandra to be ready..."

while ! sudo docker exec -it cassandra cqlsh -e "DESCRIBE KEYSPACES" > /dev/null 2>&1; do
    echo "Cassandra is not ready yet. Retrying in 5 seconds..."
    sleep 5
done

cat CassandraSchema.cql | sudo docker exec -i cassandra cqlsh
echo "Keyspace and table created!"

sudo docker exec -it kafka-connect curl -X POST -H "Content-Type: application/json" --data @/etc/kafka-connect/connectors/CassandraConnector.json http://kafka-connect:8083/connectors