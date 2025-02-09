from pyspark.sql import SparkSession 
from pyspark.sql.functions import *
# from datetime import now
import os

spark = (SparkSession.
        builder.
        config("spark.cassandra.connection.host", "cassandra").
        config("spark.cassandra.connection.port", "9042").
        appName("batchJobLogAnalysis").
        getOrCreate())

log_df = (spark.read.
    format("org.apache.spark.sql.cassandra").
    options(table="log_table", keyspace="logkeyspace").
    load())

ip_info_df = (spark.read.
    format("org.apache.spark.sql.cassandra").
    options(table="ipinfo", keyspace="logkeyspace").
    load()) 

log_df = (log_df.
          withColumn("time_stamp", to_timestamp(log_df.datetime, "dd/MMM/yyyy:HH:mm:ss Z")).
          drop('datetime'))

log_df = log_df.filter(col("time_stamp").cast("date") == current_date())

ip_info_df = ip_info_df.filter(col('status') == "success")

join_df = log_df.join(ip_info_df, ip_info_df['query'] == log_df['host'], 'inner')

final_df = join_df.select('host', 'time_stamp', 'proxy', 'country', 'isp', 'org').dropDuplicates(['host'])

url = "jdbc:postgresql://postgres_db:5432/logs_db"
properties = {
    "user": "admin",
    "password": "admin",
    "driver": "org.postgresql.Driver"
}

final_df.write.jdbc(url=url,
                    table="batch_logs.host_informations",
                    mode="append",
                    properties=properties)