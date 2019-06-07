# Introduction

## Data source
**I94 Immigration Data**: This data comes from the US National Tourism and Trade Office. A data dictionary is included in the workspace. This is where the data comes from. There's a sample file so you can take a look at the data in csv format before reading it all in. 

**World Temperature Data**: This dataset came from Kaggle. You can read more about it here.

**U.S. City Demographic Data**: This data comes from OpenSoft. You can read more about it here.

**Airport Code Table**: This is a simple table of airport codes and corresponding cities. It comes from here

## Steps for this projects:
1. Preprocess local data
2. Upload processed data to S3
3. Copy staging table to redshift
4. Run airflow for scheduled jobs and data quality check

## Scripts Structure:
1. analysis.ipynb - main iPython script for most of the analysis
2. configurations - folder for all config.cfg
3. README.md - introduction of this project.
4. airflow - all scripts for starting airflow
5. sql_queries.py - contains all 

## Tools and technology:
1. S3 - data lake
2. EMR (Optional) - run notebook
3. Redshift - data warehouse
4. Spark - python library
5. Pandas - python library
6. Airflow - job scheduler

## How often:
1. Since most of the data (demographic, airport, immigration), they don't change too frequently, we can update the data daily.

## Q&A:
### What if the data was increased by 100x
A: With S3, EMR, Redshift, most of the core services are under AWS, it can handle more 100x of data.

### How do you do if data needs to populate a dashboard that must be updated on a daily basis by 7am every day
A: Airflow can definitely handle it, just schedule a task before 7am everyday.

### What if the database needed to be accessed by 100+ people? 
A: Redshift can handle more than 100+ people access. 