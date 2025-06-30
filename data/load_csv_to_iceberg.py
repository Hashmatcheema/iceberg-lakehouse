from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CSV to Iceberg") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

df = spark.read.option("header", "true").csv("/data/2025-01-14.csv")

df.writeTo("nessie.db.stock_prices").using("iceberg").createOrReplace()

print("CSV data loaded into nessie.db.stock_prices")
