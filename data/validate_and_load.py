from pyspark.sql import SparkSession
import json
import sys

spark = SparkSession.builder \
    .appName("ValidateAndLoad") \
    .config("spark.sql.catalog.nessie", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.nessie.uri", "http://nessie:19120/api/v2") \
    .config("spark.sql.catalog.nessie.ref", "main") \
    .config("spark.sql.catalog.nessie.io-impl", "org.apache.iceberg.aws.s3.S3FileIO") \
    .config("spark.sql.catalog.nessie.s3.endpoint", "http://minio:9000") \
    .config("spark.sql.catalog.nessie.s3.access-key", "minio") \
    .config("spark.sql.catalog.nessie.s3.secret-key", "supersecret") \
    .config("spark.sql.catalog.nessie.s3.path-style-access", "true") \
    .config("spark.sql.catalog.nessie.warehouse", "s3://warehouse/") \
    .getOrCreate()

input_path = "/data/incoming/2025-01-14.csv"
raw = spark.read.option("header", True).csv(input_path)


non_null_cols = ["ticker", "volume", "open", "close", "high", "low", "window_start", "transactions"]
cond_not_null = " AND ".join([f"{c} IS NOT NULL" for c in non_null_cols])

good = raw.filter(cond_not_null).dropDuplicates()
bad = raw.subtract(good)

bad.write.mode("overwrite") \
    .option("header", True) \
    .csv("/data/rejected/bad_rows")

good.writeTo("nessie.db.stock_prices") \
    .using("iceberg") \
    .createOrReplace()

report = {
    "input_rows": raw.count(),
    "good_rows": good.count(),
    "bad_rows": bad.count(),
    "duplicates_removed": raw.count() - good.count() - bad.count()
}

with open("/data/reports/quality_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Validation complete. Report written to /data/reports/quality_report.json")
spark.stop()