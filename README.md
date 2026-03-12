

# **AWS_Airline_Data_Engineering_Project: Medallion Architecture**

This project is a **production-style data engineering pipeline built on AWS** to process airline flight delay data. It implements the **Medallion Architecture (Bronze, Silver, Gold layers)** and automates data ingestion, transformation, and loading into a cloud data warehouse for analytics.

The pipeline processes raw airline data from Kaggle and converts it into **analytics-ready star schema tables (Fact & Dimension)** using AWS services.

---

# **System Architecture Overview**

The project follows the **Medallion Architecture**, where data flows through multiple stages:

1️⃣ **Bronze Layer** – Raw data ingestion
2️⃣ **Silver Layer** – Data cleaning & transformation
3️⃣ **Gold Layer** – Star schema (Fact + Dimension tables) for analytics

![architecture](https://github.com/niranjann16/AWS_Airline_Data_Engineering_Project/blob/main/Architecture/Airline%20data%20pipeline%20and%20warehouse%20stages.png)

---

# **Project Overview**

This project builds a **modern cloud data pipeline using AWS services** to process airline flight delay data.

The system automatically detects new files uploaded to S3 and triggers a full ETL pipeline.

### **Key Features**

✔ Automated data pipeline using event-driven architecture
✔ Medallion architecture (Bronze → Silver → Gold)
✔ Data transformation using PySpark
✔ Star schema modeling (Fact & Dimensions)
✔ Data warehouse loading for analytics
✔ Pipeline monitoring and alerts

---

# **Technologies Used**

This project uses the following AWS services:

* **Amazon S3** – Data lake storage (Bronze, Silver, Gold layers)
* **AWS CloudTrail** – Detect S3 data events
* **Amazon EventBridge** – Trigger pipelines
* **AWS Step Functions** – Orchestrate the ETL pipeline
* **AWS Glue** – Data transformation
* **AWS Glue Data Catalog** – Metadata management
* **Amazon Redshift Serverless** – Data warehouse
* **Amazon SNS** – Pipeline alerts

---

# **Project Workflow**

## **Step 1: Data Ingestion**

Airline data from Kaggle is uploaded to the S3 bucket.

```
S3 Bucket
airline-data-lake-niranjan
```

Folder structure:

```
airline-data-lake-niranjan
│
├── bronze
│   └── flights_raw.csv
│
├── silver
│
└── gold
```

Bronze layer stores **raw unprocessed data**.

---

# **Step 2: Event Driven Pipeline Trigger**

When a new file lands in S3:

1️⃣ **CloudTrail detects S3 activity**

2️⃣ **EventBridge triggers pipeline**

3️⃣ **Step Functions starts ETL workflow**

This creates a **fully automated pipeline**.

---

# **Step 3: Metadata Creation**

A **Glue Crawler** scans the Bronze layer.

It automatically creates a table in the **Glue Data Catalog**.

```
Database: airline_db
Table: bronze_flights
```

This allows the data to be queried using:

* Athena
* Glue ETL
* Redshift

---

# **Step 4: Data Transformation (Bronze → Silver)**

A **Glue ETL job (PySpark)** performs:

✔ Column renaming
✔ Data cleaning
✔ Null handling
✔ Removing unwanted columns
✔ Data type conversion

Example transformations:

```
FL_DATE → flight_date
ORIGIN → origin_airport
DEST → destination_airport
DEP_DELAY → departure_delay
ARR_DELAY → arrival_delay
```

Output is written to:

```
S3
silver/flights_clean/
```

---

# **Step 5: Data Modeling (Silver → Gold)**

Another **Glue ETL job** builds a **Star Schema**.

This creates:

### **Fact Table**

```
fact_flights
```

Columns:

```
flight_id
airline_id
origin_airport
destination_airport
departure_delay
arrival_delay
distance
flight_date
```

---

### **Dimension Tables**

#### **dim_airline**

```
airline_id
airline_name
```

#### **dim_airport**

```
airport_code
airport_name
city
state
```

#### **dim_date**

```
date_id
year
month
day
weekday
```

---

# **Star Schema Architecture**

![star\_schema](https://github.com/niranjann16/AWS_Airline_Data_Engineering_Project/blob/main/Architecture/star_schema.png)

This schema improves:

✔ Query performance
✔ Analytical reporting
✔ BI dashboards

---

# **Step Functions Pipeline**

The ETL workflow is orchestrated by Step Functions.

Pipeline order:

```
Start
   ↓
Glue Crawler
   ↓
Bronze → Silver ETL
   ↓
Silver → Gold ETL
   ↓
Load to Redshift
   ↓
Send SNS Notification
```


---

# **Data Warehouse**

Final analytics tables are stored in:

**Amazon Redshift Serverless**

Tables created:

```
fact_flights
dim_airport
dim_airline
dim_date
```

Example query:

```sql
SELECT airline_id,
AVG(arrival_delay)
FROM fact_flights
GROUP BY airline_id;
```

---

# **Project Folder Structure (GitHub)**

```
aws-airline-data-engineering-project
│
├── architecture
│   ├── airline_architecture.png
│   ├── pipeline.png
│   └── star_schema.png
│
├── scripts
│   ├── bronze_to_silver.py
│   └── silver_to_gold.py
│
├── sql
│   └── redshift_tables.sql
│
├── dataset
│   └── sample_flights.csv
│
└── README.md
```

---

# **How to Deploy and Run the Project**

## **Prerequisites**

You need:

✔ AWS account
✔ IAM roles for Glue and Redshift
✔ S3 bucket

```
airline-data-lake-niranjan
```

---

## **Step 1: Upload Dataset**

Upload Kaggle dataset to:

```
S3
bronze/flights_raw.csv
```

---

## **Step 2: Create Glue Crawler**

Configure crawler:

```
Source → S3 Bronze Folder
Target → Glue Database airline_db
```

---

## **Step 3: Create Glue ETL Jobs**

Create two jobs:

### Job 1

```
bronze_to_silver.py
```

### Job 2

```
silver_to_gold.py
```

---

## **Step 4: Create Step Functions Workflow**

Add tasks:

```
Crawler → ETL1 → ETL2 → Redshift → SNS
```

---

## **Step 5: Configure EventBridge**

Trigger pipeline when new files arrive in S3.

---

# **Post Execution**

After the pipeline runs successfully:

Gold layer contains **analytics-ready data**.

Example location:

```
s3://airline-data-lake-niranjan/gold/
```

Data can be analyzed using:

* Redshift
* Athena
* BI dashboards

---

# **Future Improvements**

Possible enhancements:

✔ Real-time streaming using **Amazon Kinesis**
✔ Dashboard using **Amazon QuickSight**
✔ Data quality validation
✔ Partition optimization

---

⭐ **This project demonstrates a real-world data engineering pipeline using AWS services and modern data lake architecture.**
