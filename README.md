# Introduction
Given I94 entry records, to find any insights with dimension on city demographics/airport

## Data source
**I94 Immigration Data**: This data comes from the US National Tourism and Trade Office. A data dictionary is included in the workspace. This is where the data comes from. There's a sample file so you can take a look at the data in csv format before reading it all in. 

**U.S. City Demographic Data**: This data comes from OpenSoft. You can read more about it here.

**Airport Code Table**: This is a simple table of airport codes and corresponding cities. It comes from here

## Steps for this projects:
1. Data has been loaded into S3
2. Copy staging table to redshift
3. Run airflow for scheduled jobs to repeat step 1~2
4. Run data quality check
   1. Check if any null primary key.
   2. Count the record, check if there is 0 entries.

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
A: With S3, EMR, Redshift, most of the core services are under AWS, it can handle more 100x of data. However, it also depends the case.
If there are more writing than reading:
    then we don't need to always copy data from S3 to redshift, since the memory in redshift is very pricy. Most of the data should be stored into S3 buckets, and schedule tasks to copy the latest data from S3 to redshift periodically, for example, daily.
If there are more reading:
    then we might need more scale up redshift clusters to maintain the performance. Since there are might many users attempt to read at the same time, having multiple redshift can gurantee the reading performance. Also, we can schedule task to copy data from S3 to all redshift clusters periodically, to update their database.

### How do you do if data needs to populate a dashboard that must be updated on a daily basis by 7am every day
A: Airflow can definitely handle it, just schedule a task before 7am everyday. Just in case if the dag fails, there could be 3 approaches:
1. Shows the historical data on dashboard, but also raise warning flag that the dag is failed.
2. Do not show any data on dashboard, which effectively indicates the dag is failed.
3. Do not let the dag fail, we will have replicated dags, which would be a stable version of dags. Once the current dag is fail, start using the backup dag.

### What if the database needed to be accessed by 100+ people? 
A: Redshift can handle more than 100+ people access. However, it really depends on the senario, in some cases, there could be more users accesss to databse in the morning with 100+ connections at the same time, and no connection in the afternoon. In that case, we can use the elastic scalibity feature from redshift. [Reference](https://aws.amazon.com/blogs/big-data/scale-your-amazon-redshift-clusters-up-and-down-in-minutes-to-get-the-performance-you-need-when-you-need-it/).
If there could be 100+ connections, we can easily scale up the redshift clusters by simple API call. And if there are less users, we can scale it down.

# Data Model
## Fact Table:
### I94
**Provide details of I94 entries**
Unnamed: 0    1000 non-null int64
cicid         1000 non-null float64 - primary key
i94yr         1000 non-null float64
i94mon        1000 non-null float64
i94cit        1000 non-null float64
i94res        1000 non-null float64
i94port       1000 non-null object
arrdate       1000 non-null float64
i94mode       1000 non-null float64
i94addr       941 non-null object
depdate       951 non-null float64
i94bir        1000 non-null float64
i94visa       1000 non-null float64
count         1000 non-null float64
dtadfile      1000 non-null int64
visapost      382 non-null object
occup         4 non-null object
entdepa       1000 non-null object
entdepd       954 non-null object
entdepu       0 non-null float64
matflag       954 non-null object
biryear       1000 non-null float64
dtaddto       1000 non-null object
gender        859 non-null object
insnum        35 non-null float64
airline       967 non-null object
admnum        1000 non-null float64
fltno         992 non-null object
visatype      1000 non-null object

## Dimension Table:
### Airport
ident           55075 non-null object - primary key
type            55075 non-null object
name            55075 non-null object
elevation_ft    48069 non-null float64
continent       27356 non-null object
iso_country     54828 non-null object
iso_region      55075 non-null object
municipality    49399 non-null object
gps_code        41030 non-null object
iata_code       9189 non-null object
local_code      28686 non-null object
coordinates     55075 non-null object

### Demographics
- City                      2891 non-null object
- State                     2891 non-null object
- Median Age                2891 non-null float64
- Male Population           2888 non-null float64
- Female Population         2888 non-null float64
- Total Population          2891 non-null int64
- Number of Veterans        2878 non-null float64
- Foreign-born              2878 non-null float64
- Average Household Size    2875 non-null float64
- State Code                2891 non-null object
- Race                      2891 non-null object
- Count                     2891 non-null int64
