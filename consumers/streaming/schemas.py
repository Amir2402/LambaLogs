from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, BooleanType

ipSchema = StructType([
    StructField("query", StringType(), True),
    StructField("status", StringType(), True),
    StructField("continent", StringType(), True),
    StructField("continentcode", StringType(), True),
    StructField("country", StringType(), True),
    StructField("countrycode", StringType(), True),
    StructField("region", StringType(), True),
    StructField("regionname", StringType(), True),
    StructField("city", StringType(), True),
    StructField("district", StringType(), True),
    StructField("zip", StringType(), True),
    StructField("lat", DoubleType(), True),
    StructField("lon", DoubleType(), True),
    StructField("timezone", StringType(), True),
    StructField("offset", IntegerType(), True),
    StructField("currency", StringType(), True),
    StructField("isp", StringType(), True),
    StructField("org", StringType(), True),
    StructField("as", StringType(), True),
    StructField("asname", StringType(), True),
    StructField("mobile", BooleanType(), True),
    StructField("proxy", BooleanType(), True),
    StructField("hosting", BooleanType(), True)
])

logSchema = StructType([
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