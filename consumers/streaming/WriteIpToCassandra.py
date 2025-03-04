from pyspark.sql import SparkSession 
from pyspark.sql.functions import *
from requests import get 
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from schemas import ipSchema, logSchema

def store_ip_to_cassandra(streamDf, batchId):
    hosts_df = streamDf.select("host").collect()
    records = [] 

    for row in hosts_df: 
        host = row['host']
        ip_record = get(f'http://ip-api.com/json/{host}').json()
        records.append(ip_record) 
    
    ip_df = spark.createDataFrame(records, schema = ipSchema)
    ip_df.show()

    (ip_df.write.
        format("org.apache.spark.sql.cassandra").
        mode("append").
        option("keyspace", "logkeyspace").
        option("table", "ipinfo").
        save())

if __name__ == '__main__':
    spark = (SparkSession.
            builder.
            config("spark.cassandra.connection.host", "cassandra").
            config("spark.cassandra.connection.port", "9042").
            appName("StreamingJobLogAnalysis").
            getOrCreate())

    streamDf = (spark.readStream.format("kafka").
            option("kafka.bootstrap.servers", "kafka-broker-1:9092").
            option("subscribe", "logTopic").load())

    streamDf = (streamDf.
                selectExpr("CAST(value AS STRING)").
                select(from_json(col("value"), logSchema).alias("logInJson")).
                select('logInJson.*'))

    (streamDf.
    writeStream.
    foreachBatch(store_ip_to_cassandra).
    outputMode("append").
    start().
    awaitTermination())

