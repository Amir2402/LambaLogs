from pyspark.sql import SparkSession 
from pyspark.sql.functions import *
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
print(sys.path)
from schemas import logSchema

def AggregateToPg(streamDf, batchId):
    url = "jdbc:postgresql://postgres_db:5432/logs_db"
    properties = {
        "user": "admin",
        "password": "admin",
        "driver": "org.postgresql.Driver"
    }

    requests_per_status = (
        streamDf.
        groupBy(window(col("parsed_timestamp"), "30 seconds"), col("status_group")).
        agg(count("*").alias("request_status_count")).
        orderBy(col("window").asc()).
        withColumn('window_start', col('window.start')).
        withColumn('window_end', col('window.end')).
        drop("window")
    )
    requests_per_status.write.jdbc(url=url,
                                   table="real_time_logs.status_per_window",
                                   mode="append",
                                   properties=properties)

    requests_per_protocol = (
        streamDf.
        groupBy(window(col("parsed_timestamp"), "30 seconds"), col("protocol")).
        agg(count("*").alias("request_protocol_count")).
        orderBy(col("window").asc()).
        withColumn('window_start', col('window.start')).
        withColumn('window_end', col('window.end')).
        drop("window")
    )
    requests_per_protocol.write.jdbc(url=url,
                                     table="real_time_logs.protocol_per_window",
                                     mode="append",
                                     properties=properties)

    requests_per_method = (
        streamDf.
        groupBy(window(col("parsed_timestamp"), "30 seconds"), col("method")).
        agg(count("*").alias("request_method_count")).
        orderBy(col("window").asc()).
        withColumn('window_start', col('window.start')).
        withColumn('window_end', col('window.end')).
        drop("window")
    )
    requests_per_method.write.jdbc(url=url,
                                   table="real_time_logs.method_per_window",
                                   mode="append",
                                   properties=properties)
if __name__ == '__main__':
    spark = (SparkSession.
            builder.
            appName("AggregateToDruid").
            getOrCreate())

    streamDf = (spark.readStream.format("kafka").
            option("kafka.bootstrap.servers", "kafka-broker-1:9092").
            option("subscribe", "logTopic").load())

    streamDf = (streamDf.
                selectExpr("CAST(value AS STRING)").
                select(from_json(col("value"), logSchema).alias("logInJson")).
                select('logInJson.*'))
    
    streamDf = streamDf.withColumn(
    "parsed_timestamp",
    to_timestamp(unix_timestamp("datetime", "dd/MMM/yyyy:HH:mm:ss Z").cast("timestamp"))
    ).drop('datetime')

    streamDf = streamDf.withColumn(
            "status_group",
            when(col("status").between(100, 199), "1xx")
            .when(col("status").between(200, 299), "2xx")
            .when(col("status").between(300, 399), "3xx")
            .when(col("status").between(400, 499), "4xx")
            .when(col("status").between(500, 599), "5xx")  
        )
    
    (streamDf.
    writeStream.
    trigger(processingTime="30 seconds").
    foreachBatch(AggregateToPg).
    outputMode("update").
    start().
    awaitTermination())



