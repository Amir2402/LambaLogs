from pyspark.sql import SparkSession 
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = (SparkSession.
         builder.
         config("spark.num.executors", "2").
         appName("StreamingJobLogAnalysis").
         getOrCreate())

streamDf = (spark.readStream.format("kafka").
            option("kafka.bootstrap.servers", "kafka-broker-1:9092").
            option("subscribe", "logTopic").load())

schema = StructType([
    StructField("host", StringType(), True),
    StructField("user-identifier", StringType(), True),
    StructField("datetime", StringType(), True),
    StructField("method", StringType(), True),
    StructField("request", StringType(), True),
    StructField("protocol", StringType(), True),
    StructField("status", IntegerType(), True),
    StructField("bytes", IntegerType(), True),
    StructField("referer", StringType(), True)
])

streamDf = (streamDf.
            selectExpr("CAST(value AS STRING)").
            select(from_json(col("value"), schema).alias("logInJson")).
            select('logInJson.*'))

outputDf = (streamDf.
            writeStream.
            format("console").
            outputMode("append").
            start()) 

outputDf.awaitTermination()

