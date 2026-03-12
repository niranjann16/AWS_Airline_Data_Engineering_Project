
# bronze_to_silver.py
# AWS Glue ETL Script
# Purpose: Clean raw flight dataset, rename columns, filter bad records, and write to Silver layer in Parquet

import sys
from pyspark.context import SparkContext
from pyspark.sql.functions import col
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read Bronze Layer Data (CSV)
df = spark.read.option("header", "true").csv(
    "s3://airline-data-lake-niranjan/bronze/flights_raw/"
)

# Select and rename important columns
df_clean = df.select(
    col("YEAR").alias("year"),
    col("MONTH").alias("month"),
    col("DAY").alias("day"),
    col("AIRLINE").alias("airline_code"),
    col("ORIGIN_AIRPORT").alias("origin_airport"),
    col("DESTINATION_AIRPORT").alias("destination_airport"),
    col("DEPARTURE_DELAY").alias("departure_delay"),
    col("ARRIVAL_DELAY").alias("arrival_delay"),
    col("DISTANCE").alias("distance"),
    col("CANCELLED").alias("cancelled")
)

# Filter unwanted records
df_clean = df_clean.filter(col("cancelled") == 0)
df_clean = df_clean.filter(col("distance") > 0)
df_clean = df_clean.filter(col("arrival_delay").isNotNull())

# Write to Silver Layer in Parquet format
df_clean.write.mode("overwrite").parquet(
    "s3://airline-data-lake-niranjan/silver/flights/"
)

job.commit()
