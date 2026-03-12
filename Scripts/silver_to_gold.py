
# silver_to_gold.py
# AWS Glue ETL Script
# Purpose: Create dimension tables and fact table (Star Schema) from Silver layer

import sys
from pyspark.context import SparkContext
from pyspark.sql.functions import col, monotonically_increasing_id
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load Silver Data
flights = spark.read.parquet(
    "s3://airline-data-lake-niranjan/silver/flights/"
)

# Load dimension source datasets from Bronze
airlines = spark.read.option("header","true").csv(
    "s3://airline-data-lake-niranjan/bronze/airlines_raw/"
)

airports = spark.read.option("header","true").csv(
    "s3://airline-data-lake-niranjan/bronze/airports_raw/"
)

# ---------------------
# Create Airline Dimension
# ---------------------
dim_airline = airlines.select(
    col("IATA_CODE").alias("airline_code"),
    col("AIRLINE").alias("airline_name")
)

dim_airline = dim_airline.withColumn(
    "airline_id",
    monotonically_increasing_id()
)

dim_airline.write.mode("overwrite").parquet(
    "s3://airline-data-lake-niranjan/gold/dim_airline/"
)

# ---------------------
# Create Airport Dimension
# ---------------------
dim_airport = airports.select(
    col("IATA_CODE").alias("airport_code"),
    col("AIRPORT").alias("airport_name"),
    col("CITY").alias("city"),
    col("STATE").alias("state"),
    col("LATITUDE").alias("latitude"),
    col("LONGITUDE").alias("longitude")
)

dim_airport = dim_airport.withColumn(
    "airport_id",
    monotonically_increasing_id()
)

dim_airport.write.mode("overwrite").parquet(
    "s3://airline-data-lake-niranjan/gold/dim_airport/"
)

# ---------------------
# Create Date Dimension
# ---------------------
dim_date = flights.select(
    "year","month","day"
).distinct()

dim_date = dim_date.withColumn(
    "date_id",
    monotonically_increasing_id()
)

dim_date.write.mode("overwrite").parquet(
    "s3://airline-data-lake-niranjan/gold/dim_date/"
)

# ---------------------
# Create Fact Table
# ---------------------
fact_flights = flights.select(
    "year",
    "month",
    "day",
    "airline_code",
    "origin_airport",
    "destination_airport",
    "departure_delay",
    "arrival_delay",
    "distance"
)

fact_flights.write.mode("overwrite").partitionBy("year","month").parquet(
    "s3://airline-data-lake-niranjan/gold/fact_flights/"
)

job.commit()
